

# splittet ein lexem in einen Kernbereich und eine Differenz
def diff_grammatik(lemma, lex):
    
    
    # splittet ein lexem in einen Kernbereich und eine Differenz
    def diff_grammatik_intern(lemma, lex):
        for i, (char1, char2) in enumerate(zip_longest(lemma, lex)):
            if char1 != char2:
                if i == 0:
                    return longest_substr([lemma, lex]),'' # 
                else:
                    return lex[:i],lex[i:] # normale Ausgabe
        return lemma,'' # Strings sind identisch    
    
    
    # main
    if lemma == lex:
        return lex, ''
    basis1, zusatz1 = diff_grammatik_intern( lemma,       lex )
    #if zusatz1=='☆': # ohne Umlautproblem
     #   return basis1, zusatz1
    
    lemma_ascii = lemma.replace('ä','a').replace('ö','o').replace('ü','u')
    lex_ascii   =   lex.replace('ä','a').replace('ö','o').replace('ü','u')   
    if lemma_ascii == lex_ascii:
        return lex, ''
    
    basis2, zusatz2 = diff_grammatik_intern( lemma_ascii, lex_ascii )  
    
    if len(basis2) <= len(basis1)   and   zusatz1 != '': #d ohne Umlautproblem
        return basis1, zusatz1

    if zusatz2 == ''  or zusatz1 == '':  #or  zusatz2 == '☆':
        return lex, ''
    else: 
        return lex[:len(basis2)], lex[-len(zusatz2):]


