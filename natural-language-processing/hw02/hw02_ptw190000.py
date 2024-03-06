################################################################################
#
#         FILE:
#           hw02_ptw190000.py
#       AUTHOR:
#           Philip Wallis
#           PTW190000
#  DESCRIPTION:
#           Homework 2
#           This program will read a text file and tokenize the sentences.
#           It will then tag each word with a part of speech.
#           It will then find the first noun in the sentence and find the
#           synset for that noun. It will then print the definition of the
#           synset and the common hypernyms for the rest of the nouns in the
#           sentence.
# DEPENDENCIES:
#           Python 3.10.11
#           NLTK tag/corpus/tokenize, re
#
################################################################################
#!python

import re
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize, sent_tokenize

# nltk.download("punkt")


def printer(text, output):
    print(text)
    output.write(text + "\n")


# clean_data will remove html tags and the @@1234567 tags
def clean_data(data):
    clean = re.sub(r"<.*?>", "", data)
    clean = re.sub(r"@@\d{7}", "", clean)
    clean = re.sub(r"\n", "", clean)
    clean = re.sub(r"@", "", clean)
    clean = re.sub(r" +", " ", clean)
    return clean


def __main__():
    input = open("text_web.txt", "r")
    output = open("hw02_ptw190000.txt", "w")

    # process input
    raw_text = input.read()
    cleaned = clean_data(raw_text)

    sentences = sent_tokenize(cleaned)
    for sentence in sentences:
        # write splitter
        output.write("\n" + "=" * 80 + "\n")
        print("\n" + "=" * 80 + "\n")

        # write the sentence
        output.write("\n" + sentence + "\n\n")
        print(sentence, "\n")

        # tokenize and tag each word the sentence with a part of speech
        words = word_tokenize(sentence)
        tagged_tokens = pos_tag(words)

        # write the tagged tokens
        output.write(tagged_tokens.__str__() + "\n")
        print(tagged_tokens, "\n")

        nouns = []

        # identify all nouns in the sentence
        for token in tagged_tokens:
            if token[1].startswith("NN"):
                nouns.append(token)
        if len(nouns) == 0:
            continue

        # extract the first noun
        first_noun = nouns[0]
        nouns = nouns[1:]

        # print the first noun
        synset = wn.synsets(first_noun[0], pos=wn.NOUN)
        output.write("\nFIRST NOUN:" + first_noun[0] + "\n")
        print("FIRST NOUN:", first_noun[0])

        if len(synset) > 0:
            for syn in synset:
                # skip if the synset is not a noun
                if syn.pos() != wn.NOUN:
                    continue

                # print the definition of the synset
                output.write(syn.name() + ": " + syn.definition()[:30] + "\n")
                print(syn.name() + ": " + syn.definition()[:30])

                # if there are more nouns in the sentence, print the common hypernyms

                for noun in nouns:
                    if wn.synsets(noun[0], pos=wn.NOUN):
                        # if the noun is in wordnet, print the common hypernyms
                        noun_first_synset = wn.synsets(noun[0], pos=wn.NOUN)[0]

                        output.write(
                            "\t"
                            + noun[0]
                            + " - "
                            + noun_first_synset.name()
                            + ": \n\t\tDefinition: "
                            + noun_first_synset.definition()[:30]
                            + "\n"
                        )
                        print(
                            "\t"
                            + noun[0]
                            + " - "
                            + noun_first_synset.name()
                            + ": \n\t\tDefinition:"
                            + noun_first_synset.definition()[:30]
                        )
                        hypernyms = syn.lowest_common_hypernyms(noun_first_synset)
                        output.write(
                            "\t\tCommon Hypernym: " + hypernyms.__str__() + "\n"
                        )
                        print("\t\tCommon Hypernym: ", hypernyms)
                    else:
                        # if the noun is not in wordnet, print a message
                        output.write("\t" + noun[0] + " NOT FOUND IN WORDNET" + "\n")
                        print("\t" + noun[0] + " NOT FOUND IN WORDNET")

        else:
            # if the synset does not exist, print a message
            print("SYNSET DOES NOT EXIST")
            output.write("SYNSET DOES NOT EXIST")

    # Close the files
    input.close()
    output.close()


__main__()
