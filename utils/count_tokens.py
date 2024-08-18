from tokenizers import Tokenizer

def count_tokens(text):
    tokenizer = Tokenizer.from_pretrained("upstage/solar-1-mini-tokenizer")
    enc = tokenizer.encode(text)
    total_num_of_tokens = len(enc.tokens)

    return total_num_of_tokens
