# Here's some data. How do I need to do with it?

# configure the data to start with
collection = get_initial_start()
state_var = None
for datum in data_set:
    if condition(state_var):
        state_var = calculate_from(datum)
        new = modify(datum,state_var)
        collection.add_to(new)
    else:
        new = modify_differently(datum)
        collection.add_to(new)

# now actually work with data
for thing in collection:
    process(thing)
 
# ----
# Here's some data. What do I need to do with it?

# tuck away construction of data
def make_collection(data_set):
    collection = get_initial_start()
    state_var = None
    for datum in data_set:
        if condition(state_var):
            state_var = calculate_from(datum)
            new = modify(datum,state_var)
            collection.add_to(new)
        else:
            new = modify_differently(datum)
            collection.add_to(new)
    return collection

# now actually work with the data
for thing in make_collection(data_set):
    process(thing)
    