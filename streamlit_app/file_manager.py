from math import floor
import spacy
from polyglot.text import Text
from openai import OpenAI
from wiktionaryparser import WiktionaryParser
import json

class FileManager: 

    def __init__(self, api_key: str):
        self.uk_nlp = spacy.load('uk_core_news_sm')
        self.pl_nlp = spacy.load('pl_core_news_sm')
        self.client = OpenAI(
            api_key=api_key
        )
        self.wiktionary_parser = WiktionaryParser()

    def jaro_distance(self, s1, s2):
        
        if (s1 == s2):
            return 1.0
    
        len1 = len(s1)
        len2 = len(s2)

        max_dist = floor(max(len1, len2) / 2) - 1
    
        match = 0
    
        hash_s1 = [0] * len(s1)
        hash_s2 = [0] * len(s2)
    
        for i in range(len1):
    
            for j in range(max(0, i - max_dist),
                        min(len2, i + max_dist + 1)):
                
                if (s1[i] == s2[j] and hash_s2[j] == 0):
                    hash_s1[i] = 1
                    hash_s2[j] = 1
                    match += 1
                    break
    
        if (match == 0):
            return 0.0
    
        t = 0
        point = 0
    
        for i in range(len1):
            if (hash_s1[i]):
    
                while (hash_s2[point] == 0):
                    point += 1
    
                if (s1[i] != s2[point]):
                    t += 1
                point += 1
        t = t//2
    
        return (match/ len1 + match / len2 +
                (match - t) / match)/ 3.0

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

        return uk_lemmas, pl_lemmas 

    def create_candidate_pairs(self, uk_lemmas, pl_lemmas):
        uk_trans = {str(Text(lemma.lower(), hint_language_code='uk').transliterate('en')[0]).encode('utf-8'): lemma for lemma in uk_lemmas}
        pl_trans = {str(Text(lemma.lower(), hint_language_code='pl').transliterate('en')[0]).encode('utf-8'): lemma for lemma in pl_lemmas}

        similar_pairs = []
        contexts = []
        for u_word in uk_trans:
            for p_word in pl_trans:
                if self.jaro_distance(u_word, p_word) >= 0.8:
                    similar_pairs.append((uk_trans[u_word], pl_trans[p_word]))
                    contexts.append((uk_trans[u_word], pl_trans[p_word], uk_lemmas[uk_trans[u_word]], pl_lemmas[pl_trans[p_word]]))

        return similar_pairs, contexts

    def fetch_definition(self, word, language):
        result = self.wiktionary_parser.fetch(word, language)
        if result and 'definitions' in result[0] and result[0]['definitions']:
            return result[0]['definitions'][0]
        return {}

    def find_false_friends(self, pairs, contexts):

        template = """Task: Determine if the following pairs of Ukrainian and Polish words are false friends (different meanings) or cognates (similar meanings) and explain why.

        Example:
        {
        "word_pairs": [
            {
            "pair": {
                "рак":{}, 
                "rak":{}      
            },
            "false_friends": "False",
            "explanation":"These words are cognates because ..."
            },
            {
            "pair": {
                "магазин":{}, 
                "magazyn":{}      
            },
            "false_friends": "True",
            "explanation":"These words are false friends because ..."
            }
        ]
        }

        Return the valid JSON as above for the following Ukrainian-Polish word pairs: """ 

        template += str(pairs)

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type":"json_object"},
            messages = [
                {
                'role':'user',
                'content':template
                }
            ]
        )
        result = response.choices[0].message.content

        result_json = json.loads(result)
        
        for pair in result_json['word_pairs']:
            uk_word = list(pair['pair'].keys())[0]
            pl_word = list(pair['pair'].keys())[1]
            for context in contexts:
                if context[0] == uk_word and context[1] == pl_word:
                    pair['pair'][uk_word]['sentence'] = context[2]
                    pair['pair'][pl_word]['sentence'] = context[3]
                    pair['pair'][uk_word]['definition'] = self.fetch_definition(uk_word, 'ukrainian')
                    pair['pair'][pl_word]['definition'] = self.fetch_definition(pl_word, 'polish')
                    break

        return result_json

# Example usage:
# api_key = "your_openai_api_key"
# fm = FileManager(api_key)
# ukr_text = "your_ukrainian_text"
# pl_text = "your_polish_text"
# uk_lemmas, pl_lemmas = fm.process_text(ukr_text, pl_text)
# pairs, contexts = fm.create_candidate_pairs(uk_lemmas, pl_lemmas)
# result = fm.find_false_friends(pairs, contexts)
# print(result)
