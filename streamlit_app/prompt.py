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