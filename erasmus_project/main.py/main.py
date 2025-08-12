from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
import random

Window.size = (360, 640)

# 🎨 Atık görselleri (5'er tane)
ITEM_IMAGES = {
    'paper': [
        'erasmus_project/images/paper_1.png',
        'erasmus_project/images/paper_2.jpg',
        'erasmus_project/images/paper_3.png',
        'erasmus_project/images/paper_4.jpg',
        'erasmus_project/images/paper_5.jpg'
    ],
    'plastic': [
        'erasmus_project/images/plastic_1.png',
        'erasmus_project/images/plastic_2.png',
        'erasmus_project/images/plastic_3.png',
        'erasmus_project/images/plastic_4.png',
        'erasmus_project/images/plastic_5.png'
    ],
    'glass': [
        'erasmus_project/images/glass_1.png',
        'erasmus_project/images/glass_2.png',
        'erasmus_project/images/glass_3.png',
        'erasmus_project/images/glass_4.png',
        'erasmus_project/images/glass_5.png'
    ],
    'metal': [
        'erasmus_project/images/metal_1.png',
        'erasmus_project/images/metal_2.png',
        'erasmus_project/images/metal_3.png',
        'erasmus_project/images/metal_4.png',
        'erasmus_project/images/metal_5.png'
    ],
    'organic': [
        'erasmus_project/images/organic_1.png',
        'erasmus_project/images/organic_2.jpg',
        'erasmus_project/images/organic_3.jpg',
        'erasmus_project/images/organic_4.png',
        'erasmus_project/images/organic_5.png'
    ]
}

# 🗑️ Her tür için 1 kutu görseli
BIN_IMAGES = {
    'paper': 'erasmus_project/images/paper_bin-removebg-preview.png',
    'plastic': 'erasmus_project/images/plastic_bin.jpg',
    'glass': 'erasmus_project/images/glass_bin-removebg-preview.png',
    'metal': 'erasmus_project/images/metal_box.png',
    'organic': 'erasmus_project/images/organic_bin-removebg-preview.png'
}

INFO_CARDS = {
    'paper': "1 ton of recycled paper saves 17 trees from being cut down.",
    'plastic': "Plastic can persist in nature for 400 years without decomposing.",
    'glass': "Recycling aluminum cans saves %95 energy.",
    'organic': "Organic waste can be composted to enrich the soil."
}

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        title = Label(text="EcoQuest'e Hoş Geldin!", font_size=24, pos_hint={'x': 0, 'y': .3})
        start_btn = Button(text="Oyuna Başla", size_hint=(.4, .1), pos_hint={'x': .3, 'y': .4})
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(title)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'

class DraggableItem(ButtonBehavior, Image):
    def __init__(self, item_type, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.item_type = item_type
        self.game_screen = game_screen
        self.dragging = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging:
            self.center_x = touch.x
            self.center_y = touch.y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragging:
            self.dragging = False
            self.game_screen.handle_drop(self)
            return True
        return super().on_touch_up(touch)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.score = 0
        self.bins = {}
        self.score_label = Label(text="Skor: 0", font_size=18, pos_hint={'x': .7, 'y': .9})
        self.warning_label = Label(text="", color=(1, 0, 0, 1), font_size=16, pos_hint={'x': .05, 'y': .9})
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.warning_label)
        self.add_bins()
        self.add_items()
        self.add_widget(self.layout)

    def add_bins(self):
        for i, (t, source) in enumerate(BIN_IMAGES.items()):
            x_pos = 0.02 + i * 0.19
            bin_img = Image(source=source, size_hint=(.18, .15), pos_hint={'x': x_pos, 'y': .05})
            self.bins[t] = bin_img
            self.layout.add_widget(bin_img)

    def add_items(self):
        for t, paths in ITEM_IMAGES.items():
            for source in paths:
                x_pos = random.uniform(0.1, 0.8)
                y_pos = random.uniform(0.4, 0.8)
                item = DraggableItem(item_type=t, game_screen=self, source=source, size_hint=(.15, .15),
                                     pos_hint={'x': x_pos, 'y': y_pos})
                self.layout.add_widget(item)

    def handle_drop(self, item):
        bin_img = self.bins.get(item.item_type)
        if bin_img and bin_img.collide_point(item.center_x, item.center_y):
            self.score += 1
            self.update_score()
            self.layout.remove_widget(item)
            self.show_info_card(item.item_type)
        else:
            self.show_warning()

    def update_score(self):
        self.score_label.text = f"Skor: {self.score}"
        self.warning_label.text = ""

    def show_warning(self):
        self.warning_label.text = "Yanlış kutu! Tekrar dene."

    def show_info_card(self, item_type):
        fact = INFO_CARDS.get(item_type, "Geri dönüşüm doğayı korur!")
        content = FloatLayout()
        label = Label(text=f"[b]{item_type.capitalize()} Bilgi Kartı[/b]\n\n{fact}", markup=True,
                      font_size=16, size_hint=(.8, .6), pos_hint={'x': .1, 'y': .3})
        close_btn = Button(text="Kapat", size_hint=(.3, .1), pos_hint={'x': .35, 'y': .1})
        content.add_widget(label)
        content.add_widget(close_btn)
        popup = Popup(title="Bilgi Kartı", content=content, size_hint=(.9, .6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class EcoQuestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    EcoQuestApp().run()