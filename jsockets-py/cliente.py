import jsockets
import sys
import time
import socket

args = ['cliente.py', '1000', 'CRIPTOGRAFIA.pdf', 'localhost', '1717']
server = args[3]
port = args[4]
#ahora tengo que CAMBIAR esto
def main():
    #ahora haremos que se ejecute 5 veces todo el programa

    conect = jsockets.socket_udp_connect(server, port)

    # if conect is None:
    #     print('could not open socket')
    #     sys.exit(1)

    # if len(sys.argv) != 5:

    #     print('Use: '+sys.argv[0]+' host port')

    #     sys.exit(1)

    archivo = args[2]
    t_archivo = args[1]


    # Envío del mensaje de inicio
    conect.send(('C'+ str(t_archivo)).encode())
    tiempo_inicial = time.time()

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
                sys.exit(1)
                
            print('intento', intentos, 'fallido')
            conect.send(('C'+ str(t_archivo)).encode())

    print("Respuesta recibida: ", respuesta)

    # Lectura y envío del archivo
    with open(archivo, "rb") as f:
        bloques = []
        while True: 
            bloque = f.read(respuesta)
            if not bloque:
                break
            bloques.append(b'D' + bloque)
        # Enviamos todos los bloques
        for bloque in bloques:
            conect.send(bloque)

        # Enviamos un bloque vacío para indicar que terminamos
        conect.send(b'E')

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
                sys.exit(1)
                break
            print('intento', intentos, 'fallido')
            conect.send(b'E')

    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicial

    # Cálculo del ancho de banda

    ancho_de_banda = int(t_archivo) / tiempo_transcurrido / (1024 * 1024)
    print("Ancho de banda: " + str(ancho_de_banda))
# for i in range()
main()