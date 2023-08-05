
from bj_nlp            import blpClass
from spacy.tokens      import Doc, Token  #, Span
from spacy.matcher     import Matcher
#from bpyth             import load_pickle


# Funktionen tagZ, tagZZ
from bj_nlp.translate_tags  import *





class Merger:
    '''
    Pipeline-Komponente
    merger
    ==========
    Sucht nach Abkürzungen und fasst diese zu einem Token zusammen.
    Die Suche geschieht über RexEx sowie durch Nachschlagen im Wiktionary-Wortschatz.
    Diese Komponente muss als allererstes in der Pipeline liegen, damit die gemergten Token verarbeitet werden.
    
    Registrierung siehe blpClass.
    
    # Aktivierung:
    if not 'merger' in nlp.pipe_names:
        nlp.add_pipe('merger', 
                     first=True,          
                     config={'debug': True} 
                     ) 
        
    # direkter Zugriff auf die Pipeline-Komponente:
    merger = blp.nlp.get_pipe('merger') 
    
    .
    '''    
    
    # ===========================================================================================0 
    # init
    #    
    
    def __init__(self, blp: blpClass, debug: bool):
        
        
        self.blp   = blp                    # das blp-Objekt
        self.name  = 'merger'           # name, für Error-Messages 
        self.debug = debug
                    
        if debug:  

            if not Token.has_extension('debug'):
                Token.set_extension(   'debug', default='')               

        # load lookups
        try:
            import importlib.resources as pkg_resources
        except ImportError:
            # Try backported to PY<37 `importlib_resources`.
            import importlib_resources as pkg_resources
        from . import data     

        import pickle
        text = pkg_resources.read_binary( data, 'lookup1.pickle' )
        self.lookup1 = pickle.loads(text)      
        text = pkg_resources.read_binary( data, 'lookup4.pickle' )
        self.lookup4 = pickle.loads(text)      
            
            
        # === Matcher zur Erkennung von Abkürzungen
        self.matcher = Matcher(blp.nlp.vocab)
        patterns  = []
        
        # Ein oder zwei Zeichen, dann Punkt, dann wieder ein oder zwei Zeichen 
        token1 = {"TEXT": {"REGEX": "^.{1,2}\..{1,2}$"}}
        token2 = {"ORTH": "."}
        patterns +=  [[  token1, token2 ]] 
        
        # Ein oder zwei Konsonanten
        wird_nicht_mit_punkt_abgekürzt = ['au','ei','hm','qm','ui','mg','km','cm','mm','dm','ft','nm',
                                          'pt','m²','m³','kg','lb','db','BH','CD','CC','CT','DB','DC','DM','FH','KW','VW','XY']
        token1 = {"TEXT": {"REGEX": "^[b-df-hj-np-tv-zßB-DF-HJ-NP-TV-Z]{1,2}$"},  
                  "ORTH": {"NOT_IN": wird_nicht_mit_punkt_abgekürzt}
                 }           
        token2 = {"ORTH": "."}
        patterns +=  [[  token1, token2 ]]          
        
        #add patterns
        self.matcher.add('abbrev', patterns)  
               
        # fertig
        if self.blp.verbose:
            print( self.name + ' initialisiert')           
        


    
    
    # ===========================================================================================0
    # Hauptroutine 
    #    
    def __call__(self, doc:Doc) -> Doc:
    
        
        if len(doc) <= 1:
            return doc  
        

        
        # --------------------------------------------------------
        # Turn 0: Abkürzungen per Matcher suchen
        #               
            
        matches = self.matcher(doc)
        spans = []  # Collect the matched spans here
        for match_id, start, end in matches:
            spans.append(doc[start:end])
            if self.debug:
                try:
                    doc[start]._.debug += ' ↰'
                except:
                    pass
            try:
                doc[end].is_sent_start = False
            except:
                pass                
        
        # Token zusammenfassen
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)          
        
        
        
        # --------------------------------------------------------
        # Turn 1: Retokenize laut Wörterbuch
        # versucht zwei Token zu einem zusammenzufassen
        # wenn zwischen den Token ein Space ist, bleibt dieses erhalten!
        
        with doc.retokenize() as retokenizer:
            
            verschmolzen    = ''  
            verschmolzen_id = -1
            
            # Doppelwörter suchen 
            for i,token in enumerate(doc):
                    
                if i >= len(doc)-1:
                    continue
                    
                if doc[i].tag_ == '_SP':
                    continue
                    
                if doc[i+1].tag_ == '_SP':
                    continue                                    
                    
                span      = doc[i:i+2]  
                span_hash = self.blp.str2hash( span.text.lower() )
                eintrag   = self.lookup1.get( span_hash, None )      
                
                # Zweiter versuch
                if not eintrag: 
                    eintrag   = self.lookup4.get( span_hash, None ) 
                    
                # Immer noch nichts gefunden >> weiter                      
                if not eintrag: 
                    continue                    
                    
                # gefunden >> zu einem Token verschmelzen                                       
                # für Errors merken    
                verschmolzen_id_pre = verschmolzen_id
                verschmolzen_id     = i
                verschmolzen_pre    = verschmolzen    
                verschmolzen        = span                    

                if self.debug:
                    doc[i]._.debug     += ' ⨝'      
                    
                # Abkürzung?
                if span.text[-1] == '.':
                    try:                      
                        doc[i+2].is_sent_start = False
                    except:
                        pass                      
                    
                      
                # verschmelzen
                try: 
                    retokenizer.merge(span) 
                except ValueError:         
                    error = {'error'    : 'Überlappende Verschmelzungen',
                            'component' : self.name, 
                             'nam0'     : 'verschmolzen_pre',
                             'val0'     : verschmolzen_pre,  
                             'nam1'     : 'verschmolzen',
                             'val1'     : verschmolzen,      
                             #'nam2'     : 'doc_id',
                             #'val2'     : self.spacy_batch.doc_id,          
                             'nam3'     : 'pos',
                             'val3'     : i                                
                            }
                    if self.debug:
                        doc[i]._.debug += str(error)     
                        
                    
        
        # retokenizer end
 
                
        return doc
                
                
 
    
    
    
    
    
    
    
    
    
    
    # ===========================================================================================0 
    # Tests
    #
    
    
    TESTTEXT_0 = '''Tägl. kauft Mrs. Summer neue CDs.
Hallo Hn.g. so ist das.'''
        
    zweierworte =  ['ab','am','an','aß','da','du','eh','er','es','he','im','in','ja','je','la','mg',]
    zweierworte += ['ne','ob','oh','on','so','tu','um','wo','zu','äh','au','bi','ei','ex','ey','go','hi',]
    zweierworte += ['hm','ho','hä','hü','is','me','mi','na','nu','nö','or','qm','re','si','sä',]
    zweierworte += ['to','uh','ui','up','uz','wa','we','öd','öl','ös','üb','μm']
    zweierworte = [z+'.' for z in zweierworte]
    TESTTEXT_1 = ' '.join(zweierworte) #+ ' ' + ''.join(zweierworte)       
    
    # soll nicht verbunden werden
    TESTTEXT_2 = '''Schleswig Holstein San Franzisko'''    


    
    TESTTEXTE = { 0:TESTTEXT_0, 1:TESTTEXT_1, 2:TESTTEXT_2 }
    

    
    
    # ===========================================================================================0 
    # tests durchführen
    #
    def tests(self, only=None, verbose=True):           
        
        # Test 0: doc erstellen
        text = self.TESTTEXTE[0]
        sent_anz = text.count('\n')+1
        text = self.blp.preprocess(text)
        doc = self.blp.nlp(text)
        
        # sent
        assert len(list(doc.sents)) == sent_anz
        
        # sent und sent_pre
        assert doc[2]._.sent   == 'Mrs. Summer kauft eine CD.'
        assert doc[7]._.sent   == 'Fast tägl. kauft Mrs. Summer neue CDs!'          
        assert doc[17]._.sent  == 'Tägl. kauft Mrs. Summer neue CDs.'   
        assert doc[23]._.sent  == 'Hallo Hn.g. so ist das.'
        
        # tagZ und tagZZ
        assert doc[2]._.tagZ == 'VER'
        assert doc[2]._.tagZZ == 'V'    
        
        # lookup1    
        test = self.lookup1[  7608359307979301264  ]    
        assert test[0] == 'heimtrauen'        
        
        if verbose:
            print('wortschatz Tests 0 OK')              
        
        
        # Test1: doc erstellen
        text = self.TESTTEXTE[1]
        sent_anz = text.count('\n')+1        
        text = self.blp.preprocess(text)
        doc = self.blp.nlp(text)
        
        # sent
        assert len(list(doc.sents)) == sent_anz        
        
        # lemmaW
        assert doc[0]._.lemmaW_ == 'Lena'
        assert doc[1]._.lemmaW_ == ''  
        assert doc[2]._.lemmaW_ == 'laufen'          
        
        if verbose:
            print('wortschatz Tests 1 OK')          
            
            
        # Test2: doc erstellen
        text = self.TESTTEXTE[2]
        sent_anz = text.count('\n')+1        
        text = self.blp.preprocess(text)
        doc = self.blp.nlp(text)
        
        # sent
        assert len(list(doc.sents)) == sent_anz  
        
        if verbose:
            print('wortschatz Tests 2 OK')   
            
            
        # Test3: doc erstellen
        text = self.TESTTEXTE[3]
        sent_anz = text.count('.')       
        text = self.blp.preprocess(text)
        doc = self.blp.nlp(text)
        
        # sent
        assert len(list(doc.sents)) == sent_anz          
          
        if verbose:
            print('wortschatz Tests 3 OK')    
            
            
        # Test4: Mehr oder weniger leeres Dokument
        texte = self.sent_start + self.sent_end + ['']
        for text in texte:
            #print(text)
            doc = self.blp.nlp(text)
            assert len(doc) == len(text)     
            
            doc = self.blp.nlp(text + '.')
            assert len(doc) <= len(text) + 1     
            
            doc = self.blp.nlp('»' + text)
            assert len(doc) == len(text) + 1            
            
        
        if verbose:
            print('wortschatz Tests 4 OK')           
            
        return True
      
            
            
#          # Wortschatz prüfen    
#          prüfe_tagZ( 'X_konj',        ['z.B.','z. B.','Z.B.', 'D.h.','D. h.','d.h.', 'd. h.']   , doc )
#          prüfe_tagZ( 'ADV',           ['U.a.','u.a.','u. a.']   , doc )            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            