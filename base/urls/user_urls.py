from django.urls import path
from base.views.user_views import *

urlpatterns = [
path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('register/', RegisterUser.as_view(), name='register'),
path('profile/', GetUserProfile.as_view(), name='user_profile'),
path('profile/update/', UpdateUserProfile.as_view(), name='user_profile_update'),
path('', GetUsers.as_view(), name='users'),

path('<str:pk>/', GetUserById.as_view(), name='user'),
path('update/<str:pk>/', UpdateUser.as_view(), name='update_user'),

path('delete/<str:pk>/', DeleteUser.as_view(), name='delete_user'),
]