from doughnut.utils import process_sentence, sentence_to_tensor
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence


class SentimentGenerator(Dataset):
    def __init__(self, X, Y, vocabulary=None):
        self.X = X
        self.Y = Y
        self.vocabulary = vocabulary
        if self.vocabulary is None:
            self.vocabulary = self.get_vocab()
        else:
            vocab_dict = self.vocabulary

    def __len__(self):
        return len(self.X)

    def get_vocab(self):
        vocab = {'__PAD__': 0, '__</e>__': 1, '__UNK__': 2}
        for sentence in self.X:
            processed_sentence = process_sentence(sentence)
            for word in processed_sentence:
                if word not in vocab:
                    vocab[word] = len(vocab)
        return vocab

    def __getitem__(self, idx):
        features = self.X[idx]
        target = self.Y[idx]
        tensor = sentence_to_tensor(features, self.vocabulary)
        sample = {"features": tensor, "target": target}
        return sample


def collate_fn(batch):
    data_batch = [item["features"] for item in batch]
    target_batch = [item["target"] for item in batch]
    data_batch_tensor = []
    for item in data_batch:
        data_batch_tensor.append(torch.tensor(item))
    data_batch = pad_sequence(data_batch_tensor, batch_first=True, padding_value=0)
    target_batch = torch.tensor(target_batch)
    return [data_batch, target_batch]
