# coding: utf-8
from emoji import UNICODE_EMOJI
from unicodedata import normalize
import re

texto='aborto'


def is_emoji(s):
    count = 0
    for emoji in range(1, len(UNICODE_EMOJI)):
        count += s.count(list(UNICODE_EMOJI.keys())[emoji])
    return count


def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text


def procesa_reglas(texto):
    result=[]
    out=[]
    texto_orig=texto
    texto=texto.lower()
    #print('pasando a minusculas')
    #print(texto)
    texto=re.sub('^[ \t]+|[ \t]+$', '', texto) 
    #print('quitar trailing leading')
    #print(texto)
    if (bool(re.search('aborto', texto))) & (len(out)==0):
       # print('es hasta luego')
        out='aborto'
    if (bool(re.search('hasta luego', texto))) & (len(out)==0):
       # print('es hasta luego')
        out='hasta luego'
    if (bool(re.search('https://scontent', texto)))  & (len(out)==0):
      #  print('es like')
        out='like-fb'
    wc=len(str(texto).split(" "))
    cc_1=cc=len(str(texto))
    if bool(re.search('t.co', texto)) & (wc==1) :
       # print('es twitter')
        out='twitter-image'
    #print('nchar:'+ str(cc))
    #print('wc:'+ str(wc))
    
    if (len(re.findall("\?", texto))==cc)  & (len(out)==0):
       # print('puros ?')
        out='pregunta'
    
    texto=re.sub('[^\w\s]','', texto) #Quitar puntuacion
    #print('quitar punct '+texto)

    texto=re.sub('^[ \t]+|[ \t]+$', '', texto) #Otra vez quitar leading y trailing
    #print('quitar leading y trailing '+texto)
    
    #Contar palabras y caracteres otra vez
    wc=len(str(texto).split(" "))
    cc=len(str(texto))
    
    #print('nchar: '+ str(cc))
    #print('wc: '+ str(wc))
    
    emojis=is_emoji(texto) #Conteo de emojis
    #print('conteo de emojis: '+ str(emojis))
    
    if (emojis==cc) & (cc_1>0)  & (len(out)==0):
        #print('puros emojis')
        out='emoji'
    
    texto=give_emoji_free_text(texto)#Elimina emojis
    #print('quitar emojis:'+ texto)
    
    if (wc==1) & (bool(re.search('https|http', texto)))  & (len(out)==0):
        #print('es spam')
        out='spam'
    
    texto=normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8') # quitar acentos
    #print('quitar acentos '+texto)
    
    
    if (cc==2) & (bool(re.search('si|sii|ssi', texto))) & (len(out)==0):
        #print('es: sí')
        out='si'
    if (cc==2) & (bool(re.search('no|noo|nno', texto))) & (len(out)==0):
        #print('es: no')
        out='no'
    if (wc==1) & (bool(re.search('gracias|graicas|gracia|graciad|graciaa', texto))) & (len(out)==0):
       # print('es: gracias')
        out='gracias'
    if (wc==1) & (bool(re.search('ok|ook|okk', texto))) & (len(out)==0):
        #print('es: ok')
        out='ok'
    if (wc<=2) & (bool(re.search('hola|holaa|hhola|hoola|holi', texto))) & (len(out)==0):
        #print('es: hola')
        out='hola'
    if (wc<=4) & (bool(re.search('hola|buenad tardes|ola|buena tarde|buen dia|buena noche|buenas tardea|buenas tardes|buenas noches|buenos dias', texto))) & (len(out)==0):
            #print('es: hola')
            out='hola'
    if (wc<=5) & (bool(re.search('gracias|graicas|gracia|graciad|graciaa', texto))) & (len(out)==0):
        #print('es: gracias')
        out='gracias'
    if (bool(re.search('horario', texto))) & (bool(re.search('atencion', texto))) & (len(out)==0):
        #print('es: informacion (horario atencion)')
        out='informacion'
    if (bool(re.search('telefono', texto)))& (bool(re.search('numero', texto))) & (wc<10) & (len(out)==0):
        #print('es: informacion (telefono)')
        out='informacion'
    if (bool(re.search('added', texto))) & (len(out)==0):
       # print('es: like (added)')
        out='like-fb'
    if len(out)==0:
        out='modelo'
    else:
        out=out
        #print('ninguna 4')
    
    out={'result':out, 'texto':texto_orig,'texto_proc':texto, 'wc':wc, 'cc':cc}
    
    return(out)

# procesa_reglas(texto)

# get_ipython().system('jupyter nbconvert --to script script_reglas.ipynb')
