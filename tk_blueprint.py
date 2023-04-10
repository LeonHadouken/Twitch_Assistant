import tkinter as tk
import speech_recognition as sr
from translate import Translator


class App:
    def __init__(self, root):
        self.root = root
        self.init_ui()

    def init_ui(self):
        # создаем текстовое поле
        self.text = tk.Text(self.root, height=10, width=50)
        self.text.pack()

        # создаем кнопку и связываем ее с функцией
        self.button = tk.Button(self.root, text="Нажми меня!", command=self.speech_trans)
        self.button.pack(pady=10)

    def speech_trans(self):
        with sr.Microphone() as source:
            # настраиваем параметры распознавания
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            print("Скажите что-нибудь...")

            # записываем аудио с микрофона
            audio = r.listen(source)

            # распознаем речь с помощью Google Speech Recognition
            try:
                text = r.recognize_google(audio, language='ru-RU')
                # переводим текст с помощью библиотеки translate
                translator = Translator(to_lang="en", from_lang="ru")
                translation = translator.translate(text)
                self.text.delete(1.0, tk.END)  # очищаем текстовое поле
                self.text.insert(tk.END, f"Вы сказали: {text}\nПеревод на английский: {translation}")
            except sr.UnknownValueError:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, "Речь не распознана")
            except sr.RequestError as e:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, f"Ошибка сервиса распознавания речи: {e}")


root = tk.Tk()
app = App(root)
root.mainloop()
