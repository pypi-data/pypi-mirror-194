import nltk
from nltk.tokenize import WhitespaceTokenizer
nltk.download('punkt')



def make_ngram(document, n_grams_min,n_grams_max,):
    if n_grams_min > n_grams_max:
        return 'n_grams_min cannot be greater then n_grams_max'
    lst = list(WhitespaceTokenizer().span_tokenize(document))
    for i in range(len(lst)): 
        for j in range(n_grams_min,n_grams_max+1):
            try:
                yield  lst[i][0],lst[i+j][1], document[lst[i][0]:lst[i+j][1]]
            except:
                pass
                break
    

def key_search(document,keyword_lst, n_grams_min ='default',n_grams_max='default',partial_match= False):
    dict = {}
    if partial_match == False:
        if n_grams_min == 'default':
            n_grams_min = min([ len(i.split(" ")) for i in keyword_lst ])
        if n_grams_max == 'default':
            n_grams_max = max([ len(i.split(" ")) for i in keyword_lst ])
    else:
        n_grams_min = 0
        n_grams_max = max([ len(i.split(" ")) for i in keyword_lst ])
        keyword_lst = " ".join(keyword_lst).split(" ")

        
    
    key_dict = {keyword_lst[i]: keyword_lst[i + 1] for i in range(0, len(keyword_lst), 2)}
    for start,end,value in make_ngram(document,n_grams_min,n_grams_max):
            if value in key_dict:
                if dict.get(value):
                    dict[value].append((start,end)) 
                else:
                    dict[value] = [(start,end)]
    return dict
       


doc = 'lets all search for full stack engineers and try to give him our best'
keywords = ['full stack engineers', 'engineers']


print(key_search(doc,keywords,partial_match=False))




