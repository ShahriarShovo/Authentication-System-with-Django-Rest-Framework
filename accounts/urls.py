
from django.urls import path
from accounts import views

urlpatterns = [
    
    path('signup/', views.Signup_user.as_view()),
    path('login/', views.User_login.as_view()),
    path('profile/', views.current_user),
    path('update-profile/<int:user_id>/', views.update_profile),
    path('change-password/', views.User_Change_Password.as_view()),
]
