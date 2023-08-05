
# Importe
import gensim
import bpyth as bpy

# ==================================================================================================
#  Vereinfachung und Säuberung 
# 

def preprocess_strings( dirty, how=''):
    """ 
    Simplification and cleaning
    * dirty is Series or DataFrame. For a dataframe, all str columns are treated.
    * how determines which purge steps are executed.
      - fillna is always executed anyway
      - strip
      - minus2space replaces hyphens with spaces
      - lower
      - filter_letters deletes everything that is not a letter or number or space
      - umlaut2single replaces umlauts with single letters
      - umlaut2double replaces umlauts with letter combinations          
      - solowhite replaces multiple whitespaces with single space
      - but_anything takes the original if nothing else is left in the end
    * for how there are also presets, these are signalled by an abbreviation

  
    
    
    Vereinfachung und Säuberung
        * dirty ist Series oder DataFrame. Bei einem Dataframe werden alle str-Spalten behandelt.
        * how legt fest, welche Säuberungsschritte ausgeführt werden.
          - fillna wird sowieso immer ausgeführt
          - strip
          - minus2space ersetzt Bindestriche durch Spaces
          - lower
          - filter_letters löscht alles, was nicht Buchstabe oder Zahl oder Space ist
          - umlaut2single ersetzt Umlaute durch Einzelbuchstaben
          - umlaut2double ersetzt Umlaute durch Buchstabenkombinationen          
          - solowhite ersetzt multiple Whitespaces durch einzelnen Space
          - but_anything nimmt dann doch das Original, falls am Ende sonst gar nichts übrig bleibt
        * für how gibt es auch Presets, diese werden durch ein Kürzel signalisiert
    """
    
    # Presets
    if how == '':
        how = 'solowhite strip'
    elif how == 'STD_0': # lower_and_std
        how += ' strip minus2space lower filter_letters solowhite but_anything' 
    elif how == 'GROB_1': # str_grob
        how += ' umlaut2single esszett2ss'       
        
    # Series
    if   type(dirty) == pd.Series:
        
        result      = pd.DataFrame(dirty) 
        result.columns = ['A'] 
        result['A'] = result.A.fillna('') # Kopie, falls für but_anything benötigt
        result['B'] = result.A.copy()
        
        if 'strip'         in how:
            result.B = result.B.str.strip()           
        if 'minus2space'   in how:
            result.B = result.B.str.replace('-', ' ', regex=False)     
        if 'lower'         in how:
            result.B = result.B.str.lower() 
        if 'filter_letters'  in how:
            result.B = result.B.str.replace(r'[^ÄÖÜäüößA-Z a-z0-9]+', '', regex=True)   
        if 'umlaut2single' in how:
            table = str.maketrans({'ä':'a','ö':'o','ü':'u','Ä':'A','Ö':'O','Ü':'U' })
            result.B = result.B.str.translate(table)  
        if 'umlaut2double' in how:
            table = str.maketrans({'ä':'ae','ö':'oe','ü':'ue','Ä':'Ae','Ö':'Oe','Ü':'Ue' })
            result.B = result.B.str.translate(table)              
        if 'esszett2ss'    in how:
            result.B = result.B.str.replace('ß','ss', regex=False) 
        if 'solowhite'     in how:
            result.B = result.B.replace('\s+', ' ', regex=True)                
        if 'strip'         in how:
            result.B = result.B.str.strip()    
        if 'but_anything'      in how:  
            mask = (result.B == '') # nichts übrig geblieben?
            result.loc[mask,'B'] = result[mask].A                 

        return result.B        


    # DataFrame: auf alle Spalten anwenden
    elif type(dirty) == pd.DataFrame:
        
        result = dirty.copy()      
        cols = col_names(result, only='str')
        
        # ausführen
        for col in cols: 
            result[col] = preprocess_strings( result[col], how=how )
        return result
        
    else:
        assert 'wrong datatype'
            
    return result




      

def simplyfy_charset(mystring):
    ''' 
    Vereinfacht den Zeichensatz. 
    Es werden keine Zeichen gelöscht. Aber es können Zeichenkombinationen zu einem Zeichen zusammengefasst werden.
      * öffnende und schließende Anführungszeichen werden zu » und « vereinheitlicht
      * lange und kurze Striche werden zu - vereinheitlicht
      * Pünktchen Pünktchen wird zur Elipse
      * verschiedene Sternchen und Kuller werden zu *
      * diverse Kleinigkeiten
    '''

    ERSETZEN = [('–', '-'),        ('−', '-'),        ('‑', '-'), ('—', '-'), ('‒', '-'), ('‐', '-'), 
                ('›',  '»'),       ('‹',  '«'), 
                ('„',  '»'),       ('“',  '«'),        
                ('‚',  '»'),       ('‘',  '«'),         
                ('“',  '»'),       ('”',  '«'),   
                ('>>', '»'),       ('<<', '«'),   
                ('\u200b', ' '),           
                ('....','…'),      ('...','…'),       ('..','…'),    
                ('œ', 'oe'),       ('Ł','L'),         ('¿', '?'),
                ('❊','*'),         ('✖','*'),         ('•','*'),    ('о','*'),   ('∗','*'),               

               ] 

    for k, v in ERSETZEN:
        mystring = mystring.replace(k, v) 
    return mystring




def remove_bad_chars(mystring, bad_chars=None):
    '''
    Entfernt einige Junk-Zeichen
    '''

    if not bad_chars:
        bad_chars = ['©', '®', '�', '\xad']

    for i in bad_chars :
        mystring = mystring.replace(i, '')
 
    return mystring








def remove_accents(mystring):
    ''' 
    Entfernt Accents. Erhält deutsche Umlaute.
    '''
    
    MASKIEREN = [('ä', '<auml>'),   ('ö', '<ouml>'),   ('ü', '<uuml>'), 
                 ('Ä', '<Auml>'),   ('Ö', '<Öuml>'),   ('Ü', '<Uuml>'), 
                ]     
    
    DEMASKIEREN = [('<auml>','ä'),  ('<ouml>','ö'),    ('<uuml>','ü'), 
                   ('<Auml>','Ä'),  ('<Ouml>','Ö'),    ('<Uuml>','Ü'), 
                   ('`',''),        ('´',''),          ('’', ''),          ('ʹ', ''),  
                ]        
    
    # maskieren
    for k, v in MASKIEREN:
        mystring = mystring.replace(k, v)  
    
    # deaccent
    mystring = gensim.utils.deaccent(mystring)          
    
    # demaskieren    
    for k, v in DEMASKIEREN:
        mystring = mystring.replace(k, v)    
        
    return mystring        
    
    

    
def remove_dupstings(mystring):
    '''
    Entfernt Doppelungen wie z.B. in "Vereinigtes Königreich Vereinigtes Königreich"
    '''
    return ' '.join(bpy.remove_dups(mystring.split(' ')))    




def preprocess(text, preserve_paragraphs=False, config=0):
    '''
    Wendet eine Liste von Funktion nacheinander auf einen String an
    '''
    
    if preserve_paragraphs:
        return '\n'.join(  [preprocess(absatz, preserve_paragraphs=False, config=config) for absatz in text.split('\n') if len(absatz) > 1]   )    

    CONFIG_0 = [simplyfy_charset,
                remove_bad_chars,
                remove_accents, 
               ]
  
    if config == 0:
        config = CONFIG_0   
    elif config == 1:
        config = CONFIG_1       
    
    result = ' '.join(  gensim.parsing.preprocessing.preprocess_string(  str(text), config)  )    
    return result



  
    

                
                

      