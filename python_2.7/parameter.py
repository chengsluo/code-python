def demo(new_item, old_list=[]):
    if old_list is None:
        old_list = []
    old_list.append(new_item)
    return old_list

print(demo('5', [1, 2, 3, 4]))
print(demo('aaa', ['a', 'b']))
print(demo('a'))
print(demo('b'))