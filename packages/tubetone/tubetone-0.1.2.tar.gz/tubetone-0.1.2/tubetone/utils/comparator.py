def compare_two_dicts(dict1, dict2):
    diff = set(dict1) - set(dict2)
    print('first has, second dont:')
    print(diff)
    diff = set(dict2) - set(dict1)
    print('second has, first dont:')
    print(diff)
    print('common words:')
    print(set(dict1.keys()).intersection(dict2.keys()))
