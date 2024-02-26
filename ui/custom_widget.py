from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.metrics import dp

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
    
    def on_disabled(self, instance, value):
        self.opacity = 0.5 if value else 1.0

class SizedTextInput(TextInput):
    def __init__(self, **kwargs):
        super(SizedTextInput, self).__init__(**kwargs)
        self.write_tab = False
        self.multiline = False
        self.size_hint_y = None
        self.bind(minimum_height=lambda instance, value: setattr(instance, 'height', value))

class SizedButton(Button):
    def __init__(self, **kwargs):
        super(SizedButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(48)

class SizedLabel(Label):
    def __init__(self, **kwargs):
        super(SizedLabel, self).__init__(**kwargs)
        self.size_hint_y = None
        self.bind(texture_size=lambda instance, value: setattr(instance, 'size', value))

class ConfirmPopup(Popup):

    message = StringProperty()

    def __init__(self, message='', **kwargs):
        super(ConfirmPopup, self).__init__(**kwargs)
        self.content = BoxLayout(orientation='vertical', spacing=dp(8))
        self.content.add_widget(Widget())
        self.message_label = SizedLabel(text=message)
        self.content.add_widget(self.message_label)
        self.content.add_widget(Widget())
        self.message = message

        dismiss_button = SizedButton(text='OK')
        dismiss_button.bind(on_press=self.dismiss)
        self.content.add_widget(dismiss_button)
        self.size_hint_y = None
        self.height = dp(192)
    
    def on_message(self, instance, value):
        self.message_label.text = value

class YesNoPopup(Popup):

    message = StringProperty()

    def __init__(self, message='', **kwargs):
        super(YesNoPopup, self).__init__(**kwargs)
        self.content = BoxLayout(orientation='vertical', spacing=dp(8))
        self.content.add_widget(Widget())
        self.message_label = SizedLabel(text=message)
        self.content.add_widget(self.message_label)
        self.content.add_widget(Widget())
        self.message = message

        self.yes_button = SizedButton(text='Si')
        self.yes_button.bind(on_press=self.dismiss_popup)
        self.no_button = SizedButton(text='No')
        self.no_button.bind(on_press=self.dismiss_popup)
        button_layout = BoxLayout(spacing=dp(8))
        button_layout.add_widget(self.yes_button)
        button_layout.add_widget(self.no_button)

        self.content.add_widget(button_layout)
        self.size_hint_y = None
        self.height = dp(192)
    
    def on_message(self, instance, value):
        self.message_label.text = value
    
    def dismiss_popup(self, instance):
        if instance == self.yes_button:
            self.yes_callback()
        else:
            self.no_callback()
        self.dismiss()
    
    def yes_callback(self):
        pass
    
    def no_callback(self):
        pass
