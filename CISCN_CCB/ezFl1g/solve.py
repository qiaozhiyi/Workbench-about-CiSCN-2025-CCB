def fib_mod_16(n):
    if n == 0: return 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % 16
    return a

K = "012ab9c3478d56ef"

v11 = 1
flag = "flag{"
for i in range(32):
    # f(v11) returns K[fib(v11) % 16]
    # Since we need fib(v11) % 16, and the period is 24:
    idx = fib_mod_16(v11 % 24)
    v9 = K[idx]
    flag += v9
    if i in [7, 12, 17, 22]:
        flag += "-"
    v11 = (v11 * 8 + i + 64)

flag += "}"
print(flag)