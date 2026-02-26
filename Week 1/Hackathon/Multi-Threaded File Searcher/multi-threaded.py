import os
import csv
from concurrent.futures import ThreadPoolExecutor

dir_path = "C:/Training"
keywords_set = ["username", "password", "emailid", "email"]
MAX_THREADS = 5

def scan_file(file_path):
    results = []
    try:
        with open(file_path, "r", errors="ignore") as file:
            csv_file = csv.reader(file)
            for index, row in enumerate(csv_file, start=1):
                row_value = " ".join(row).lower()
                for word in keywords_set:
                    if word in row_value:
                        results.append((file_path, index, " ".join(row)))
                        break
    except:
        pass
    return results

files_to_scan = [
    os.path.join(dir_path, filename)
    for filename in os.listdir(dir_path)
    if filename.lower().endswith(".csv")
]

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    all_results = executor.map(scan_file, files_to_scan)

for file_result in all_results:
    for file_path, index, row_value in file_result:
        print("Warnings found some data issues")
        print("filename: ",file_path,"\nline: ",index,"\nrow: ",row_value)
