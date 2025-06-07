import socket
import requests
import csv
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

CUNOSCUTI = ["google", "facebook", "meta", "amazon", "doubleclick", "googlesyndication", "rubicon", "adnxs", "pubmatic", "yahoo", "teads", "quantserve", "adform", "casalemedia", "3lift", "openx", "zemanta"]
IPINFO_TOKEN = None  # opțional

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def get_owner(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        headers = {"Authorization": f"Bearer {IPINFO_TOKEN}"} if IPINFO_TOKEN else {}
        r = requests.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            return r.json().get("org", "necunoscut")
    except:
        return "eroare"
    return "necunoscut"

def process_domain(domain):
    ip = get_ip(domain)
    owner = get_owner(ip) if ip else "nerezolvat"
    apartine = "necunoscut"

    for companie in CUNOSCUTI:
        if companie in domain or (owner and companie in owner.lower()):
            apartine = companie
            break
    return (domain, ip or "nerezolvat", owner, apartine)

def main():
    with open("blocate.txt", "r") as f:
        domenii = list(set(line.strip().lower() for line in f if line.strip()))

    statistici = []
    counter = Counter()

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_domain, domeniu) for domeniu in domenii]
        for future in as_completed(futures):
            domeniu, ip, owner, companie = future.result()
            statistici.append([domeniu, ip, owner, companie])
            if companie != "necunoscut":
                counter[companie] += 1

    with open("statistici_blocate.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Domeniu", "IP", "Organizație", "Companie identificată"])
        writer.writerows(statistici)

    print("Statistici salvate în 'statistici_blocate.csv'")
    print("Top companii blocate:")
    for companie, nr in counter.most_common():
        print(f"  {companie}: {nr} domenii")

if __name__ == "__main__":
    main()
