from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from auth_token import AUTH_TOKEN


class nllb200:
    def __init__(self, src_lang):
        self.pretrained_model_name = "facebook/nllb-200-distilled-600M"
        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrained_model_name, use_auth_token=AUTH_TOKEN, src_lang=src_lang)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.pretrained_model_name, use_auth_token=AUTH_TOKEN)

    def translate(self, text, target_lang, max_length=1024):
        if target_lang == 'EN' or target_lang == 'EN-GB' or target_lang == 'EN-US':
            target_lang = "eng_Latn"
        if target_lang == 'PT' or target_lang == 'PT-BR':
            target_lang = "por_Latn"
        inputs = self.tokenizer(text, return_tensors="pt")
        translated_tokens = self.model.generate(**inputs, forced_bos_token_id=self.tokenizer.lang_code_to_id[target_lang], max_length=max_length)
        result = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
        return result[0]
