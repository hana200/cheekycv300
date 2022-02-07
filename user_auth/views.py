from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.conf import settings
import os

from django.views.generic import  DetailView, CreateView, UpdateView, DeleteView


from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy
from .forms import SignUpForm, PasswordChangingForm, EditPForm, ProfilePageForm
#from .forms import SignUpForm, EditPForm, PasswordChangingForm, ProfilePageForm
from app.models import PImg, CV

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import  PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def model_check(x,model):
    user = x.user
    img_p = 0
    try :
        img = model.objects.get(user = user)
        #img_url = img.image.url
        img_p = 1
    except:
        img_p = 0   
    return img_p
#-------------------------------------------------

def password_reset_req(request):
	user_r = request.user.username
	if request.method == 'POST':
		password_form = PasswordResetForm(request.POST)
		if password_form.is_valid():
			data= password_form.cleaned_data['email']
			user_email = User.objects.filter(Q(email = data))
			if user_email.exists:
				for user in user_email:
					subject = 'Password Reset Request | CHEEKY CV'
					email_template_name = '../templates/registration/reset/password_message.txt'
					parameters = {
					'email': user.email,
					'domain': '127.0.0.1:8000',
					'site_name': 'CHEEKY CV',
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol':'http',
				}
				email = render_to_string(email_template_name, parameters)
				try:
					send_mail(subject,email,'',[user.email],fail_silently = False)
				except:
					return HttpResponse('Invalid Header')
				return redirect('password_reset_done')
	else:
		password_form = PasswordResetForm()
	
	context={
		'password_form': password_form, 
		'user_r': user_r
	}
	return render(request, 'registration/reset/password_reset_req.html', context)


class UserRegisterView(CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')
	# def saveIMG(self,form):
	# 	if form.is_valid():
	# 		user = form.instance.username
	# 		image = "https://previews.123rf.com/images/subbotina/subbotina1405/subbotina140500010/28119033-beautiful-face-of-teen-girl-with-clean-fresh-skin.jpg"
	# 		add_db = PImg(user = user,image = image)
	# 		add_db(save)


class PasswordsChangeView(PasswordChangeView):
	#form_class = PasswordChangeForm
	form_class = PasswordChangingForm
	success_url = reverse_lazy('success')

	def get_context_data(self, *args, **kwargs):
		context = super( PasswordsChangeView, self).get_context_data(*args, **kwargs)
		#----repeat
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p

		if self.request.user.is_authenticated:
			user = self.request.user
			context["user_"] = user
			img_p = model_check(self.request,PImg)
			cv = model_check(self.request,CV)
			context["user"] = user
			context["cv_"] = cv
			cv_=1
			context["img_p"] = img_p
		#---------

		return context



def password_success(request):
	return render(request, 'registration/password_success.html', {})


class UserEditView(UpdateView):
	form_class = EditPForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_context_data(self, *args, **kwargs):
		context = super(UserEditView, self).get_context_data(*args, **kwargs)
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p
		if self.request.user.is_authenticated:
			try:
				user = self.request.user
				img_p = model_check(self.request,PImg)
				cv = model_check(self.request,CV)
				pimg = PImg.objects.get(id = self.kwargs['pk'])  
				context["cv_"] = cv
				context["img_p"] = img_p
				context["user_"] = user
				#----
				context["img"] = pimg.image.url
				context["exists"] = 1
			except: 
				context["exists"] = 0
		return context

	def get_object(self):
		return self.request.user

#-----------------profile image----------------------------------------------------


class ShowProfPageView(DetailView):
	model = PImg
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ShowProfPageView, self).get_context_data(*args, **kwargs)
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p
		if self.request.user.is_authenticated:
			try:
				user = self.request.user
				img_p = model_check(self.request,PImg)
				cv = model_check(self.request,CV)
				pimg = PImg.objects.get(id = self.kwargs['pk'])  
				pimg_user = pimg.user
				context["pimg_user"] = pimg_user
				context["cv_"] = cv
				context["img_p"] = img_p
				context["user_"] = user
				#----
				context["img"] = pimg.image.url
				context["exists"] = 1
			except: 
				context["exists"] = 0
		else:
			try:
				pimg = PImg.objects.get(id = self.kwargs['pk'])  
				context["img"] = pimg.image.url
				context["exists"] = 1
			except:
				context["exists"] = 0
		return context

class CreateProfilePageView(CreateView):
	model = PImg
	form_class = ProfilePageForm
	template_name = 'registration/create_profile_page.html'
	success_url = reverse_lazy('success')

	def get_context_data(self, *args, **kwargs):
		context = super(CreateProfilePageView, self).get_context_data(*args, **kwargs)
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p
		if self.request.user.is_authenticated:
			user = self.request.user
			context["user_"] = user
			img_p = model_check(self.request,PImg)
			cv = model_check(self.request,CV)
			context["cv_"] = cv
			context["img_p"] = img_p
		return context

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditProfPageView(UpdateView):
	model = PImg
	form_class = ProfilePageForm
	template_name = 'registration/edit_profile_page.html'
	fields = ['image',]
	success_url = reverse_lazy('success')
	'''
	def get_success_url(self):
		pk = self.kwargs["pk"]
		return reverse('edit_profile_page', kwargs={"pk": pk})
		'''

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfPageView, self).get_context_data(*args, **kwargs)
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p
		if self.request.user.is_authenticated:
			user = self.request.user
			context["user_"] = user
			img_p = model_check(self.request,PImg)
			cv = model_check(self.request,CV)
			pimg = PImg.objects.get(id = self.kwargs['pk'])  
			context["cv_"] = cv
			context["img_p"] = img_p
			context["img"] = pimg.image.url
		return context
	def form_valid(self,form):
		form.instance.user = self.request.user
		return super().form_valid(form)


def success(request):
	return render(request, 'success.html')

class DeleteProfPageView(DeleteView):
	model = PImg
	template_name = 'registration/delete_profile_page.html'
	fields = ['image',]
	success_url = reverse_lazy('success')

	def get_context_data(self, *args, **kwargs):
		context = super(DeleteProfPageView, self).get_context_data(*args, **kwargs)
		cv_=0
		img_p=0
		context["cv_"] = cv_
		context["img_p"] = img_p
		
		if self.request.user.is_authenticated:
			user = self.request.user
			context["user_"] = user
			img_p = model_check(self.request,PImg)
			cv = model_check(self.request,CV)
			context["cv_"] = cv
			context["img_p"] = img_p
			#pimg = PImg.objects.get(id = self.kwargs['pk'])
			#if self.object.exists():
				#success_url = self.get_success_url()

		return context

def delete_pic(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    try:      
        img = PImg.objects.get(id = pk)
        context['img'] = img
        if request.method == 'POST':
            img.delete()
            return redirect(reverse('success'))
    except:
        return redirect(reverse('error'))
    return render(request, "registration/delete_profile_page.html", context)