from django.urls import path
from base.views.product_views import *

urlpatterns = [
path('', GetProducts.as_view(), name='products'),
path('create/', CreateProduct.as_view(), name='product_create'),
path('upload/', UploadImage.as_view(), name='image_upload'),
path('top/', GetTopProducts.as_view(), name='top_products'),
path('<int:pk>/', GetProductDetail.as_view(), name='product'),
path('<int:pk>/reviews/', CreateProductReview.as_view(), name='create_review'),
path('update/<int:pk>/', UpdateProduct.as_view(), name='product_update'),
path('delete/<int:pk>/', DeleteProduct.as_view(), name='product_delete'),
]