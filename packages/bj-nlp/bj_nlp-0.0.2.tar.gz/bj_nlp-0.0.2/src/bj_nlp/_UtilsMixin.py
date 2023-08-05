
#####################################################################################################
# Schnittstellen zu den Klassenmethoden
#####################################################################################################  

import bj_nlp
import bpyth as bpy

from spacy.matcher import PhraseMatcher

class UtilsMixin:
    
#####################################################################################################
# Schnittstellen zu den Klassenmethoden
#####################################################################################################  
    
    
    def testtext(self, variant='Kokosnuss'):
        return bj_nlp.testtext(variant=variant)
    
    
    def preprocess(self, text, config=0):
        return bj_nlp.preprocess(text, config=config)
    
    
    

#####################################################################################################
# Eigene Utils
#####################################################################################################  
    


    
    def phrasematcher( self, terms=[], match_id='no_id', on_match=None, attr='ORTH', validate=False, verbose=False):
        '''
        
        Liefert einen einfachen PhraseMatcher mit den angegebenen Rules.
        
        terms kann eine Liste von Strings oder eine Liste von Dictionaries sein.
        
        === list of dictionaries ===
        terms ist eine list of dictionaries mit den keys 'match_id' und 'text', z.B.:
        [{  'match_id': 'WREDE_L',   'text': '»'  },
         {  'match_id': 'WREDE_R',   'text': '«'  }, ]
         
        Oder, wenn eine Callback-Funktion angegeben werden soll:
        [{  'match_id': 'WREDE_L',   'text': '»',   'on_match': wrede_func  },
         {  'match_id': 'WREDE_R',   'text': '«',   'on_match': wrede_func   }, ] 
        Eine Callback-Funktion pro match_id ist möglich. 
        Alternativ kann die Callback-Funktion auch global über den Parameter on_match angegeben werden.
        
        === list of strings ===
        terms kann auch einfach eine Liste von Strings sein. 
        Dann können match_id und on_match
        '''
        
        #print(bpy.rtype(terms))

        matcher = PhraseMatcher(self.nlp.vocab, attr=attr, validate=validate)
        rtype_terms = bpy.rtype(terms)
        
        # terms ist Liste von Dictionaries 
        if rtype_terms[:2] == ('list', 'dict' ):
            
            # docs erstellen
            for term in terms:
                term['doc'] = self.nlp.make_doc( term['text']  )       

            # für jede id eine Rule
            matchids = { term['match_id'] for term in terms }
            for m in matchids:

                # alle patterns dieser id
                patterns  = [ term['doc']      for term in terms if term['match_id'] == m]
                callbacks = { term['on_match'] for term in terms if term['match_id'] == m and 'on_match' in term}
                if on_match:
                    callbacks.add(on_match)
                if len(callbacks) == 0:
                    matcher.add( m, patterns )   
                    if verbose:
                        print(m, attr, patterns, 'no callback')                     
                elif len(callbacks) == 1:
                    callback = list(callbacks)[0]
                    matcher.add( m, patterns, on_match=callback ) 
                    if verbose:
                        print(m, attr, patterns, callback )                         
                else:
                    raise ValueError('Only 1 callback per id')
     
                    
        # terms ist Liste von Strings 
        elif rtype_terms == ('list', 'str'):   
            patterns = [  self.nlp.make_doc(term) for term in terms  ]
            matcher.add(match_id, patterns)     
            if verbose:
                print(match_id, attr, patterns)                
            

        else:
            raise ValueError('terms must be list of str or list of dicts')
            
        return matcher
    
    
    
    
    def str2hash( self, text):
        '''Liefert den Hashwert eines Strings'''
        return self.nlp.vocab.strings[text]
    
    def hash2str( self, zahl):
        '''Liefert den String eines Hashwertes'''
        return self.nlp.vocab.strings[zahl]    
    
    
    def tagZ(self, taghash):
        '''Liefert tagZ, ein zusammenfassendes tag.
        Dies ist die Methode blp.tagZ des blp-Objektes, die Hashwerte annimmt.
        Es gibt auch die Funktion bj_nlp.tagZ, die Strings annimmt.
        '''        
        return bj_nlp.tagZ( self.hash2str(taghash) )
    
    
    def tagZZ(self, taghash):
        '''Liefert tagZZ, ein stark zusammenfassendes tag.
        Dies ist die Methode blp.tagZZ des blp-Objektes, die Hashwerte annimmt.
        Es gibt auch die Funktion bj_nlp.tagZZ, die Strings annimmt.
        '''        
        return bj_nlp.tagZZ( self.hash2str(taghash) )    
    
    
    
