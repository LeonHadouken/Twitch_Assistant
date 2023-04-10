import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from translate import Translator


class SpeechTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Речь в текст с переводом")

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.devices_frame = tk.Frame(self.root)
        self.devices_frame.pack(pady=10)

        self.mic_label = tk.Label(self.devices_frame, text="Выберите устройство записи:")
        self.mic_label.pack(side=tk.LEFT, padx=10)

        # выводим информацию обо всех устройствах ввода
        self.mic_devices = sr.Microphone.list_microphone_names()
        self.current_device = tk.StringVar()
        self.devices_dropdown = ttk.Combobox(self.devices_frame, values=self.mic_devices, textvariable=self.current_device)
        self.devices_dropdown.current(0)
        self.devices_dropdown.pack(side=tk.LEFT)

        self.translate_btn = tk.Button(self.root, text="Перевести", command=self.speech_trans)
        self.translate_btn.pack(pady=10)

        self.translated_text = tk.Text(self.root, height=10, width=50)
        self.translated_text.pack(pady=10)

    def speech_trans(self):
        # настраиваем объект Recognizer, чтобы он использовал выбранное устройство
        r = sr.Recognizer()
        current_device = self.devices_dropdown.current()

        with sr.Microphone(device_index=current_device) as source:
            # настраиваем параметры распознавания
            r.adjust_for_ambient_noise(source)
            print("Скажите что-нибудь...")
            # записываем аудио с микрофона
            audio = r.listen(source)
            # распознаем речь с помощью Google Speech Recognition
            response = r.recognize_google(audio, language='ru-RU', show_all=True)
            if 'alternative' in response:
                text = response['alternative'][0]['transcript']
                # переводим текст с помощью библиотеки translate
                translator = Translator(to_lang="en", from_lang="ru")
                translation = translator.translate(text)
                self.translated_text.delete('1.0', tk.END)
                self.translated_text.insert('1.0', translation)
            else:
                self.translated_text.delete('1.0', tk.END)
                self.translated_text.insert('1.0', "Речь не распознана")


if __name__ == "__main__":
    speech_translator = SpeechTranslator()
