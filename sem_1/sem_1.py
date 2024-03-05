import csv
import socket

from ping3 import ping


domains = ['proffloud.ru', 'test.proffloud.ru', 'vk.com', 'google.com', 'github.com', 'stackoverflow.com', 'python.org', 'youtube.com', 'fucken.ua', 'pornhub.com']

with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Domain', 'Ping Result', 'IP Address'])
    writer.writerow('')

    for domain in domains:
        try:
            result = ping(domain)
            ip_address = socket.gethostbyname(domain)
            writer.writerow([domain, result, ip_address])
        except socket.gaierror:
            writer.writerow([domain, 'Error: Invalid domain', ''])
