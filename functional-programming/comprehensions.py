# 内包含/推导式/list/set/dict comprehensions

# original code

collection = list()
for datum in collection:
    if condition(datum):
        collection.append(datum)
    else:
        new = modify(datum)
        collection.append(new)

# somewhat more compactly we could write this as:

collection = [ d if condition(d) else modify(d) for d in data_set]
