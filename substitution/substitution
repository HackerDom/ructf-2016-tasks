#!/usr/bin/python3

def calc_ones_count(x):
    count = 0
    while x > 0:
        if x & 1 == 1:
            count += 1
        x >>= 1
    return count

def add_checksum(x, check_len):
    ones_count = calc_ones_count(x) % check_len
    x <<= check_len - 1 - ones_count
    for i in range(ones_count):
        x <<= 1
        x |= 1
    return x

def check_checksum(x, check_len):
    ones_count = calc_ones_count(x >> (check_len - 1)) % check_len
    checksum = x & ((1 << (check_len - 1)) - 1)
    cnt = 0
    while checksum & 1 == 1:
        cnt += 1
        checksum >>= 1
    if checksum > 0:
        return False
    return ones_count == cnt

def calc_prob(k, m):
    check_len = m
    msg_len = k - m + 1

    cnt = dict()
    for msg in range(2 ** msg_len):
        key = add_checksum(msg, check_len)
        for new_msg in range(2 ** msg_len):
            if new_msg == msg:
                continue
            new_cyph = add_checksum(new_msg, check_len) ^ key
            if not new_cyph in cnt:
                cnt[new_cyph] = 0
            cnt[new_cyph] += 1
    return float(max(cnt.values())) / (2 ** msg_len)

k, m = list(map(int, input().split()))
print(calc_prob(k, m))