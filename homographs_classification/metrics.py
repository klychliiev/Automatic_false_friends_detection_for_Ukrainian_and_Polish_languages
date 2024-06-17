from difflib import SequenceMatcher
from math import floor, ceil

class SimilarityMetrics: 

    def jaro_distance(self, s1: str, s2: str) -> float:
        """
        Функція для обрахування подібності слів за метрикою "подібність Джаро".
        Приймає на вхід два обʼєкти типу string, які є українським та польським словом, 
        для яких буде обрховується показник подібності.

        Args:
            s1 (str): українська слово;
            s2 (str): польське слово.

        Returns:
            float: обрахований коефіціент подібності для поданих слів.
        """
        
        if (s1 == s2):
            return 1.0
    
        len1 = len(s1)
        len2 = len(s2)
    
        max_dist = floor(max(len1, len2) / 2) - 1
    
        # кількість збігів; початково - 0
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
    
        # перевірка на відсутність збігів
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
    
        # остаточне обрахування показники подібності Джаро
        return (match/ len1 + match / len2 +
                (match - t) / match)/ 3.0

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def levenshtein_distance(self, word1, word2):
        # Create a table to store results of subproblems
        dp = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

        # Fill dp[][] in bottom up manner
        for i in range(len(word1) + 1):
            for j in range(len(word2) + 1):

                # If first string is empty, the only option is to
                # insert all characters of second string
                if i == 0:
                    dp[i][j] = j    # Min. operations = j

                # If second string is empty, the only option is to
                # remove all characters of first string
                elif j == 0:
                    dp[i][j] = i    # Min. operations = i

                # If last characters are the same, ignore the last char
                # and recur for remaining string
                elif word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]

                # If last character is different, consider all
                # possibilities and find the minimum
                else:
                    dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                    dp[i-1][j],        # Remove
                                    dp[i-1][j-1])      # Replace

        return dp[-1][-1]

    def tversky_index(self, s1, s2, alpha=0.5, beta=0.5):
        """
        Функція для обрахування індексу Тверськи для вхідного українського та польського слів.

        Args:
            s1 (str): українське слово;
            s2 (str): польське слово.

        Returns:
            float: обрахований коефіціент подібності для поданих слів.
        """

        # створення сетів для двох слів
        set1, set2 = set(s1), set(s2)

        # обрахування перетинів і відмінностей
        intersection = len(set1 & set2)
        only_in_set1 = len(set1 - set2)
        only_in_set2 = len(set2 - set1)

        # обрахування індексу
        denominator = intersection + alpha * only_in_set1 + beta * only_in_set2
        if denominator == 0:
            return 0  # обробка ділення на 0
        tversky_index = intersection / denominator
        return tversky_index


    def simple_matching_coefficient(self, s1: str, s2: str) -> float:
        """
        Функція для обрахування Simple Matching Coefficient для вхідного українського та польського слів.

        Args:
            s1 (str): українське слово;
            s2 (str): польське слово.

        Returns:
            float: обрахований коефіціент подібності для поданих слів.
        """

        set1, set2 = set(s1), set(s2)

        union = set1.union(set2)
        intersection = set1.intersection(set2)

        m00 = len(union - intersection)  # символи яких нема в жодному зі слів
        m11 = len(intersection)          # є в обох словах
        m01 = len(set1 - set2)           # лише у слові 1
        m10 = len(set2 - set1)           # лише у слові 2

        smc = (m11 + m00) / (m11 + m00 + m01 + m10)
        return smc


    def dices_coefficient(self, word1: str, word2: str) -> float:
        """
        Функція для обрахування коефіцієнта Дайса для вхідного українського та польського слів.

        Args:
            word1 (str): українське слово;
            word2 (str): польське слово.

        Returns:
            float: обрахований коефіціент подібності для поданих слів.
        """
        def generate_character_set(word):
            return set(word)

        set1 = generate_character_set(word1)
        set2 = generate_character_set(word2)

        intersection = len(set1.intersection(set2))
        total_chars = len(set1) + len(set2)

        if total_chars == 0:
            return 0 
        return (2 * intersection) / total_chars

    def overlap_coefficient(self, word1: str, word2: str) -> float:
        """
        Функція для обрахування подібності слів за коефіціентом перетину.
        Приймає на вхід два обʼєкти типу string, які є українським та польським словом, 
        для яких буде обраховано показник подібності за метрикою "коефіціент перетину".

        Args:
            word1 (str): українська слово;
            word2 (str): польське слово.

        Returns:
            float: обрахований коефіціент подібності для поданих слів.
        """

        set1 = set(word1)
        set2 = set(word2)

        intersection_size = len(set1.intersection(set2))

        min_size = min(len(set1), len(set2))

        if min_size == 0:
            return 0 

        return intersection_size / min_size
    
metrics = SimilarityMetrics()