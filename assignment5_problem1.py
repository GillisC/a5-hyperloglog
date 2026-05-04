#!/usr/bin/env python3

import argparse

def rol32(x,k):
    """Auxiliary function (left rotation for 32-bit words)"""
    return ((x << k) | (x >> (32-k))) & 0xffffffff

def murmur3_32_scramble(k):
    k = (k * 0xcc9e2d51) & 0xffffffff
    k = ((k << 15) & 0xffffffff) | ((k >> 17) & 0xffffffff)
    k = (k * 0x1b873593) & 0xffffffff
    return k

def murmur3_32(key, seed):
    """Computes the 32-bit murmur3 hash"""
    
    # convert the input key (unicode) to utf-8
    arr = bytearray(key, "utf-8")
    print(f"\nlength of bytearray: {len(arr)}")
    num_full_blocks = len(arr) // 4
    num_rest_blocks = (len(arr) % 4)

    main_data = memoryview(arr[0:num_full_blocks * 4])
    main_data = main_data.cast("I") # 32bit integer

    tail_data = memoryview(arr[num_full_blocks * 4:])
    tail_data = tail_data.cast("B") # unsigned single byte

    h = seed
    
    for i in main_data:
        k = i
        
        h = h ^ murmur3_32_scramble(k)
        h = (h << 13) | (h >> 19)
        h = (h * 5 + 0xe6546b64) & 0xffffffff

    k = 0x0
    for i in reversed(range(len(tail_data))):
        # we are on little-endian system so we dont need to swap
        k = k << 8
        k = k & 0xffffffff
        k = k | tail_data[i]

    h = h ^ murmur3_32_scramble(k)

    h = h ^ len(arr)
    h = h ^ (h >> 16)
    h = (h * 0x85ebca6b) & 0xffffffff
    h = h ^ (h >> 13)
    h = (h * 0xc2b2ae35) & 0xffffffff
    h = h ^ (h >> 16)

    return h


def auto_int(x):
    """Auxiliary function to help convert e.g. hex integers"""
    return int(x,0)


def test() -> None:
    tests = [
        {"string": "", "seed": 0x00000000, "hash_val": 0x00000000},
        {"string": "", "seed": 0x00000001, "hash_val": 0x514e28b7},
        {"string": "", "seed": 0xffffffff, "hash_val": 0x81f16f39},
        {"string": "test", "seed": 0x00000000, "hash_val": 0xba6bd213},
        {"string": "test", "seed": 0x9747b28c, "hash_val": 0x704b81dc},
        {"string": "Hello, world!", "seed": 0x00000000, "hash_val": 0xc0363e43},
        {"string": "Hello, world!", "seed": 0x9747b28c, "hash_val": 0x24884cba},
        {
            "string": """The quick brown fox jumps over the lazy dog""",
            "seed": 0x00000000,
            "hash_val": 0x2e4ff723
        },
        {
            "string": """The quick brown fox jumps over the lazy dog""",
            "seed": 0x9747b28c,
            "hash_val": 0x2fa826cd
        },
        {
            "string": """Rýchla hnedá líška preskočila lenivého psa""",
            "seed": 0x00000000,
            "hash_val": 0x678b9be9
        },
        {
            "string": """Rýchla hnedá líška preskočila lenivého psa""",
            "seed": 0x9747b28c,
            "hash_val": 0x8d3382a7
        },
        {
            "string": """Быстрая коричневая лиса перепрыгивает через ленивую собаку""",
            "seed": 0x00000000,
            "hash_val": 0xa94f1f75
        },
        {
            "string": """Быстрая коричневая лиса перепрыгивает через ленивую собаку""",
            "seed": 0x9747b28c,
            "hash_val": 0x4152021b
        },
        {"string": "敏捷的棕色狐狸跳过了懒狗", "seed": 0x00000000, "hash_val": 0x6687dfe4},
        {"string": "敏捷的棕色狐狸跳过了懒狗", "seed": 0x9747b28c, "hash_val": 0xc7df48f1},
    ]

    for test in tests:
        key = test["string"]
        seed = test["seed"]
        expected = test["hash_val"]

        actual = murmur3_32(key, seed)

        p: bool = actual == expected
        if p:
            print(f"PASS key: {key}\tseed: {seed:#010x})")
        else:
            print(f"FAIL key: {key}\tseed: {seed:#010x})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Computes MurMurHash3 for the keys."
    )
    parser.add_argument("key", nargs="*", help="key(s) to be hashed", type=str)
    parser.add_argument("-s", "--seed", type=auto_int, default=0, help="seed value")
    args = parser.parse_args()


    test()

    seed = args.seed
    for key in args.key:
        h = murmur3_32(key, seed)
        print(f"{h:#010x}\t{key}")
