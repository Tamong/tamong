################################################################################
#
#         FILE:
#           hw05_ptw190000.py
#       AUTHOR:
#           Philip Wallis
#           PTW190000
#  DESCRIPTION:
#           Homework 5
#           This program will read a url, get the p tags, and then tokenize
#           the text. It will then tag the words and then chunk them. It will
#           then print the chunks. It will also use a gazetteer to replace
#           the tags with the gazetteer tags.
#
# DEPENDENCIES:
#           Python 3.11.4
#           NLTK, requests, beautifulsoup4
#
################################################################################
#!python


import requests
from nltk.tag import pos_tag
from nltk import ne_chunk
from nltk.tokenize import word_tokenize, sent_tokenize
from bs4 import BeautifulSoup
from nltk.tree import Tree


# Load the gazetteer from a file
def load_gazetteer(filename):
    gazetteer = {}
    with open(filename, "r") as file:
        for line in file:
            name, entity = line.strip().split(",")
            gazetteer[name] = entity
    return gazetteer


# Read the article from the web
def fetch_article(url):
    if (
        url
        == "https://www.espn.com/mlb/story/_/id/38759897/world-series-2023-rangers-diamondbacks-game-2-live-updates-analysis-takeaways"
    ):
        with open("espn.html", "r") as espn:
            soup = BeautifulSoup(espn, "html.parser")

    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    # Assuming that the article text is within <p> tags
    paragraphs = soup.find_all("p")
    article_text = " ".join([para.get_text() for para in paragraphs])
    return article_text


def replace_with_gazetteer(tokens, gazetteer):
    new_tokens = []
    skip = 0
    for i in range(len(tokens)):
        if skip:
            skip -= 1
            continue

        matched = False
        # Check if the current token starts a sequence matching a gazetteer entry
        for phrase in gazetteer.keys():
            phrase_tokens = phrase.split(" ")
            # If the next few tokens match the phrase in the gazetteer, add the matched phrase as a new token
            if tokens[i : i + len(phrase_tokens)] == phrase_tokens:
                new_tokens.append(
                    phrase
                )  # Use underscore as a placeholder for spaces in multi-word tokens
                skip = (
                    len(phrase_tokens) - 1
                )  # Skip the next few tokens that are part of the matched phrase
                matched = True
                break

        if not matched:
            new_tokens.append(
                tokens[i]
            )  # Add the current token as is if no match is found

    return new_tokens


# Process text with or without gazetteer
def process_text(text, use_gazetteer=False, gazetteer=None):
    sentences = sent_tokenize(text)
    tagged_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        # First apply gazetteer to see if tokens can be replaced before tagging
        if use_gazetteer:
            words = replace_with_gazetteer(words, gazetteer)

        tagged_words = pos_tag(words)

        # Now handle any tokens that have been replaced by gazetteer terms
        if use_gazetteer:
            corrected_tags = []
            for word in tagged_words:
                entity = gazetteer.get(
                    word[0]
                )  # Look for the original phrase without placeholders
                if entity:
                    corrected_tags.append(
                        (word[0], entity)
                    )  # Replace the tag with the gazetteer entity
                else:
                    corrected_tags.append(
                        word
                    )  # Keep the original tag for words not in the gazetteer
            tagged_tree = ne_chunk(corrected_tags, binary=False)
        else:
            tagged_tree = ne_chunk(tagged_words, binary=False)

        tagged_sentences.append(tagged_tree)

    # Print out the sentences with their chunks
    for i, tree in enumerate(tagged_sentences, 1):
        print(
            f"############################### Sentence: {i:04} ###############################"
        )
        for subtree in tree:
            if isinstance(subtree, Tree):
                ner = " ".join(c[0] for c in subtree.leaves())
                print((subtree.label(), ner))
            else:
                print(subtree)
        print("\n")


# URLs to process
urls = [
    "https://www.cbssports.com/mlb/news/world-series-game-1-score-highlights-rangers-get-dramatic-win-as-adolis-garcia-corey-seager-hit-late-homers/live/",
    "https://www.cbssports.com/mlb/news/world-series-game-1-score-highlights-rangers-get-dramatic-win-as-adolis-garcia-corey-seager-hit-late-homers/live/",
    "https://www.mlb.com/news/stats-facts-from-game-1-of-2023-world-series",
    "https://www.mlb.com/news/d-backs-lose-world-series-game-1-after-2-rangers-homers",
    "https://www.espn.com/mlb/story/_/id/38759897/world-series-2023-rangers-diamondbacks-game-2-live-updates-analysis-takeaways",
    "https://theathletic.com/live-blogs/rangers-vs-diamondbacks-world-series-game-2-live-score-updates/DsYeK8y1sZCi/",
]
# Main execution
if __name__ == "__main__":
    # Load the gazetteer from a file
    gazetteer = load_gazetteer("gazetteer.txt")

    for url in urls:
        print(f"Processing {url}")
        article = fetch_article(url)
        # process_text(article, use_gazetteer=False)
        process_text(article, use_gazetteer=True, gazetteer=gazetteer)
