import jsockets
import sys
import time
# tengo que poder correr esto
# % ./bwc.py 5000 /etc/C:\Users\User\Downloads\CRIPTOGRAFÍA.pdf anakena.dcc.uchile.cl 1818
print(sys.argv)

server = sys.argv[3]
port = sys.argv[4]
conect = jsockets.socket_udp_connect(sys.argv[3], sys.argv[4])

#ahora tengo que CAMBIAR esto

if conect is None:
    print('could not open socket')
    sys.exit(1)

if len(sys.argv) != 5:

    print('Use: '+sys.argv[0]+' host port')

    sys.exit(1)

archivo = sys.argv[2]
t_archivo = sys.argv[1]

conect.send(('C'+ str(t_archivo)).encode())
respuesta = int(conect.recv(1024).decode()[1:])

#ahora hay que enviar el archivo, el cliente envia en forma: 'Cxxxxx' y recive de forma 'Cyyyyy'
# se envian los bytes del archivo
# el cliente lee el archivo y lo envia en forma de bytes al servidor

with open(archivo, "rb") as f:
        bytes_enviados = 0
        bloques = []
        while True: 
            bloque = f.read(respuesta)
            if bloque == b'':
                break
            bloques.append("D" + str(bloque))
        tiempo_inicial = time.time()
        # Enviamos todos los bloques
        for bloque in bloques:
            conect.send(bloque.encode())

        conect.send(('E').encode())


print(conect.recv(1024).decode())

intentos = 5
while intentos > 0:
    time.timeout(10)
    try:
        conect.ssettimeout(10)
        respuesta2 = (conect.recv(1024).decode())[0]
        respuesta = respuesta[0]
        if respuesta == b'C':
            # Se recibió la respuesta esperada
            print("Respuesta recibida: ", respuesta)
            break
    except conect.timeout:
        # Se agotó el timeout, reintentar
        intentos -= 1
        print("Timeout, reintentando... (", intentos, " intentos restantes)")
        continue

# Si se agotaron los intentos, abortar con mensaje de error
if intentos == 0:
    print("Error: se agotaron los reintentos para recibir respuesta 'C'")
    sys.exit(1)


tiempo_final = time.time()
ancho_banda = respuesta / (tiempo_final - tiempo_inicial)
# Imprimimos los resultados
print("Tamaño del archivo: ", t_archivo, " bytes")
print("Tiempo total de envío: ", (tiempo_final - tiempo_inicial), " segundos")
print("Ancho de banda: ", ancho_banda / (1024*1024), " MB/s")

