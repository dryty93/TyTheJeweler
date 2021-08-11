from django.urls import include, path
from . import views
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls import url

urlpatterns = [
    path('',views.index, name='home'),

    path('Products/',views.product_page, name='product_page'),
    path('Products/<int:product_id>/', views.det_view, name='det_view'),
    path('Products/Categories/<int:category_id>/', views.det_cat_view, name='det_cat_view'),
    path('Products/Categories/', views.category_page, name='category_page'),
    path('Products/Material/', views.MaterialList.as_view()),
    path('Products/Material/<pk>/', views.MaterialDetail.as_view()),
    # path('<int:aoi_id>/', views.one_aoi, name='one_aoi'),

    ]