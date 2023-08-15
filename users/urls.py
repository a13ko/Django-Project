from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("change-password/", views.password_change_view, name="change-password"),
    path("reset/", views.reset_password_view, name="reset"),
    path("reset-complete/<slug>/", views.reset_password_complete_view, name="reset-complete"),
    path("activate/<slug>/", views.account_activate_view, name="activate"),
    path("before-reset/",views.before_reset, name="before-reset"),
    path("privacy/",views.show_privacy, name="privacy"),
    path("profile/",views.profile, name="profile"),
    path("plan/",views.plan, name="plan"),
    path("faq/",views.faq, name="faq"),
    path("checkout/",views.checkout, name="checkout")
]