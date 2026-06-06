"""
Employee Onboarding System
"""

import argparse
import base64
import json
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

S3_BUCKET      = os.getenv("ONBOARD_S3_BUCKET",  "company-onboarding-docs")
KMS_KEY_ALIAS  = os.getenv("ONBOARD_KMS_ALIAS",  "alias/onboarding-cmk")
SECRET_PREFIX  = os.getenv("ONBOARD_SECRET_PFX", "onboarding")
AWS_REGION     = os.getenv("AWS_DEFAULT_REGION",  "us-east-1")

session        = boto3.Session(region_name=AWS_REGION)
kms_client     = session.client("kms")
s3_client      = session.client("s3")
secrets_client = session.client("secretsmanager")

def encrypt_file_content(plaintext, context):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    dk_resp = kms_client.generate_data_key(KeyId=KMS_KEY_ALIAS, KeySpec="AES_256", EncryptionContext=context)
    data_key_plaintext  = dk_resp["Plaintext"]
    data_key_ciphertext = dk_resp["CiphertextBlob"]
    nonce      = os.urandom(12)
    aes        = AESGCM(data_key_plaintext)
    ciphertext = aes.encrypt(nonce, plaintext, None)
    return {
        "encrypted_data_key": base64.b64encode(data_key_ciphertext).decode(),
        "nonce":               base64.b64encode(nonce).decode(),
        "ciphertext":          base64.b64encode(ciphertext).decode(),
        "encryption_context":  context,
    }

def decrypt_file_content(envelope):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    data_key_ciphertext = base64.b64decode(envelope["encrypted_data_key"])
    nonce               = base64.b64decode(envelope["nonce"])
    ciphertext          = base64.b64decode(envelope["ciphertext"])
    context             = envelope["encryption_context"]
    dk_resp = kms_client.decrypt(CiphertextBlob=data_key_ciphertext, EncryptionContext=context)
    aes = AESGCM(dk_resp["Plaintext"])
    return aes.decrypt(nonce, ciphertext, None)

def upload_document(employee_id, doc_name, content):
    context  = {"employee_id": employee_id, "document": doc_name}
    envelope = encrypt_file_content(content, context)
    s3_key = f"{employee_id}/{doc_name}.enc.json"
    s3_client.put_object(
        Bucket=S3_BUCKET, Key=s3_key,
        Body=json.dumps(envelope).encode(),
        ContentType="application/json",
        ServerSideEncryption="aws:kms",
        SSEKMSKeyId=KMS_KEY_ALIAS,
        Metadata={"employee-id": employee_id, "document-name": doc_name},
    )
    print(f"  [S3] Uploaded  s3://{S3_BUCKET}/{s3_key}")
    return s3_key

def download_document(employee_id, doc_name):
    s3_key = f"{employee_id}/{doc_name}.enc.json"
    obj    = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
    envelope = json.loads(obj["Body"].read())
    return decrypt_file_content(envelope)

def store_employee_secret(employee_id, payload):
    secret_name = f"{SECRET_PREFIX}/{employee_id}/credentials"
    value       = json.dumps(payload)
    try:
        secrets_client.create_secret(
            Name=secret_name,
            Description=f"Onboarding credentials for {employee_id}",
            KmsKeyId=KMS_KEY_ALIAS,
            SecretString=value,
            Tags=[
                {"Key": "employee-id",  "Value": employee_id},
                {"Key": "environment",  "Value": "onboarding"},
                {"Key": "created-date", "Value": datetime.utcnow().isoformat()},
            ],
        )
        print(f"  [SM]  Created secret  {secret_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceExistsException":
            secrets_client.put_secret_value(SecretId=secret_name, SecretString=value)
            print(f"  [SM]  Updated secret  {secret_name}")
        else:
            raise
    return secret_name

def retrieve_employee_secret(employee_id):
    secret_name = f"{SECRET_PREFIX}/{employee_id}/credentials"
    resp = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(resp["SecretString"])

def onboard_employee(first_name, last_name, email, department, documents):
    employee_id = f"emp-{uuid.uuid4().hex[:8]}"
    print(f"\n{'─'*50}")
    print(f"  Onboarding: {first_name} {last_name} ({email})")
    print(f"  Employee ID: {employee_id}")
    print(f"{'─'*50}")

    print("\n[1/3] Storing credentials in Secrets Manager ...")
    temp_password = base64.urlsafe_b64encode(os.urandom(18)).decode()
    credentials   = {
        "employee_id":   employee_id,
        "email":         email,
        "temp_password": temp_password,
        "vpn_key":       base64.urlsafe_b64encode(os.urandom(24)).decode(),
        "slack_token":   f"xoxp-{uuid.uuid4().hex}",
        "created_at":    datetime.utcnow().isoformat(),
        "department":    department,
    }
    secret_name = store_employee_secret(employee_id, credentials)

    print("\n[2/3] Uploading documents to S3 (KMS envelope encryption) ...")
    s3_keys = {}
    for doc_name, content in documents.items():
        s3_key = upload_document(employee_id, doc_name, content)
        s3_keys[doc_name] = s3_key

    print("\n[3/3] Onboarding complete ✓")
    summary = {
        "employee_id":   employee_id,
        "full_name":     f"{first_name} {last_name}",
        "email":         email,
        "department":    department,
        "secret_name":   secret_name,
        "s3_documents":  s3_keys,
        "onboarded_at":  datetime.utcnow().isoformat(),
    }
    print(f"\n  Summary: {json.dumps(summary, indent=4)}")
    return summary

def _demo():
    docs = {
        "offer_letter": b"Dummy PDF/Doc content for Offer Letter",
        "nda":          b"Dummy PDF/Doc content for NDA",
        "it_policy":    b"Dummy PDF/Doc content for IT Policy",
    }
    summary = onboard_employee(
        first_name="Jane", last_name="Smith",
        email="jane.smith@company.com",
        department="Engineering", documents=docs,
    )
    emp_id = summary["employee_id"]
    print("\n──── Verification ────")
    creds = retrieve_employee_secret(emp_id)
    print(f"  Retrieved temp_password: {creds['temp_password'][:10]}...")
    
    # Save the decrypted raw file to local disk instead of printing it
    raw = download_document(emp_id, "offer_letter")
    output_filename = f"{emp_id}_offer_letter_decrypted.bin"
    with open(output_filename, "wb") as f:
        f.write(raw)
    print(f"  Decrypted 'offer_letter' saved locally as: {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="Employee Onboarding System")
    sub    = parser.add_subparsers(dest="cmd")
    sub.add_parser("demo", help="Run the full demo flow")
    args = parser.parse_args()
    if args.cmd == "demo":
        _demo()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
