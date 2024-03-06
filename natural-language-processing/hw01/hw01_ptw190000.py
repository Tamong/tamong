################################################################################
#
#         FILE:
#           hw01.py
#       AUTHOR:
#           Philip Wallis
#           PTW190000
#  DESCRIPTION:
#           Homework 1
#           This program will read in a text file and output the top 20 most
#           frequent words in the file. It will also output the frequency and
#           percentage of each word. It then saves the cleaned text to a new
#           file, and a new file with the top 20 words, frequency, and percentage.
# DEPENDENCIES:
#           Python 3.10.11
#           NLTK, re, collections (Counter)
#
################################################################################
#!python

import re
import nltk

nltk.download("punkt")

from collections import Counter

frequency_map = {}  # Keep track of the frequency of each word


# clean_data will remove html tags and the @@1234567 tags
def clean_data(data):
    no_html = re.sub(r"<.*?>", "", data)
    no_tags = re.sub(r"@@\d{7}", "", no_html)
    return no_tags


# frequency will count the frequency of each word
def frequency(data):
    for word in data:
        if word in frequency_map:
            frequency_map[word] += 1
        else:
            frequency_map[word] = 1


def top_words(count):
    # Get the top 20 frequent words
    counter = Counter(frequency_map)
    result = dict(counter.most_common(count))
    # Get the total count of words
    total_count = sum(frequency_map.values())
    return result, total_count


def __main__():
    input = open("text_news.txt", "r")
    output = open("hw01_ptw190000.txt", "w")
    top_words_output = open("hw01_ptw190000_top20.txt", "w")

    # process line by line
    for line in input:
        cleaned = clean_data(line)
        tokens = nltk.word_tokenize(cleaned)
        words = [word.lower() for word in tokens if word.isalpha()]
        frequency(words)
        output.write(cleaned)

    # Get the top 20 frequent words
    result, total_count = top_words(20)

    # Print the results
    print(" #  Word  Frequency  Percentage")
    top_words_output.write("#  Word  Frequency  Percentage\n")
    print("--- ----  ---------  ----------")
    top_words_output.write("--- ----  ---------  ----------\n")
    count = 1
    for word in result:
        print(
            "{:<4} {:<7} {:<9} {:<7}".format(
                count,
                word,
                result[word],
                round((result[word] / total_count), 5),
            )
            + "%"
        )
        top_words_output.write(
            "{:<4} {:<7} {:<9} {:<7}".format(
                count,
                word,
                result[word],
                round((result[word] / total_count), 5),
            )
            + "%\n"
        )

        count += 1

    # Close the files
    input.close()
    output.close()
    top_words_output.close()


__main__()
