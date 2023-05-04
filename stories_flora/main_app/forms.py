from .models import Stories, Stories_i18n, Pages, Languages, Categories, Categories_i18n
from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, NumberInput, ImageField, forms, EmailInput, \
    PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class StoriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select..."

    class Meta:
        model = Stories  # table
        # fields = ['id', 'category', 'hide_in_stories', 'post_priority', 'fresh_after', 'fresh_before',
        #           'geolocations', 'clients_eligible', 'deleted']  # столбцы fields = '__all__'
        fields = '__all__'
        # characteristics for each column
        widgets = {
            "category": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Category id'
            }),
            "post_priority": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fresh before date'
            }),
            "fresh_after": DateInput(attrs={
                'class': 'form-control',
                'type': "date",
                'placeholder': 'dd-mm-yyyy'
            }),
            "fresh_before": DateInput(attrs={
                'class': 'form-control',
                'type': "date",
                'placeholder': 'Fresh before date'
            }),
            "geolocations": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Geolocations'
            }),

            "clients_eligible": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Clients eligible'
            })
        }


class Stories_i18nForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['story'].empty_label = "Select..."
        self.fields['language'].empty_label = "Select..."

    class Meta:
        model = Stories_i18n
        fields = ['story', 'language', 'title_icon', 'title_image', 'title', 'subtitle']
        widgets = {
            "story": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Story id'
            }),
            "language": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Language id'
            }),
            "title": Textarea(attrs={
                'class': 'form-control',

                'placeholder': 'Title'
            }),
            "subtitle": Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Subtitle'
            })
            # "title_icon": ImageField(attrs={
            #     'class': 'form-control'
            #
            # }),
            # "title_image": ImageField(attrs={
            #     'class': 'form-control'
            #
            # })
        }


class PagesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['story_i18n'].empty_label = "Select..."

    class Meta:
        model = Pages
        fields = ['story_i18n', 'mark_deleted', 'order', 'image', 'icon', 'headline', 'text']
        widgets = {
            "story_i18n": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Story_i18n id'
            }),
            # "image": ImageField(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Image'
            # }),
            # "icon": ImageField(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Icon'
            # }),
            "headline": Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Headline'
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'rows': 16,
                'placeholder': 'Text'
            }),
            "order": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Order'
            }),
        }


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'})

    class Meta:
        model = User  # table(model) auth_user
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})


# class LanguagesForm(ModelForm):
#     class Meta:
#         model = Languages  # table
#        # fields = '__all__'  # 'language'
#         fields = ['language']
#         widgets = {
#             "language": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Language'
#             })
#         }
#
