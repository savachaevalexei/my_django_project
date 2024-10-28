import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import ForeignLanguagesList


# Форма авторизации
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# Форма регистрации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
 

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
 

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
    


# Форма редактирования профиля
class EditProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(label='Дата рождения',widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))
    foreign_languages = forms.ModelMultipleChoiceField(
        queryset=ForeignLanguagesList.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    def __init__(self, *args, **kwargs):
        super(EditProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['foreign_languages'].required = False


    class Meta:
        model = get_user_model()

        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name', 'specialization',  
                  'country_of_residence', 'city_of_residence', 'website', 'github', 'education', 
                  'employment_status', 'place_of_work', 'work_experience', 'courses', 'skills', 'about_me',
                  'hobby', 'publications', 'foreign_languages',
                  ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name' : forms.TextInput(attrs={'class': 'form-input'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-input'}),
            'specialization' : forms.TextInput(attrs={'class': 'form-input'}),
            'country_of_residence' : forms.TextInput(attrs={'class': 'form-input'}),
            'city_of_residence' : forms.TextInput(attrs={'class': 'form-input'}),
            'website' : forms.TextInput(attrs={'class': 'form-input'}),
            'github' : forms.TextInput(attrs={'class': 'form-input'}),
            'education' : forms.TextInput(attrs={'class': 'form-input'}),
            'employment_status' : forms.Select(attrs={'class': 'form-input'}),
            'place_of_work' : forms.TextInput(attrs={'class': 'form-input'}),
            'skills' : forms.TextInput(attrs={'class': 'form-input'}),
            'hobby' : forms.TextInput(attrs={'class': 'form-input'}),
        }


# Форма смены пароля
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))