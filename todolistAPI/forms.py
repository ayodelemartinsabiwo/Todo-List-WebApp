from django import forms
from django.contrib.auth import authenticate
from .models import TodoItem, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data


class TodoItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'description'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title'}))


    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'date'}),
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['avatar']
