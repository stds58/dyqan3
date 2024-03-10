from django.contrib import admin
from .models import Images, Category, Tovars, TovarsImages, TovarsCategory, Klient, KlientTovars
from django.utils.html import format_html

@admin.register(Images)
class Images(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" alt="obj.image.id"/>'.format(obj.image.url))
        #return format_html('<img src="{}" width="100" height="100" alt="obj.image.id"/>', obj.image.url)
    image_tag.short_description = 'Image'
    list_display = ['image_tag',]

#admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Tovars)
admin.site.register(TovarsImages)
admin.site.register(TovarsCategory)
admin.site.register(Klient)
admin.site.register(KlientTovars)
