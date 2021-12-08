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
            audio = recognizer.listen(microphone, 5, 5)

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


def get_person(lang):
    if lang == 'ru':
        return parser.get_random_author_ru()
    elif lang == 'en':
        return parser.get_random_author_en()


def change_lang(eng, lang):
    id_ = ''
    if lang == 'en':
        id_ = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
    elif lang == 'ru':
        id_ = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
    for voice in eng.getProperty('voices'):
        if id_ == voice.id:
            eng.setProperty('voice', voice.id)
            return True


def main():
    eng = pyttsx3.init()
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    language = input('Choose language: en - English, ru - Russian: ')
    print('You choose: ' + language)
    if change_lang(eng, language):
        while True:
            result = voice_recognition(recognizer, microphone, language)
            if not result:
                continue
            print(result + '\n')
            if result == phrases['command1'][language]:
                text = get_poem(language)
                print(text)
            elif result == phrases['stop'][language]:
                text = phrases['off'][language]
            elif result == phrases['person'][language]:
                text = get_person(language)
                print(text)
            else:
                text = phrases['unknown_command'][language]
                print(text)
            speech_synthesis(eng, text)
            if result == phrases['stop'][language]:
                break


if __name__ == '__main__':
    main()
