# Automatic_false_friends_detection_for_Ukrainian_and_Polish_languages

Course project aimed at automatic detection of false friends between Ukrainian and Polish languages using orthographic and semantic features of word pairs
Files in this repository:
* requirements.txt - libraries required for installation to run this project
* alignment matrices - folder containing alignment matrices for Ukrainian and Polish languages. These matrices allow us to place vectors of Ukrainian and Polish words in a single vector space
* datasets - folder containing datasets of Ukrainian and Polish word pairs that belong to one of the three categories: false friends, cognates, and unrelated.
* fast_vector.py - script for generation of multilingual vector space (single vector space for Ukrainian and Polish words in this case)
* homographs_classification.ipynb - code for automatic classification of words based on their othpgraphic similarity. This script allows us to detect potential cognates and false friends while filtrating unrelated word pairs.
* false_friends_detection.ipynb - code for automatic classification of false friends and cognates using word embeddings
To process vectors of Ukrainian and Polish words one must create a new folder "wiki_vectors" and download there bin+text vectors for Ukrainian and Polish from this website: https://fasttext.cc/docs/en/pretrained-vectors.html. 
