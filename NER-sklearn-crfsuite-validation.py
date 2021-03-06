# -*- coding: utf-8 -*-
"""NER using sklearn-crfsuite(validation).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oeEYh9OcQ0R9e5klpEihGWFcd3SZQ-Ol
"""
# Instalar e importar bibliotecas
!pip install sklearn_crfsuite
!pip3 install dnspython
import dns
from itertools import chain
import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, RandomizedSearchCV, train_test_split

import sklearn_crfsuite
from sklearn_crfsuite import scorers, metrics

from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import TweetTokenizer

from joblib import dump, load

import numpy as np

from pymongo import MongoClient #access MongoDB
import pandas as pd


# Acessar MongoDB
#A variável `collection` armazenará os *tweets* coletados por meio do *streaming*.
#A variável `collection_crf` armazenará os *tweets* classificados. É uma nova coleção e será alimentada com novos documentos a partir da execução dos parágrafos. 


uri = "mongodb+srv://url-para-o-mongo"
db = MongoClient(uri, connectTimeoutMS=300000).get_database('Twitter')
collection = db.get_collection('your-database')
collection_crf = db.get_collection('your-collection')

#Selecionar *tweets* e Remover *retweets*.

df_allmedicines_truncated_true = \
pd.DataFrame(list(collection.find({'truncated':True, 'text': {'$regex': '^(?!RT)'}} ,{ "_id": 1, 'id_str': 1, "truncated":1, "extended_tweet.full_text": 1, 'created_at':1 })))
df_allmedicines_truncated_true['text'] = df_allmedicines_truncated_true['extended_tweet'].apply(lambda cell: cell['full_text'])
df_allmedicines_truncated_true.drop('extended_tweet', 1, inplace=True)

df_allmedicines_truncated_false = \
pd.DataFrame(list(collection.find({'truncated':False, 'text': {'$regex': '^(?!RT)'}},{ "_id": 1, 'id_str': 1, "truncated":1, "text": 2, 'created_at': 1 }).limit(2000)))

#Concatenar dataframes: truncados e não truncados
frames = [df_allmedicines_truncated_false, df_allmedicines_truncated_true]

df_allmedicines_full = pd.concat(frames)

df_allmedicines_full['text_remove_newline'] = df_allmedicines_full['text'].str.replace('\\n',' ')

df_allmedicines_full.head()

# Tokenização
#Função `identify_tokens` criará um vetor de palavras.
#`strip_handles=False`: Não remove usuários (exemplo: @fluoxetina)
#`reduce_len=True`: Remove sequencias de caracteres repetidos (exemplo: de waaaaayyyy para waaayyy)


def identify_tokens(row):
    review = row['text']
    tknzr = TweetTokenizer(strip_handles=False, reduce_len=True) 
    tokens = tknzr.tokenize(review)        
    token_words = [w for w in tokens]
    return token_words

#A função `identify_tokens` será aplicada a uma nova coluna **words** no dataframe.

df_allmedicines_full['words'] = df_allmedicines_full.apply(identify_tokens, axis=1)

df_allmedicines_full.head()

# Construção das características
#As características de cada postagem serão enviadas ao modelo para a classificação.
#A função `word2features` construirá as características.

def word2features(sent, i):    
    word = sent[i]    
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),        
    }
    if i > 0:
        word1 = sent[i-1][0]        
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),            
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]                
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),            
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

X_validation = [sent2features(s) for s in df_allmedicines_full['words']]


#O exemplo abaixo mostra as características de uma única postagem.

X_validation[2]

# Carregar o modelo
#Acessar o Google drive e carregar o modelo.
crf = load('/content/drive/MyDrive/MyFolder/' + 'arq_name.joblib')


# Classificação das postagens
y_validation = crf.predict(X_validation)

#A variável `y_validation` armazenará as classificações.
#ATENÇÃO: a variável armazenará a classificação de cada palavra por postagem. Será necessário realizar a correlação com a mensagem original.
#O exemplo abaixo mostra a classificação de apenas 10 postagens.

y_validation[0:10]

"""O parágrafo abaixo foi criado apenas para mostrar a correlação entre uma postagem e a sua classificação.

A postagem escolhida foi a que possui o índice 77. Observem a correlação entre as duas bases: df_allmedicines_full e y_validation 
"""

for i in range(len(list(df_allmedicines_full['words'])[77])):
  print(list(df_allmedicines_full['words'])[77][i], y_validation[77][i])

"""A função `concatentity` receberá 2 parâmetros:

`position`: A posição da entidade reconhecida na postagem. Exemplo `[11, 14]`

`words`: Um vetor com as palavras da postagem['@sertralina', 'me', 'ajuda', 'a', 'te', 'dormir', ',', 'não', 'consigo', 'fazer', 'o', 'nada'):']

Retornará as entidades reconhecidas na postagem `['dormir', 'fazer', 'nada']`

A utilização do `##` foi necessária para separar mais de 1 entidade por postagem.
"""

def concatentity(position, words):
  print(position, words)
  phrase = ''    
  for i in range(len(position)):
     phrase = phrase + words[position[i]] + ' '
     if(i < len(position)-1):
       if(position[i+1] - position[i] > 1):
         phrase = phrase.strip() + '##'
  print(phrase.strip().split('##'))
  return phrase.strip().split('##')

def insertDocument(Doc, Collection):  
  Collection.insert_one(Doc)

"""Realizará a inserção no banco de dados MongoDB.

A instrução `collection.find({ '_id': list(df_allmedicines_full['_id'])[i] })` buscará o JSON da postagem na coleção original. Motivo: este JSON será enriquecido com as informações das entidades identificadas e depois inserido em uma nova coleção no MongoDB, definida nos parágrafos iniciais.

"""

drug = []
reaction = []

for i in range(len(y_validation)):
  
  arr = np.array(y_validation[i])
  x = np.where((arr == 'B-Drug') | (arr == 'I-Drug') | (arr == 'B-ADR') | (arr == 'I-ADR'))

  if (len(list(x[0])) > 0):        
    array_reaction = np.where((arr == 'B-ADR') | (arr == 'I-ADR'))
    if (len(list(array_reaction[0])) > 0):    
      reaction = concatentity(list(array_reaction[0]), list(df_allmedicines_full['words'])[i])
    
    array_drug = np.where((arr == 'B-Drug') | (arr == 'I-Drug'))
    if (len(list(array_drug[0])) > 0):    
      drug = concatentity(list(array_drug[0]), list(df_allmedicines_full['words'])[i])      
    
    cc = collection.find({ '_id': list(df_allmedicines_full['_id'])[i] })
    
    jsonPost = {}
    jsonPost = list(cc)[0]
    if (len(drug) > 0): jsonPost['Drug'] = drug
    if (len(reaction) > 0): jsonPost['ADR'] = reaction    
    
    drug = []
    reaction = []
    insertDocument(jsonPost, collection_crf)

