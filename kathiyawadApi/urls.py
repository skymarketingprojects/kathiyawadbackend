
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # Product List/Search: /products/ and /products/search?querys=...
    path('products/', views.productsListView, name='product-list-search'),
    path('products/home/', views.productForHomeView, name='product-list-search'),
    
    # Product Detail: /products/<productId>/
    path('products/<int:productId>/', views.productDetailView, name='product-detail'),
    
    # Blog List: /blogs/
    path('blogs/', views.blogsListView, name='blog-list'),
    
    # Blog Filter by Category: /blogs/search/<categoryId>/
    path('blogs/search/<int:categoryId>/', views.blogsSearchByCategoryView, name='blog-search-category'),
    
    # Blog Detail: /blog/<blogId>/
    path('blogs/<int:blogId>/', views.blogDetailView, name='blog-detail'),
    
    # Hero Images: /hero-images/
    path('stock/hero/', views.heroImagesView, name='hero-images'),
]
