from __future__ import annotations

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty

from .config import CORPUS_DIR, MOSAIC_DIR, CORPUS_CACHE, MOSAIC_CACHE, LAST_VISITED_DIR
from .utils import capture_exceptions, log_done, log_message, UserConfirmation

from ..features import Corpus, Mosaic
from ..config import AUDIO_FORMATS

from tkinter.filedialog import askopenfilename
import os


class MosaicFactoryWidget(Widget):
    delete_mosaic_button = ObjectProperty(None)
    create_mosaic_button = ObjectProperty(None)
    mosaic_name = ObjectProperty(None)
    target = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.has_name = False
        Clock.schedule_once(lambda _: self.mosaic_name.bind(text=self.on_mosaic_name_update), 1)

    def get_selected_corpora(self):
        return [toggle.text for toggle in App.get_running_app().root.corpus_module.menu.corpora_menu.children if toggle.state == 'down']

    def update_create_mosaic_button(self):
        value = all([self.has_name, self.get_selected_corpora(), self.target])
        self.create_mosaic_button.set_disabled(not value)

    def on_mosaic_name_update(self, instance, value):
        self.has_name = bool(value)
        self.update_create_mosaic_button()

    def update_mosaic_menu(self):
        App.get_running_app().root.mosaic_module.menu.update_mosaic_menu()

    def load_target(self):
        global LAST_VISITED_DIR
        self.target = askopenfilename(filetypes=[('Audio files', " ".join(AUDIO_FORMATS))], initialdir=LAST_VISITED_DIR)
        if self.target:
            LAST_VISITED_DIR = os.path.dirname(self.target)
        self.update_create_mosaic_button()

    @capture_exceptions
    @log_done
    def create_mosaic(self):
        mosaic_name = self.mosaic_name.text
        log_message(f"Creating mosaic: {mosaic_name}...")
        corpus_names = self.get_selected_corpora()
        corpora = []
        for corpus_name in corpus_names:
            log_message(f"Loading corpus: {corpus_name}...")
            if corpus_name in CORPUS_CACHE:
                corpora.append(CORPUS_CACHE[corpus_name])
            else:
                path = os.path.join(CORPUS_DIR, f"{corpus_name}.gamut")
                corpus = Corpus().read(path)
                corpora.append(corpus)
                CORPUS_CACHE[corpus_name] = corpus
        log_message(f"Maching segments...")
        global MOSAIC_CACHE
        mosaic = Mosaic(target=self.target, corpus=corpora)
        mosaic.write(os.path.join(MOSAIC_DIR, f'{mosaic_name}.gamut'))
        MOSAIC_CACHE[mosaic_name] = mosaic
        self.update_mosaic_menu()


class MosaicMenuWidget(Widget):
    delete_mosaic_button = ObjectProperty(None)
    mosaic_menu = ObjectProperty(None)
    audio_module = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_mosaic = None
        Clock.schedule_once(lambda _: self.update_mosaic_menu(), 1)

    def update_mosaic_menu(self):
        last_selected = [toggle.text for toggle in self.get_selected_toggles()]
        self.clear_menu()
        for path in sorted(os.listdir(MOSAIC_DIR)):
            mosaic_name = os.path.basename(os.path.splitext(path)[0])
            state = 'down' if mosaic_name in last_selected else 'normal'
            t = ToggleButton(text=mosaic_name,
                             state=state,
                             on_release=lambda toggle: self.exclusive_select(toggle) or self.update_delete_button())
            self.mosaic_menu.add_widget(t)
        self.update_delete_button()

    def clear_menu(self):
        while self.mosaic_menu.children:
            self.mosaic_menu.clear_widgets()
        self.update_delete_button()

    def exclusive_select(self, toggle):
        if toggle.state == 'normal':
            self.selected_mosaic = None
        else:
            for child in self.mosaic_menu.children:
                if child != toggle:
                    child.state = 'normal'
            self.selected_mosaic = toggle.text
        self.update_audio_synth_button()

    def delete_selected_mosaics(self):
        def on_confirm():
            for toggle in self.get_selected_toggles():
                self.mosaic_menu.remove_widget(toggle)
                os.remove(os.path.join(MOSAIC_DIR, f"{toggle.text}.gamut"))
            self.selected_mosaic = None
            self.update_delete_button()
            self.update_audio_synth_button()
            log_message(f"Mosaic deleted", log_type='error')
        UserConfirmation(on_confirm=on_confirm, long_text=f"You're about to delete this mosaic.").open()

    def update_audio_synth_button(self):
        App.get_running_app().root.mosaic_module.audio_module.synth_button.set_disabled(not bool(self.selected_mosaic))

    def get_selected_toggles(self):
        return [toggle for toggle in self.mosaic_menu.children if toggle.state == 'down']

    def update_delete_button(self):
        self.delete_mosaic_button.set_disabled(not bool(self.get_selected_toggles()))


class MosaicWidget(Widget):
    menu = ObjectProperty(None)
    factory = ObjectProperty(None)
