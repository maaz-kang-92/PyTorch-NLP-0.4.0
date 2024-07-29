from torchnlp.encoders.text.static_tokenizer_encoder import StaticTokenizerEncoder


class TreebankEncoder(StaticTokenizerEncoder):
    """ Encodes text using the Treebank tokenizer.

    **Tokenizer Reference:**
    http://www.nltk.org/_modules/nltk/tokenize/treebank.html

    Args:
        sample (list): Sample of data used to build encoding dictionary.
        min_occurrences (int, optional): Minimum number of occurrences for a token to be added to
          the encoding dictionary.
        append_eos (bool, optional): If ``True`` append EOS token onto the end to the encoded
          vector.
        reserved_tokens (list of str, optional): List of reserved tokens inserted in the beginning
            of the dictionary.
        eos_index (int, optional): The eos token is used to encode the end of a sequence. This is
          the index that token resides at.
        unknown_index (int, optional): The unknown token is used to encode unseen tokens. This is
          the index that token resides at.
        padding_index (int, optional): The unknown token is used to encode sequence padding. This is
          the index that token resides at.

    Example:

        >>> encoder = TreebankEncoder(["This ain't funny.", "Don't?"])
        >>> encoder.encode("This ain't funny.")
        tensor([5, 6, 7, 8, 9])
        >>> encoder.vocab
        ['<pad>', '<unk>', '</s>', '<s>', '<copy>', 'This', 'ai', "n't", 'funny', '.', 'Do', '?']
        >>> encoder.decode(encoder.encode("This ain't funny."))
        "This ain't funny."

    """

    def __init__(self, *args, **kwargs):
        if 'tokenize' in kwargs:
            raise TypeError('Encoder does not take keyword argument tokenize.')

        try:
            import nltk

            # Required for moses
            nltk.download('perluniprops')
            nltk.download('nonbreaking_prefixes')

            from nltk.tokenize.treebank import TreebankWordTokenizer
            from nltk.tokenize.treebank import TreebankWordDetokenizer
        except ImportError:
            print("Please install NLTK. " "See the docs at http://nltk.org for more information.")
            raise

        self.detokenizer = TreebankWordDetokenizer()

        super().__init__(*args, tokenize=TreebankWordTokenizer().tokenize, **kwargs)

    def decode(self, tensor):
        tokens = [self.itos[index] for index in tensor]
        return self.detokenizer.detokenize(tokens)
