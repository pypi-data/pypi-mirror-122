import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from doughnut.utils import char_to_tensor


class CharLevelDeepNGram(Dataset):
    def __init__(self, X):
        self.X = X

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        features = self.X[idx]
        features = char_to_tensor(features)
        sample = {"features": features}
        return sample


def collate_fn(batch):
    data_batch = [item["features"] for item in batch]
    data_batch_tensor = []
    for item in data_batch:
        data_batch_tensor.append(torch.tensor(item))
    data_batch = pad_sequence(data_batch_tensor, batch_first=True, padding_value=123)
    return [data_batch]
