inp = open("in").readlines()

def transform(x):
    val = x // 3 - 2
    if val <= 0:
        return 0
    return val + transform(val)

print(sum(map(transform, map(int, inp))))
