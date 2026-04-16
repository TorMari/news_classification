import pandas as pd
import ast
from gensim.models import Word2Vec, FastText
from nltk.tokenize import word_tokenize
import nltk
from gensim.models import Word2Vec, FastText

df = pd.read_csv('data/processed_v2.csv')
texts = df["text"].apply(lambda x: ast.literal_eval(x)["clean"])

nltk.download('punkt')
nltk.download('punkt_tab')

def preparation(df):
    df = df.dropna(subset=['text'])
    df = df[df['text'].str.strip() != ""]
    df['word_count'] = df['text'].apply(lambda x: len(str(x).split()))
    df = df[df['word_count'] >= 3]
    tokenized_data = [
        [word.lower() for word in word_tokenize(text) if word.isalpha()]
        for text in df['text']
    ]

    num_docs = len(tokenized_data)
    total_tokens = sum(len(doc) for doc in tokenized_data)
    
    return tokenized_data, num_docs, total_tokens

tokenized_data, num_docs, total_tokens = preparation(df)

params = {
  "vector_size": 100,
  "window": 5,
  "min_count": 3,
  "sg": 1, 
  "workers": 4
}

w2v_model = Word2Vec(sentences=tokenized_data, **params)

ft_model = FastText(sentences=tokenized_data, **params)