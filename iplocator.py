import requests,folium

def locateip(ip):
    map = folium.Map(location=[float(x) for x in requests.get(f"https://ipinfo.io/{ip}/json").json()['loc'].split(',')])
    map.add_child(folium.Marker(location=[float(x) for x in requests.get(f"https://ipinfo.io/{ip}/json").json()['loc'].split(',')]))
    map.save(f'{ip}.html')
    del ip