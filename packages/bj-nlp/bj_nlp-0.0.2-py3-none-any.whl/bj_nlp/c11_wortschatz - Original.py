
# TODO: Punkt und Großgeschriebenes Adjektiv o.ä. weist auf Satzende hin.

#import pandas as pd

from bj_nlp            import blpClass
from spacy.tokens      import Doc, Token  #, Span
from spacy.matcher     import Matcher
#from bpyth             import load_pickle


# Funktionen tagZ, tagZZ
from bj_nlp.translate_tags  import *





class Wortschatz:
    '''
    Pipeline-Komponente
    wortschatz
    ==========
    Schlägt im Wiktionary nach und stellt einige Custom Attributes zur Verfügung:
    - Token._.tagZ und tagZZ
    - Token._.sent und sent_pre  
    - Token._.lemmaW_ und lemmaW
    Außerdem werden die Satzgrenzen neu geschrieben:
    - Token.is_sent_start


    Registrierung siehe blpClass.
    
    # Aktivierung:
    if not 'wortschatz' in nlp.pipe_names:
        nlp.add_pipe('wortschatz', 
                     before='parser',             # in jedem Fall vor dem Parser
                     config={'debug': True} 
                     ) 
        
    # direkter Zugriff auf die Pipeline-Komponente:
    wortschatz = blp.nlp.get_pipe('wortschatz') 
    
    .
    '''    
    
    # ===========================================================================================0 
    # init
    #    
    
    def __init__(self, blp: blpClass, debug: bool):
        
        
        self.blp   = blp                    # das blp-Objekt
        self.name  = 'wortschatz'           # name, für Error-Messages 
        self.debug = debug
        
        self.sent_end   = ['.',':','!','?','«']   # Zeichen, die Satzende bedeuten         
        self.sent_start = ['»']                   # Zeichen, die baldigen Satzanfang bedeuten 
                    
        if debug:
            if not Doc.has_extension('debug'):
                Doc.set_extension(   'debug', default='' )     

            if not Token.has_extension('debug'):
                Token.set_extension(   'debug', default='')   
            
            
        if not Token.has_extension('tagZ'):
            Token.set_extension(   'tagZ',  getter=self.get_tagZ)
            
        if not Token.has_extension('tagZZ'):
            Token.set_extension(   'tagZZ', getter=self.get_tagZZ)          
            
            
        if not Token.has_extension('sent'):
            Token.set_extension(   'sent', getter=self.get_sent)     
            
        if not Token.has_extension('sent_pre'):
            Token.set_extension(   'sent_pre', getter=self.get_sent_pre)               
            
                        
        if not Token.has_extension('lemmaW_'):
            Token.set_extension(   'lemmaW_',   default = '' )   
            
        if not Token.has_extension('lemmaW'):
            Token.set_extension(   'lemmaW',  getter=self.get_lemmaW )               
                         
        if not Token.has_extension('tagW_'):
            Token.set_extension(   'tagW_',   default = '' )   
            
        if not Token.has_extension('tagW'):
            Token.set_extension(   'tagW',  getter=self.get_tagW )     
            
        if not Token.has_extension('member'):
            Token.set_extension(   'member',  default = '' )             
            

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
        text = pkg_resources.read_binary( data, 'lookup2.pickle' )
        self.lookup2 = pickle.loads(text) 
        text = pkg_resources.read_binary( data, 'lookup3.pickle' )
        self.lookup3 = pickle.loads(text) 
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
        
        
        # === Matcher zur Wiedererkennung von Abkürzungen
        self.matcher2 = Matcher(blp.nlp.vocab)
        patterns  = []
        
        # Wort mit Punkt
        token1 = {"TEXT": {"REGEX": "\w+\."}}
        patterns +=  [[  token1 ]]      
        
        #add patterns
        self.matcher2.add('no_sentstart', patterns)          
        
        
        
        if self.blp.verbose:
            print( self.name + ' initialisiert')           
        

        
    
    
    # ===========================================================================================0
    # getter
    #      
    
    def get_tagZ(self,token):
        return self.blp.tagZ(token.tag)       
    
    
    
    def get_tagZZ(self,token):
        return self.blp.tagZZ(token.tag)       
    
    
    
    def get_sent(self,token):
        return token.sent.text.strip()    
    
    
    
    def get_sent_pre(self,token):

        i = token.sent.start-1
        if i > 0:
            return token.doc[i]._.sent 
        else:
            return ''    
    
    
    
    def get_lemmaW(self,token):
        try:
            return self.blp.str2hash(  token._.lemmaW_ )   
        except KeyError:
            if self.debug:
                token._.debug += '↯'
            return -7 

        
        
    def get_tagW(self,token):
        try:
            return self.blp.str2hash(  token._.tagW_ )   
        except KeyError:
            if self.debug:
                token._.debug += '↯'
            return -7         
    
    
    
    # ===========================================================================================0
    # Hauptroutine: 
    # - belegt lemmaW_ und tagW_
    # - joined Token (retokenize)
    # - schreibt is_sent_start
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
                doc[end]._.debug += ' ↰'            
            doc[end].is_sent_start = False

        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)          
        
     
        
        # --------------------------------------------------------
        # Turn 1: Retokenize laut Wörterbuch
        #          
        
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
                doc[i]._.lemmaW_       = eintrag[0]     
                doc[i]._.tagW_         = eintrag[1]   

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
        
        
        
        # --------------------------------------------------------
        # Turn 2: Abkürzungen wiederfinden
        #               
            
        matches = self.matcher2(doc)
        for match_id, start, end in matches:
            try:
                doc[end]._.debug += ' ⧉'
                doc[end].is_sent_start = False
            except:
                pass
            #

       
          
        
        
        
        # --------------------------------------------------------
        # Turn 3: Einzelwörter suchen und Sentencizer
        #    
        
        # DIESE ZEILEN ERZEUGEN EXTREME CPU_LAST
        #for i,token in enumerate(doc): 
            #doc.c[i].sent_start = -1
            #doc[i].is_sent_start   = False 
        
        for i,token in enumerate(doc):      
            
            # Custom Sentencizer: Zeichen für Satzende berücksichtigen
            if i <= len(doc)-2:

                if token.text in self.sent_start:
                    doc[i].is_sent_start = True   
                    try:
                        doc[i+1].is_sent_start   = False                        
                        doc[i-1].is_sent_start   = False  
                    except:
                        pass
                    
                elif token.text in self.sent_end:
                    doc[i+1].is_sent_start = True 
                    if self.debug:
                        doc[i+1]._.debug += ' ⒠' 
                    doc[i].is_sent_start   = False                    
                    
                else:
                    # DIESE ZEILE ERZEUGT EXTREME CPU_LAST
                    #doc[i+1].is_sent_start = False  # Tell the default sentencizer to ignore this token   
                    #doc[i+1].is_sent_start = None 
                    pass

      
            
            # lemmaW_ schon belegt
            if token._.lemmaW_:
                continue
            
            # in lookup1 suchen, d.h. die eindeutigen Fälle
            eintrag = self.lookup1.get( token.lower, None )  
            if eintrag:
                if self.debug:
                    token._.debug += ' ⑴'
                token._.lemmaW_    = eintrag[0]
                token._.tagW_      = eintrag[1]               
                continue
                
            # in lookup2 suchen, d.h. nach lex_lower und tagZ           
            suchetuple = (token.lower, token._.tagZ)
            eintrag = self.lookup2.get( suchetuple, None )  
            if eintrag:
                if self.debug:
                    token._.debug += ' ⑵'
                token._.lemmaW_    = eintrag[0]
                token._.tagW_      = eintrag[1]                     
                continue  
                    
            # in lookup3 suchen, d.h. nach lex_lower und tag           
            suchetuple = (token.lower, token.tag_)
            eintrag = self.lookup3.get( suchetuple, None )  
            if eintrag:
                if self.debug:
                    token._.debug += ' ⑶'
                token._.lemmaW_    = eintrag[0]
                token._.tagW_      = token.tag_                    
                continue     
                
            # in lookup4 suchen, d.h. bei großen Unterschieden zwischen Spacys lemma und Wiktionarys lemma
            eintrag = self.lookup4.get( token.lower, None )  
            if eintrag:
                if self.debug:
                    token._.debug += ' ⑷'
                token._.lemmaW_    = eintrag[0]
                token._.tagW_      = eintrag[1]               
                continue                
                    

                    
            # end for token
            
            
          
                
        return doc
                
                
 
    
    
    
    
    
    
    
    
    
    
    # ===========================================================================================0 
    # Tests
    #
    
    
    TESTTEXT_0 = '''Mrs. Summer kauft eine CD.
Fast tägl. kauft Mrs. Summer neue CDs!
Tägl. kauft Mrs. Summer neue CDs.
Hallo Hn.g. so ist das.'''
    
    TESTTEXT_1 = 'Lena z. läuft z. B. sie rennt z.B. sie d.h. sie d. h. rennt gbRteWq.'
    
    TESTTEXT_2 = '''Wie geht es dir z.z. ja. 
Sein Satz. 
Hallo gs. Bär es sind 5 mm.
U.a. mag ich Butter und Tee, am liebsten tägl. und heute auch.
Heute geschl. außer 500 ca. n.Chr. etc. bzw. Ende.
Auch u.a. deswegen, weil was denkt der Herr z.B. über dies oder u.a. diese Abkürzung, fragte Prof. Dr. Blöd.
Was denkst du z. B. oder u. a. diese Abkürzung?
D.h. wenn du willst.
D. h. wenn du willst.
Ja, d.h. nein, doch nicht.
Ja, d. h. nein, doch nicht.
Ja, tgl. bedeutet tägl., wissen Mr. Spock und Mrs. Spock.
Kennen Dr. Dumm und denn z.B. diese Abkürzung?
Z.B. diese hier.
Hat Prof. Selering die Tür geschlossen?
Tägl. Dusche erforderlich.
Bzw. eine Handwäsche.
U.a. mit Haare usw. waschen.
Ca. drei Stunden!
Nr. 5 lebt.
Auch Nr.3 erfreut sich bester Gesundheit.
Ja, Mrs. Miller sieht das genauso.'''
    
    zweierworte =  ['ab','am','an','aß','da','du','eh','er','es','he','im','in','ja','je','la','mg',]
    zweierworte += ['ne','ob','oh','on','so','tu','um','wo','zu','äh','au','bi','ei','ex','ey','go','hi',]
    zweierworte += ['hm','ho','hä','hü','is','me','mi','na','nu','nö','or','qm','re','si','sä',]
    zweierworte += ['to','uh','ui','up','uz','wa','we','öd','öl','ös','üb','μm']
    zweierworte = [z+'.' for z in zweierworte]
    TESTTEXT_3 = ' '.join(zweierworte) #+ ' ' + ''.join(zweierworte)       
        
    
    TESTTEXT_4 = '''Leni fragt: »Kannst du dir das alles merken?«
Sascha sagt: »Das Spiel gefällt mir gut.«
Der Vater befiehlt: »Mach jetzt endlich deine Hausaufgaben! Wie oft soll ich das noch sagen?«
»Kannst du dir das alles merken? Ich nicht«, sagt Leni.
»Das Spiel gefällt mir gut! Dir auch?«, fragt Sascha.
»Mach jetzt endlich deine Hausaufgaben!«, befiehlt der Vater.
»Kannst du«, fragt Leni, »dir das alles merken?«
»Das Spiel«, sagt Sascha, »gefällt mir gut.«
»Mach jetzt«, befiehlt der Vater, »endlich deine Hausaufgaben!«
»M'''    
    
    
    TESTTEXT_5 ='''U.a. mag ich Butter und Tee tägl. geschl. n.Chr. ca. etc. bzw. Ende.
U.a. was denkt der Herr z.B. über dies oder u.a. diese Abkürzung?
, fragte Prof. Dr. Blöd.
Was denkst du z. B. oder u. a. diese Abkürzung?
D.h. wenn du willst.
D. h. wenn du willst.
Ja, d.h. nein, doch nicht.
Ja, d. h. nein, doch nicht.
Ja, tgl. bedeutet tägl., wissen Mr. Spock und Mrs. Spock.
Kennen Dr. Dumm und denn z.B. diese Abkürzung?
Z.B. diese hier.
Hat Prof. Selering die Tür geschlossen?
Tägl. Dusche erforderlich.
Bzw. eine Handwäsche.
U.a. mit Haare usw. waschen.
Ca. drei Stunden!
Nr. 5 lebt.
Auch Nr.3 erfreut sich bester Gesundheit.
Ja, Mrs. Miller sieht das genauso.
Der Schlusssatz steht am Ende, inkl. Punkt.
'''            
    
    
    
    TESTTEXTE = { 0:TESTTEXT_0, 1:TESTTEXT_1, 2:TESTTEXT_2, 3:TESTTEXT_3, 4:TESTTEXT_4, 5:TESTTEXT_5, }
    

    
    
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
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            