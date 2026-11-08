import csv
import io
import os
import subprocess


def CheckValidTask(creator, task):
  allowlist = ['Microsoft', 'Mozilla', 'Adobe Systems Incorporated']
  extensions = ['.exe', '.py', '.dll', '.vbs', '.ps1', '.bat']

  trusted = any(creator.startswith(x) for x in allowlist)
  executable = any(ext in task.lower() for ext in extensions)

  if executable:
    exe = task.split(' ')[0]
    p = os.path.expandvars(exe).lower()

    if p.startswith(r'c:\windows\system32') or p.startswith(r'c:\windows'):
      return True
    else:
      return trusted
  else:
    return True


# 1. Capture raw output properly as string
raw_bytes = subprocess.check_output('schtasks /query /v /fo csv /nh', shell=True)
decoded_output = raw_bytes.decode('latin-1')

# 2. Use Python's CSV reader to parse quotes and commas safely
csv_file = io.StringIO(decoded_output)
reader = csv.reader(csv_file)

count_parsed = 0
count_flagged = 0

for result in reader:
  if len(result) >= 9:
    count_parsed += 1
    name = result[1]
    creator = result[7]
    task = result[8]

    if not CheckValidTask(creator, task):
      count_flagged += 1
      print(f'[!] Flagged: Task="{name}" | User="{creator}" | Command="{task}"')

print(f'\n--- Audit Complete: Scanned {count_parsed} tasks, flagged {count_flagged}. ---')
