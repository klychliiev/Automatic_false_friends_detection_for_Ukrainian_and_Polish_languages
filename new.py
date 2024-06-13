import numpy as np
import pandas as pd
import torch
from transformers import BertModel, BertTokenizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Sample dataset
data = {
    'word1': ['snidanek', 'kawa', 'angelski', 'garbus'],
    'word2': ['sniadanie', 'kawa', 'angielski', 'arbuz'],
    'label': [0, 0, 1, 1]  # 0: true friend, 1: false friend
}

df = pd.DataFrame(data)

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')

# Function to get embeddings
def get_embedding(word):
    inputs = tokenizer(word, return_tensors='pt')
    outputs = model(**inputs)
    # Use the embeddings of the [CLS] token
    return outputs.last_hidden_state[:, 0, :].detach().numpy()

# Extract embeddings and calculate cosine similarity
def embedding_similarity(word1, word2):
    emb1 = get_embedding(word1)
    emb2 = get_embedding(word2)
    return np.dot(emb1, emb2.T) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

df['embedding_similarity'] = df.apply(lambda row: embedding_similarity(row['word1'], row['word2']), axis=1)

# Prepare data for training
X = df[['embedding_similarity']].values
y = df['label'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Prediction and evaluation
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# Output results
# Accuracy: (depends on the dataset)
# Precision: (depends on the dataset)
# Recall: (depends on the dataset)
# F1 Score: (depends on the dataset)