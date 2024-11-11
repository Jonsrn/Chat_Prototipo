import sys
import os
import random
import socket
import threading
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QTextEdit, QTabWidget, QInputDialog
from PyQt5.QtCore import Qt

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat - Cliente")
        self.setGeometry(100, 100, 600, 500)
        
        self.mac_id = self.load_or_generate_mac()
        self.user_name = self.load_or_request_name()
        self.message_history_dir = "chat_histories"
        os.makedirs(self.message_history_dir, exist_ok=True)
        self.nome_para_mac = {}
        self.active_chat = None
        self.unread_messages = {}
        self.pending_messages = {}  # Dicionário para armazenar mensagens não lidas

        # Conectar ao servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 12345))
        self.client_socket.sendall((json.dumps({"type": "register", "mac": self.mac_id, "name": self.user_name}) + '\n').encode())
        
        # Criar a interface
        self.initUI()

        # Thread para receber mensagens continuamente
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Área de lista de clientes
        left_layout = QVBoxLayout()
        client_label = QLabel("Usuários Online:")
        client_label.setAlignment(Qt.AlignCenter)
        self.client_list_widget = QListWidget()
        self.client_list_widget.itemClicked.connect(self.change_chat)
        left_layout.addWidget(client_label)
        left_layout.addWidget(self.client_list_widget)
        main_layout.addLayout(left_layout, 1)

        # Área de mensagens e entrada
        right_layout = QVBoxLayout()

        # Área de exibição das abas de conversa
        self.chat_tabs = QTabWidget()
        self.chat_tabs.currentChanged.connect(self.switch_tab)
        right_layout.addWidget(self.chat_tabs, 4)

        # Entrada de mensagem
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Digite sua mensagem...")
        right_layout.addWidget(self.message_input)

        # Botão de enviar
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        right_layout.addWidget(send_button)

        main_layout.addLayout(right_layout, 3)

        self.setCentralWidget(main_widget)

    def load_or_generate_mac(self):
        mac_file = "mac_address.txt"
        if os.path.exists(mac_file):
            with open(mac_file, "r") as file:
                return file.read().strip()
        
        mac_id = f"{random.randint(1000, 9999)}"
        with open(mac_file, "w") as file:
            file.write(mac_id)
        return mac_id

    def load_or_request_name(self):
        name_file = "user_name.txt"
        if os.path.exists(name_file):
            with open(name_file, "r") as file:
                return file.read().strip()
        
        name, ok = QInputDialog.getText(self, "Nome de Usuário", "Digite seu nome:")
        if ok and name:
            with open(name_file, "w") as file:
                file.write(name)
            return name
        return "Usuário"

    
