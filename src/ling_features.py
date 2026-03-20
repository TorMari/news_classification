import stanza
import pandas as pd

stanza.download("uk")

nlp = stanza.Pipeline(
   lang="uk",
   processors="tokenize,pos,lemma",
   tokenize_pretokenized=True,
   use_gpu=False
)

def process_from_sentences(text_dict):
   sentences = text_dict["sentences"]

   tokenized_input = [s.split() for s in sentences]

   doc = nlp(tokenized_input)

   lemmas = []
   upos_tags = []

   for sentence in doc.sentences:
      for word in sentence.words:
         lemmas.append(word.lemma)
         upos_tags.append(word.upos)

   return " ".join(lemmas), " ".join(upos_tags)


