
import pandas as pd

from bj_nlp            import blpClass
from spacy.tokens      import Doc, Token, Span






class WRede:
    '''
    Pipeline-Komponente
    wrede
    ========
    Liefert folgende Custom Attibutes:
    - doc._.wrede          (eine Liste von Spans)
    - token._.is_wrede     (Integer, Anzahl der zusammenhängenden Token die wörtliche Rede sind, 
                            0 wenn außerhalb wörtlicher Rede)

    Registrierung siehe blpClass.
    
    # Aktivierung:
    if not 'wrede' in nlp.pipe_names:
        nlp.add_pipe('wrede',
                     before='parser',            # vor wortschatz
                     config={'debug': False} 
                    )   
                
    # direkter Zugriff auf die Pipeline-Komponente:
    wrede = blp.nlp.get_pipe('wrede') 
    
    .
    '''    
    
    # ===========================================================================================0 
    # init
    #    
    
    def __init__(self, blp: blpClass, debug: bool):        
        
        self.blp   = blp                # das blp-Objekt
        self.name  = 'wrede'            # name, für Error-Messages     
        self.debug = debug        
        
        # Create the matcher    
        rules = []
        rules += [{  'match_id': 'WREDE_L',   'text': '»',  }]
        rules += [{  'match_id': 'WREDE_R',   'text': '«',  }]  
        rules += [{  'match_id': 'WREDE',     'text': '"',  }]             
        self.matcher = blp.phrasematcher(rules, verbose=False )
        
        # Register custom extension on the Doc
        if not Doc.has_extension('wrede'):
            Doc.set_extension('wrede', default=[])
            
        if not Token.has_extension('is_wrede'):
            Token.set_extension('is_wrede', default=0)            
            
        if debug:            
            if not Doc.has_extension('debug'):
                Doc.set_extension('debug', default=[])            
                        
        if self.blp.verbose:
            print( self.name + ' initialisiert')            

        
    
   
    
    # ===========================================================================================0
    # Hauptroutine
    #    
    
    def __call__(self, doc:Doc) -> Doc:
        
        # Finden
        matches = self.matcher(doc)
        
        if len(matches) == 0:
            return doc
        
        # in DataFrame wandeln
        df = self.blp.df_matches(matches, as_string=True)
        
        # Passende Anführungszeichen finden
        df['Anfang']          = df.start.shift(1).astype('Int32')
        df['Anfang_match_id'] = df.match_id.shift(1)      
        
        # Jeden zweiten Datensatz löschen

        
        # Unpassende löschen
        maskA = (df.Anfang_match_id == 'WREDE_R')  &  (df.match_id == 'WREDE_L')
        maskB = (df.Anfang_match_id == 'WREDE')    &  (df.match_id != 'WREDE')    
        maskC = (df.match_id == 'WREDE')           &  (df.Anfang_match_id != 'WREDE')     
        maskD = (df.Anfang_match_id == 'WREDE_L')  &  (df.match_id == 'WREDE_L')
        maskE = (df.Anfang_match_id == 'WREDE_R')  &  (df.match_id == 'WREDE_R')        
        maskF =  df.Anfang_match_id.isnull()
        mask = maskA | maskB  |  maskC  |  maskD  |  maskE  |  maskF
        df = df[~mask]        
        
        #df = df.iloc[1::2, :]
        
        if self.debug:
            doc._.debug = df
        
        # is_wrede
        for index, row in df.iterrows():
            for i in range(row.Anfang+1, row.end-1):
                doc[i]._.is_wrede = row.end-row.Anfang-2       
        
      
        # Funktion Span heraussuchen
        def collect_wrede(zeile):
            zeile['wrede'] = doc[zeile.Anfang+1 : zeile.end-1]
            return zeile    
        
        # apply Span heraussuchen
        df['wrede'] = ''
        df = df.apply(collect_wrede, axis=1)        
           
        # Ergebnisse speichern    
                
        doc._.wrede = list(df.wrede)
        
        return doc
    
    
    
    # ===========================================================================================0 
    # testtext
    #
    
    TESTTEXT_0 = 'Kap›utt ›Hallo!‹ ›Wie geht es dir?‹ "Mir?" ››Mir geht es gut.‹ Kap"utt'    
    
    TESTTEXT_1 = '''Leni fragt: »Kannst du dir das alles merken?«
Sascha sagt: »Das Spiel gefällt mir gut.«
Der Vater befiehlt: »Mach jetzt endlich deine Hausaufgaben!«
»Kannst du dir das alles merken?«, fragt Leni.
»Das Spiel gefällt mir gut«, sagt Sascha.
»Mach jetzt endlich deine Hausaufgaben!«, befiehlt der Vater.
»Kannst du«, fragt Leni, »dir das alles merken?«
»Das Spiel«, sagt Sascha, »gefällt mir gut.«
»Mach jetzt«, befiehlt der Vater, »endlich deine Hausaufgaben!«
»M'''
    

    
  
    
    TESTTEXTE = {0:TESTTEXT_0, 1:TESTTEXT_1}
    

    
    
    # ===========================================================================================0 
    # tests durchführen
    #
    def tests(self, only=None, verbose=True):  
        
        # Leeres Dokument
        doc = self.blp.nlp('')
        assert len( list(doc.sents)  ) == 0        
        
        # Anzahl der Sätze in TESTTEXT_0 prüfen            
        if only is None or only == 0:
            
            text_0 = self.TESTTEXTE[0]
            text_1 = self.blp.preprocess(text_0)
            doc = self.blp.nlp(text_1)
            assert len(list(doc.sents)) == 5
            assert len(doc._.wrede) == 4
            if verbose:
                print('wrede Test 0 OK')           
        
        
        
        # Anzahl der Sätze in TESTTEXT_1 prüfen
        if only is None or only == 1:    

            text_0 = self.TESTTEXTE[1]
            text_1 = self.blp.preprocess(text_0)
            doc = self.blp.nlp(text_1)
            assert len(list(doc.sents)) == 10
            assert len(doc._.wrede) == 12
            if verbose:
                print('wrede Test 1 OK')    
             
            
            
             
    
    
    
    
        
        
