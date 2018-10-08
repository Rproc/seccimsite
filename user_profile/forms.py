from django import forms


class UserRegistrationForm(forms.Form):

    name = forms.CharField(
        required=True,
        label='name',
        max_length=100,
    )
    email = forms.CharField(
        required=True,
        label='email',
    )
    schooling = forms.IntegerField(
        required=True,
        label='schooling',
    )
    password = forms.CharField(
        required=True,
        label='password',
        widget=forms.PasswordInput(),
    )
    confirmPassword = forms.CharField(
        required=True,
        label='confirmPassword',
        widget=forms.PasswordInput(),
    )
