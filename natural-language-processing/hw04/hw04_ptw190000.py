################################################################################
#
#         FILE:
#           hw04_ptw190000.py
#       AUTHOR:
#           Philip Wallis
#           PTW190000
#  DESCRIPTION:
#           Homework 4
#           This program will read wikipedias page and tokenize the sentences.
#           It will then tag each word with a part of speech, and DATE.
#           For each dates in the sentence, it will show days since the first date of the sentence

# DEPENDENCIES:
#           Python 3.11.4
#           NLTK tag/corpus/tokenize, re, datetime, beautifulsoup4
#
################################################################################
#!python

import re
import datetime
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup

date_format = r"(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+\d{1,2},\s+\d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}/\d{1,2}/\d{2}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+\d{4}"

format_patterns = [
    "%B %d, %Y",  # Full month name, day, and year
    "%b %d, %Y",  # Abbreviated month name, day, and year
    "%d %B, %Y",  # Full month name, day, and year
    "%d %b, %Y",  # Abbreviated month name, day, and year
    "%m/%d/%Y",  # Date in the format mm/dd/yyyy
    "%m/%d/%y",  # Date in the format mm/dd/yy
    "%Y-%m-%d",  # Date in the ISO format yyyy-mm-dd
]

# Combine date_formats into a single regular expression pattern
# date_pattern = "|".join(date_formats)


# Prints ===== Sentence # =====
def splitter(size, num):
    sen = "Sentence"
    num_str = str(num).zfill(5)  # pad with 0s
    new_size = size - len(num_str) - len(sen)
    print("\n" + "=" * new_size, sen, num_str, "=" * new_size)


# Removes html tags, brackets, and extra spaces
def clean_data(data):
    clean = re.sub(r"<.*?>", "", data)
    clean = re.sub(r"\[.*?]", "", clean)
    clean = re.sub(r" +", " ", clean)
    return clean


# Returns a BeautifulSoup object from the URL
def get_page(html):
    page = BeautifulSoup(html, "html.parser")

    return page


# Returns a list of sentences from the page
def get_text(page):
    main = page.find("main")

    tags = main.find_all("p")
    references = main.find_all("li", id=re.compile(r"cite_note-\d+"))

    data = []
    for tag in tags:
        data.append(clean_data(tag.get_text()))

    sentences = sent_tokenize("\n".join(data))

    for reference in references:
        sentences.append(reference.get_text())

    return sentences


# Print and tokenize the sentence to POS.
def tokenize(sentence, count, output):
    splitter(40, count)
    print(sentence, "\n")
    # output.write(sentence + "\n")
    date_counter = 1
    # Initialize date_dict as a dictionary

    # Tokenize the sentence into words
    dates = re.findall(date_format, sentence)

    for date in dates:
        # Replace the date with a placeholder
        placeholder = f"DATE_{str(date_counter).zfill(6)}"
        sentence = sentence.replace(date, placeholder)
        # Add the mapping to the date dictionary
        date_counter += 1

    words = word_tokenize(sentence)
    # Get POS tags for each word
    pos_tags = pos_tag(words)

    # Print the POS tags
    print(pos_tags)
    # output.write(str(pos_tags) + "\n")

    # For each date in the date dictionary
    for date in dates:
        print(date)
        for i, format_pattern in enumerate(format_patterns, 1):
            try:
                dateobj = datetime.datetime.strptime(date, format_pattern)
                print(dateobj)
            except ValueError:
                continue  # Try the next format pattern if this one raises an error


def parse(html, output):
    page = get_page(html)  # returns a BeautifulSoup object
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


def __main__():
    output = open("hw04_ptw190000.txt", "w")

    with open("2023_Maldivian_presidential_election.html", "r") as f:
        mpe = f.read()

    with open("American_Revolutionary_War.html", "r") as f:
        arw = f.read()

    with open("Katalin Karikó.html", "r") as f:
        kk = f.read()

    parse(mpe, output)

    # url = "https://en.wikipedia.org/wiki/American_Revolutionary_War"

    # Close the files
    output.close()


__main__()
