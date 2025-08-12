# kütüphaneler yüklendi mi test etmek için yazdım oyunla alakası yok
from kivy.app import App
from kivy.uix.label import Label

class MerhabaApp(App):
    def build(self):
        return Label(text="Merhaba Zeynep!")

MerhabaApp().run()