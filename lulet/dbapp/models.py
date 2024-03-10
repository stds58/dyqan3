from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, time, timezone
from django.conf import settings
from django.utils.html import format_html


class Images(models.Model):
    image = models.ImageField(upload_to='images', unique=True)
    data_create = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Images"
        verbose_name_plural = "Images"
    def __str__(self):
        #return f'{self.id} {self.image}'
        #return f'<img src="F:/pitonprojekt/dyqan3/lulet/media/{self.image}" width="100" height="100" alt="">'
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.image.url))
    def get_absolute_url(self):
        return reverse('images_edit')
#https://pocoz.gitbooks.io/django-v-primerah/content/glava-5-obschii-dostup-k-kontentu-na-saite/sozdanie-miniatyur-izobrazhenii-s-pomoschyu-sorl-thumbnail.html

class Category(models.Model):
    namecat = models.CharField(max_length=20)
    data_create = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

    def create_category(namecat):
        categories = Category.objects.values_list("namecat", flat=True)
        if not categories:
            cat1 = Category.objects.create(namecat=namecat)
            cat1.save()
        for cat in categories:
            if namecat == cat:
                return 'такая категория уже есть'
            else:
                cat1 = Category.objects.create(namecat=namecat)
                cat1.save()

    def __str__(self):
        return f'{self.id} {self.namecat}'
#from dbapp.models import *
#from datetime import datetime, time, timezone
#Category.create_category('yyy')


class Tovars(models.Model):
    POSITIONS = [(0, 'на рассмотрении'),(1, 'принято'),(2, 'исправить'),]

    nametov = models.CharField(max_length=20)
    tekst = models.TextField()
    price = models.FloatField(default = 0.0)
    kolvo = models.IntegerField(default = 0)
    data_izm = models.DateTimeField(auto_now_add=True)
    reshenie_moderator = models.IntegerField(choices=POSITIONS, default=0)
    tekst_moderator = models.TextField(blank=True, null = True)
    data_moderator = models.DateTimeField(blank=True, null = True)
    images = models.ManyToManyField(Images, through='TovarsImages')
    category = models.ManyToManyField(Category, through='TovarsCategory')

    def create_tovar(self, nametov,tekst,price,kolvo,images,category):
        tovars = Tovars.objects.values_list("nametov", flat=True)
        if not tovars:
            tov1 = Tovars.objects.create(nametov=nametov,tekst=tekst,price=price,kolvo=kolvo,images=images)
            tov1.save()
        for tov in tovars:
            if nametov == tov:
                return 'такой товар уже есть'
            else:
                Tovars.objects.create(nametov=nametov,tekst=tekst,price=price,kolvo=kolvo,images=images)

    # from dbapp.models import *
    # from datetime import datetime, time, timezone
    # Tovars.create_tovar('товар1', 'ghgf', 10.0, 5, None, None)

    def upd_data_izm(self):
        tovar = Tovars.objects.get(id = self.id)
        tovar.data_izm = datetime.now(timezone.utc).strftime ("%Y-%m-%d %H:%M:%S%z")
        tovar.save()

    def upd_data_moderator(self):
        tovar = Tovars.objects.get(id = self.id)
        tovar.data_moderator = datetime.now(timezone.utc).strftime ("%Y-%m-%d %H:%M:%S%z")
        tovar.save()

    class Meta:
        verbose_name = "Tovars"
        verbose_name_plural = "Tovars"

    def __str__(self):
        return f'{self.nametov} остаток:{self.kolvo} шт'

    def get_absolute_url(self):
        # = 'tovars_detail'
        #return reverse(x, args=[str(self.id)])
        return reverse('tovars')


class TovarsImages(models.Model):
    tovars = models.ForeignKey(Tovars, on_delete=models.CASCADE)
    images = models.ForeignKey(Images, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "TovarsImages"
        verbose_name_plural = "TovarsImages"
    def __str__(self):
        #x = format_html('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return f'{self.tovars} {self.images}'


class TovarsCategory(models.Model):
    tovars = models.ForeignKey(Tovars, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "TovarsCategory"
        verbose_name_plural = "TovarsCategory"

    def __str__(self):
        return f'{self.category} - {self.tovars}'


class Klient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kolvo = models.IntegerField(default = 0)
    summa = models.FloatField(default = 0.0)
    data_oplati = models.DateTimeField(blank=True, null = True)
    tovars = models.ManyToManyField(Tovars, through='KlientTovars')

    def oplatit(self):
        klient = Klient.objects.get(id = self.id)
        if klient.data_oplati is not None:
            klient.data_oplati = datetime.now(timezone.utc).strftime ("%Y-%m-%d %H:%M:%S%z")
            klient.save()
        else:
            return "товар уже оплачен"

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klient"

    def __str__(self):
        if self.data_oplati is not None:
            oplaceno = f'от {self.data_oplati.strftime("%d.%m.%Y")}'
        else:
            oplaceno = 'не оплачено'
        return f'{self.user} итого:{self.summa} {oplaceno}'

class KlientTovars(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    tovars = models.ForeignKey(Tovars, on_delete=models.CASCADE)
    kolvo = models.IntegerField(default = 0)
#добавить предупреждение о невозможности добавить убрать товар
    def add_kolvo_tovar(self):
        tovar = Tovars.objects.get(id = self.tovars.id)
        klient = Klient.objects.get(id = self.klient.id)
        if tovar.reshenie_moderator == 1 and tovar.kolvo >=1 and klient.data_oplati is not None:
            self.kolvo += 1
            tovar.kolvo -= 1
            klient.kolvo +=1
            klient.summa +=tovar.price
            tovar.save()
            klient.save()
            self.save()
        else:
            error1 = 'модератор_не_одобрил' if tovar.reshenie_moderator != 1 else ''
            error2 = 'товара_нет' if tovar.kolvo <= 0 else ''
            error3 = 'уже_оплачено' if klient.data_oplati is None else ''
            return f'{error1} {error2} {error3}'

    def ubrat_kolvo_tovar(self):
        tovar = Tovars.objects.get(id = self.tovars.id)
        klient = Klient.objects.get(id=self.klient.id)
        if tovar.reshenie_moderator == 1 and self.kolvo >=1 and klient.data_oplati is not None:
            self.kolvo -= 1
            tovar.kolvo += 1
            klient.kolvo -= 1
            klient.summa -= tovar.price
            tovar.save()
            klient.save()
            self.save()

    class Meta:
        verbose_name = "KlientTovars"
        verbose_name_plural = "KlientTovars"

    def __str__(self):
        return f'{self.klient} "{self.tovars}" {self.kolvo} шт в корзине'

#from dbapp.models import *
#from datetime import datetime, time, timezone
#k1 = Klient.objects.get(id = 1)   #vasja итого:0.0 от 2024-02-18 21:55:45+00:00
#t1 = Tovars.objects.get(id = 1)   #Tovars object (1)
#kt1 = KlientTovars.objects.create(klient=k1, tovars=t1)
#kt1.add_kolvo_tovar()
#
#kt1 = KlientTovars.objects.get(id=6)
#kt1.add_kolvo_tovar()
#kt1.ubrat_kolvo_tovar()
#
#Tovars.objects.filter(reshenie_moderator=1)&Tovars.objects.filter(kolvo__gt=0)
#Tovars.objects.filter(kolvo__gt=0)



