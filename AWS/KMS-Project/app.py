import base64, json, os, uuid, io
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify, request, render_template_string, send_file

S3_BUCKET = os.getenv("ONBOARD_S3_BUCKET", "company-onboarding-docs")
KMS_KEY_ALIAS = os.getenv("ONBOARD_KMS_ALIAS", "alias/onboarding-cmk")
SECRET_PREFIX = os.getenv("ONBOARD_SECRET_PFX", "onboarding")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

session = boto3.Session(region_name=AWS_REGION)
s3_client = session.client("s3")
secrets_client = session.client("secretsmanager")
app = Flask(__name__)

def upload_document(employee_id, doc_name, content, content_type):
    key = f"{employee_id}/{doc_name}"
    s3_client.put_object(
        Bucket=S3_BUCKET, 
        Key=key, 
        Body=content, # Uploading raw binary data directly
        ContentType=content_type,
        ServerSideEncryption="aws:kms", # Forcing S3 to encrypt before saving to disk
        SSEKMSKeyId=KMS_KEY_ALIAS,      # Using your Terraform-managed CMK
        Metadata={"employee-id": employee_id, "document-name": doc_name}
    )
    return key

def store_secret(employee_id, payload):
    name = f"{SECRET_PREFIX}/{employee_id}/credentials"
    try:
        secrets_client.create_secret(
            Name=name, 
            KmsKeyId=KMS_KEY_ALIAS, 
            SecretString=json.dumps(payload), 
            Tags=[{"Key": "employee-id", "Value": employee_id}]
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceExistsException":
            secrets_client.put_secret_value(SecretId=name, SecretString=json.dumps(payload))
        else:
            raise
    return name

def list_employees():
    result = s3_client.list_objects_v2(Bucket=S3_BUCKET, Delimiter="/")
    employees = []
    for p in result.get("CommonPrefixes", []):
        emp_id = p["Prefix"].rstrip("/")
        objs = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=emp_id + "/")
        # Extract exact names with extensions (e.g., 'offer_letter.pdf')
        docs = [obj["Key"].split("/")[-1] for obj in objs.get("Contents", []) if obj["Key"] != f"{emp_id}/"]
        employees.append({"employee_id": emp_id, "docs": docs})
    return employees

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/onboard", methods=["POST"])
def onboard():
    # 1. Parse standard text fields from form data
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    department = request.form.get("department")
    role = request.form.get("role")

    if not all([first_name, last_name, email, role]):
        return jsonify({"error": "Missing required fields"}), 400

    emp_id = f"emp-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    
    # 2. Extract and process uploaded files
    s3_keys = {}
    uploaded_files = request.files
    
    if not uploaded_files:
        return jsonify({"error": "No files uploaded"}), 400

    for input_name, file_storage in uploaded_files.items():
        file_content = file_storage.read()
        if not file_content:
            continue
            
        # Keep original extension so files open correctly when downloaded
        original_ext = os.path.splitext(file_storage.filename)[1]
        doc_name = input_name + original_ext 
        content_type = file_storage.content_type
        
        s3_key = upload_document(emp_id, doc_name, file_content, content_type)
        s3_keys[doc_name] = s3_key

    # 3. Handle Secrets Manager credentials
    creds = {
        "employee_id": emp_id,
        "email": email,
        "temp_password": base64.urlsafe_b64encode(os.urandom(18)).decode(),
        "vpn_key": base64.urlsafe_b64encode(os.urandom(24)).decode(),
        "slack_token": f"xoxp-{uuid.uuid4().hex}",
        "created_at": now,
        "department": department,
        "role": role
    }
    secret_name = store_secret(emp_id, creds)

    return jsonify({
        "success": True,
        "employee_id": emp_id,
        "full_name": f"{first_name} {last_name}",
        "secret_name": secret_name,
        "s3_documents": s3_keys,
        "temp_password": creds["temp_password"]
    })

@app.route("/api/employees")
def employees():
    return jsonify(list_employees())

