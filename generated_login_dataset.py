import csv
import random
import string
import time

OUTPUT_FILE = "login_dataset.csv"

def rand_str(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def gen_good_requests(n=500):
    data = []
    for _ in range(n):
        username = rand_str(random.randint(6, 12))
        password = rand_str(random.randint(8, 16))

        body = f"username={username}&password={password}"
        row = [
            "POST",
            "/login",
            body,
            0, 0, 0, 0, 0, 0,
            "good"
        ]
        data.append(row)
    return data

def gen_bad_requests(n=500):
    payloads = [
        "admin' OR '1'='1",
        "' OR ''='",
        "' UNION SELECT * FROM users --",
        "admin'/*",
        "'; DROP TABLE users;--",
        "admin' OR 1=1--",
        "' OR 1=1#",
        "\" OR \"\"=\"",
        "' AND SLEEP(5)--",
        "' OR 'x'='x",
        "<script>alert(1)</script>",
        "'; exec xp_cmdshell('dir');--",
        "' OR 1=1 limit 1 --",
        "' OR EXISTS(SELECT * FROM users)--",
        "' WAITFOR DELAY '0:0:5'--",
        "../../etc/passwd",
    ]
    
    data = []
    for _ in range(n):
        username = random.choice(payloads)
        password = random.choice(payloads)

        body = f"username={username}&password={password}"

        # Add random anomaly flag integers to mirror your bad dataset pattern
        f1 = random.choice([0,1])
        f2 = random.choice([0,1])
        f3 = random.choice([0,1,2,3,4])

        row = [
            "POST",
            "/login",
            body,
            f1, f2, f3, 0, 0, 0,
            "bad"
        ]
        data.append(row)
    return data

# ============================
# CREATE DATASET
# ============================
good = gen_good_requests(500)
bad = gen_bad_requests(500)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in good + bad:
        writer.writerow(row)

print("Dataset created:", OUTPUT_FILE)
