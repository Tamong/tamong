################################### IMPORTS ####################################
import nltk
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
# from nltk.stem import PorterStemmer as ps
from nltk.stem import PorterStemmer
ps = PorterStemmer()

from nltk import word_tokenize, sent_tokenize, pos_tag
import requests
from bs4 import BeautifulSoup
import re
################################################################

def divider(text='',length=80,char='#',case=None):
    if(case=='upper'):
        text = text.upper()
    elif(case=='lower'):
        text = text.lower()
    elif(case=='title'):
        text = text.title()
    if (text!=''):
        text = ' ' + text + ' '
    print('\n' + text.center(length,char) + '\n')

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
    elif(type(obj)==nltk.corpus.reader.framenet.PrettyList):
        return True
    elif(type(obj)==list):
        return True
    elif(type(obj)==dict):
        return False

################################################################
#  Retreive the FrameNet object from NLTK by its name.
#  In this case the 'Opinion' Frame
frame = fn.frame('Piracy')
divider('Semantic Frame: ' + frame.name) # Display the name of the frame to stdout

#  Each semantic frame has several different properties.
#  One of the most important of which is a list of Lexical Units (LUs)
#  That is, a list of words (along with their part-of-speech) that
#  "evoke" or "signal" the possibility of a particular semantic frame
#  in a sentence.
lu_list = [lu.split('.')[0] for lu in frame['lexUnit']]
#  Every member of the LU List is a string of the form 'word.pos'
#  For example, some of the 'Opinion' frame LUs are think.v, believe.v,
#  opinion.n, etc.

#  Change to if(True) to display the list of LUs
if(False):
    divider('SEARCH SENTENCES FOR LEXICAL UNITS')
    for lu in lu_list:
        print('\t' + lu)

################################################################
#  Retrieve the web page where we want to search for instances of
#  our chosen frame--in this case, the 'Opinion' frame.
url = 'https://en.wikipedia.org/wiki/September_11_attacks'
respObj = requests.get(url)
raw_html_text = respObj.text # NOT encoded in any specific text format
#  print(raw_html_text) # NOT encoded, throws an error

#  Manually examine the web page header to see what the encoding is.
#  If it's already encoded in UTF-8, the following line isn't needed.
#  Otherwise, it's safer to force the web page's HTML source code to 
#  be UTF-8 encoded to make sure Python can deal with non-ASCII characters.
html_text = raw_html_text.encode("utf8")

#  Create a Beautiful Soup object from the raw HTML source code.
soupObj = BeautifulSoup(html_text, "html.parser")

#  We examined the HTML source code of the IMDB website to determine which HTML
#  tags they use to store the text of user reviews. Scanning the source code
#  revealed that reviews are in tags like... 
#      <div class="text show-more__control">
#  Beautiful Soup uses the following syntax for the find_all function to locate
paragraphs = soupObj.find_all('div', class_='text show-more__control')
#  Note that each "paragraph" has the contents of <div class="text show-more__control"> tag.


divider(' PARSE SENTENCES ')
sentence_count = 1
for p in paragraphs:
    p = p.text.strip() #  Remove HTML tags and newlines
    sentences = []     #  Initialize an empty list to store the website sentences
    sentences += sent_tokenize(p) #  Tokenize each <div... paragraph into sentences

    #  Loop through the sentences and test each one for presence of an LU word
    #  Optionally, you may also want to filter by matching part-of-speech.
    for sent in sentences:
        sent_words = word_tokenize(sent)
        pos_tagged = pos_tag(sent_words)
        for word in sent_words:
            #  Test if the sentence word is one of the 'Opinion' LUs in the LU List
            #  If yes, print the word followed by the sentence that it was found in.
            if(word in lu_list):
                divider('Found LU Word: "' + word + '" in sentence ' + str(sentence_count).zfill(5), char='-')
                print(sent)
        sentence_count += 1



