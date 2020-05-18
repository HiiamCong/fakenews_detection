# INSTALL:
conda env create -f conda_environment_export.yml

pip install spacy==2.1.3
python -m spacy download en_core_web_sm

import nltk
nltk.download('wordnet')

# StanfordCoreNLP
https://stanfordnlp.github.io/CoreNLP/
java -mx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

java -mx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000

# OpenKE doc
http://139.129.163.161//static/notes/installation.html


# STEP BY STEP:
1. gen_train_data.py
2. convert_to_training_form.py
3. copy data folder to OpenKE/benchmarks/FAKE_NEWS
4. n-n.py
5. train_transe_fakenews.py
6. predict_news.py