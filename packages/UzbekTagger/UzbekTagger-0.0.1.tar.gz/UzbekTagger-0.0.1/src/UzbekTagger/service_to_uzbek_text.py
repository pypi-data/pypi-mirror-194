import nltk.tokenize
from nltk.tokenize import RegexpTokenizer

def text_normalizer(text):
    #text=text.lower()
    text = text.replace("'", "‘")
    text = text.replace("`", "‘")
    text = text.replace("‘", "‘")
    text = text.replace("‘", "‘")
    text = text.replace("‘", "‘")
    text = text.replace("’", "‘")
    solid_sign=["sun‘iy","sur‘at","jur‘at","sa‘y"]
    for x in solid_sign:
        if(x in text):
            new_x=x.replace("‘","ʼ")
            text=text.replace(x,new_x)
    return text

def word_normalizer(word):
    word=word.lower()
    word=word.strip()
    word = word.replace("'", "‘")
    word = word.replace("`", "‘")
    word = word.replace("‘", "‘")
    word = word.replace("‘", "‘")
    word = word.replace("‘", "‘")
    word = word.replace("’", "‘")
    solid_sign=["sun‘iy","sur‘at","jur‘at","sa‘y"]
    for x in solid_sign:
        if(x in word):
            new_x=x.replace("‘","ʼ")

    return word

def word_tokenizer(text):
    text=text_normalizer(text)
    tokenize = RegexpTokenizer("[\w`'‘‘‘’‘-]+")
    tokens = tokenize.tokenize(text)
    return tokens

#import nltk
#nltk.download('punkt')

def sent_tokenizer(text):
    sent=nltk.tokenize.sent_tokenize(text)
    return sent