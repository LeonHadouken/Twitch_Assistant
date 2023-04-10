import tkinter as tk
import speech_recognition as sr
from translate import Translator


class TranslatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Голосовой переводчик")

        # создаем список доступных аудиоустройств
        self.devices = sr.Microphone.list_microphone_names()
        self.selected_device = tk.StringVar(value=self.devices[0])

        # добавляем выпадающий список для выбора аудиоустройства
        device_label = tk.Label(self.root, text="Выберите аудиоустройство")
        device_label.pack()
        device_dropdown = tk.OptionMenu(self.root, self.selected_device, *self.devices)
        device_dropdown.pack()

        # добавляем кнопку запуска записи
        record_button = tk.Button(self.root, text="Распознать и перевести", command=self.record)
        record_button.pack()

        # добавляем текстовую область для отображения перевода
        self.translation_text = tk.Text(self.root)
        self.translation_text.pack()

    def record(self):
        # получаем индекс выбранного аудиоустройства
        device_index = self.devices.index(self.selected_device.get())

        # создаем объект Recognizer, чтобы он использовал выбранное устройство
        r = sr.Recognizer()

        with sr.Microphone(device_index=device_index) as source:
            # настраиваем параметры распознавания
            r.adjust_for_ambient_noise(source)
            self.translation_text.delete("1.0", tk.END)
            self.translation_text.insert("1.0", "Скажите что-нибудь...\n")
            # записываем аудио с микрофона
            audio = r.listen(source)
            # распознаем речь с помощью Google Speech Recognition
            try:
                text = r.recognize_google(audio, language='ru-RU')
                # переводим текст с помощью библиотеки translate
                translator = Translator(to_lang="en", from_lang="ru")
                translation = translator.translate(text)
                self.translation_text.insert(tk.END, f"Вы сказали: {text}\n")
                self.translation_text.insert(tk.END, f"Перевод: {translation.text}\n")
            except sr.UnknownValueError:
                self.translation_text.insert(tk.END, "Речь не распознана\n")
            except sr.RequestError as e:
                self.translation_text.insert(tk.END, f"Ошибка сервиса распознавания речи: {e}\n")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TranslatorGUI()
    app.run()
