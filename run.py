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
        try:
            text = r.recognize_google(audio, language='ru-RU')
            # переводим текст с помощью библиотеки translate
            translator = Translator(to_lang="en", from_lang="ru")
            translation = translator.translate(text)
            # print(f"Вы сказали: {text}")
            print(f"Перевод на английский: {translation}")
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания речи: ", e)

while True:
    speech_trans()


