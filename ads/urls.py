from django.urls import path

from ads.views import ad as ad_view
from ads.views import category as cat_view


urlpatterns = [
    path('', ad_view.index, name='home'),
    path('ad/', ad_view.AdListView.as_view()),
    path('ad/<int:pk>/', ad_view.AdDetailView.as_view()),
    path('ad/create/', ad_view.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ad_view.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', ad_view.AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', ad_view.AdImageView.as_view()),
    path('cat/', cat_view.CategoryListView.as_view()),
    path('cat/<int:pk>/', cat_view.CategoryDetailView.as_view()),
    path('cat/<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),
    path('cat/<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('cat/create/', cat_view.CategoryCreateView.as_view()),
]