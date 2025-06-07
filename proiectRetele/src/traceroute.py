import subprocess
import re
import requests

def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        (ip.startswith("172.") and 16 <= int(ip.split(".")[1]) <= 31)
    )

def get_ip_location(ip):
    try:
        headers = {
            'referer': 'https://ipinfo.io/',
            'user-agent': 'Mozilla/5.0',
            'X-Forwarded-For': '185.55.55.185'
        }
        r = requests.get(f"https://ipinfo.io/{ip}/json", headers=headers)
        data = r.json()
        if data.get("bogon"):
            return "(IP privat)"
        return f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country', '')}"
    except:
        return "(localizare indisponibilă)"


def traceroute(ip):
    print(f"Traceroute către {ip}:\n")
    proc = subprocess.Popen(["tracert", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    ip_list = []

    for line in proc.stdout:
        match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
        if match:
            ip_found = match.group(0)
            if is_private_ip(ip_found):
                print(f"{ip_found}  → (IP privat)")
            else:
                loc = get_ip_location(ip_found)
                print(f"{ip_found}  → {loc}")
                ip_list.append(ip_found)
        elif "*" in line:
            print("* * * (timeout)")

    return ip_list


if __name__ == "__main__":
    ips = traceroute("8.8.8.8")

    with open("../ip/ipuri_traceroute.txt", "w") as f:
        for ip in ips:
            f.write(ip + "\n")

    print("\nIP-urile publice au fost salvate în 'ipuri_traceroute.txt'")
