import socket, jsockets
from scapy.all import *


client_ip = "127.0.0.1"
client_port = 65122 #puerto del cliente, se debe modificar para que coincida con el puerto del cliente
server_ip = "127.0.0.1"
server_port = 1818 
message = "Paquete interceptado y modificado."

#conf.L3socket = L3RawSocket

packet = IP(src=client_ip, dst=server_ip) / UDP(sport=client_port, dport=server_port) / Raw(load=message.encode())
   
send(packet)