import re

import unicodedata

class LinguisticRules:

    def remove_diacritics(self, text):
        normalized_text = unicodedata.normalize('NFKD', text)
        return ''.join([c for c in normalized_text if not unicodedata.combining(c)])

    def replace_suffix(self, text):
        return re.sub(r"(ok|yk|ik)$", "ek", text)


    # Function to replace prefix 'vid' with 'od'
    def replace_prefix(self, text):
        return re.sub(r"^vid", "od", text)


    # Function to replace 'sh' at the beginning of a word with 'sz'
    def replace_sh_with_sz(self, text):
        return re.sub(r"^sh", "sz", text)


    # Function to replace 'uwa' with 'owa'
    def replace_uwa_with_owa(self, text):
        return re.sub(r"uva", "ova", text)


    def replace_ch_with_cz(self, text):
        return re.sub(r"ch", "cz", text)
        
    def ere(self, text):
        return re.sub(r"ere", "rze", text)

    def je(self, text):
        return re.sub(r"^je", "o", text)

    def sie(self, text):
        return re.sub(r"sie", "si", text)

    def nie(self, text):
        return re.sub(r"nie", "ne", text)

    def dz(self, text):
        return re.sub(r"dz", "d", text)

    def rz(self, text):
        return re.sub(r"rz", "r", text)

    def replace_ti_with_c(self, text):
        return re.sub(r'ti$', 'c', text)
    
rules = LinguisticRules()