import os
import re
import csv

dir_path="C:/Training"

keywords_set=[
    "username", "password", "emailid", "email"
]

patterns_set={
    "Email id": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}",
    "Password": r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}"
}

def keywords_found(text):
    found=[]
    text=text.lower()
    for words in keywords_set:
        if words in text:
            found.append(f"Keyword:{words}")
    return found
    
def patterns_found(text):
    found = []
    for label, pattern in patterns_set.items():
        if re.search(pattern, text):
            found.append(f"Pattern: {label}")
    return found

    
for filename in os.listdir(dir_path):
    if filename.lower().endswith(".csv"):
        file_path=os.path.join(dir_path,filename)
        with open(file_path,mode='r') as file:
            csv_file=csv.reader(file)
            for index, value in enumerate(csv_file,start=1):
                row_value=" ".join(value)
                key_call=keywords_found(row_value)
                pattern_call=patterns_found(row_value)
                if key_call or pattern_call:
                    print("Warnings found some data issues")
                    print("filename: ",filename,"\nline: ",index,"\nissues: ",key_call + pattern_call,"\nrow: ",row_value)   

