
import re
import unicodedata
import nltk
import pandas as pd
import script_reglas
from nltk.stem.snowball import SnowballStemmer
from numpy import reshape, shape, concatenate, nan
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from xgboost import XGBClassifier
from sklearn.externals import joblib
from bots.models import HistoricalMessage
from django.cache import cache


def procesa_texto(texto):
    # Esta función manda todo a minúsculas, quita la segunda parte de las urls, quita puntuación y espacios finales
    # Posteriormente, quita emojis del texto, quita acentos y ñs,
    #calcula número de palabras y quita frases de apertura iniciales
    
    texto=texto.lower()
    
    
    part=texto.partition('http') 
    part=part[0]+part[1]+' '+ ' '.join(part[2].split(' ')[1:])
    texto=part
    
    part=texto.partition('bit.ly')
    part=part[0]+part[1]+' '+ ' '.join(part[2].split(' ')[1:])
    texto=part
    
    texto=re.sub('^[ \t]+|[ \t]+$', '', texto) 

    texto=re.sub('[^\w\s]','', texto)

    texto=re.sub('^[ \t]+|[ \t]+$', '', texto)

    texto=script_reglas.give_emoji_free_text(texto)

    texto=unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    wc=len(str(texto).split(" "))
    texto=re.sub('ola|buena noche|buenos dias|buenos dia|buen dia|buenas noches|buenas tardes|buenas tarde|buen dia|bien dia|buena tardes|buena tarde|saludos|hola','', texto)
    texto=re.sub('\n',' ', texto)
    texto=re.sub('^[ \t]+|[ \t]+$', '', texto)
    return texto , wc

stemmer = SnowballStemmer("spanish")


def tokenize_and_stem(text):
    #Esta función separa el mensaje por palabras y reduce las palabras a su raíz
    #
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def train_model(id_model, version):
    historical_messages = HistoricalMessage\
        .objects\
        .filter(id_bot=id_model)\
        .extra(select={
            'texto': 'message',
            'categ_opi': 'user_tag',
            'hora_ultimo': 'message_date'
        })\
        .values('message_date', 'message', 'user_tag')

    respuestas_etiquetas = pd.DataFrame(list(historical_messages))

    train_target = respuestas_etiquetas['categ_opi'].values
    train_texto = respuestas_etiquetas['texto'].values

    train_texto_stem = []
    wc = []

    for i in range(0, shape(train_texto)[0]):
        wc.append(procesa_texto(train_texto[i])[1])
        train_texto[i]=procesa_texto(train_texto[i])[0]
        train_texto_stem.append(tokenize_and_stem(train_texto[i]))
        train_texto_stem[i]=' '.join(train_texto_stem[i])
    wc = reshape(wc, (-1, 1))

    hora = respuestas_etiquetas.hora_ultimo.values
    hora = reshape(hora, (-1, 1))

    stop = nltk.corpus.stopwords.words("spanish")

    for i in range(0, shape(stop)[0]):
        stop[i] = unicodedata.normalize('NFD', stop[i]).encode('ascii', 'ignore').decode('utf-8')

    tfidf = TfidfVectorizer(
        sublinear_tf=True,
        min_df=0.006,
        norm='l2',
        encoding='utf-8',
        ngram_range=([1, 2]),
        stop_words=stop
    )
    tfidf = tfidf.fit(train_texto_stem)

    features_stem = tfidf.transform(train_texto_stem)
    labels = respuestas_etiquetas.categ_opi
    features_stem.shape

    features_stem = features_stem.toarray()
    pca = TruncatedSVD(n_components=33)
    pca = pca.fit(features_stem, features_stem)
    features_stem_pca = pca.transform(features_stem)

    x_train = concatenate((features_stem_pca, wc), axis=1)

    x_train = concatenate((x_train, hora), axis=1)

    clasificador = XGBClassifier(metrics='auc')
    clasificador = clasificador.fit(X=x_train,y=train_target)

    cache.set('mat_tfidf_{0}_{1}'.format(id_model, version), tfidf, None)
    cache.set('pca_{0}_{1}'.format(id_model, version), pca, None)
    cache.set('modelo_{0}_{1}'.format(id_model, version), clasificador, None)

    return version
