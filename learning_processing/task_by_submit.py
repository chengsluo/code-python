from concurrent.futures import ThreadPoolExecutor, as_completed
# 除了用map，另外一个常用的方法是submit。如果你要提交的任务的函数是一样的，就可以简化成map。
# 但是假如提交的任务函数是不一样的，或者执行的过程之可能出现异常
# （使用map执行过程中发现问题会直接抛出错误）就要用到submit：
NUMBERS = list(range(30, 35))
def fib(n):
    if n == 34:
        raise Exception("Don't do this")
    if n<= 2:
        return 1
    return fib(n-1) + fib(n-2)
with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_num = {executor.submit(fib, num): num for num in NUMBERS}
    for future in as_completed(future_to_num):
        num = future_to_num[future]
        try:
            result = future.result()
        except Exception as e:
            print('raise an exception: {}'.format(e))
        else:
            print('fib({}) = {}'.format(num, result))
with ThreadPoolExecutor(max_workers=3) as executor:
    for num, result in zip(NUMBERS, executor.map(fib, NUMBERS)):
        print('fib({}) = {}'.format(num, result))