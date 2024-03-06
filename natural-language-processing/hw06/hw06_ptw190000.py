################################################################################
#  AUTHOR:
#       Philip Wallis,
#       Chris Irwin Davis
#  COURSE:
#       CS-4395
#  DESCRIPTION:
#       Example code for Homework #6 written during lecture 
#       Edited by Philip Wallis, to fit Homework #6.     
#  DATE:
#       2023-12-08
################################### IMPORTS ####################################
import nltk
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
ps = PorterStemmer()

from nltk import word_tokenize, sent_tokenize, pos_tag
import requests
from bs4 import BeautifulSoup
import re
############################# FUNCTION DEFINITIONS #############################


def divider(text='',length=80,char='#',case=None):
    if(case=='upper'):
        text = text.upper()
    elif(case=='lower'):
        text = text.lower()
    elif(case=='title'):
        text = text.title()
    if (text!=''):
        text = ' ' + text + ' '
    print(text.center(length,char))

def comment_div(text):
    divider(text,case='upper',char='#')

def printSub(content,level=0):
    indent = '    ' * level
    print(indent + str(content))

def strip_refs(text):
    return re.sub(r'\[\d+\]','',text)

def unique_list(lst):
    return list(set(lst))

def is_iterable(obj):
    if(type(obj)==nltk.corpus.reader.framenet.PrettyDict):
        return True
    elif(type(obj)==nltk.corpus.reader.framenet.AttrDict):
        return True
    elif(type(obj)==nltk.corpus.reader.framenet.PrettyList):
        return True
    elif(type(obj)==list):
        return True
    elif(type(obj)==dict):
        return False

################################################################################

frame1 = fn.frame('Piracy') 
divider(frame1.name)

print(frame1)
#
frame2 = fn.frame('Violence') 
divider(frame2.name)

print(frame2)
#
frame3 = fn.frame('Vehicle') 
divider(frame3.name)

print(frame3)

################################################################################


url = 'https://en.wikipedia.org/wiki/September_11_attacks' # This one article covers all three frames
respObj = requests.get(url)
raw_html_text = respObj.text # NOT encoded in any specific text format


soupObj = BeautifulSoup(raw_html_text, "html.parser")
paragraphs = soupObj.find_all('p')


divider('PARSE SENTENCES')

# Declare an empty list of store article sentences
sentences = []

# Declare and initialize a sentence counter
sentence_count = 1

# Loop over the paragraphs and tokenize sentences into the 'sentences' list
for para in paragraphs:
    # Remove HTML, newlines, and citation references
    para = strip_refs(para.text.strip())
    #divider(char='.')
    sentences += sent_tokenize(para)

# Loop over the sentences searching for instances of your chosen semantic frame
for sent in sentences:
    # Retreive the lexical units in the frame that
    # evoke/signal the presence of the semantic frame
    
    # combine the three lexUnits into one list
    lu_dict1 = {lu: 'Piracy frame' for lu in frame1['lexUnit']}
    lu_dict2 = {lu: 'Violence frame' for lu in frame2['lexUnit']}
    lu_dict3 = {lu: 'Vehicle frame' for lu in frame3['lexUnit']}

    # Merge the dictionaries
    lu_dict = {**lu_dict1, **lu_dict2, **lu_dict3}
    #lu_list = frame1['lexUnit'] 
    
    # Identify if a given Lexical Unit (LU) is in the current sentence
    for lu, frame_name in lu_dict.items():
        # If the LU is found in the sentence, then do something...
        if(lu.split('.')[0] in sent):
            divider('SENTENCE: ' + str(sentence_count).zfill(5))
            print(f'{frame_name} - {lu}')   # display the LU
            print(sent) # display the Sentence

            # Test for other Frame Elements (FEs) in the current sentence
            # Specifically, test here for regular expressions that look like sports scores.
            scores = re.findall(r'[\d]+–[\d]+',sent)
            if not(scores==[]):
                print('Score FE found')
                print(scores)
            # Search for other FEs, which may require other techniques...
                # WordNet, word_tokenize, pos_tag, chunking, named entity recognition, etc.
            # sent_words = word_tokenize(sent)
            # pos_tagged = pos_tag(sent_words)
            # print(sent)
            # divider(char='-')
            # print(sent_words)
            # divider(char='-')
            # print(pos_tagged)
    sentence_count += 1
    
    
    









