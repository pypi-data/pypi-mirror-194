"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = tinyshakespeareloader.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from tinyshakespeareloader import __version__

__author__ = "Artur A. Galstyan"
__copyright__ = "Artur A. Galstyan"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from tinyshakespeareloader.skeleton import fib`,
# when using this Python module as a library.


import numpy as np
from torch.utils.data import Dataset, DataLoader


class MiniShakesPeare(Dataset):
    def __init__(self, data, block_size=8) -> None:
        super().__init__()
        self.block_size = block_size
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if index == -1:
            index = len(self.data) - 1
        x = self.data[index : index + self.block_size]
        y = self.data[index + 1 : index + self.block_size + 1]

        if index + self.block_size + 1 > len(self.data):
            diff = index + self.block_size + 1 - len(self.data)

            to_add_on_x = diff - 1
            to_add_on_y = diff

            x = np.concatenate((x, self.data[:to_add_on_x]))
            y = np.concatenate((y, self.data[:to_add_on_y]))

        return x, y


def get_data(batch_size=4, train_ratio=0.9, block_size=8):
    """Get the train and test dataloaders as well as the vocabulary size, the vocabulary itself, the encoding and decoding functions.
    Args:
        batch_size (int, optional): The batch size. Defaults to 4. 
        train_ratio (float, optional): The ratio of the training data. Defaults to 0.9.
        block_size (int, optional): The size of the block. Defaults to 8.

    """


    # check if the file "input.txt" exists in the current directory
    # if not, download it from the internet
    import os

    if not os.path.exists("input.txt"):
        import urllib.request

        url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
        logging.info("Downloading the dataset from %s", url)
        urllib.request.urlretrieve(url, "input.txt")

    with open("input.txt", "r") as f:
        text = f.read()
    chars = sorted(list(set(text)))
    # print("".join(chars))
    vocabulary_size = len(chars)

    # Lookup table to map single characters to integers
    char_to_idx = {ch: i for i, ch in enumerate(chars)}

    # Lookup table to map integers to single characters
    idx_to_char = {i: ch for i, ch in enumerate(chars)}

    encode = lambda string: np.array([char_to_idx[ch] for ch in string])
    decode = lambda latent: "".join([idx_to_char[idx] for idx in latent])
    data = np.array(encode(text))
    n = int(train_ratio * len(data))

    train_data = data[:n]
    test_data = data[n:]

    train_dataset = MiniShakesPeare(train_data, block_size=block_size)

    test_dataset = MiniShakesPeare(test_data, block_size=block_size)
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=False,
    )
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
    )

    return {
        "train_dataloader": train_dataloader,
        "test_dataloader": test_dataloader,
        "vocabulary_size": vocabulary_size,
        "chars": chars,
        "encode": encode,
        "decode": decode,
    }


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )
