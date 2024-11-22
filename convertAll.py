from glob import glob
from datetime import datetime
from xmltocsv import convert

xml_files = glob('**/*.xml', recursive=True)

def now():
    return datetime.now().strftime("%H:%M:%S")

startTime = datetime.now()
n_files = len(xml_files)

print(f"Starting Time: {now()}, File Count {n_files}")
for idx, file in enumerate(xml_files):
    delta = datetime.now() - startTime
    est = delta.seconds / (idx + 1) * (n_files - idx - 1)
    print(f"  [{idx}] File: {file}, Time: {now()}, Est remaining: {est} seconds")
    try:
        convert(file)
    except Exception as e:
        print(f"**** File: {file} failed because:\n" + e)
print(f"Ending Time: {now()}")
