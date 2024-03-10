from django import forms
from .models import Images, Category, Tovars, TovarsImages, TovarsCategory, Klient, KlientTovars
from django.core.exceptions import ValidationError
from django.utils.html import format_html
import hashlib
import os


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



class TovarsForm(forms.ModelForm):

   class Meta:
       model = Tovars
       fields = [
           'nametov',
           'tekst',
           'price',
           'kolvo',
           'reshenie_moderator',
           'tekst_moderator',
           'images',
           'category',
           #'klient',
       ]


       # def clean(self):
   #     cleaned_data = super().clean()
   #     tekst = cleaned_data.get("tekst")
   #     if tekst is not None and len(tekst) < 20:
   #         raise ValidationError({
   #             "tekst": "Описание не может быть менее 20 символов."
   #         })
   #
   #     head = cleaned_data.get("head")
   #     # tekst = cleaned_data.get("tekst")
   #     if head == tekst:
   #         raise ValidationError(
   #             # "текст статьи не должен совпадать с заголовком"
   #             {
   #                 "tekst": "текст новости не должен совпадать с заголовком"
   #             }
   #         )
   #
   #     return cleaned_data


class ImagesForm(forms.ModelForm):
   image = MultipleFileField(label='выбрать файлы', required=False)
   class Meta:
       model = Images
       fields = ['image',]

   def get_hash_md5(self,filename):
       with open(filename, 'rb') as f:
           m = hashlib.md5()
           while True:
               data = f.read(8192)
               if not data:
                   break
               m.update(data)
           return m.hexdigest()

   def delete_file(self,filenames):
       for filename in filenames:
           if os.path.exists(filename):
               os.remove(filename)






