from django.urls import path 

from . import views 

app_name="account"
urlpatterns = [ 
    path("login", views.UserLoginView.as_view(), name="login"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
    path("logout", views.UserLogout, name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("profile-update", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("change-passworld",views.PassswordChangeView.as_view(), name="password-change"),
]