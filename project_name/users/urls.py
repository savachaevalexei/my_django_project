from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView


app_name= "users"

urlpatterns = [
    # Авторизоваться
    path('login/', views.LoginUser.as_view(), name='login'),

    # Выйти
    path('logout/', LogoutView.as_view(), name='logout'),

    # Регистрация
    path('register/', views.RegisterUser.as_view(), name='register'),

    # Просмотр профиля любого пользователя
    path('view_profile/<int:pk>/', views.ViewProfileUser.as_view(), name='view_profile'),

    # Профайл
    path('profile/', views.ProfileUser.as_view(), name='profile'),

    # Редактирование профайла
    path('edit_profile/', views.EditProfileUser.as_view(), name='edit_profile'),

    # Смена пароля
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),

    # Восстановление пароля
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"), name='password_reset_done'),
    path('password-reset/', PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                                        email_template_name="users/password_reset_email.html",
                                                        success_url=reverse_lazy("users:password_reset_done")),name='password_reset'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                                        success_url=reverse_lazy("users:password_reset_complete")),name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),

]

