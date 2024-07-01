import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class CustomTokenizer():
    def __init__(self):
        pass


    

    def remove_urls(text, replacement_text=""):
    # Define a regex pattern to match URLs
      url_pattern = re.compile(r'https?://\S+|www\.\S+')
 
    # Use the sub() method to replace URLs with the specified replacement text
      text_without_urls = url_pattern.sub(replacement_text, text)
      return text_without_urls
    
    def convert_to_lower(text):
      return text.lower()
    def remove_numbers(text):
      number_pattern = r'\d+'
      without_number = re.sub(pattern=number_pattern, repl=" ", string=text)
      return without_number


    def remove_punctuation(text):
      return text.translate(str.maketrans('', '', string.punctuation))

    def remove_stopwords(text):
      removed = []
      stop_words = list(stopwords.word("english"))
      tokens = word_tokenize(text)
      for i in range(len(tokens)):
        if tokens[i] not in stop_words:
            removed.append(tokens[i])
      return " ".join(removed)
    def remove_extra_white_spaces(text):
      single_char_pattern = r'\s+[a-zA-Z]\s+'
      without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
      return without_sc

    def lemmatizing(text):
       lemmatizer = WordNetLemmatizer()
       tokens = word_tokenize(text)
    
       for i in range(len(tokens)):
          lemma_word = lemmatizer.lemmatize(tokens[i])
          tokens[i] = lemma_word
       return " ".join(tokens)