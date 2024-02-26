# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:10:44 2024

@author: Amlan Ghosh
"""

# Tokens for the sentence "It shows, my dear Watson, that we are dealing with an
# exceptionally astude and dangerous man."
sample1 = ['It', 'shows', ',', 'my', 'dear', 'Watson', ',', 'that', 'we', 'are', 
           'dealing', 'with', 'an', 'exceptionally', 'astute', 'and', 'dangerous',
           'man', '.']
# Tokens for the sentence "How would Lausanne do, my dear Watson?"
sample2 = ['How', 'would', 'Lausanne', 'do', ',', 'my', 'dear', 'Watson', '?']

'''Building n-grams function'''
def build_ngrams(tokens:list, n:int) -> list:
    all_ngram = []
    for word_index in range(len(tokens) - n + 1):
        ngram = ()
        for number in range(n):
            ngram += (tokens[word_index + number],)
        all_ngram.append(ngram)
    return all_ngram

# Tests:
assert len(build_ngrams(sample1, n=3)) == 17
assert build_ngrams(sample1, n=3)[0] == ('It', 'shows', ',')
assert build_ngrams(sample1, n=3)[10] == ('dealing', 'with', 'an')
assert len(build_ngrams(sample1, n=2)) == 18
assert build_ngrams(sample1, n=2)[0] == ('It', 'shows')
assert build_ngrams(sample1, n=2)[10] == ('dealing', 'with')
assert len(build_ngrams(sample2, n=2)) == 8
assert build_ngrams(sample2, n=2)[0] == ('How', 'would')
assert build_ngrams(sample2, n=2)[7] == ('Watson', '?')

'''Building n-gram conrols'''
def build_ngrams_ctrl(tokens:list, n:int) -> list:
    tokens = ['<BOS>']*(n-1) + tokens + ['<EOS>']*(n-1)
    all_ngram = []
    for word_index in range(len(tokens) - n + 1):
        ngram = ()
        for number in range(n):
            ngram += (tokens[word_index + number],)
        all_ngram.append(ngram)
    return all_ngram

# Tests:
assert len(build_ngrams_ctrl(sample1, n=3)) == 21
assert build_ngrams_ctrl(sample1, n=3)[0] == ('<BOS>', '<BOS>', 'It')
assert build_ngrams_ctrl(sample1, n=3)[10] == ('we', 'are', 'dealing')
assert len(build_ngrams_ctrl(sample1, n=2)) == 20
assert build_ngrams_ctrl(sample1, n=2)[0] == ('<BOS>', 'It')
assert build_ngrams_ctrl(sample1, n=2)[10] == ('are', 'dealing')
assert len(build_ngrams_ctrl(sample2, n=2)) == 10
assert build_ngrams_ctrl(sample2, n=2)[0] == ('<BOS>', 'How')
assert build_ngrams_ctrl(sample2, n=2)[9] == ('?', '<EOS>')

def count_ngrams(tokens:list, n:int) -> list:
    all_ngram = []
    for token in tokens:
        all_ngram += build_ngrams_ctrl(token, n)
    count_ngram_dict = {}
    for ngram in all_ngram:
        if ngram[:-1] not in count_ngram_dict:
            count_ngram_dict[ngram[:-1]] = {ngram[-1]:1}
        else:
            if ngram[-1] not in count_ngram_dict[ngram[:-1]]:
                count_ngram_dict[ngram[:-1]][ngram[-1]] = 1
            else:
                count_ngram_dict[ngram[:-1]][ngram[-1]] += 1
    return count_ngram_dict

# Tests:
assert len(count_ngrams([sample1, sample2], n=3)) == 28
assert len(count_ngrams([sample1, sample2], n=3)['<BOS>', '<BOS>']) == 2
assert count_ngrams([sample1, sample2], n=3)['<BOS>', '<BOS>']['It'] == 1
assert count_ngrams([sample1, sample2], n=3)['<BOS>', '<BOS>']['How'] == 1
assert count_ngrams([sample1, sample2], n=3)['my', 'dear']['Watson'] == 2
assert len(count_ngrams([sample1, sample2], n=2)) == 24
assert len(count_ngrams([sample1, sample2], n=2)['<BOS>',]) == 2
assert count_ngrams([sample1, sample2], n=2)['<BOS>',]['It'] == 1
assert count_ngrams([sample1, sample2], n=2)['<BOS>',]['How'] == 1
assert count_ngrams([sample1, sample2], n=2)['dear',]['Watson'] == 2

def build_ngram_model(tokens:list, n:int) -> list:
    all_ngram = []
    for token in tokens:
        all_ngram += build_ngrams_ctrl(token, n)
    count_ngram_dict = {}
    for ngram in all_ngram:
        if ngram[:-1] not in count_ngram_dict:
            count_ngram_dict[ngram[:-1]] = {ngram[-1]:1}
        else:
            if ngram[-1] not in count_ngram_dict[ngram[:-1]]:
                count_ngram_dict[ngram[:-1]][ngram[-1]] = 1
            else:
                count_ngram_dict[ngram[:-1]][ngram[-1]] += 1
    for key in count_ngram_dict:
        occurrence = sum([count_ngram_dict[key][context] for context in count_ngram_dict[key]])
        for context in count_ngram_dict[key]:
            count_ngram_dict[key][context] = count_ngram_dict[key][context]/occurrence
    return count_ngram_dict

# Tests:
assert build_ngram_model([sample1, sample2], n=3)['<BOS>', '<BOS>']['It'] == 0.5
assert build_ngram_model([sample1, sample2], n=3)['<BOS>', '<BOS>']['How'] == 0.5
assert build_ngram_model([sample1, sample2], n=3)['my', 'dear']['Watson'] == 1.0
assert build_ngram_model([sample1, sample2], n=2)['<BOS>',]['It'] == 0.5
assert build_ngram_model([sample1, sample2], n=2)['<BOS>',]['How'] == 0.5
assert build_ngram_model([sample1, sample2], n=2)['dear',]['Watson'] == 1.0