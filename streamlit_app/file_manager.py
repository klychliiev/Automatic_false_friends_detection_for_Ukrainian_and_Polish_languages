from math import floor 
import spacy 
from polyglot.text import Text
from openai import OpenAI


class FileManager: 

    def __init__(self, api_key: str):
        self.uk_nlp = spacy.load('uk_core_news_sm')
        self.pl_nlp = spacy.load('pl_core_news_sm')
        self.client = OpenAI(
            api_key=api_key
        )

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

        uk_lemmas = [token.lemma_ for token in uk_doc if token.is_alpha and not token.is_stop]
        pl_lemmas = [token.lemma_ for token in pl_doc if token.is_alpha and not token.is_stop]

        return uk_lemmas, pl_lemmas 
    
    def create_candidate_pairs(self, uk_lemmas, pl_lemmas):
        # uk_lemmas, pl_lemmas = self.process_text()

        uk_trans = {str(Text(word.lower(), hint_language_code='uk').transliterate('en')[0]).encode('utf-8'):word for word in uk_lemmas}
        pl_trans = {str(Text(word.lower(), hint_language_code='pl').transliterate('en')[0]).encode('utf-8'):word for word in pl_lemmas}

        similar_pairs = []
        for u_word in uk_trans:
            for p_word in pl_trans:
                if self.jaro_distance(u_word, p_word) >= 0.8:
                    similar_pairs.append((uk_trans[u_word], pl_trans[p_word]))

        return similar_pairs

    def find_false_friends(self, pairs):

        # similar_pairs = self.create_candidate_pairs()

        template = """Task: Determine if the following pairs of Ukrainian and Polish words are false friends (different meanings) or cognates (similar meanings).

        Example:
        {
        "word_pairs": [
            {
            "words": ["рак", "rak"],
            "status": "Cognates"
            },
            {
            "words": ["магазин", "magazyn"],
            "status": "False friends"
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
        return response.choices[0].message.content
