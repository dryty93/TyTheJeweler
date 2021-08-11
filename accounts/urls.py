
from django.urls import include, path
from . import views


from django.conf.urls import url
urlpatterns = [
    path("", include('django.contrib.auth.urls')),  # new

    path("/logout/",views.Logout.as_view(),name="logout"),
    path("login/",views.Logout.as_view(),name="login"),
    path("signup/",views.SignUp.as_view(),name="signup"),
    path("password_change/",views.PassChange.as_view(),name="password_change"),
    path("password_change/done/",views.PassChangeSuccess.as_view(),name="password_change_done"),
    path("password_reset/",views.PassReset.as_view(),name='password_reset'),
    path("password_reset/done/",views.PassResetDone.as_view(),name='password_reset_done'),
    path("reset/<uidb64>/<token>/",views.PassResetConfirm.as_view(),name='password_reset_confirm'),
    path("reset/done/",views.PassResetDone.as_view,name='password_reset_complete'),

]