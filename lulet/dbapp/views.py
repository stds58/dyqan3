from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView )
from .models import Images, Category, Tovars, TovarsImages, TovarsCategory, Klient, KlientTovars
from .filters import TovarsFilter
from .forms import TovarsForm, ImagesForm
from django.conf import settings
import os


class TovarsList(ListView):
    model = Tovars
    qyeryset = Tovars.objects.filter(price__lt=300).order_by('-data_izm')
    template_name = 'tovars.html'
    context_object_name = 'tovars'
    paginate_by = 2


class TovarsDetail(DetailView):
    model = Tovars
    template_name = 'tovar.html'
    context_object_name = 'tovar'


class TovarsListSearch(ListView):
    model = Tovars
    queryset = Tovars.objects.filter(reshenie_moderator=1).order_by('-data_izm')
    template_name = 'tovars_search.html'
    context_object_name = 'tovars_search'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = TovarsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryList(ListView):
    model = Category
    ordering = 'namecat'
    template_name = 'categories.html'
    context_object_name = 'category_list'
    paginate_by = 10


class TovarCreate(CreateView):
    form_class = TovarsForm
    model = Tovars
    template_name = 'tovar_edit.html'



class TovarUpdate(UpdateView):
    form_class = TovarsForm
    model = Tovars
    template_name = 'tovar_edit.html'

class TovarDelete(DeleteView):
    model = Tovars
    template_name = 'tovar_delete.html'
    success_url = reverse_lazy('tovars')


class ImageCreate(CreateView):
    form_class = ImagesForm
    model = Images
    template_name = 'images_edit.html'
    success_url = reverse_lazy('images_edit')


def image_upload_view(request):
    if request.method == 'POST':
        form = ImagesForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                nov = Images.objects.create(image=f)
                f1 = f'{settings.BASE_DIR}{settings.MEDIA_URL}{nov.image}'.replace('\\', '/')
                DEL = []
                IDDEL = []
                images = Images.objects.all().exclude(id=nov.id)
                for img in images:
                    f2 = f'{settings.BASE_DIR}{settings.MEDIA_URL}{img.image}'.replace('\\', '/')
                    if form.get_hash_md5(f1) == form.get_hash_md5(f2):
                        DEL.append(f1)
                        IDDEL.append(nov.id)
                form.delete_file(DEL)
                for id in IDDEL:
                    Images.objects.filter(id=id).delete()
            return render(request, 'downloadimage.html', {'form': form, 'img_obj': f})
    else:
        form = ImagesForm()
    return render(request, 'downloadimage.html', {'form': form})

def image_detail_view(request, pk):
    image = get_object_or_404(Images, pk=pk)
    return render(request, 'image_detail.html', {'image': image})