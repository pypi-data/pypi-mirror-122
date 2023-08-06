import numpy as np
from doughnut.utils import load_tweets, process_sentence, read_embedding_vectors, get_vocab, load_tweets


class CustomDictionary:
    def __init__(self, data, embedding_dir, embedding_dimension):
        self.data = data
        self.embedding_dimension = embedding_dimension
        self.embedding_matrix = None
        self.vocabulary = None
        self.embedding_dir = embedding_dir

    def set_embedding_matrix(self):
        words_to_index, index_to_words, word_to_vec_map = read_embedding_vectors(self.embedding_dir)
        vocab = get_vocab(self.data)
        all_vocab_words = set(list(vocab.keys()))
        all_pretrained_words = set(list(words_to_index.keys()))
        common_words = all_vocab_words.intersection(all_pretrained_words)

        vocab_with_words_in_embedding = {'__PAD__': 0, '__</e>__': 1, '__UNK__': 2}
        for word, index in vocab.items():
            if word in common_words:
                vocab_with_words_in_embedding[word] = len(vocab_with_words_in_embedding)

        matrix_len = len(vocab_with_words_in_embedding)
        weights_matrix = np.zeros((matrix_len, self.embedding_dimension))
        zeros_matrix = np.zeros(self.embedding_dimension)
        weights_matrix[0] = zeros_matrix
        weights_matrix[1] = zeros_matrix
        weights_matrix[2] = zeros_matrix

        vocab_with_words_in_embedding_latest = {value: key for key, value in vocab_with_words_in_embedding.items()}
        counter = 3
        while counter < len(weights_matrix):
            word = vocab_with_words_in_embedding_latest[counter]
            weights_matrix[counter] = word_to_vec_map[word]
            counter = counter + 1
        self.embedding_matrix = weights_matrix
        self.vocabulary = vocab_with_words_in_embedding_latest
