import ctypes,struct,codecs
import requests,socket,subprocess
import json,folium,re

from requests import Response
from ipaddress import IPv4Address

from psutil import Popen as cmd
from psutil import AccessDenied as PSAD
from psutil import process_iter

from pathlib import Path
from os import getcwd

database_ports = {
    3306: 'MySQL',
    5432: 'PostgreSQL',
    27017: 'MongoDB',
    1433: 'Microsoft SQL Server',
    1521: 'Oracle Database',
    6379: 'Redis',
    8086: 'InfluxDB',
    3306: 'Aurora MySQL',
    5432: 'Aurora PostgreSQL',
}

aws_services_ports = {
    80: 'HTTP (Amazon S3 website hosting)',
    443: 'HTTPS (Amazon S3 website hosting)',
    22: 'SSH (Amazon EC2)',
    3389: 'RDP (Remote Desktop Protocol - Amazon EC2 Windows instances)',
    3306: 'MySQL (Amazon RDS)',
    5439: 'Redshift (Amazon Redshift)',
    6379: 'Redis (Amazon ElastiCache)',
    8080: 'HTTP (Amazon EC2)',
    11211: 'Memcached',
}

randomports = {
    110: "POP3",
    115: "SFTP",
    135: "RPC",
    139: "NETBIOS",
    143: "IMAP",
    1433: "MSSQL",
    194: "IRC",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    25565: "Minecraft",
    3306: "MySQL",
    3389: "RDP",
    443: "SSL",
    53: "DNS",
    5632: "PCAnywhere",
    5900: "VNC",
    80: "HTTP",
    68: "DHCP UDP Client",
    67: "DHCP UDP Server",
    106: "MacOS Server",
    119: "Network News Transfer Protocol",
    384: "Remote Network Server System",
    434: "Mobile Agent Ip",
    401: "Uninterruptible Power Supply(UPS)",
    427: "Service Location Protocol",
    443: "HTTPS",
    513: "RLogin",
    514: "Remote Shell",
    830: "NetConf Over SSH",
    831: "NetConf Over Beep",
    832: "NetConf for SOAP over HTTPS",
    833: "NetConf for SOAP over BEEP",
    981: "Remote HTTPS Management for firewall devices running embedded check point VPN Software",
    987: "Sonny Playstation Wake On Lan",
    989: "FTPS Protocol (data)",
    990: "FTPS Protocol (control)",
    995: "POP3S",
}

class URL:
    def __init__(self,url):
        if not requests.get(f"http://{url}").ok == True:
            self.url = None
            print('The url may not exist or you typed the wrong format.Right Example : www.yoururl.com')
        else:
            self.url = url
            self.ip = socket.gethostbyname(f"{self.url}")
            self.ports = []
    def encoding(self):
        return requests.get(f'http://{self.url}').encoding
    def transferhistory(self):
        for x in requests.get(f"http://{self.url}").history:
            print(x.headers)
    def reversepointer(self):
        return IPv4Address(socket.gethostbyname(f"{self.ip}")).reverse_pointer
    def ipinfo(self):
        return requests.get(f"https://ipinfo.io/{self.ip}/json").json() if self.url is not None else 'URL Not Valid'
    def route(self):
        ip_address_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        return ip_address_pattern.findall(codecs.decode(subprocess.check_output(['tracert',f'{self.url}'])))
    def httpgetheaders(self):
        print(requests.get(f"http://{self.url}").headers)
    def urlquery(self,query):
        return requests.get(f"http://{self.url}/{query}")
    def allrandomportscan(self):
        self.ports.append([key for key in randomports if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((f"{self.ip}",key)) == 0])
    def specificportscan(self,adict):
        self.ports.append([key for key in adict if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((f"{self.ip}",key)) == 0])
    def servgeo(self):
        map = folium.Map(location=[float(x) for x in requests.get(f"https://ipinfo.io/{self.ip}/json").json()['loc'].split(',')])
        map.add_child(folium.Marker(location=[float(x) for x in requests.get(f"https://ipinfo.io/{self.ip}/json").json()['loc'].split(',')]))
        map.save(f'{self.url}.html')
