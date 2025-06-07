import requests
import time
import plotly.graph_objects as go

with open("../ip/ipuri_traceroute.txt") as f:
    ip_list = [line.strip() for line in f if line.strip()]

def get_ip_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        data = r.json()
        if data["status"] == "success":
            return {
                "ip": ip,
                "lat": data["lat"],
                "lon": data["lon"],
                "city": data.get("city", ""),
                "region": data.get("regionName", ""),
                "country": data.get("country", "")
            }
    except:
        pass
    return None

locations = []
for ip in ip_list:
    loc = get_ip_location(ip)
    if loc:
        locations.append(loc)
    time.sleep(1)  # respectă limita API ip-api

lats = [loc["lat"] for loc in locations]
lons = [loc["lon"] for loc in locations]
texts = [f'{loc["ip"]}<br>{loc["city"]}, {loc["region"]}, {loc["country"]}' for loc in locations]


fig = go.Figure(go.Scattergeo(
    lon=lons,
    lat=lats,
    text=texts,
    mode='lines+markers',
    line=dict(width=2, color='blue'),
    marker=dict(size=8, color='red')
))

fig.update_layout(
    title="🌐 Ruta Traceroute (din fișier)",
    geo=dict(
        showland=True,
        landcolor="rgb(240, 240, 240)",
        countrycolor="gray",
    )
)

fig.show()
