import folium,re,json
import subprocess,codecs,ipaddress
import requests

ippattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

def is_bogon(ip_address_str):
    bogon_patterns = [
        re.compile(r'^0\.'),                    # 0.0.0.0/8
        re.compile(r'^10\.'),                   # 10.0.0.0/8
        re.compile(r'^100\.'),                  # 100.64.0.0/10 (Carrier-grade NAT)
        re.compile(r'^127\.'),                  # 127.0.0.0/8 (Loopback)
        re.compile(r'^169\.254\.'),             # 169.254.0.0/16 (Link-local)
        re.compile(r'^192\.168\.'),             # 192.168.0.0/16 (Private-use)
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),  # 172.16.0.0/12 (Private-use)
        re.compile(r'^224\.'),                  # 224.0.0.0/4 (Multicast)
        re.compile(r'^240\.'),                  # 240.0.0.0/4 (Reserved for future use)
    ]

    try:
        ip = ipaddress.ip_address(ip_address_str)
        for pattern in bogon_patterns:
            if pattern.match(ip_address_str):
                return True
        return False
    except ValueError:
        # Invalid IP address format
        return False

def tomap(basepath):

    baseroute = codecs.decode(subprocess.check_output(["tracert",basepath]))
    ip_addresses = re.findall(ippattern, baseroute)
    ips = [x for x in ip_addresses if not is_bogon(x)==True]
    content = [requests.get(f'http://ipinfo.io/{x}').json()['loc'].split((',')) for x in ips]

    map = folium.Map(location=content[-1],zoom_start=4)
    for x in range(len(content)):
        markerobj = folium.Marker(location=content[x])
        markerobj.add_to(map)
    map.save(f'{basepath[4:-4]}.html')
    del baseroute,ip_addresses,ips,content

tobepathed = []

while int(input('Anything To Add , -1 To Cancel :>')) != int(-1):
    a = str(input('-> URL or IP Address >:'))
    tobepathed.append(a)
    del a

[tomap(x) for x in tobepathed]

