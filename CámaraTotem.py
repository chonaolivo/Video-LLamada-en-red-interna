import tkinter as tk
import cv2
import numpy as np
import socket
from tkinter import messagebox

# Nombre del archivo de configuración
CONFIG_FILE = "config.txt"

def abrir_camara(ip, puerto):
    try:
        # Configuración del cliente
        HOST = ip
        PORT = int(puerto)

        # Inicializar el cliente socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # Crear la ventana de advertencia
        ventana_advertencia = tk.Toplevel()
        ventana_advertencia.title("Advertencia")
        ventana_advertencia.geometry("400x200")

        label_advertencia = tk.Label(ventana_advertencia, text="Conexion establecida con el totem")
        label_advertencia.pack(pady=20)

        # Función para mostrar la cámara
        def mostrar_camara():
            # Crear una nueva ventana para mostrar el video
            cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Video",1024,768)

            while True:
                # Recibe el tamaño del fotograma
                data = client_socket.recv(16)
                frame_size = int(data.decode())
                # Recibe el fotograma
                data = b""
                while len(data) < frame_size:
                    packet = client_socket.recv(frame_size - len(data))
                    if not packet:
                        break
                    data += packet
                # Decodifica el fotograma y muestra la imagen
                frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Cierra la conexión
            client_socket.close()
            cv2.destroyAllWindows()

        # Función para cerrar la ventana de advertencia
        def cerrar_ventana():
            ventana_advertencia.destroy()

        # Botón para mostrar la cámara
        boton_mostrar_camara = tk.Button(ventana_advertencia, text="Mostrar cámara", command=mostrar_camara)
        boton_mostrar_camara.pack()

        # Botón para cerrar la ventana de advertencia
        boton_cerrar = tk.Button(ventana_advertencia, text="Cerrar", command=cerrar_ventana)
        boton_cerrar.pack()

    except Exception as e:
        messagebox.showerror("Error", "No se pudo conectar con la cámara remota.")

def on_click_abrir():
    ip = entry_ip.get()
    puerto = entry_puerto.get()
    abrir_camara(ip, puerto)

# Crear la ventana principal
root = tk.Tk()
root.title("Totem")
root.geometry("300x500")  # Establecer el tamaño de la ventana

# Crear los widgets
label_ip = tk.Label(root, text="IP:")
entry_ip = tk.Entry(root, width=30)
label_puerto = tk.Label(root, text="Puerto:")
entry_puerto = tk.Entry(root, width=30)
button_abrir = tk.Button(root, text="Ejectutar", width=40, command=on_click_abrir)

# Ubicar los widgets en la ventana
label_ip.pack(side="top", padx=10, pady=5)
entry_ip.pack(side="top", padx=10, pady=5)
label_puerto.pack(side="top", padx=10, pady=5)
entry_puerto.pack(side="top", padx=10, pady=5)
button_abrir.pack(side="bottom", padx=10, pady=10)

# Cargar la configuración al iniciar el programa
try:
    with open(CONFIG_FILE, "r") as file:
        lines = file.readlines()
        ip = lines[0].strip()
        puerto = lines[1].strip()
        entry_ip.insert(0, ip)
        entry_puerto.insert(0, puerto)
except FileNotFoundError:
    pass

# Guardar la configuración al cerrar el programa
def on_closing():
    ip = entry_ip.get()
    puerto = entry_puerto.get()
    with open(CONFIG_FILE, "w") as file:
        file.write(ip + "\n")
        file.write(puerto)

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar el bucle de eventos
root.mainloop()
