def convert(filepath, byte_per_str):
    with open(filepath, 'rb') as f:
        s = dict()
        st = f.read(byte_per_str)
        while st:
            s[st] = s.get(st, 0) + 1
            st = f.read(byte_per_str)
        return sorted([s[key] for key in s])