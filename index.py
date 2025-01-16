import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Intenta conectarse a un puerto en una dirección IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Tiempo de espera en segundos
            s.connect((ip, port))
            return port, True
    except (socket.timeout, ConnectionRefusedError):
        return port, False

def main():
    print("--- Escáner de Puertos ---")
    target = input("Introduce la dirección IP o dominio: ").strip()
    start_port = int(input("Puerto inicial: "))
    end_port = int(input("Puerto final: "))

    print(f"Escaneando {target} desde el puerto {start_port} hasta {end_port}...")

    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)

    if open_ports:
        print("\nPuertos abiertos:")
        for port in open_ports:
            print(f"- Puerto {port} está abierto.")
    else:
        print("\nNo se encontraron puertos abiertos en el rango especificado.")

if __name__ == "__main__":
    main()
