from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '480')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.core.window import Window
import random

Window.clearcolor = (0.13, 0.16, 0.23, 1)  # Modern blue-gray

class GuessGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=24, spacing=16, **kwargs)
        self.streak = 0
        self.first_try = True
        self.round = 1  # Track which round we're on
        self.a = random.randint(1, 20)

        self.streak_label = Label(
            text="Streak: 0",
            color=(0.2, 0.9, 0.7, 1),  # Teal
            font_size=26,
            bold=True
        )
        self.add_widget(self.streak_label)

        self.label = Label(
            text="Guess a number between 1 and 20",
            color=(0.95, 0.95, 0.95, 1),
            font_size=20,
            halign='center'
        )
        self.label.text_size = (320 - 40, None)  # Ensure text wraps nicely
        self.add_widget(self.label)

        self.entry = TextInput(
            multiline=False,
            input_filter='int',
            font_size=20,
            background_color=(0.18, 0.22, 0.32, 1),
            foreground_color=(0.95, 0.95, 0.95, 1),
            cursor_color=(0.2, 0.9, 0.7, 1)
        )
        self.add_widget(self.entry)

        self.guess_btn = Button(
            text="Guess",
            background_color=(0.2, 0.7, 0.5, 1),
            font_size=20
        )
        self.guess_btn.bind(on_press=self.check_guess)
        self.add_widget(self.guess_btn)

        self.play_again_btn = Button(
            text="Play Again",
            background_color=(0.25, 0.4, 0.7, 1),
            font_size=20
        )
        self.play_again_btn.bind(on_press=self.play_again)
        self.add_widget(self.play_again_btn)

    def check_guess(self, instance):
        text = self.entry.text.strip()
        # Developer note for 007 with proverb
        if text == "007":
            self.label.text = (
                "🕵️‍♂️ You found the developer! Hehehe.\n"
                "Tip: Keep moving forward, that's how life works!"
            )
            self.label.halign = 'center'
            self.label.text_size = (320 - 40, None)
            anim = Animation(font_size=22, color=(1, 0.8, 0.2, 1), duration=0.5) + Animation(font_size=20, color=(0.95, 0.95, 0.95, 1), duration=0.5)
            anim.start(self.label)
            self.entry.text = ""
            return  
        try:
            guess = int(text)
            if not 1 <= guess <= 20:
                self.label.text = "Enter a number between 1 and 20."
                return

            if guess == self.a:
                # First round: always increase streak to 1, no matter how many tries
                if self.round == 1:
                    self.streak += 1
                    self.streak_label.text = f"Streak: {self.streak}"
                    self.label.text = "🎉 You win! 🎉\nStreak started!"
                # Second round onward: only increase streak if first_try is True
                else:
                    if self.first_try:
                        self.streak += 1
                        self.streak_label.text = f"Streak: {self.streak}"
                        self.label.text = "🎉 First try! Streak increased! 🎉"
                    else:
                        self.streak = 0
                        self.streak_label.text = "Streak: 0"
                        self.label.text = "Correct! But not on first try. Streak reset."
                anim = Animation(font_size=26, color=(0.2, 0.9, 0.7, 1), duration=0.4) + Animation(font_size=20, color=(0.95, 0.95, 0.95, 1), duration=0.4)
                anim.start(self.label)
                from kivy.clock import Clock
                Clock.schedule_once(self.next_round, 1.3)
                self.guess_btn.disabled = True
            elif guess < self.a:
                self.label.text = "My number is greater. Try again."
                self.first_try = False
            else:
                self.label.text = "My number is lesser. Try again."
                self.first_try = False
        except ValueError:
            self.label.text = "Please enter a valid number."

    def next_round(self, dt):
        self.a = random.randint(1, 20)
        self.label.text = "Guess a number between 1 and 20"
        self.guess_btn.disabled = False
        self.entry.text = ""
        self.first_try = True
        self.round += 1

    def play_again(self, instance):
        self.a = random.randint(1, 20)
        self.label.text = "Guess a number between 1 and 20"
        self.guess_btn.disabled = False
        self.entry.text = ""
        self.first_try = True
        self.streak = 0
        self.streak_label.text = "Streak: 0"
        self.round = 1

class GuessApp(App):
    def build(self):
        return GuessGame()

if __name__ == '__main__':
    GuessApp().run()