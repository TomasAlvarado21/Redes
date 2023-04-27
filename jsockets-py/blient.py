import jsockets
import sys, threading
import time
import socket
#import subprocess
#import matplotlib.pyplot as plt

#paquetes = [100, 500, 1000, 2000, 5000, 9999]
#
#resultados = []
#for tamano in paquetes:
#    comando = ["python3", "cliente.py", str(tamano), "Notes_230406_154910.pdf", "anakena.dcc.uchile.cl", "1818"]
#    resultado = subprocess.run(comando, capture_output=True, text=True, timeout=180)
#    if resultado.returncode == 0:
#        ancho_banda = float(resultado.stdout.strip())
#        resultados.append(ancho_banda)
#    else:
#        print(f"Error: {resultado.stderr}")
#        resultados.append(None)
#
#plt.plot(paquetes, resultados)
#plt.xlabel("Tamaño de paquete")
#plt.ylabel("Ancho de banda (MB/s)")
#plt.title("Experimentos de tamaño de paquete")
#plt.show()
#
#print("Recomendación:")
#mejor_tamano = paquetes[resultados.index(max(resultados))]
#print(f"Utilizar un tamaño de paquete de {mejor_tamano}")
#

argumentos = ['cliente.py', '5000', 'CRIPTOGRAFIA.pdf', 'anakena.dcc.uchile.cl', '1818']

import matplotlib.pyplot as plt
import numpy as np

def experiment(packet_size):
    argumentos = ['cliente.py', '5000', 'CRIPTOGRAFIA.pdf', 'anakena.dcc.uchile.cl', '1818']
    conect = jsockets.socket_udp_connect(argumentos[3], argumentos[4])

    if conect is None:
        print('could not open socket')
        sys.exit(1)


    archivo = argumentos[2]
    t_archivo = packet_size


    # Envío del mensaje de inicio
    conect.send(('C'+ str(t_archivo)).encode())

    # Recepción de la respuesta del servidor
    intentos = 0
    while True:
        try:
            conect.settimeout(10)  
            respuesta, _ = conect.recvfrom(1024)
            respuesta = int(respuesta.decode()[1:])
            print('funciona')
            break
        except socket.timeout:
            intentos += 1
            if intentos == 5:
                print('no se logro hacer la coneccion')
                return 0
                
            print('intento', intentos, 'fallido')
            conect.send(('C'+ str(t_archivo)).encode())

    print("Respuesta recibida: ", respuesta)

    # Lectura y envío del archivo
    with open(archivo, "rb") as f:
        bytes_enviados = 0
        bloques = []
        while True: 
            bloque = f.read(respuesta)
            if not bloque:
                break
            bloques.append(b'D' + bloque)
        tiempo_inicial = time.time()
        # Enviamos todos los bloques
        for bloque in bloques:
            conect.send(bloque)

        # Enviamos un bloque vacío para indicar que terminamos
        conect.send(b'E')
        print("Enviados: ", bytes_enviados)

    # Recepción de la respuesta de finalización del servidor
    intentos = 0
    while True:
        try:
            conect.settimeout(10)  
            respuesta, _ = conect.recvfrom(1024)
            respuesta = int(respuesta.decode()[1:])
            print('funciona')
            break
        except socket.timeout:
            intentos += 1
            if intentos == 5:
                print('no se logro hacer la coneccion')
                return 0
            print('intento', intentos, 'fallido')
            conect.send(b'E')

    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicial

    # Cálculo del ancho de banda

    ancho_de_banda = (t_archivo/ tiempo_transcurrido) / (1024*1024)
    print("Ancho de banda: %.2f bytes/segundo" % ancho_de_banda)
    return ancho_de_banda

packet_sizes = [1, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 9999]
import random

x_values = [] 
for i in range(1, 5000, 100):

    x_values.append(i)

bandwidths = []
for packet_size in x_values:
    print('Tamano de paquete: ', packet_size)
    bandwidth = experiment(packet_size)
    bandwidths.append(bandwidth)

print(bandwidths)

plt.plot(x_values, bandwidths)
plt.xlabel('Tamaño de paquete (bytes)')
plt.ylabel('Ancho de banda (Mbps)')
plt.title('Ancho de banda vs Tamaño de paquete')

plt.show()

