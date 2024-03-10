from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, DateFilter, NumberFilter
from .models import Images, Category, Tovars, TovarsImages, TovarsCategory, Klient, KlientTovars
from django import forms

class TovarsFilter(FilterSet):
   nametov = CharFilter(
      field_name='nametov',
      lookup_expr='contains',
      #queryset=Tovars.objects.filter(reshenie_moderator=1)&Tovars.objects.filter(kolvo__gt=0),
      label='nametov'
   )
   price__gte = NumberFilter(field_name='price', lookup_expr='gte', label='price >=') #queryset=Tovars.objects.filter(kolvo__gt=0),
   price__lte = NumberFilter(field_name='price', lookup_expr='lte', label='price <=') #queryset=Tovars.objects.filter(kolvo__gt=0),
   kolvo__gte = NumberFilter(field_name='kolvo', lookup_expr='gte', label='kolvo >=')
   kolvo__lte = NumberFilter(field_name='kolvo', lookup_expr='lte', label='kolvo <=')
   data_izm = DateFilter(
      field_name='data_izm',
      lookup_expr='gte',  # lookup_expr='lt',
      label='data_izm',
      widget=forms.DateInput(attrs={'type': 'date'})
   )
   category = ModelChoiceFilter(field_name='category', queryset=Category.objects.filter(tovars__kolvo__gt=0).distinct(),label='category')
   #cat = Category.objects.filter(tovars__kolvo__gt=0).values_list('tovars').distinct()
   #category = ModelChoiceFilter(field_name='category__namecat',queryset=Tovars.objects.filter(id__in=cat),label='category')
   #avtor =   ModelChoiceFilter(field_name='author__user', queryset=User.objects.all(), label='автор')

