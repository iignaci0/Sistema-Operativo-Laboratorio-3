import socket
import threading

clientes = []
lock = threading.Lock()


def broadcast(mensaje_bytes, origen_socket=None):
    with lock:
        for sock, _ in clientes:
            if sock is not origen_socket:
                try:
                    sock.send(mensaje_bytes)
                except OSError:
                    pass


def manejar_cliente(sc, addr):
    nombre = "Desconocido"
    try:
        sc.send("Ingresá tu nombre de usuario: ".encode("utf-8"))
        nombre = sc.recv(1024).decode("utf-8").strip() or "Anónimo"

        with lock:
            clientes.append((sc, nombre))

        print(f"[+] {nombre} conectado desde {addr[0]}:{addr[1]}")
        broadcast(f"*** {nombre} se unió al chat ***\n".encode("utf-8"), sc)

        while True:
            try:
                datos = sc.recv(1024)
            except OSError:
                break

            if not datos:
                break

            texto = datos.decode("utf-8").strip()

            if texto.lower() == "exit":
                break

            linea = f"{nombre}: {texto}\n"
            print(linea, end="")
            broadcast(linea.encode("utf-8"), sc)

    finally:
        with lock:
            clientes[:] = [(s, n) for s, n in clientes if s is not sc]
        broadcast(f"*** {nombre} salió del chat ***\n".encode("utf-8"))
        try:
            sc.close()
        except OSError:
            pass
        print(f"[-] {nombre} desconectado")


def main():
    HOST = "0.0.0.0"
    PORT = 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT} — Ctrl+C para detener")

    try:
        while True:
            sc, addr = s.accept()
            hilo = threading.Thread(
                target=manejar_cliente, args=(sc, addr), daemon=True
            )
            hilo.start()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
