DEFAULT_MOD = 10 ** 9 + 7


def mod_permutation(n, k, mod=DEFAULT_MOD):
    if k >= mod:
        return 0
    ret = 1
    for i in range(n, n - k, -1):
        ret = (ret * i) % mod
    return ret


def mod_factorial(n, mod=DEFAULT_MOD):
    if n >= mod:
        return 0
    else:
        return mod_permutation(n, n, mod)


def mod_combination(n, k, mod=DEFAULT_MOD):
    k = min(k, n - k)
    mod_power = 0
    numerator = 1
    denominator = 1

    for i in range(n, n - k, -1):
        while i % mod == 0:
            i //= mod
            mod_power += 1
        numerator = (numerator * i) % mod

    for i in range(k, 0, -1):
        while i % mod == 0:
            i //= mod
            mod_power -= 1
        denominator = (denominator * i) % mod

    if mod_power > 0:
        return 0
    else:
        return (numerator * pow(denominator, mod - 2, mod)) % mod
