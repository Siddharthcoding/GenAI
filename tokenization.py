import tiktoken

## Now we have to specify for which model we want to make the tokenizer
encoder = tiktoken.encoding_for_model('gpt-4o')

## Tells how many unique tokens are there
print("Vocab size", encoder.n_vocab) ## 200019

text = "The cat sat on the mat"

## To create tokens from given input
tokens = encoder.encode(text)
print("Tokens", tokens)      ## Tokens [976, 9059, 10139, 402, 290, 2450]

my_tokens = [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode(my_tokens)
print("Decoded", decoded)