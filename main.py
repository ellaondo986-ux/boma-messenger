from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# Définition des couleurs du thème moderne (Sombre / Cyan / Bleu)
COLOR_BG = (0.07, 0.09, 0.12, 1)      # Fond sombre moderne
COLOR_PANEL = (0.11, 0.14, 0.19, 1)  # Panneaux
COLOR_ACCENT = (0.0, 0.6, 0.9, 1)    # Cyan / Bleu vif
COLOR_TEXT = (0.9, 0.9, 0.9, 1)      # Blanc cassé
COLOR_MUTED = (0.5, 0.5, 0.5, 1)     # Gris

Window.clearcolor = COLOR_BG

# --- ÉCRAN 1 : CONNEXION / INSCRIPTION ---
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Titre
        layout.add_widget(Label(
            text="BOMA 3040", 
            font_size='32sp', 
            bold=True, 
            color=COLOR_ACCENT,
            size_hint_y=None, height=60
        ))
        
        layout.add_widget(Label(
            text="Connexion au réseau sécurisé", 
            font_size='14sp', 
            color=COLOR_MUTED,
            size_hint_y=None, height=30
        ))
        
        # Champ Nom / Identifiant
        self.username_input = TextInput(
            hint_text='Ton Nom ou Identifiant', 
            multiline=False,
            size_hint_y=None, height=50,
            background_color=(0.15, 0.18, 0.24, 1),
            foreground_color=COLOR_TEXT,
            cursor_color=COLOR_ACCENT
        )
        layout.add_widget(self.username_input)
        
        # Champ Numéro / Téléphone
        self.phone_input = TextInput(
            hint_text='Numéro ou Code Tél', 
            multiline=False,
            size_hint_y=None, height=50,
            background_color=(0.15, 0.18, 0.24, 1),
            foreground_color=COLOR_TEXT,
            cursor_color=COLOR_ACCENT
        )
        layout.add_widget(self.phone_input)
        
        # Bouton Valider
        btn_login = Button(
            text="COMMENCER",
            size_hint_y=None, height=50,
            background_normal='',
            background_color=COLOR_ACCENT,
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_login.bind(on_press=self.go_to_contacts)
        layout.add_widget(btn_login)
        
        self.add_widget(layout)

    def go_to_contacts(self, instance):
        # Passage vers l'écran des contacts
        self.manager.current = 'contacts'

# --- ÉCRAN 2 : LISTE DES CONTACTS ---
class ContactsScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactsScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(
            text="VOS CONTACTS", 
            font_size='20sp', 
            bold=True, 
            color=COLOR_TEXT,
            size_hint_y=None, height=40
        ))
        
        # Liste automatique de contacts simulés (plus de saisie manuelle lourde)
        contacts_layout = BoxLayout(orientation='vertical', spacing=10)
        
        dummy_contacts = ["Canal Sécurisé Alpha", "Support Technique", "Agent 3040"]
        for contact_name in dummy_contacts:
            btn_contact = Button(
                text=contact_name,
                size_hint_y=None, height=60,
                background_normal='',
                background_color=COLOR_PANEL,
                color=COLOR_TEXT,
                bold=True
            )
            btn_contact.bind(on_press=self.open_chat)
            contacts_layout.add_widget(btn_contact)
            
        layout.add_widget(contacts_layout)
        self.add_widget(layout)

    def open_chat(self, instance):
        # Passage vers l'écran de discussion
        self.manager.current = 'chat'

# --- ÉCRAN 3 : DISCUSSION ---
class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Barre supérieure avec bouton de retour
        top_bar = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_back = Button(
            text="< Retour", 
            size_hint_x=None, width=100,
            background_normal='',
            background_color=COLOR_PANEL,
            color=COLOR_TEXT
        )
        btn_back.bind(on_press=self.go_back)
        top_bar.add_widget(btn_back)
        
        top_bar.add_widget(Label(
            text="Canal Sécurisé Boma 3040", 
            bold=True, 
            color=COLOR_ACCENT
        ))
        layout.add_widget(top_bar)
        
        # Zone de messages (affichage)
        self.chat_display = Label(
            text="[ Canal sécurisé actif ]\nEnvoie ton premier message ci-dessous.",
            halign='center',
            valign='middle',
            color=COLOR_MUTED
        )
        layout.add_widget(self.chat_display)
        
        # Barre de saisie de message
        bottom_bar = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.msg_input = TextInput(
            hint_text='Écris ton message...',
            multiline=False,
            background_color=(0.15, 0.18, 0.24, 1),
            foreground_color=COLOR_TEXT
        )
        bottom_bar.add_widget(self.msg_input)
        
        btn_send = Button(
            text="ENVOYER",
            size_hint_x=None, width=120,
            background_normal='',
            background_color=COLOR_ACCENT,
            bold=True
        )
        btn_send.bind(on_press=self.send_message)
        bottom_bar.add_widget(btn_send)
        
        layout.add_widget(bottom_bar)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'contacts'

    def send_message(self, instance):
        text = self.msg_input.text.strip()
        if text:
            self.chat_display.text = f"Moi : {text}"
            self.msg_input.text = ""

# --- APPLICATION PRINCIPALE ---
class BomaMessengerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ContactsScreen(name='contacts'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    BomaMessengerApp().run()
