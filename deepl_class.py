import deepl
from auth_key import AUTH_KEY

class deepl_translator:
    def __init__(self, src_lang):
        self.translator = deepl.Translator(AUTH_KEY)
        self.src_lang = src_lang
    
    def translate(self, text, target_lang):
        if target_lang == 'EN':
            target_lang = 'EN-US'
        elif target_lang == 'PT':
            target_lang = 'PT-BR'
        translate_text = None
        try:
            translate_text = self.translator.translate_text(text, source_lang=self.src_lang, target_lang=target_lang).text
        except Exception as e:
            translate_text = e
        return translate_text