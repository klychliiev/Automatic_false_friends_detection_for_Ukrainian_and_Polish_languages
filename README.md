# Automatic_false_friends_detection_for_Ukrainian_and_Polish_languages

Course project aimed at automatic detection of false friends between Ukrainian and Polish languages using orthographic and semantic features of word pairs

## Contents
Files in this repository:
* requirements.txt - libraries required for installation to run this project
* alignment matrices - folder containing alignment matrices for Ukrainian and Polish languages. These matrices allow us to place vectors of Ukrainian and Polish words in a single vector space
* datasets - folder containing datasets of Ukrainian and Polish word pairs that belong to one of the three categories: false friends, cognates, and unrelated.
* fast_vector.py - script for generation of a multilingual vector space (single vector space for Ukrainian and Polish words in this case)
* homographs_classification.ipynb - code for automatic classification of words based on their orthographic similarity. This script allows us to detect potential cognates and false friends while filtrating unrelated word pairs.
* false_friends_detection.ipynb - code for automatic classification of false friends and cognates using word embeddings
* ! note. to process vectors of Ukrainian and Polish words one must create a new folder "wiki_vectors" and download there bin+text vectors for Ukrainian and Polish from this website: https://fasttext.cc/docs/en/pretrained-vectors.html. 

## Program execution
To execute the program one should run two notebooks in the following order:
1. homographs_classification.ipynb
2. false_friends_detection.ipynb

## Accuracy
The first classifier (homographs classification) showed an overall accuracy of 92%, the second one (false friends and cognates classification) showed an overall accuracy of 82%. Overall accuracy of the model is the mean of the accuracies of the separate classifiers, which is 87%.

```bash 
$ python3 -m venv false-friends 

$ source false-friends/bin/activate

$ streamlit run streamlit_app/app.py 
```