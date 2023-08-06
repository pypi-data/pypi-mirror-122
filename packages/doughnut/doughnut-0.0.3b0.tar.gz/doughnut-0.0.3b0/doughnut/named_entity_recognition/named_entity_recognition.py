import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader

"""
    Example
    X = 'data/sentences.txt'
    Y = 'data/labels.txt'
    words = 'data/words.txt'
    tags = 'data/tags.txt'
    vocab, tag_map = get_vocab_ner(words, tags)
    t_sentences, t_labels, t_size = get_params_ner(vocab, tag_map, X, Y)
    dataloader = DataLoader(transformed_dataset, batch_size=2,
                            shuffle=True, num_workers=0,collate_fn=collate_fn)
"""


class NamedEntityRecognitionGenerator(Dataset):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        features = self.X[idx]
        target = self.Y[idx]
        sample = {"features": features, "target": target}
        return sample


def collate_fn(batch):
    data_batch = [item["features"] for item in batch]
    target_batch = [item["target"] for item in batch]
    data_batch_tensor = []
    for item in data_batch:
        data_batch_tensor.append(torch.tensor(item))
    data_batch = pad_sequence(data_batch_tensor, batch_first=True, padding_value=123)
    target_batch_tensor = []
    for item in target_batch:
        target_batch_tensor.append(torch.tensor(item))
    target_batch = pad_sequence(target_batch_tensor, batch_first=True, padding_value=123)
    return [data_batch, target_batch]
