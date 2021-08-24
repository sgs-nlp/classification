def bag_of_word2one_hot(bag_of_word_vec: list, vector_len: int):
    tmp = [0] * (vector_len + 1)
    for idx in bag_of_word_vec:
        tmp[idx] = 1
    return tmp
