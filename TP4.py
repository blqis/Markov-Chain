#### Génération de texte avec des chaînes de Markov

import random
import nltk
from nltk import (TreebankWordTokenizer, word_tokenize, wordpunct_tokenize, TweetTokenizer, MWETokenizer)

ponctuation = ['.', '!', '?']
NB_MOTS_MAXI = 100

""" Exercice 0 - Préparation des données """

def doc_to_word_list(path):

    path = './corpus.txt'

    with open(path, encoding='utf-8-sig') as input_stream:
        # compléter en utilisant les outils de découpage en phrases et en tokens 

        # découpage en mots
        
        word_list_beta = word_tokenize(input_stream.read())
        word_list = []
        punctuation = ['.', ',', ';', ':', '!', '?', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '-', '_', '+', '=', '*', '&', '^', '%', '$', '#', '@', '£', '€', '¥', '§', '°', '²', '³', 'µ', '·', '•', '…', '“', '”', '«', '»', '„', '‟', '‹', '›']
        for word in word_list_beta:
            if word[-1] not in punctuation:
                word_list.append(word)
            else:
                punct = word[-1]
                clean_word = word[0:len(word)-1]
                if clean_word != '':
                    word_list.append(clean_word)
                word_list.append(punct)
        return word_list

# print(doc_to_word_list('./corpus.txt')[:40])

""" Exercice 1 : chaîne de Markov de premier ordre (unigrammes)"""

def count_unigram_transitions(corpus):

    transitions = {}
    for i, word in enumerate(corpus):
        if word not in transitions:
            transitions[word] = {}
        if i < len(corpus) - 1:
            next_word = corpus[i + 1]
            if next_word not in transitions[word]:
                transitions[word][next_word] = 1
            else:
                transitions[word][next_word] += 1

    return transitions

# print(count_unigram_transitions(doc_to_word_list('./corpus.txt')))

def probabilify(comptes_transitions):

    probabilites = {}
    for word in comptes_transitions:
        total = sum(comptes_transitions[word].values())
        probabilites[word] = {next_word: count / total for next_word , count in comptes_transitions[word].items()}
    return probabilites

# print(probabilify(count_unigram_transitions(doc_to_word_list('./corpus.txt'))))

def markov_chain_unigram(corpus):
    transitions = count_unigram_transitions(corpus)
    return probabilify(transitions)

corpus = doc_to_word_list('./corpus.txt')
markov_chain = markov_chain_unigram(corpus)


def generate_unigram(markov_chain, start_token):

    maximum = NB_MOTS_MAXI
    token = start_token
    while token not in ponctuation and maximum > 0:
        print(token, end=' ')
        if token in markov_chain:
            # without random
            token = max(markov_chain[token], key=markov_chain[token].get)
        else:
            break
        maximum -= 1
    print(token)



# generate_unigram(markov_chain, "May")


def generer_unigramme_alea(markov_chain, start_token, n_best=1):

    maximum = NB_MOTS_MAXI
    token = start_token
    while token not in ponctuation and maximum > 0:
        print(token, end=' ')
        if token in markov_chain:
            # with random
            token = random.choice(sorted(markov_chain[token], key=markov_chain[token].get, reverse=True)[:n_best])
        else:
            break
        maximum -= 1
    print(token)

    
print("Exercice 1 : chaîne de Markov de premier ordre (unigrammes n_best)\n")
generer_unigramme_alea(markov_chain, "May", 10)


""" Exercice 2 : chaîne de Markov d'ordre 2 (bigrammes) """
    

def count_bigrammes_transitions(corpus):

    transitions = {}

    for i in range(len(corpus) - 2):
        token = corpus[i] + " " + corpus[i + 1]

        if token not in transitions:
            transitions[token] = {}

        next_word = corpus[i + 2]
            
        if next_word not in transitions[token]:
            transitions[token][next_word] = 1
        else:
            transitions[token][next_word] += 1



    return transitions

# print(count_bigrammes_transitions(corpus))

def chaines_markov_bigrammes(corpus):
    
        transitions = count_bigrammes_transitions(corpus)
        return probabilify(transitions)

# print(chaines_markov_bigrammes(corpus))

def find_bigram(markov_chain, start_token):
    bigrams = []
    for bigram in markov_chain:
        if bigram.split()[0] == start_token:
            bigrams.append(bigram)
    return bigrams


