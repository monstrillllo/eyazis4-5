import pyttsx3
import speech_recognition
import parser
from phrases import phrases


def speech_synthesis(engine: pyttsx3.Engine, text_: str) -> None:
    engine.say(text_)
    engine.runAndWait()


def voice_recognition(recognizer, microphone, lang='ru'):
    if lang == 'en':
        lang = 'en-US'
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 0, 10)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=lang).lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


def get_poem(lang):
    if lang == 'ru':
        main_page = parser.get_src(parser.url_ru)
        poem_url = parser.get_random_poem_ru(main_page)
        poem_page = parser.get_src(poem_url)
        return parser.get_text(poem_page)
    elif lang == 'en':
        page = parser.get_src(parser.url_en)
        return parser.get_random_poem_en(page)


def main():
    eng = pyttsx3.init()
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    language = input('Choose language: en - English, ru - Russian: ')
    print('You choose: ' + language)
    while True:
        result = voice_recognition(recognizer, microphone, language)
        print(result + '\n')
        if result == phrases['command1'][language]:
            text = get_poem(language)
            print(text)
        elif result == phrases['stop'][language]:
            text = phrases['off'][language]
        else:
            text = phrases['unknown_command'][language]
        speech_synthesis(eng, text)
        if result == phrases['stop'][language]:
            break


if __name__ == '__main__':
    main()
