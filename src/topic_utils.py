from topic_modeling import pipeline_lsa 
from topic_modeling import pipeline_lda
import numpy as np
import pandas as pd
import ast 
import re

df = pd.read_csv('data/processed_v2.csv')
texts = df["text"].apply(lambda x: ast.literal_eval(x)["clean"])

def clean_processed_text(text_item):
    if isinstance(text_item, list):
        text = " ".join(text_item)
    else:
        text = str(text_item)
    
    text = text.lower()
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

texts_cleaned = texts.apply(clean_processed_text)
texts_cleaned = texts_cleaned[texts_cleaned.str.len() > 0]

# === LSA top words, top documents ===

X_reduced_lsa = pipeline_lsa.fit_transform(texts_cleaned)
tfidf = pipeline_lsa.named_steps['tfidf']
svd = pipeline_lsa.named_steps['svd']

terms = tfidf.get_feature_names_out()

koef = [5, 8]

for k in koef:
  print("\nLSA k =", k)
  for i, comp in enumerate(svd.components_[:k]): 
      terms_in_comp = [terms[idx] for idx in np.argsort(comp)[-10:]]
      print(f"Тема {i}: {', '.join(terms_in_comp)}")

top_n = 5

for topic_idx in range(6):
    print(f"\n=== Тема {topic_idx} ===")
    topic_values = X_reduced_lsa[:, topic_idx]
    
    top_doc_indices = np.argsort(topic_values)[-top_n:][::-1]
    
    for i, doc_idx in enumerate(top_doc_indices):
        print(f"\nДокумент {i+1}, id={doc_idx} (score={topic_values[doc_idx]:.4f}):")
        print(ast.literal_eval(df.iloc[doc_idx]['text'])['clean'][:300])


# === LDA top words, top documents ===

X_reduced_lda = pipeline_lda.fit_transform(texts_cleaned)
cntvect = pipeline_lda.named_steps['cntvect']
lda = pipeline_lda.named_steps['lda']

terms = cntvect.get_feature_names_out()

koef = [5, 8]

for k in koef:
  print("\nLDA k =", k)
  for i, comp in enumerate(lda.components_[:k]): 
      terms_in_comp = [terms[idx] for idx in np.argsort(comp)[-10:]]
      print(f"Тема {i}: {', '.join(terms_in_comp)}")

import numpy as np

top_n = 5

for topic_idx in range(6):
    print(f"\n=== Тема {topic_idx} ===")
    topic_values = X_reduced_lda[:, topic_idx]
    
    top_doc_indices = np.argsort(topic_values)[-top_n:][::-1]
    
    for i, doc_idx in enumerate(top_doc_indices):
        print(f"\nДокумент {i+1}, id={doc_idx} (score={topic_values[doc_idx]:.4f}):")
        print(ast.literal_eval(df.iloc[doc_idx]['text'])['clean'][:300])