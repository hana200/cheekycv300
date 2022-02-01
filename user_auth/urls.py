from django.urls import path
from django.contrib.auth import views as auth_view

from .views import UserRegisterView, PasswordsChangeView, success, UserEditView, delete_pic, password_reset_req
from .views import ShowProfPageView, EditProfPageView, CreateProfilePageView
#from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfPageView, EditProfPageView, CreateProfilePageView

from . import views

urlpatterns = [
	
	path('register/', UserRegisterView.as_view(), name = 'register'),
	path('edit_profile/', UserEditView.as_view(), name = 'edit_profile'),
	#path('password/', auth_views.PasswordChangeViews.as_view(template_name = 'registration/change_password')),
	path('password/', PasswordsChangeView.as_view(template_name = 'registration/change_password.html'), name = "password_change"),
	path('password_success', views.password_success, name = "password_success"),
	path('<int:pk>/profile/', ShowProfPageView.as_view(), name = 'show_profile_page'),
	path('<int:pk>/edit_profile_page/', EditProfPageView.as_view(), name = 'edit_profile_page'),
	# path('<int:pk>/delete_profile_page/', DeleteProfPageView.as_view(), name = 'delete_profile_page'),
	path('create_profile_page/', CreateProfilePageView.as_view(), name = 'create_profile_page'),
	path('success/', success, name = 'success'),

	path('<int:pk>/delete_pic/', delete_pic, name = 'delete_pic'),

    	path('password_reset_req/',password_reset_req,name='password_reset_req'),
    	path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='registration/reset/password_reset_done.html'),
         name='password_reset_done'),
    	path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='registration/reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    	path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='registration/reset/password_reset_complete.html'),
         name='password_reset_complete'),

    # Forget Password
    path('password-reset/',
         auth_view.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_view.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_view.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
