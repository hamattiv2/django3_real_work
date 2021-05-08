from django import forms
from django.contrib.auth import get_user_model
from mysite.models import Profile, Prefecture


class UserCreateForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    prefecture = forms.ModelChoiceField(Prefecture.objects.all())
    class Meta:
        model = Profile
        fields = ['username', 'zipcode', 'prefecture', 'city', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'