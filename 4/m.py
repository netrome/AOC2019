import tqdm

start = 197487
stop = 673251


def criteria(n):
    s = str(n)

    last = int(s[0])
    double = False
    for c in s[1:]:
        d = int(c)
        if d == last:
            double = True

        if d < last:
            return False
        last = d

    return double


def criteria2(n):
    s = tuple(map(int, str(n)))

    last = s[0]
    double = False
    for i, d in enumerate(s[1:]):
        if d == last:
            try:
                if d == s[i-1]:
                    continue
            except Exception:
                pass
            try:
                if d == s[i+2]:
                    continue
            except Exception:
                pass
            double = True

        if d < last:
            return False
        last = d

    return double


print(criteria2(112233))
print(criteria2(123444))
print(criteria2(111122))

print(len(tuple(filter(criteria, range(start, stop)))))
print(len(tuple(filter(criteria2, range(start, stop)))))
