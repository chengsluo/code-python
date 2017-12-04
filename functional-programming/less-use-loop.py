# for e in it:
#     func(e) # statement-based loop

# # equivalent
# map(func,it) # map-based loop

do_it = lambda f,*args:f(*args)
hello = lambda first,last:print("hello to",first,last)
bye = lambda first,last:print("byebye to",first,last)
_ = list(map(do_it,[hello,bye],["Chengs","Anna"],["Luo","Benis"]))

# combine
do_all_funcs = lambda fns,*args: [list(map(fn,*args)) for fn in fns]
_ = do_all_funcs([hello,bye],["Chengs","Anna","Deses"],["Luo","Benis","Neol"])

do_all_funcs = lambda fns,*args: [list(map(fns,*args))]
_ = do_all_funcs(hello,["Chengs","Anna","Deses"],["Luo","Benis","Neol"])


# # statement-based while loop
# while <cond>:
#     <pre-suite>
#     if <break_condition>:
#         break
#     else:
#         <suite>

# # FP-style recursive while loop
# def while_block():
#     <pre-suite>
#     if <break_condition>:
#         return 1
#     else:
#         <suite>
#         return 0
# while_FP = lambda: (<cond> and while_block()) or while_FP()
# while_FP()
# # statement-based while loop
# while <cond>:
#     <pre-suite>
#     if <break_condition>:
#         break
#     else:
#         <suite>

# # FP-style recursive while loop
# def while_block():
#     <pre-suite>
#     if <break_condition>:
#         return 1
#     else:
#         <suite>
#         return 0
# while_FP = lambda: (<cond> and while_block()) or while_FP()
# while_FP()

# iterative version echo()
def echo_IMP():
    while 1:
        str = input("IMP --")
        if str == "quit":
            break
        else:
            print(str)

echo_IMP()

# FP version echo() FP:functional programming
def identity_print(x): # identity with I/O side-effect
    print(x)
    return x

echo_FP = lambda : identity_print(input("FP --"))=='quit' or echo_FP()

echo_FP()
