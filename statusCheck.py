import re
import os

if not os.path.exists("./status/status_store.txt"):
    print("No status_store.txt found")
    exit()
with open("./status/status_store.txt") as f:
    lines = f.readlines()
words = ["account", "ticker", ":"]
pattern = r'\b(?:' + '|'.join(map(re.escape, words)) + r')\b'  
for line in lines:
    split_info = re.split(pattern, line)
    key = split_info[0].strip()
    account = split_info[1].strip()
    ticker = split_info[2].strip()
    rest = split_info[3].strip()
    print(f"{key} account {account} ticker {ticker}: {rest}")

#os.remove("./status/status_store.txt")