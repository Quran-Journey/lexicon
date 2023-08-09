import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector()


def check_lang(sentence: str):
    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    text = sentence
    doc = nlp(text)
    return doc._.language

# https://pypi.org/project/spacy-langdetect/
# To use
# need to install -> download spacy library or package
#                    pip install spacy-langdetect
#                    python -m spacy download en_core_web_sm


def get_lang(text):
    translator = Translator()

    lang = check_lang(text)
    # print(lang)
    if lang['language'] == 'ar':
        # print(f' {text} is Arabic')
        return 'Arabic'

    elif lang['language'] == 'en':
        # print(f" '{text}' is English")
        return 'English'

    else:
        # print()
        # print(f" '{text}' is not in either")
        # print()
        return 'Neither'
