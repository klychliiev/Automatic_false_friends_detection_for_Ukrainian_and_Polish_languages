class ClaudeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.claude.com/v1/"

    def find_false_friends(self, pairs):
        import requests
        import json

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

        template += json.dumps(pairs)

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "claude-1",
            "messages": [
                {
                    'role': 'user',
                    'content': template
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7,
            "response_format": "json"
        }

        response = requests.post(self.base_url + "chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return response.text

# Example usage
api = ClaudeAPI(api_key="your_api_key_here")
pairs = [
    ["слово1", "słowo1"],
    ["слово2", "słowo2"]
]
result = api.find_false_friends(pairs)
print(result)
