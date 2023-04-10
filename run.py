import speech_recognition as sr
from translate import Translator


# выводим информацию обо всех устройствах ввода
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Устройство {index}: {name}")

# запрашиваем у пользователя выбор устройства
current_device = int(input("Введите номер устройства, которое вы хотите использовать: "))

# настраиваем объект Recognizer, чтобы он использовал выбранное устройство
r = sr.Recognizer()

def speech_trans():
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
            print(translation)
        else:
            print("Речь не распознана")

while True:
    speech_trans()
