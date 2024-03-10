from django.urls import path
from .views import TovarsList, TovarsListSearch, CategoryList, TovarCreate, TovarUpdate, TovarDelete, TovarsDetail, ImageCreate, image_upload_view, image_detail_view

urlpatterns = [
   path('tovars/', TovarsList.as_view(), name= 'tovars'),
   path('tovars/search/', TovarsListSearch.as_view(), name= 'tovars_search'),
   path('categories/<int:pk>/', CategoryList.as_view(), name= 'category_list'),
   path('tovars/edit/<int:pk>/', TovarUpdate.as_view(), name='tovar_update'),
   path('tovars/delete/<int:pk>/', TovarDelete.as_view(), name='tovar_delete'),
   path('tovars/create/', TovarCreate.as_view(), name='tovar_create'),
   path('tovars/<int:pk>/', TovarsDetail.as_view(), name= 'tovars_detail'),
   path('images/create/', ImageCreate.as_view(), name= 'images_edit'),
   path('upload/', image_upload_view),
   path('images/<int:pk>/', image_detail_view, name= 'image_detail'),

]