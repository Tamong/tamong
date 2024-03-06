################################################################################
#
#         FILE:
#           hw03_ptw190000.py
#       AUTHOR:
#           Philip Wallis
#           PTW190000
#  DESCRIPTION:
#           Homework 3
#           This program will read a wikipedia page and tokenize the sentences.
#           It will then tag each word with a part of speech.

# DEPENDENCIES:
#           Python 3.11.4
#           NLTK tag/corpus/tokenize, re, beautifulsoup4
#
################################################################################
#!python

import re
import requests
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup


# Prints ===== Sentence # =====
def splitter(size, num, output):
    sen = "Sentence"
    num_str = str(num).zfill(5)  # pad with 0s
    new_size = size - len(num_str) - len(sen)
    print("\n" + "=" * new_size, sen, num_str, "=" * new_size)
    # output.write("\n" + "=" * new_size + " Sentence " + num_str + " " + "=" * new_size + "\n")


# Removes html tags, brackets, and extra spaces
def clean_data(data):
    clean = re.sub(r"<.*?>", "", data)
    clean = re.sub(r"\[.*?]", "", clean)
    clean = re.sub(r" +", " ", clean)
    return clean


# Returns a BeautifulSoup object from the URL
def get_page(url):
    print("Reading from the web...")
    html = requests.get(url).text
    page = BeautifulSoup(html, "html.parser")

    return page


# Returns a list of sentences from the page
def get_text(page):
    main = page.find("main")

    p_tags = main.find_all("p")

    data = []
    for p_tag in p_tags:
        data.append(clean_data(p_tag.get_text()))

    sentences = sent_tokenize("\n".join(data))

    return sentences


# Print and tokenize the sentence to POS.
def tokenize(sentence, count, output):
    splitter(40, count, output)
    print(sentence, "\n")
    # output.write(sentence + "\n")

    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Get POS tags for each word
    pos_tags = pos_tag(words)

    # Print the POS tags
    print(pos_tags)
    # output.write(str(pos_tags) + "\n")


def __main__():
    output = open("hw03_ptw190000.txt", "w")
    url = "https://en.wikipedia.org/wiki/American_Revolutionary_War"
    page = get_page(url)  # returns a BeautifulSoup object
    sentences = get_text(page)  # returns a list of sentences

    count = 0
    for sentence in sentences:
        # if there is multiple lines:
        if "\n" in sentence:
            for line in sentence.split("\n"):
                if line == "":
                    continue
                tokenize(line.lower(), count, output)
                count = count + 1
        else:
            if sentence == "":
                continue
            tokenize(sentence.lower(), count, output)
            count = count + 1

    # Close the files
    output.close()


__main__()
