import re
from collections import Counter

def lower_text(text): 
    """
    returns the text tokenized into words
    and as lower case characters in a list
    """
    return re.findall(r'\w+', text.lower())

#dict counting the number of each word in the text file
tokenized_words = Counter(lower_text(open('bncwwri_untag.txt').read()))
# print(tokenized_words)
#print(len(tokenized_words)) #376715 different words
#print(sum(tokenized_words.values())) #appearing 89376867 times in the text
#print(tokenized_words.most_common(10)) 

def P(word, N=sum(tokenized_words.values())): 
    "Probability of `word`."
    return tokenized_words[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def edits1(word):
    "All edits that are one edit away from `word`"
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # print(splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    # print(deletes)
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # print(transposes)
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    # print(replaces)
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # print(inserts)
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def known(words): 
    "The subset of `words` that appear in the dictionary of words"
    return set(w for w in words if w in tokenized_words)

#print(correction('korrectud'))
print(edits1('smoothe'))
#print(known(edits1('somthing')))

def unit_tests():
    assert correction('dresed') == 'dressed'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('hauing') == 'having'                 # replace
    #assert correction('frighted') == 'frightened'           # insert 2
    assert correction('smoothe') == 'smooth'                    # delete
    #assert correction('anely') == 'only'                    #delete and replace
    #assert correction('sunne') == 'sun'
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert lower_text('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(lower_text('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(tokenized_words) == 376715
    assert sum(tokenized_words.values()) == 89376867
    assert tokenized_words.most_common(10) == [
     ('the', 5647035),
     ('of', 2877671),
     ('to', 2371089),
     ('and', 2365752),
     ('a', 1977507),
     ('in', 1814307),
     ('that', 893692),
     ('is', 887134),
     ('for', 814558),
     ('it', 802975)]
    assert tokenized_words['the'] == 5647035
    #assert P('quintessential') == 0
    assert 0.06 < P('the') < 0.07
    return 'unit_tests pass'

#print(P('the')) #0.06318228854452909
print(unit_tests())

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in tokenized_words)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, tokenized_words[w], right, tokenized_words[right]))
    print('{:.0%} of {} correct ({:.0%} unknown) '
          .format(good / n, n, unknown / n, n))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


spelltest(Testset(open('dev.txt'))) # Development set
#spelltest(Testset(open('test.txt'))) # Final test set
