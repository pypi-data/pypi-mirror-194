    
#import pandas     as pd 
import pandasklar as pak 


# key         0                     1            2          3         4  
# TAG         tag_help              tagZ         is_mutable to_lemma  tagZZ
bj_tags = {

  'AFIX':   ['Präfix',              'FIX',       False,     'W',       'Z'    ],    # Fixe disqualifizieren sich meistens, wenn man N, V oder A sucht 
  'MFIX':   ['Midfix',              'FIX',       False,     'W',       'Z'    ],         
  'ZFIX':   ['Postfix',             'FIX',       False,     'W',       'Z'    ],     

  'NN'  :   ['Nomen',               'NOM',       True,      'N',       'N'    ],
  'NE'  :   ['Eigenname',           'NAM',       True,      'W',       'N'    ],  
  'NNE' :   ['Eigenname',           'NAM',       True,      'W',       'N'    ],       

  'ADV':    ['Adverb',              'ADV',       False,     'W',       'A'    ],    # links, hier, heute, vielleicht, deshalb 
  'PROAV':  ['Adverb',              'ADV',       False,     'W',       'A'    ],     
  'PTKA':   ['Adverb',              'ADV',       False,     'W',       'A'    ],    # zu am     

  'ADJA':   ['Adjektiv',            'ADJ',       True,      'A',       'A'    ],    # gut klein ganz rosa
  'ADJD':   ['Adjektiv',            'ADJ',       True,      'A',       'A'    ], 
  'VVPP':   ['Ptz2',                'ADJ',       True,      'V',       'A'    ],    # ausprobiert   (ist wie ein Adjektiv)     

  'VVIZU':  ['Verb',                'VER',       True,      'V',       'V'    ],  

  'VVFIN':  ['Verb',                'VER',       True,      'V',       'V'    ],    # fragen sagen sehen   
  'VVIMP':  ['Verb',                'VER',       True,      'V',       'V'    ],       
  'VVINF':  ['Verb',                'VER',       True,      'V',       'V'    ],  

  'VMFIN':  ['Modalverb',           'VER_mod',   True,      'V',       'V'    ],    # müssen sollen können
  'VMINF':  ['Modalverb',           'VER_mod',   True,      'V',       'V'    ],  
  'VMPP':   ['Modalverb',           'VER_mod',   True,      'V',       'V'    ],       
  'VAFIN':  ['Hilfsverb',           'VER_hilf',  True,      'V',       'V'    ],    # sein haben 
  'VAIMP':  ['Hilfsverb',           'VER_hilf',  True,      'V',       'V'    ],   
  'VAINF':  ['Hilfsverb',           'VER_hilf',  True,      'V',       'V'    ],  
  'VAPP':   ['Hilfsverb',           'VER_hilf',  True,      'V',       'V'    ],  


  'PPER':   ['Personalpronomen',    'PRO',       True,      'W',       'P'    ],    # ich mir er 
  'PRF':    ['Personalpronomen',    'PRO',       True,      'W',       'P'    ],    
  'PPOSAT': ['Possessivpronomen',   'PRO',       True,      'W',       'P'    ],    # mein dein sein         
  'PPOSS':  ['Possessivpronomen',   'PRO',       True,      'W',       'P'    ],    
  'PRELAT': ['Relativpronomen',     'PRO',       True,      'W',       'P'    ],    # mich mir                              # Kann ev. auch lemmatisiert werden
  'PRELS':  ['Reflexivpronomen',    'PRO',       True,      'W',       'P'    ],     
  'PDAT':   ['Demonstrativpronomen','PRO',       True,      'W',       'P'    ],    # dieser jener der   
  'PDS':    ['Demonstrativpronomen','PRO',       True,      'W',       'P'    ],    
  'PIAT':   ['Indefinitpronomen',   'PRO',       True,      'W',       'P'    ],    # manche alle keiner  
  'PIS':    ['Indefinitpronomen',   'PRO',       True,      'W',       'P'    ],       
  'PWAT':   ['Fragepronomen',       'PRO',       True,      'W',       'P'    ],    # wer was wem wessen welcher   
  'PWAV':   ['Fragepronomen',       'PRO',       True,      'W',       'P'    ],    
  'PWS':    ['Fragepronomen',       'PRO',       True,      'W',       'P'    ],     
  'PRO':    ['Pronomen',            'PRO',       True,      'W',       'P'    ],     


  'APPO':   ['Präposition',         'X_prep',    False,     'W',       'X'    ],    # im auf
  'APPR':   ['Präposition',         'X_prep',    False,     'W',       'X'    ],     
  'APPRART':['Präposition',         'X_prep',    False,     'W',       'X'    ], 
  'APZR':   ['Präposition',         'X_prep',    False,     'W',       'X'    ],     
  'KOKOM':  ['Konjunktion',         'X_konj',    False,     'W',       'X'    ],    # und aber als
  'KON':    ['Konjunktion',         'X_konj',    False,     'W',       'X'    ],       
  'KOUI':   ['Konjunktion',         'X_konj',    False,     'W',       'X'    ], 
  'KOUS':   ['Konjunktion',         'X_konj',    False,     'W',       'X'    ],    
  'ART' :   ['Artikel',             'X_art',     True,      'W',       'X'    ],    # der die das ein eine     
  'PTKANT': ['Antwortpartikel',     'X_antw',    False,     'W',       'X'    ],    # ja nein bitte danke
  'PTKNEG': ['Negationspartikel',   'X_neg',     False,     'W',       'X'    ],    # nicht      
  'PTKVZ':  ['Verbpartikel',        'X_div',     False,     'W',       'X'    ],    # inne, dar, zurecht    
  'CARD':   ['Zahl',                'X_zahl',    False,     'W',       'X'    ],    # eins zwei 3
  'ITJ':    ['Interjektion',        'X_itj',     False,     'W',       'X'    ],    # Hallo ach  
  'KOMBI':  ['Wortkombination',     'X_kombi',   False,     'W',       'X'    ],    # Dampf ablassen, Seine Heiligkeit
  'DIV':    ['Diverses',            'X_div',     False,     'W',       'X'    ],    
    

  '$('  :   ['Satzzeichen',         'SYM',       False,     'W',       'Y'    ],    
  '$,'  :   ['Satzzeichen',         'SYM',       False,     'W',       'Y'    ],  
  '$.'  :   ['Satzzeichen',         'SYM',       False,     'W',       'Y'    ],   
  '_SP':    ['Satzzeichen',         'SYM',       False,     'W',       'Y'    ],          

  'PTKZU':  ['Müll',                'z',         False,     'W',       'Z'    ],    # zu   
  'XY':     ['Müll',                'z',         False,     'W',       'Z'    ],     
  'TRUNC':  ['Müll',                'z',         False,     'W',       'Z'    ],     
  'FM':     ['Fremdsprachliches',   'z',         False,     'W',       'Z'    ],    

  'TODO':   ['(todo!)',             'X_todo',    False,     'W',       'X'    ],       

}

    
# erstellt ein DataFrame namens translate_tagZ
# zur Konvertierung tag >> tagZ >> tagZZ (verschiedene Abstraktionsstufen der Tags)
# sowie Wortarten wie sie im Wiktionary verwendet werden zu tags 
#
def generate_translate_tags():    
        
    # in DataFrame wandeln   
    result = pak.dataframe(bj_tags, verbose=False).transpose().reset_index()
    result.columns = ['tag','wortart_lang','tagZ','is_mutable','to_lemma','tagZZ']
    result = pak.move_cols(result, 'tagZZ','tagZ')
    return result




