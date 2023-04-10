import speech_recognition as sr
from googletrans import Translator
import tkinter as tk

# получаем список доступных устройств
devices = sr.Microphone.list_microphone_names()

# создаем графический интерфейс
root = tk.Tk()
root.geometry('300x200')
root.title('Выбор устройства записи')

# создаем надпись для выбора устройства
label = tk.Label(root, text='Выберите устройство записи:')
label.pack()

# создаем выпадающий список для выбора устройства
var = tk.StringVar()
var.set(devices[0])  # по умолчанию выбрано первое устройство
dropdown = tk.OptionMenu(root, var, *devices)
dropdown.pack()

# создаем кнопку для запуска записи
def start_recording():
    # получаем выбранное устройство записи
    device_index = devices.index(var.get())

    # настраиваем объект Recognizer, чтобы он использовал выбранное устройство
    r = sr.Recognizer()

    # запускаем запись звука
    with sr.Microphone(device_index=device_index) as source:
        # настраиваем параметры распознавания
        r.adjust_for_ambient_noise(source)
        print("Скажите что-нибудь...")
        # записываем аудио с микрофона
        audio = r.listen(source)
        # распознаем речь с помощью Google Speech Recognition
        try:
            text = r.recognize_google(audio, language='ru-RU')
            # print(f"Вы сказали: {text}")
            # переводим текст с помощью библиотеки translate
            translator = Translator()
            translation = translator.translate(text, dest='en')
            print(translation)
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания речи: ", e)

button = tk.Button(root, text='Запись', command=start_recording)
button.pack()

root.mainloop()
