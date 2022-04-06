import os
from PIL import Image
from core.settings import BASE_DIR
from django.template.defaultfilters import slugify


def image_deleter(instance):
    try: 
        if instance.image.url != '/media/post/default.png':
            os.remove(str(BASE_DIR)+ str(instance.image.url).replace('/',"\\"))
            print('dosyadan silindi.')
        else:
            print('default resim')
    except:
        print('İmage Delete Error:')


def image_size_converter(instance):
    img = Image.open(instance.image.path)
    if img.height > 320 or img.width > 320:
        new_img = (320, 320)
        img.thumbnail(new_img)
        img.save(instance.image.path)

