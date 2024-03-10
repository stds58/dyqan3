import hashlib
from lulet.dbapp.models import Images


def get_hash_md5(filename):
    m = hashlib.md5()
    m.update(filename)
    return m.hexdigest()

images = Images.objects.all()
for img in images:
    print(img)
    print(img.image)


