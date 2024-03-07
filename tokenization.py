# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:53:54 2024

@author: Amlan Ghosh
"""

'The quick brown fox jumps over the lazy dog.'.split(' ')

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('distilgpt2')

split_text = tokenizer.tokenize('I visited Glasgow.')

print (tokenizer.tokenize('volcano'))

print (tokenizer.vocab['ĠGlasgow'])

print (len(tokenizer.vocab))

print (tokenizer.encode('I visited Glasgow.'))

print (tokenizer.decode([464, 7850, 46922, 4539, 832, 23995, 13]))

print (tokenizer.encode('Kelvingrove is a park in Glasgow.', truncation = True, max_length = 5))

print (tokenizer('Kelvingrove is a park in Glasgow.', return_tensors='pt'))

spanish_tokenizer = AutoTokenizer.from_pretrained('datificate/gpt2-small-spanish')
print(spanish_tokenizer.tokenize('The river Clyde runs through Glasgow.'))
print(spanish_tokenizer.encode('The river Clyde runs through Glasgow.'))
print(spanish_tokenizer.tokenize('Que te vaya bien'))
print(tokenizer.tokenize('Que te vaya bien'))