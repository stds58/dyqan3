import hashlib


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

filename = 'F:/pitonprojekt/dyqan3/lulet/media/images/3.jpeg'
x = get_hash_md5(filename)
print(x)
filename = 'F:/pitonprojekt/dyqan3/lulet/media/images/3_AvbXPRg.jpeg'
x = get_hash_md5(filename)
print(x)

# 39140ddbe3b0edf6f5b9becbc2ed0a8c  3.jpeg
# 39140ddbe3b0edf6f5b9becbc2ed0a8c 3_AvbXPRg.jpeg
# 94e459f3a814c0b43763b20c0280936a WhatsApp_Image_2021-04-03_at_18.07.29_5pjclyd.jpeg
# 94e459f3a814c0b43763b20c0280936a WhatsApp_Image_2021-04-03_at_18.07.29_5pjclyd_IuYTBpf.jpeg
