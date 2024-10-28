from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, EditProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView 
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User
from articles.models import Article
from .utils import DataMixin



# Авторизация
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация',
                     'default_image': settings.DEFAULT_USER_IMAGE,}
 


# Регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация",
                     'default_image': settings.DEFAULT_USER_IMAGE,}
    success_url = reverse_lazy('users:login')


# Просмотр профиля любого пользователя
class ViewProfileUser(DataMixin, ListView):
    model = get_user_model()
    context_object_name = 'profile_data'
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE,
    }


    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])
    

# Просмотр личного профиля пользователя (своего профиля)
class ProfileUser(DataMixin, LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    context_object_name = 'profile_data'
    title_page = 'Вакансии'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            user_obj = User.objects.get(pk=self.request.user.pk)
            foreign_languages = user_obj.foreign_languages.all()
            
            return self.get_mixin_context(context, foreign_languages=foreign_languages)
        
        else:
            context = super().get_context_data(**kwargs)
            return self.get_mixin_context(context)

    
    def get_queryset(self):
        # !!!!!!!!!!!!!!!!!!ВРЕМЕННО!!!!!!!!!!
        return User.objects.filter(pk=self.request.user.id)


# Редактирование профиля пользователя
class EditProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EditProfileUserForm
    template_name = 'users/edit_profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}