from django.urls import path
from base.views.order_views import *

urlpatterns = [
path('', GetOrders.as_view(), name='orders'),
path('add/', AddOrderItems.as_view(), name='orders_add'),
path('myorders/', GetMyOrders.as_view(), name='myorders'),

path('<int:pk>/deliver/', UpdateOrderToDelivered.as_view(), name='order_delivered'),
path('<int:pk>/', GetOrderById.as_view(), name='user_order'),
path('<int:pk>/pay/', UpdateOrderToPaid.as_view(), name='pay'),
]