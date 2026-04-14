import socket
import threading
import sys


def recibir(sc):
    while True:
        try:
            datos = sc.recv(1024)
            if not datos:
                break
            print(datos.decode("utf-8"), end="", flush=True)
        except OSError:
            break
    print("[Conexión cerrada por el servidor]")


def main():
    HOST = "10.3.66.21"
    PORT = 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Error: no se puede conectar al servidor. ¿Está corriendo servidor.py?")
        sys.exit(1)

    hilo_rx = threading.Thread(target=recibir, args=(s,), daemon=True)
    hilo_rx.start()

    try:
        while True:
            msg = input()
            s.send(msg.encode("utf-8"))
            if msg.strip().lower() == "exit":
                break
    except (KeyboardInterrupt, EOFError):
        try:
            s.send(b"exit")
        except OSError:
            pass
    finally:
        s.close()


if __name__ == "__main__":
    main()
