from spacy.language    import Language
    
from bj_nlp.translate_tags    import *
from bj_nlp._PandaziseMixin   import *    # Schnittstellen zu Pandas
from bj_nlp._UtilsMixin       import *    # Wichtige Klassenmethoden


try:
    from dframcy import DframCy
except:
    pass

# blpClass ist die Klasse des blp-Objektes, das einmal instanziiert wird.
# PandaziseMixin und UtilsMixin werden hineingemixt.
#
class blpClass( PandaziseMixin, UtilsMixin ):
    
# ===========================================================================================0
# __init__
#       
    
    def __init__( self, lang='en', model=0, verbose=True ):  
        '''
        Initialisierung z.B.:
        if not 'blp' in globals() or True:
            blp = bj_nlp.blpClass(lang='de')        
            
        Statt nlp verwendet man dann blp.nlp
        
        
        '''
        
        # merken
        self.lang    = lang
        self.model   = model
        self.verbose = verbose
        
        # geladenes model
        self.model_name = 'blank'        
        
        # translate_tagZ (DataFrame zum Übersetzen tag > tagZ > tagZZ)
        self.translate_tagZ = generate_translate_tags()        
        
        
        # nlp-Instanz / load model        
        if lang == 'en':
            if model == 0:
                self.model_name = 'en_core_web_sm' 
            elif model == 1:           
                self.model_name = 'en_core_web_trf'  
            elif model == 2:           
                self.model_name = 'en_core_web_md'  
            elif model == 3:           
                self.model_name = 'en_core_web_lg'                  
                
        elif lang == 'de':     
            if model == 0:
                self.model_name = 'de_core_news_sm' 
            elif model == 1:           
                self.model_name = 'de_core_news_trf'  
            elif model == 2:           
                self.model_name = 'de_core_news_md'  
            elif model == 3:           
                self.model_name = 'de_core_news_lg'       

                
        if self.model_name != 'blank': 
            self.nlp = spacy.load(self.model_name)
        else:
            self.nlp = spacy.blank(lang)
            
        
        if self.verbose:
            print(self.model_name, 'loaded')       
            
        # vocab korrigieren
        lex = self.nlp.vocab['»']
        lex.is_left_punct = True
        lex.is_right_punct = False

        lex = self.nlp.vocab['«']
        lex.is_left_punct = False
        lex.is_right_punct = True                
            

        # DframCy-Instanz
        try:
            self.dframcy = DframCy(self.nlp)        
        except:
            pass
        
        
        # DE-Pipeline-Komponenten registrieren
        if lang=='de':
            
            # === merger ===             
            if not Language.has_factory('merger'):
                if self.verbose:
                    print('registriere merger')
                @Language.factory('merger',
                                  assigns=[], 
                                  retokenizes=True,
                                  default_config={'debug': True}
                                 )
                def create_wortschatz_component(nlp: Language, name: str, debug: bool):
                    return bj_nlp.Merger(nlp.blp, debug)    
            else:
                if self.verbose:
                    print('merger bereits registriert')              
                                
                        
                        
            # === wrede ====
            if not Language.has_factory('wrede'):
                if self.verbose:
                    print('registriere wrede')
                @Language.factory('wrede', 
                                  assigns=['token._.is_wrede','doc._.wrede'],
                                  default_config={'debug': True}
                                 )
                def create_wrede_component(nlp: Language, name: str, debug: bool):
                    return bj_nlp.WRede(nlp.blp, debug)    
            else:
                if self.verbose:
                    print('wrede bereits registriert')   
                    
                    

                    
            # === wortschatz ===             
            if not Language.has_factory('wortschatz'):
                if self.verbose:
                    print('registriere wortschatz')
                @Language.factory('wortschatz',
                                  assigns=['token._.tagZ',   'token._.tagZZ',
                                           'token._.sent',   'token._.sent_pre', 'token._.is_sent_start',
                                           'token._.lemmaW', 'token._.lemmaW_',], 
                                  retokenizes=True,
                                  default_config={'debug': True}
                                 )
                def create_wortschatz_component(nlp: Language, name: str, debug: bool):
                    return bj_nlp.Wortschatz(nlp.blp, debug)    
            else:
                if self.verbose:
                    print('wortschatz bereits registriert')                      

  
                    
                   
            
            
        # TESTTEXTE
        #self.TESTTEXTE = bj_nlp.TESTTEXTE
        
        if lang=='de':        
            self.TESTTEXTE = {       0  :  bj_nlp.TESTTEXT_0, 
                                     1  :  bj_nlp.TESTTEXT_DE1,
                          'Preprocess'  :  bj_nlp.TESTTEXT_0,               
                           'Kokosnuss'  :  bj_nlp.TESTTEXT_DE1,

                        }   
        else:        
            self.TESTTEXTE = {       0  :  bj_nlp.TESTTEXT_0, 
                                     1  :  bj_nlp.TESTTEXT_EN1,                              
                          'Preprocess'  :  bj_nlp.TESTTEXT_0,               

                        }                
    
    
