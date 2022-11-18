import deepl
from auth_key import AUTH_KEY
from languages import target_lang


def init_deepl():
    return deepl.Translator(AUTH_KEY)

def translate_text(text, target_lang, translator):
    if target_lang == 'EN':
        target_lang = 'EN-US'
    elif target_lang == 'PT':
        target_lang = 'PT-BR'
    return translator.translate_text(text, target_lang=target_lang).text