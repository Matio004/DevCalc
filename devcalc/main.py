from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

from devcalculator import Calculator
from colorchooser import ColorChooser


class DevCalculator(App):
    # Root Settings
    icon = 'icon.png'
    title = None  # 'Kalkulator Programisty'

    def build(self):
        screen_manager = ScreenManager(transition=SlideTransition())
        calc_screen = Screen(name='calc')
        calc_screen.add_widget(Calculator())
        color_screen = Screen(name='color')
        color_screen.add_widget(ColorChooser())
        screen_manager.add_widget(calc_screen)
        screen_manager.add_widget(color_screen)
        return screen_manager


if __name__ == "__main__":
    DevCalculator().run()
