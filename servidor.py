import socket
import threading
import os
import json
import time

# Configuração do servidor
HOST = '127.0.0.1'
PORT = 12345
clientes = {}
cliente_status_file = "clientes_registrados.txt"
palavras_proibidas = ["Tomate Cru", "Mexilhões", "Molho Tartaro", "Faz o L", "Xandao"]
strikes = {}
strike_timer = {}
STRIKE_LIMIT = 3
STRIKE_TIME_LIMIT = 60  # em segundos

def register_mac(mac_id):
    if not os.path.exists(cliente_status_file):
        with open(cliente_status_file, "w") as file:
            pass

    with open(cliente_status_file, "r") as file:
        if mac_id in file.read():
            return

    with open(cliente_status_file, "a") as file:
        file.write(f"{mac_id} True\n")

def update_client_status(mac_id, status):
    # Atualiza o status do cliente no arquivo
    lines = []
    with open(cliente_status_file, "r") as file:
        lines = file.readlines()

    with open(cliente_status_file, "w") as file:
        for line in lines:
            if line.startswith(mac_id):
                line = f"{mac_id} {status}\n"
            file.write(line)