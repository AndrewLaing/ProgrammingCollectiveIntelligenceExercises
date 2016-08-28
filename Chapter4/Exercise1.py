from string import punctuation

def separatewords(text):
    punctuation1 = punctuation.replace('+','').replace('$','').replace('#','')
    res = []
    result = text.replace('\n',' ').replace('\t',' ').replace('\r',' ').replace('\x0b',' ').replace('\x0c',' ').lower()
    result1 = result.split(' ')
    
    # Passes reiterates over the cleaned text to get, for example, a ? within quotes 
    for passes in range(2):
        for a in range(len(result1)):
            for punk in punctuation1:
                if result1[a] == punk:
                    result1[a] = ""
                if result1[a][-1:] == punk:
                    result1[a] = result1[a].replace(punk, ' ')[:-1]
                if result1[a][:0] in punk:
                    result1[a] = result1[a].replace(punk, '')[0:]
    
    for b in result1:
        if b != '': res.append(b)
    
    return res
