from math import floor
import json

import spacy
from polyglot.text import Text
from openai import OpenAI


from prompt import template


class FileManager:

    def __init__(self, api_key: str):
        self.uk_nlp = spacy.load("uk_core_news_sm")
        self.pl_nlp = spacy.load("pl_core_news_sm")
        self.key = api_key

    @staticmethod
    def jaro_distance(s1, s2):

        if s1 == s2:
            return 1.0

        len1 = len(s1)
        len2 = len(s2)

        max_dist = floor(max(len1, len2) / 2) - 1

        match = 0

        hash_s1 = [0] * len(s1)
        hash_s2 = [0] * len(s2)

        for i in range(len1):

            for j in range(max(0, i - max_dist), min(len2, i + max_dist + 1)):

                if s1[i] == s2[j] and hash_s2[j] == 0:
                    hash_s1[i] = 1
                    hash_s2[j] = 1
                    match += 1
                    break

        if match == 0:
            return 0.0

        t = 0
        point = 0

        for i in range(len1):
            if hash_s1[i]:

                while hash_s2[point] == 0:
                    point += 1

                if s1[i] != s2[point]:
                    t += 1
                point += 1
        t = t // 2

        return (match / len1 + match / len2 + (match - t) / match) / 3.0

    def process_text(self, ukr_text, pl_text):
        uk_doc = self.uk_nlp(ukr_text)
        pl_doc = self.pl_nlp(pl_text)

        uk_lemmas = {}
        pl_lemmas = {}

        for sent in uk_doc.sents:
            for token in sent:
                if token.is_alpha and not token.is_stop:
                    lemma = token.lemma_
                    if lemma not in uk_lemmas:
                        uk_lemmas[lemma] = []
                    uk_lemmas[lemma].append(sent.text)

        for sent in pl_doc.sents:
            for token in sent:
                if token.is_alpha and not token.is_stop:
                    lemma = token.lemma_
                    if lemma not in pl_lemmas:
                        pl_lemmas[lemma] = []
                    pl_lemmas[lemma].append(sent.text)

        print(uk_lemmas)
        return uk_lemmas, pl_lemmas

    def create_candidate_pairs(self, uk_lemmas, pl_lemmas):
        uk_trans = {
            str(
                Text(lemma.lower(), hint_language_code="uk").transliterate("en")[0]
            ).encode("utf-8"): lemma
            for lemma in uk_lemmas
        }
        pl_trans = {
            str(
                Text(lemma.lower(), hint_language_code="pl").transliterate("en")[0]
            ).encode("utf-8"): lemma
            for lemma in pl_lemmas
        }

        similar_pairs = []
        contexts = []
        for u_word in uk_trans:
            for p_word in pl_trans:
                jaro_sim = FileManager.jaro_distance(u_word, p_word)
                if jaro_sim >= 0.7:
                    similar_pairs.append((uk_trans[u_word], pl_trans[p_word]))
                    contexts.append(
                        (
                            uk_trans[u_word],
                            pl_trans[p_word],
                            uk_lemmas[uk_trans[u_word]],
                            pl_lemmas[pl_trans[p_word]],
                        )
                    )

        return similar_pairs, contexts

    def find_false_friends(self, template, pairs, contexts):

        template += str(pairs)

        client = OpenAI(api_key=self.key)

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": template}],
        )
        result = response.choices[0].message.content

        result_json = json.loads(result)

        for pair in result_json["word_pairs"]:
            uk_word = list(pair["pair"].keys())[0]
            pl_word = list(pair["pair"].keys())[1]
            for context in contexts:
                if context[0] == uk_word and context[1] == pl_word:
                    pair["pair"][uk_word]["sentence"] = context[2]
                    pair["pair"][pl_word]["sentence"] = context[3]
                    break

        return result_json