def generate_bi(markov_chain, start_token):
    maximum = NB_MOTS_MAXI
    token = start_token
    prevs = ["", ""]
    
    token = find_bigram(markov_chain, start_token)[0]
    print(token, end=' ')

    while token.split()[0] not in ponctuation and token.split()[1] not in ponctuation and maximum > 0:
        if token in markov_chain:
            token = max(markov_chain[token], key=markov_chain[token].get)
            prevs = [prevs[1], token.split()[-1]]

            bigrams = find_bigram(markov_chain, prevs[1])
            if bigrams != []:
                token = bigrams[0]
            else:
                break

        else:
            break
        maximum -= 1
        if token.split()[0] in ponctuation:
            print(token.split()[0], end='')
        else:
            print(token, end=' ')


# generate_bi(chaines_markov_bigrammes(corpus), "Bourgh")

def generate_bi_alea(markov_chain, start_token, n_best=1):

    maximum = NB_MOTS_MAXI
    token = start_token
    prevs = ["", ""]
    
    token = random.choice(find_bigram(markov_chain, start_token))
    print(token, end=' ')

    while token.split()[0] not in ponctuation and token.split()[1] not in ponctuation and maximum > 0:
        if token in markov_chain:
            token = random.choice(sorted(markov_chain[token], key=markov_chain[token].get, reverse=True)[:n_best])
            prevs = [prevs[1], token.split()[-1]]

            bigrams = find_bigram(markov_chain, prevs[1])
            if bigrams:
                token = random.choice(bigrams)
            else:
                break
        maximum -= 1
        if token.split()[0] in ponctuation:
            print(token.split()[0], end='')
        else:
            print(token, end=' ')


print("\n\n\n")
print("Exercice 2 : chaîne de Markov d'ordre 2 (bigrammes n_best)\n")
generate_bi_alea(chaines_markov_bigrammes(corpus), "May", 10)


"""Exercice 3 : chaîne de Markov d'ordre arbitraire"""


def count_transitions(corpus, ordre):
    
    transitions = {}
    for i in range(len(corpus) - ordre):
        token = " ".join(corpus[i:i+ordre])

        if token not in transitions:
            transitions[token] = {}

        next_word = corpus[i + ordre]

        if next_word not in transitions[token]:
            transitions[token][next_word] = 1
        else:
            transitions[token][next_word] += 1

    return transitions

# print(count_transitions(corpus, 3))

def chaines_markov(corpus, ordre):
    
    transitions = count_transitions(corpus, ordre)
    return probabilify(transitions)

# print(chaines_markov(corpus, 3))
markov_chain = chaines_markov(corpus, 3)

def find_ngram(markov_chain, start_token, ordre):
    ngrams = []
    for ngram in markov_chain:
        if ngram.split()[0] == start_token:
            ngrams.append(ngram)
    return ngrams

def generate_ngram(markov_chain, start_token, ordre):
    maximum = NB_MOTS_MAXI
    token = start_token
    prevs = [""] * ordre
    
    token = find_ngram(markov_chain, start_token, ordre)[0]
    print(token, end=' ')

    while token.split()[-1] not in ponctuation and maximum > 0:
        if token in markov_chain:
            token = max(markov_chain[token], key=markov_chain[token].get)
            prevs = prevs[1:] + [token.split()[-1]]

            ngrams = find_ngram(markov_chain, prevs[-1], ordre)
            if ngrams:
                token = ngrams[0]
            else:
                break

        else:
            break
        maximum -= 1
        if token.split()[0] in ponctuation:
            print(token.split()[0], end='')
        else:
            print(token, end=' ')

# generate_ngram(markov_chain, "May", 3)

def generate_ngram_alea(markov_chain, start_token, ordre, n_best=1):

    maximum = NB_MOTS_MAXI
    token = start_token
    prevs = [""] * ordre
    
    token = random.choice(find_ngram(markov_chain, start_token, ordre))
    print(token, end=' ')

    while token.split()[-1] not in ponctuation and maximum > 0:
        if token in markov_chain:
            token = random.choice(sorted(markov_chain[token], key=markov_chain[token].get, reverse=True)[:n_best])
            prevs = prevs[1:] + [token.split()[-1]]

            ngrams = find_ngram(markov_chain, prevs[-1], ordre)
            if ngrams:
                token = random.choice(ngrams)
            else:
                break
        maximum -= 1

        for split_element in token.split():
            if split_element in ponctuation:
                print(split_element, end='')
                return
            else:
                print(token, end=' ')

print("\n\n\n")
print("Exercice 3 : chaîne de Markov d'ordre arbitraire (trigrammes, n_best)\n")
generate_ngram_alea(markov_chain, "May", 3, 2)