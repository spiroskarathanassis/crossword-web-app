import spacy
import re

class Search_Similarity:
  def __init__(self):
    self.nlp = spacy.load("en_core_web_lg")

  def similar_percentage(self, theme: str, sentence: str) -> set:
    """Compare theme sentece/word with current sentence to find similarity via nlp"""
    doc1 = self.nlp(sentence)
    doc2 = self.nlp(theme)
    
    # Similarity of tokens and spans
    similar_tokens = set()

    try:
      for token in doc1:
        if (
          len(token.text) > 2
          and token.has_vector
          and token.pos_ in ['VERB', 'NOUN', 'PROPN']
          and self.nlp(token.lemma_).similarity(doc2) > 0.2
        ):
          text = token.text.lower()

          if re.match('^[a-z]*$', text):
            similar_tokens.add(text)
            
    except:
      print('Token error detected')

    return similar_tokens