# interne Funktion für den Zugriff auf bj_tags
def bj_key( key, position ):    
    if key in bj_tags:
        return bj_tags[key][position]
    else:
        if position == 0:
            return spacy.explain(key) 
        elif position == 1:
            return '¿¿¿'     # tagZ
        elif position == 2:
            return False     # is_mutable  
        elif position == 3:
            return 'W'       # to_lemma  
        elif position == 4:
            return '¿'       # tagZZ           
        

# Langform von tag
def tag_help(key):
    return bj_key(key,0)        
        
    

def tagZ( tag ):
    '''Liefert tagZ, ein zusammenfassendes tag.
    Dies ist die Funktion bj_nlp.tagZ, die Strings annimmt.
    Es gibt auch die Methode blp.tagZ des blp-Objektes, die Hashwerte annimmt.
    '''
    return bj_key(tag,1)         

        

def tagZZ( tag ):
    '''Liefert tagZZ, ein stark zusammenfassendes tag.
    Dies ist die Funktion bj_nlp.tagZZ, die Strings annimmt.
    Es gibt auch die Methode blp.tagZZ des blp-Objektes, die Hashwerte annimmt.
    '''    
    return bj_key(tag,4)   



# Wird das Wort konjugiert, dekliniert o.ä.?
# Kann TEXT!=LEMMA ?   
def is_mutable(key):
    return bj_key(key,2) 


# Hilfsfunktion für Lemma2
# siehe Lemma2
#
def to_lemma(key):
    return bj_key(key,3) 




# Liefert eine Liste von  Wortarten
def wortarten(key='alle'):
    alle_tags = list(bj_tags.keys())
    alle_tags.sort()
    if key == 'alle':
        return alle_tags 
    else:
        result = [tag for tag in alle_tags if wortart(tag).startswith(key)  ]
        return result 
    




##################################################################################################
    
bj_tagZ = {
    'NOM'     :  'NN',
    'NAM'     :  'NE',
    'ADV'     :  'ADV',    
    'ADJ'     :  'ADJA',       
    'VER'     :  'VVFIN',       
    'VER_mod' :  'VMFIN',   
    'VER_hilf':  'VAFIN',     
    'PRO'     :  'PDAT',
    'X_prep'  :  'APPRART',    
    'X_art'   :  'ART',     
    'X_antw'  :  'PTKANT',  
    'X_neg'   :  'PTKNEG',  
    'X_zahl'  :  'CARD',  
    'X_itj'   :  'ITJ',    
    '$('      :  'SYM',     
    'z'       :  '',       
}

# Liefert einen passenden tag, wenn nur tagZ gegeben ist
def tag(key):
    if key in bj_tagZ:
        return bj_tagZ[key]
    return ''




# ===========================================================================================0
# Test-Utils
#    
    
    
# Generator, liefert alle token mit einem bestimmten text     
def find_token(text, doc):
    for token in doc:
        if token.text == text:
            yield token     




def check_tagZ(soll_sein, check_token, doc):
    '''
    # Beispiel    
    bj_nlp.check_tagZ( 'X_konj',        ['z.B.','z. B.','Z.B.', 'D.h.','D. h.','d.h.', 'd. h.']   , doc )
    bj_nlp.check_tagZ( 'ADV',           ['U.a.','u.a.','u. a.']   , doc )    
    '''
    for check in check_token:
        tokenliste = list(find_token(check, doc))
        assert len(tokenliste) > 0
        for token in tokenliste:
            tagz = tagZ(token.tag_)
            if tagz != soll_sein:
                print(token.text + ':', 'ist:' + tagz, 'soll:'+soll_sein)
            assert tagz == soll_sein       