from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import socket
import threading
import random

class BomaApp(App):
    def build(self):
        self.title = "Boma Cyber-Messenger"
        self.client_socket = None
        self.my_matricule = f"BM-{random.randint(10000, 99999)}"
        self.active_target_matricule = None
        
        # Interface principale (Écran d'inscription)
        self.root_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.lbl_title = Label(text="BOMA MATRIX - IDENTIFICATION", font_size=20, color=(0, 1, 0.8, 1))
        self.root_layout.add_widget(self.lbl_title)
        
        self.pseudo_input = TextInput(hint_text="Ton Pseudo...", multiline=False, size_hint_y=None, height=50)
        self.root_layout.add_widget(self.pseudo_input)
        
        self.phone_input = TextInput(hint_text="Ton Numéro de téléphone...", multiline=False, size_hint_y=None, height=50)
        self.root_layout.add_widget(self.phone_input)
        
        self.btn_connect = Button(text="ENTRER DANS LE RÉSEAU", size_hint_y=None, height=50, background_color=(0, 1, 0.8, 1))
        self.btn_connect.bind(on_press=self.connect_to_server)
        self.root_layout.add_widget(self.btn_connect)
        
        return self.root_layout

    def connect_to_server(self, instance):
        pseudo = self.pseudo_input.text.strip()
        phone = self.phone_input.text.strip()
        if not pseudo or not phone:
            return
        
        self.my_phone = phone
        self.my_pseudo = pseudo

        try:
            # Adresse IP de ton serveur (remplace par l'IP de ton PC sur le Wi-Fi local lors du test en direct)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('192.168.1.100', 55555)) 
            
            reg_packet = f"INSCRIPTION:{pseudo}:{phone}:{self.my_matricule}"
            self.client_socket.send(reg_packet.encode('utf-8'))
            
            response = self.client_socket.recv(1024).decode('utf-8')
            if "OK" in response:
                self.build_chat_interface()
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def build_chat_interface(self):
        self.root_layout.clear_widgets()
        self.root_layout.orientation = 'horizontal'

        # Barre latérale (Contacts)
        sidebar = BoxLayout(orientation='vertical', size_hint_x=0.35, spacing=5, padding=5)
        sidebar.add_widget(Label(text=f"Moi: {self.my_pseudo}\nTél: {self.my_phone}", font_size=12, color=(0, 1, 0.8, 1)))
        
        self.contact_name = TextInput(hint_text="Nom du contact", multiline=False, size_hint_y=None, height=40)
        self.contact_phone = TextInput(hint_text="Numéro du contact", multiline=False, size_hint_y=None, height=40)
        
        btn_add = Button(text="Ajouter Contact", size_hint_y=None, height=40, background_color=(0.2, 0.7, 0.3, 1))
        btn_add.bind(on_press=self.verify_and_add_contact)
        
        sidebar.add_widget(self.contact_name)
        sidebar.add_widget(self.contact_phone)
        sidebar.add_widget(btn_add)
        
        self.contacts_list_view = TextInput(text="--- CONTACTS ---\n", readonly=True)
        sidebar.add_widget(self.contacts_list_view)
        
        self.root_layout.add_widget(sidebar)

        # Zone de chat principale
        chat_area = BoxLayout(orientation='vertical', size_hint_x=0.65, spacing=5, padding=5)
        
        self.chat_display = TextInput(text="=== CANAL BOMA SÉCURISÉ ===\n", readonly=True)
        chat_area.add_widget(self.chat_display)
        
        bottom_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.msg_input = TextInput(hint_text="Écris ton message...", multiline=False)
        
        btn_send = Button(text="ENVOYER", size_hint_x=0.3, background_color=(0.1, 0.4, 0.8, 1))
        btn_send.bind(on_press=self.send_message)
        
        bottom_box.add_widget(self.msg_input)
        bottom_box.add_widget(btn_send)
        chat_area.add_widget(bottom_box)
        
        self.root_layout.add_widget(chat_area)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def verify_and_add_contact(self, instance):
        name = self.contact_name.text.strip()
        phone = self.contact_phone.text.strip()
        if name and phone:
            query = f"CHERCHE_NUMERO:{phone}"
            self.client_socket.send(query.encode('utf-8'))
            
            response = self.client_socket.recv(1024).decode('utf-8')
            if response.startswith("TROUVE:"):
                parts = response.split(":")
                found_matricule = parts[3]
                self.active_target_matricule = found_matricule
                
                self.contacts_list_view.text += f"• {name} ({phone})\n"
                self.chat_display.text += f"[SYSTÈME] Contact '{name}' lié !\n"
                self.contact_name.text = ""
                self.contact_phone.text = ""
            else:
                self.chat_display.text += f"[SYSTÈME] Numéro introuvable.\n"

    def send_message(self, instance):
        contenu = self.msg_input.text.strip()
        if not contenu or not self.active_target_matricule:
            return

        packet = f"MSG:{self.active_target_matricule}:{contenu}"
        self.client_socket.send(packet.encode('utf-8'))

        # Bulles à droite pour les messages envoyés
        self.chat_display.text += f"{' ' * 20}[Moi] ➔ {contenu}\n"
        self.msg_input.text = ""

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message.startswith("RECU:"):
                    parts = message.split(":", 3)
                    sender_pseudo = parts[2]
                    contenu = parts[3]
                    
                    # Bulles à gauche pour les messages reçus
                    Clock.schedule_once(lambda dt: self.append_received_msg(sender_pseudo, contenu))
            except:
                break

    def append_received_msg(self, pseudo, contenu):
        self.chat_display.text += f"⬅ [{pseudo}] : {contenu}\n"

if __name__ == '__main__':
    BomaApp().run()