from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput
# from db.models import *
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField


# Form class for create myuser
class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=_('New password'), widget=PasswordInput(attrs={'class': 'uk-input uk-input uk-width-5-6'}))
    password2 = forms.CharField(label=_('New password confirmation'), widget=PasswordInput(attrs={'class': 'uk-input uk-input uk-width-5-6'}))
    captcha = CaptchaField(label='验证码', error_messages={"invalid": "Verification code error"})

    class Meta:
        # model = MyUser
        model = get_user_model()
        # fields = ['username', 'first_name', 'last_name', 'mbu_email']
        fields = ['username', 'mbu_email']
        labels = {
            # 'password1': _('New password:'),
            # 'password2': _('Confirm password:'),
            'mbu_email': _('Email'),
            'mbu_avatar': _('Avatar'),
        }
        help_texts = {
            'username': _('Your login account name.'),
            # 'first_name': _('Your first name.'),
            # 'last_name': _('Your last name'),
            'mbu_email': _('E-mail address'),
        }
        error_messages = {
            'username': {
                'max_length': _("This writer's name is too long."),
            },
        }
        widgets = {
            'username': TextInput(attrs={'class': 'uk-input uk-width-5-6', 'placeholder': ''}),
            # 'first_name': TextInput(attrs={'class': 'uk-input uk-form-width-medium', 'placeholder': ''}),
            # 'last_name': TextInput(attrs={'class': 'uk-input uk-form-width-medium', 'placeholder': ''}),
            'mbu_email': TextInput(attrs={'class': 'uk-input uk-input uk-width-5-6', 'placeholder': ''}),
        }


'''
	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords is/are empty, or don't match!")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		#user.set_password(self.cleaned_data["password1"])
		user.set_password(self.clean_password2())
		if commit:
			user.save()
		return user
'''
