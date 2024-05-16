from polyglot.downloader import downloader
from polyglot.text import Text 
from math import floor, ceil
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd
from difflib import SequenceMatcher

from rules import linguistic_rules
import unicodedata


class Classifier:

    def __init__(self):
        self.y_true, self.word_pairs = self.preprocess_data('datasets/dataset.csv')

    def preprocess_data(self, file_path):
        dataset = pd.read_csv(file_path)
        dataset = dataset.drop('Unnamed: 0', axis=1)
        dataset['orthographic_sim'] = dataset['false_friends'].replace({0: 1, 1: 1, 2: 0})

        word_pairs = []
        y_true = []

        for _, row in dataset.iterrows():
            pl_word = row[1]
            uk_word = row[2]

            if uk_word != '':  # Check if uk_word is not an empty string
                blob = uk_word
                text = Text(blob, hint_language_code='uk')
                if "’" in text:
                    text = text.replace("’", "й")
                uk_transliterated = str(text.transliterate('en')[0])

                blob2 = pl_word
                text2 = Text(blob2, hint_language_code='pl')
                pl_transliterated = str(text2.transliterate('en')[0])

                word_pairs.append((uk_transliterated, pl_transliterated))
                y_true.append(row['orthographic_sim'])  # Append the corresponding value to y_true

        return y_true, word_pairs

    @staticmethod
    def remove_diacritics(text):
        normalized_text = unicodedata.normalize('NFKD', text)
        return ''.join([c for c in normalized_text if not unicodedata.combining(c)])

    def apply_diacritics(self):
        self.normalized = [(first, Classifier.remove_diacritics(second)) for first, second in self.word_pairs]
        return self.normalized

    def apply_rules(self):
        self.modified_list = [
        (
            linguistic_rules.replace_suffix(
                linguistic_rules.ere(
                    linguistic_rules.replace_ch_with_cz(
                        linguistic_rules.replace_prefix(
                            linguistic_rules.replace_sh_with_sz(
                                linguistic_rules.replace_uwa_with_owa(
                                    t[0]
                                )
                            )
                        )
                    )
                )
            ).replace('v','w'),
            linguistic_rules.replace_sh_with_sz(
                linguistic_rules.replace_ch_with_cz(
                    t[1]
                )
            ).replace('v','w')
        )
        for t in self.normalized
        ]

        return self.modified_list

    