@app.route("/api/employee/<emp_id>/secret")
def get_secret(emp_id):
    try:
        resp = secrets_client.get_secret_value(SecretId=f"{SECRET_PREFIX}/{emp_id}/credentials")
        return jsonify(json.loads(resp["SecretString"]))
    except ClientError:
        return jsonify({"error": "Secret not found"}), 404

@app.route("/api/employee/<emp_id>/document/<doc_name>")
def download_doc(emp_id, doc_name):
    try:
        s3_key = f"{emp_id}/{doc_name}"
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        
        # We no longer manually decrypt. S3 handles KMS decryption automatically
        # based on our IAM role permissions before returning the obj body.
        return send_file(
            io.BytesIO(obj["Body"].read()),
            as_attachment=True,
            download_name=doc_name
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Onboard</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0e0f11;--surface:#16181c;--surface2:#1e2127;--border:#2a2d35;--accent:#00e5a0;--accent2:#0066ff;--text:#e8eaf0;--muted:#6b7280;--danger:#ff4d6d}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-weight:300;min-height:100vh}
.grid-bg{position:fixed;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:40px 40px;opacity:.3;pointer-events:none}
header{padding:2rem 3rem;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);position:relative;z-index:1}
.logo{font-family:'DM Serif Display',serif;font-size:1.4rem;letter-spacing:-.02em}
.logo span{color:var(--accent)}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 8px var(--accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.status{display:flex;align-items:center;gap:8px;font-size:.8rem;color:var(--muted)}
main{display:grid;grid-template-columns:1fr 1fr;min-height:calc(100vh - 73px);position:relative;z-index:1}
.panel{padding:2.5rem 3rem;border-right:1px solid var(--border)}
.panel:last-child{border-right:none}
.panel-title{font-family:'DM Serif Display',serif;font-size:1.6rem;margin-bottom:.4rem}
.panel-sub{color:var(--muted);font-size:.85rem;margin-bottom:2rem}
label{display:block;font-size:.75rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:.4rem}
input,select{width:100%;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:.7rem 1rem;color:var(--text);font-family:'DM Sans',sans-serif;font-size:.9rem;font-weight:300;outline:none;transition:border-color .2s}
input[type="file"] {padding: .5rem .8rem; font-size: .8rem; cursor: pointer; color: var(--muted);}
input[type="file"]::file-selector-button {background: var(--surface2); border: 1px solid var(--border); color: var(--text); padding: .3rem .6rem; border-radius: 4px; margin-right: 10px; cursor: pointer; font-family: 'DM Sans';}
input:focus,select:focus{border-color:var(--accent)}
select option{background:var(--surface2)}
.field{margin-bottom:1.2rem}
.row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.btn{width:100%;padding:.9rem;background:var(--accent);color:#000;border:none;border-radius:6px;font-family:'DM Sans',sans-serif;font-size:.9rem;font-weight:500;cursor:pointer;margin-top:.5rem;transition:opacity .2s}
.btn:hover{opacity:.9}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-ghost{background:transparent;border:1px solid var(--border);color:var(--text);margin-top:.6rem}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
.result{margin-top:1.5rem;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:1.25rem;display:none}
.result.show{display:block}
.result-header{display:flex;align-items:center;gap:10px;margin-bottom:1rem;padding-bottom:.8rem;border-bottom:1px solid var(--border)}
.badge{font-size:.7rem;font-weight:500;padding:3px 10px;border-radius:20px}
.badge-green{background:rgba(0,229,160,.12);color:var(--accent);border:1px solid rgba(0,229,160,.25)}
.kv{display:flex;flex-direction:column;gap:.6rem}
.kv-row{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;font-size:.82rem}
.kv-key{color:var(--muted);white-space:nowrap;flex-shrink:0}
.kv-val{font-family:'DM Mono',monospace;font-size:.78rem;color:var(--text);text-align:right;word-break:break-all}
.kv-val.accent{color:var(--accent)}
.emp-list{display:flex;flex-direction:column;gap:.6rem;margin-top:1rem}
.emp-card{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:.9rem 1.1rem;display:flex;justify-content:space-between;align-items:center;cursor:pointer;transition:border-color .2s}
.emp-card:hover{border-color:var(--accent2)}
.emp-id{font-family:'DM Mono',monospace;font-size:.82rem;color:var(--accent)}
.emp-docs{font-size:.75rem;color:var(--muted)}
.reveal-btn{font-size:.72rem;padding:3px 10px;background:transparent;border:1px solid var(--border);border-radius:4px;color:var(--muted);cursor:pointer;font-family:'DM Mono',monospace; transition: color 0.2s, border-color 0.2s;}
.reveal-btn:hover {color: var(--accent); border-color: var(--accent);}
.secret-box{margin-top:.8rem;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:.9rem;display:none}
.secret-box.show{display:block}
.loader{display:inline-block;width:14px;height:14px;border:2px solid rgba(0,229,160,.2);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;vertical-align:middle;margin-right:6px}
@keyframes spin{to{transform:rotate(360deg)}}
.empty{color:var(--muted);font-size:.85rem;text-align:center;padding:2rem;border:1px dashed var(--border);border-radius:8px}
.tag{font-size:.7rem;padding:2px 8px;border-radius:4px;background:var(--surface2);border:1px solid var(--border);color:var(--muted);font-family:'DM Mono',monospace}
.services{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:2rem}
</style>
</head>
<body>
<div class="grid-bg"></div>
<header>
  <div class="logo">onboard<span>.</span></div>
  <div class="status"><div class="status-dot"></div>AWS connected</div>
</header>
<main>
  <div class="panel">
    <div class="panel-title">New employee</div>
    <div class="panel-sub">Credentials stored in Secrets Manager. Documents encrypted via KMS and uploaded to S3.</div>
    <div class="services"><span class="tag">KMS</span><span class="tag">S3 (SSE)</span><span class="tag">Secrets Manager</span></div>
    
    <div class="row">
      <div class="field"><label>First name</label><input id="fn" placeholder="Jane"></div>
      <div class="field"><label>Last name</label><input id="ln" placeholder="Smith"></div>
    </div>
    
    <div class="field"><label>Email</label><input id="em" type="email" placeholder="jane.smith@company.com"></div>
    
    <div class="row">
      <div class="field"><label>Department</label>
        <select id="dept">
          <option>Engineering</option>
          <option>Product</option>
          <option>Design</option>
          <option>Marketing</option>
          <option>Sales</option>
          <option>HR</option>
          <option>Finance</option>
        </select>
      </div>
      <div class="field"><label>Role</label><input id="role" placeholder="Senior Engineer"></div>
    </div>

    <div class="field"><label>Offer Letter</label><input type="file" id="file_offer_letter" accept=".pdf,.doc,.docx,.png,.jpg"></div>
    <div class="field"><label>NDA Document</label><input type="file" id="file_nda" accept=".pdf,.doc,.docx,.png,.jpg"></div>
    <div class="field"><label>IT Policy Acknowledgement</label><input type="file" id="file_it_policy" accept=".pdf,.doc,.docx,.png,.jpg"></div>

    <button class="btn" id="onboard-btn" onclick="doOnboard()">Onboard employee</button>
    
    <div class="result" id="result">
      <div class="result-header"><span class="badge badge-green">Success</span><span id="res-name" style="font-size:.9rem;font-weight:500"></span></div>
      <div class="kv" id="res-kv"></div>
    </div>
  </div>
  
  <div class="panel">
    <div class="panel-title">Employee records</div>
    <div class="panel-sub">SSE-KMS encrypted at rest. Click to reveal credentials from Secrets Manager.</div>
    <button class="btn btn-ghost" onclick="loadEmployees()">Refresh list</button>
    <div id="emp-list" class="emp-list"></div>
  </div>
</main>
<script>
async function doOnboard(){
  const btn = document.getElementById('onboard-btn');
  const fn = document.getElementById('fn').value.trim();
  const ln = document.getElementById('ln').value.trim();
  const em = document.getElementById('em').value.trim();
  const role = document.getElementById('role').value.trim();
  const dept = document.getElementById('dept').value;

  const offerFile = document.getElementById('file_offer_letter').files[0];
  const ndaFile = document.getElementById('file_nda').files[0];
  const itFile = document.getElementById('file_it_policy').files[0];

  if(!fn || !ln || !em || !role || !offerFile || !ndaFile || !itFile){
    alert('Please fill all fields and select all three documents.');
    return;
  }

  btn.disabled = true; 
  btn.innerHTML = '<span class="loader"></span>Onboarding...';

  const formData = new FormData();
  formData.append('first_name', fn);
  formData.append('last_name', ln);
  formData.append('email', em);
  formData.append('department', dept);
  formData.append('role', role);
  
  formData.append('offer_letter', offerFile);
  formData.append('nda', ndaFile);
  formData.append('it_policy', itFile);

  try {
    const res = await fetch('/api/onboard', {
      method: 'POST',
      body: formData 
    });
    
    const d = await res.json();
    if(d.error) {
       alert('Server Error: ' + d.error);
    } else {
       document.getElementById('res-name').textContent = d.full_name;
       document.getElementById('res-kv').innerHTML = kv([
         ['Employee ID', d.employee_id, true],
         ['S3 documents', Object.keys(d.s3_documents).join(', ')],
         ['Secret path', d.secret_name],
         ['Temp password', d.temp_password, true]
       ]);
       document.getElementById('result').classList.add('show');
       loadEmployees();
       
       document.getElementById('file_offer_letter').value = '';
       document.getElementById('file_nda').value = '';
       document.getElementById('file_it_policy').value = '';
    }
  } catch(e) {
    alert('Error sending request: ' + e.message);
  }
  
  btn.disabled = false; 
  btn.textContent = 'Onboard employee';
}

function kv(rows){
  return rows.map(([k,v,a])=>`<div class="kv-row"><span class="kv-key">${k}</span><span class="kv-val${a?' accent':''}">${v}</span></div>`).join('');
}

async function loadEmployees(){
  const list = document.getElementById('emp-list');
  list.innerHTML = '<div class="empty">Loading...</div>';
  const res = await fetch('/api/employees');
  const emps = await res.json();
  
  if(!emps.length){
    list.innerHTML = '<div class="empty">No employees onboarded yet.</div>';
    return;
  }
  
  list.innerHTML = emps.map(e => {
    const docLinks = e.docs.map(d => 
      `<a href="/api/employee/${e.employee_id}/document/${d}" target="_blank" class="reveal-btn" style="text-decoration:none; margin-right:4px; display:inline-block; margin-top:4px;" onclick="event.stopPropagation()">📥 ${d}</a>`
    ).join('');
    
    return `
      <div class="emp-card" onclick="toggleSecret('${e.employee_id}')">
        <div>
          <div class="emp-id">${e.employee_id}</div>
          <div class="emp-docs">${docLinks}</div>
        </div>
        <button class="reveal-btn">reveal creds</button>
      </div>
      <div class="secret-box" id="sb-${e.employee_id}"></div>
    `;
  }).join('');
}

async function toggleSecret(id){
  const box=document.getElementById('sb-'+id);
  if(box.classList.contains('show')){box.classList.remove('show');return;}
  box.innerHTML='<span class="loader"></span> Fetching from Secrets Manager...';
  box.classList.add('show');
  const res=await fetch('/api/employee/'+id+'/secret');
  const d=await res.json();
  if(d.error){box.innerHTML=`<span style="color:var(--danger);font-size:.8rem">${d.error}</span>`;return;}
  box.innerHTML='<div class="kv">'+kv([['Email',d.email||'-'],['Department',d.department||'-'],['Role',d.role||'-'],['Temp password',d.temp_password||'-',true],['Created',(d.created_at||'').slice(0,19).replace('T',' ')]])+'</div>';
}
loadEmployees();
</script>
</body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
