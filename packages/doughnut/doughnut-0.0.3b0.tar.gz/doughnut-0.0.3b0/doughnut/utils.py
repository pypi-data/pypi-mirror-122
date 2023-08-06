import re
import string
import numpy as np
from nltk.corpus import stopwords, twitter_samples
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

stopwords_english = stopwords.words('english')
stemmer = PorterStemmer()


def process_sentence(sentence):
    # remove stock market tickers like $GE
    sentence = re.sub(r'\$\w*', '', sentence)
    sentence = re.sub(r'^RT[\s]+', '', sentence)
    # remove hyperlinks
    sentence = re.sub(r'https?:\/\/.*[\r\n]*', '', sentence)
    # remove hashtags
    # only removing the hash # sign from the word
    sentence = re.sub(r'#', '', sentence)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    sentence_tokens = tokenizer.tokenize(sentence)
    sentence_clean = []
    for word in sentence_tokens:
        if (word not in stopwords_english and
                word not in string.punctuation):
            stem_word = stemmer.stem(word)  # stemming word
            sentence_clean.append(stem_word)
    return sentence_clean


def sentence_to_tensor(tweet, vocab_dict, unk_token='__UNK__'):
    word_l = process_sentence(tweet)
    tensor_l = []
    unk_id = vocab_dict[unk_token]

    for word in word_l:
        if word in vocab_dict:
            word_id = vocab_dict[word]
        else:
            word_id = unk_id
        tensor_l.append(word_id)
    return tensor_l


def remove_greater_than_max(lines, max_len):
    new_lines = []
    for line in lines:
        if len(line) < max_len:
            new_lines.append(line)
    return new_lines


def char_to_tensor(line, EOS_int=1):
    tensor = []
    for c in line:
        c_int = ord(str(c))
        tensor.append(c_int)
    tensor.append(EOS_int)
    return tensor


def get_vocab_ner(vocab_path, tags_path):
    vocab = {}
    with open(vocab_path) as f:
        for i, l in enumerate(f.read().splitlines()):
            vocab[l] = i  # to avoid the 0
        # loading tags (we require this to map tags to their indices)
    vocab['<PAD>'] = len(vocab)  # 35180
    tag_map = {}
    with open(tags_path) as f:
        for i, t in enumerate(f.read().splitlines()):
            tag_map[t] = i
    return vocab, tag_map


def get_params(vocab, tag_map, sentences_file, labels_file):
    sentences = []
    labels = []

    with open(sentences_file) as f:
        for sentence in f.read().splitlines():
            # replace each token by its index if it is in vocab
            # else use index of UNK_WORD
            s = [vocab[token] if token in vocab
                 else vocab['UNK']
                 for token in sentence.split(' ')]
            sentences.append(s)

    with open(labels_file) as f:
        for sentence in f.read().splitlines():
            # replace each label by its index
            l = [tag_map[label] for label in sentence.split(' ')]  # I added plus 1 here
            labels.append(l)
    return sentences, labels, len(sentences)


def get_params_ner(vocab, tag_map, sentences_file, labels_file):
    sentences = []
    labels = []

    with open(sentences_file) as f:
        for sentence in f.read().splitlines():
            # replace each token by its index if it is in vocab
            # else use index of UNK_WORD
            s = [vocab[token] if token in vocab
                 else vocab['UNK']
                 for token in sentence.split(' ')]
            sentences.append(s)

    with open(labels_file) as f:
        for sentence in f.read().splitlines():
            # replace each label by its index
            l = [tag_map[label] for label in sentence.split(' ')] # I added plus 1 here
            labels.append(l)
    return sentences, labels, len(sentences)


def load_tweets():
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')
    return all_positive_tweets, all_negative_tweets


def read_embedding_vectors(embedding_file):
    with open(embedding_file, 'r') as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)

        i = 1
        words_to_index = {}
        index_to_words = {}
        for w in sorted(words):
            words_to_index[w] = i
            index_to_words[i] = w
            i = i + 1
    return words_to_index, index_to_words, word_to_vec_map


def get_vocab(data):
    vocab = {'__PAD__': 0, '__</e>__': 1, '__UNK__': 2}
    for sentence in data:
        processed_sentence = process_sentence(sentence)
        for word in processed_sentence:
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab