PROMPT_TEMPLATE = """
False friends are words in similar languages which have similar spelling, but different meaning. 
Cognates, on the other hand, are words in similar languages which have both similar spelling and meaning.
Find pairs of false friends and cognates in the following texts between Ukrainian and Polish languages.

Output must be formatted as follows:

**False friends**
1. Матка - Matka
2. Ангельський - Angielski
3. Склеп - Sklep

**Cognates**
1. Хліб - Chleb
2. Пес - Pies 
3. Розмова - Rozmowa

No other comments. Only listings of false friends and cognates. If you can't find false friends or cognates, keep the list empty. 

Now, search for false friends and cognates in given texts.
Ukrainian text: 
{ukrainian_text}

Polish text: 
{polish_text}
"""

FALSE_FRIENDS_TEMPLATE = ""
COGNATES_TEMPLATE = ""