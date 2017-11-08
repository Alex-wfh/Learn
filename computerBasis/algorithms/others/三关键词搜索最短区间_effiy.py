def calculate_shortest(words, search_words):
    all_existed = set([])
    all_existed_map = {}
    ret_list = []
    for idx, word in enumerate(words):
        if word in search_words:
            all_existed.add(word)
            all_existed_map[word] = idx
            if all_existed == search_words:
                idx_list  = [val for key, val in all_existed_map.iteritems()]
                idx_list.sort()
                tmp_str_idxs = map(lambda x: str(x) + ',', idx_list)
                ret_key = ''.join(tmp_str_idxs)[:-1]
                ret_value = idx_list[-1] - idx_list[0]
                ret_list.append({ret_key: ret_value})
    return ret_list
    pass


if __name__ == '__main__':
    for item in calculate_shortest(['a','b','c','b','e','c','a','c','e','a'], set(['a','e','c'])):
        print item
