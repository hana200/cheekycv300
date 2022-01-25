
from django.contrib.auth.forms import PasswordResetForm,UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from app.models import PImg
from typing import Final
from django.contrib.auth.tokens import default_token_generator 
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email...'}))
	
	class Meta:
		model = User
		fields = ('username', 'email','password1','password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'user name...'
			
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'password...'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'type the password again...'
	
	def clean(self):

		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		username_len=len(str(username))
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		err=[]


		if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
			# er1="Email and Username already registered, please try again!"
			# err.append(er1)
			raise ValidationError("Email and Username already registered, please try again!")
		elif User.objects.filter(email=email).exists():
			# er2="Email already registered, please try to log in!"
			# err.append(er2)
			raise ValidationError("Email already registered, please try to log in!")
		elif User.objects.filter(username=username).exists():
			# er3 = "Username already exists! Please select a different one"
			# err.append(er3)
			raise ValidationError("Username already exists! Please select a different one")
		elif username == 'admin':
			# er4 = "Not allowed! Please choose a different name"
			# err.append(er4)
			raise ValidationError("Not allowed! Please choose a different name")
		elif username_len<4:
			# er5 = "Username too short, please use 4 characters or more"	
			# err.append(er5)
			raise ValidationError("Username too short, please use 4 characters or more")
		


		return self.cleaned_data



class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password1 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
	new_password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

	class Meta:
		model = User
		fields = ('old_password', 'new_password1','new_password2')

class EditPForm(UserChangeForm):
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email...', 'type': 'hidden'}))
	username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email','password')
		

class ProfilePageForm(forms.ModelForm):
	class Meta: 
		model = PImg
		fields = ('image',)



