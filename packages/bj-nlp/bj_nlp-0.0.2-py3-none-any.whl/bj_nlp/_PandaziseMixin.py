
#####################################################################################################
# Schnittstellen zu Pandas
#####################################################################################################     
   
import spacy
from spacy.tokens         import Doc, Token, Span    
    
try:
    from dframcy import DframCy
except:
    pass
    
import pandas     as pd
import pandasklar as pak     
    
#from bj_nlp.translate_tags  import *



class PandaziseMixin:

    
    def df_token(self, doc, columns = ['BASIC']):
        '''
        Liefert einen DataFrame mit den gewünschten Feldern.
        Input ist eine Sequenz von Token, z.B. ein doc oder ein subtree.
        An Pseudofeldern stehen ['BASIC','HELP','LING'] zur Verfügung, diese werden jeweils durch ein Defaultset von Feldern ersetzt.
        Wenn möglich, wird statt eines Hashwertes ein String ausgegeben.
        Will man explizit den Hashwert statt des Strings, so verwendet man den Funktionsnamen mit angehängtem '_hash'. 
        '''
        
        cols = []
        if 'BASIC' in columns:
            cols += ['text', 'lemma', 'tag', 'pos']   
                
        if 'ENT' in columns:
            cols += ['ent_type', 'ent_iob_int',]                 
                
        if 'DEP' in columns:
            cols += ['text', 'pos', 'tag', 'dep', 'dep_help', 'head', 'head_pos', 'ancestors', 'children',] 
            
        if 'HELP' in columns:
            cols += ['tag_help', 'pos_help', 'dep_help']       
            
        if 'CHAR' in columns:
            cols += ['text', 'pos', 'is_punct', 'is_left_punct', 'is_right_punct', 'is_sent_start'] 
            
        cols += columns            
        cols = [  c for c in cols if c not in ['BASIC','ENT','DEP','HELP','CHAR']  ]    
        cols = list(dict.fromkeys(cols))   # remove dups keep order    
        #print('cols=',cols)
        
        # Daten zusammenstellen
        result_raw = []
        for token in doc:
            zeile = list( self.token_xxx(doc, token, symbol )  for symbol in cols )
            result_raw.append(zeile)

        # DataFrame liefern
        result = pd.DataFrame(result_raw, columns=cols) 
        
        # Reihenfolge
        if 'pos_help' in result.columns:
            result = pak.move_cols(result, 'pos_help', 'pos')            
        if 'tag_help' in result.columns:
            result = pak.move_cols(result, 'tag_help', 'tag')            
        if 'dep_help' in result.columns:
            result = pak.move_cols(result, 'dep_help', 'dep')            
            
        return result    
    
    
    
       
    

    # Hilfsroutine
    def token_xxx( self, doc, token, func_name ):
        
        # Liefert zu einem Token eine Liste von ancestor-Lemmas, ggf. gefiltert
        def ancestor_lemmas(token, pos=''):
            if pos == '':
                result = [token.lemma_ for token in token.ancestors]  
            else:
                result = [token.lemma_ for token in token.ancestors if token.pos_ == pos]  
            return result    
        
        # Liefert zu einem Token eine Liste von ancestors, ggf. gefiltert
        def ancestors(token, pos=''):
            if pos == '':
                result = [token.text for token in token.ancestors]  
            else:
                result = [token.text for token in token.ancestors if token.pos_ == pos]  
            return result            
        
        # Liefert zu einem Token eine Liste von children-Lemmas, ggf. gefiltert
        def children_lemmas(token, pos=''):
            if pos == '':
                result = [token.lemma_ for token in token.children]  
            else:
                result = [token.lemma_ for token in token.children if token.pos_ == pos]  
            return result        
        
        # Liefert zu einem Token eine Liste von children-Lemmas, ggf. gefiltert
        def children(token, pos=''):
            if pos == '':
                result = [token.text for token in token.children]  
            else:
                result = [token.text for token in token.children if token.pos_ == pos]  
            return result          
        
        def ent_iob_int(token):
            t = {'B':1, 'I':2, 'O':0}
            return t[token.ent_iob_]
        
        # text
        if func_name == 'text':
            return token.text  
        
        # ent 
        elif func_name == 'ent_iob_int':              # 0=outside, 1=start, 2=inside          
            return ent_iob_int(token)           
        
        # Tree
        elif func_name == 'head_pos':                # The part-of-speech tag of the token head
            return token.head.pos_               
        elif func_name == 'children':                # The immediate syntactic dependents of the token
            return children(token) 
        elif func_name == 'children_lemmas':               
            return children_lemmas(token)         
        elif func_name == 'ancestors':                
            return ancestors(token)
        elif func_name == 'ancestor_lemmas':                
            return ancestor_lemmas(token)        
        
        elif func_name == 'verben':
            return ancestors(token,'VERB')    
        elif func_name == 'adjektive':
            return ancestors(token,'ADJA')    
        
        
       # elif func_name == 'sent':                  # sent ist in bj_tools realisiert
       #     return token.sent.text.strip()    
       # elif func_name == 'sent_pre':
       #     satz_span = token.sent.text.strip()   
       #     return doc[satz_span.start-1].sent           
        
        # HELP
        elif func_name == 'dep_help':
            return spacy.explain(token.dep_) 
        elif func_name == 'pos_help':
            return spacy.explain(token.pos_)    
        elif func_name == 'tag_help':
            return tag_help(token.tag_)   
        
        # morph
        elif func_name == 'morph_dict':
            return token.morph.to_dict()        
        elif func_name.startswith('morph_list_'):   # z.B. morph_Person liefert Person des morph-Dictionary als Liste
            return token.morph.get(func_name[11:])
        elif func_name.startswith('morph_'):        # z.B. morph_Person liefert Person des morph-Dictionary als Skalar. 
            m = token.morph.get(func_name[6:])      # Falls es mehrere Werte sind, dann nur den ersten Wert. 
            if len(m) > 0:
                return m[0]
            else:
                return None
    
        # standard attributes: Versucht stets str zurückzugeben, wenn möglich
        else:
            
            # Eingebautes Attribut, str
            if hasattr(token, func_name+'_'):
                try:
                    return getattr(token, func_name+'_')
                except:
                    return 'Error: ' + func_name+'_'                 
            
            # Eingebautes Attribut, hash            
            if func_name[-5:] == '_hash' and hasattr(token, func_name[:-5] ):     
                try:
                    return getattr(token, func_name[:-5])                     
                except:
                    return 'Error: ' + func_name[:-5]                 
            
            # Eingebautes Attribut
            if hasattr(token, func_name):
                try:
                    return getattr(token, func_name).text            
                except:
                    try:
                        return getattr(token, func_name)  
                    except:
                        return 'Error: ' + func_name
                    
            
            # Selbst definiertes Attribut, str
            if hasattr(token._, func_name+'_'):
                try:
                    return getattr(token._, func_name+'_')
                except:
                    return 'Error: ' + '_.'+func_name+'_'                     
            
            # Selbst definiertes Attribut, hash            
            if func_name[-5:] == '_hash' and hasattr(token._, func_name[:-5] ):     
                try:
                    return getattr(token._, func_name[:-5])                     
                except:
                    return 'Error: ' + '_.'+func_name[:-5]                  
            
            # Selbst definiertes Attribut            
            if hasattr(token._, func_name):
                try:
                    return getattr(token._, func_name)                     
                except:
                    return 'Error: ' + '_.'+func_name      
                

            
            
            return 'ERRORi: ' + func_name
                
           

        
        
        




        
        
        
    # Liefert einen DataFrame mit den gewünschten Feldern
    #
    def df_span(self, spans, columns=['BASIC']):
        '''
        Liefert einen DataFrame mit den gewünschten Feldern.
        Input ist eine Sequenz von Token, z.B. doc.ents
        An Pseudofeldern steht nur ['BASIC'] zur Verfügung, diese werden jeweils durch ein Defaultset von Feldern ersetzt.
        '''        
        cols = []
        if 'BASIC' in columns:
            cols += ['start', 'end', 'text', 'label', ]   
            if Token.has_extension('meta'): 
                cols += ['meta']
            if Token.has_extension('info'):
                cols += ['info']
            
        cols += columns            
        cols = [  c for c in cols if c not in ['BASIC','LING','HELP']  ]    
        cols = list(dict.fromkeys(cols))   # remove dups keep order    
        #print('cols=',cols)        

        # Daten zusammenstellen
        result_raw = []
        for span in spans:
            zeile = list( self.span_xxx(spans, span, symbol )  for symbol in cols )
            result_raw.append(zeile)

        # DataFrame liefern
        result = pd.DataFrame(result_raw, columns=cols) 
        return result         
        
        

    # Hilfsroutine
    def span_xxx( self, spans, span, func_name ):
        
        # text
        if func_name == 'text':
            return span.text   
        
        # Tree
        elif func_name == 'root_dep':         # Dependency relation connecting the root to its head
            return span.root.dep_        
        elif func_name == 'root_head':        # The text of the root token’s head
            return span.root.head.text           
        
        # extensions
        elif func_name == 'meta':
            print('TODO: in General-Zweig unten einbauen')
            return spans[span.start]._.meta   
        elif func_name == 'info':
            print('TODO: in General-Zweig unten einbauen')
            return spans[span.start]._.info    
            
        # standard attributes: Versucht stets str zurückzugeben, wenn möglich
        else:
            if hasattr(span, func_name+'_'):
                return getattr(span, func_name+'_')
            if hasattr(span, func_name):
                try:
                    return getattr(span, func_name).text            
                except:
                    try:
                        return getattr(span, func_name)  
                    except:
                        return 'Error: ' + func_name
            if hasattr(span._, func_name):
                try:
                    return getattr(span._, func_name) 
                except:
                    pass
            
            return 'ERROR: ' + func_name                    
                    
          

        
        
        
    # Liefert einen DataFrame mit den gewünschten Feldern
    #
    def df_lex(self, doc, columns=['BASIC']):
        '''
        Liefert einen DataFrame mit den gewünschten Feldern.
        Input ist eine Sequenz von Token, z.B. doc.ents
        An Pseudofeldern steht nur ['BASIC'] zur Verfügung, diese werden jeweils durch ein Defaultset von Feldern ersetzt.
        '''        
        cols = []
        if 'BASIC' in columns:
            cols += ['text', 'is_alpha', 'is_digit','is_punct', 'is_title', 'shape']     
        if 'CHAR' in columns:
            cols += ['text', 'is_punct', 'is_left_punct', 'is_right_punct','is_bracket','is_quote']
            
        cols += columns            
        cols = [  c for c in cols if c not in ['BASIC','CHAR','HELP']  ]    
        cols = list(dict.fromkeys(cols))   # remove dups keep order    
        #print('cols=',cols)        

        # Daten zusammenstellen
        result_raw = []
        for token in doc:
            lex = doc.vocab[token.text]
            zeile = list( self.lex_xxx(lex, symbol )  for symbol in cols )
            result_raw.append(zeile)

        # DataFrame liefern
        result = pd.DataFrame(result_raw, columns=cols) 
        return result         
        
        

    # Hilfsroutine
    def lex_xxx( self, lex, func_name ):
        
        # text
        if func_name == 'text':
            return lex.text   
        
        # standard attributes: Versucht stets str zurückzugeben, wenn möglich
        else:
            if hasattr(lex, func_name+'_'):
                return getattr(lex, func_name+'_')
            if hasattr(lex, func_name):
                try:
                    return getattr(lex, func_name).text            
                except:
                    try:
                        return getattr(lex, func_name)  
                    except:
                        return 'Error: ' + func_name
            if hasattr(lex._, func_name):
                try:
                    return getattr(lex._, func_name) 
                except:
                    pass
            
            return 'ERROR: ' + func_name                

        
           
    def analyze_pipes(self, pretty=False):
        '''
        Wie spacys analyze_pipes, liefert aber DataFrame
        '''
        analyse = self.nlp.analyze_pipes(pretty=pretty)
        result = pak.dataframe(  analyse['summary']   ).transpose()        
        result = pak.reset_index( result,  keep_as='component' )     
        if pretty:
            print()
        for key, value in analyse['problems'].items():
            if len(value) > 0:
                print('Problem in {0}: {1}'.format(key, value))   
        
        # Info printen
        print(  'model_name:', self.model_name       )
        print(   'vocab_len:', len(self.nlp.vocab)   )
        
        
        
        if len(self.nlp.disabled) > 0:
            print('pipe component disabled:',self.nlp.disabled)
                
        return result
    
    
    
    def df_matches( self, matches, as_string=True ):
        '''
        Converts the result of a Matcher to DataFrame
        '''
        result = pd.DataFrame(matches)
        result.columns = ['match_id','start','end']
        if as_string:
            result['match_id'] = result.match_id.apply( self.hash2str )
        return result        
        
        

    
    
    
