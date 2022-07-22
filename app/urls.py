from django.contrib import admin
from django.urls import path
#------------------------------------------------------
from .views import home, error, error_deleted, pdf_, ask
from .views import cv_show, cv_show_edit
#ADD
from .views import add_bio, add_edu, add_job, add_jobrole, add_jobrolecat
from .views import add_lang, add_web, add_intro, add_skill1, add_skill2
#ADD ONLY
from .views import add_job_only, add_jobrole_only, add_jobrolecat_only, add_edu_only
from .views import add_lang_only, add_web_only, add_intro_only, add_skill1_only, add_skill2_only
#EDIT
from .views import edit_bio, edit_lang, edit_web, edit_skill1, edit_skill2, edit_intro
from .views import edit_job, edit_jobrole, edit_jobrolecat, edit_edu, edit_color
#DELETES
from .views import delete_lang, delete_web, delete_skill1, delete_skill2, delete_intro, delete_intro
from .views import delete_job, delete_edu, delete_cv, delete_jobrole, delete_jobrolecat
from user_auth.views import password_reset_req


#from .views import  add_jobrole_back, add_jobrolecat_back, add_job_back,add_edu_back, add_bio_back


urlpatterns = [
    path('', home, name='home'),
    path('pdf_',pdf_, name = 'pdf_'),
    path('ask/',ask, name = 'ask'),

    path('error', error, name='error'),
    path('error/', error_deleted, name='error_deleted'),

    path('cv/<str:pk>', cv_show ,name='cv_show'),
    path('cv_edit/<str:pk>', cv_show_edit ,name='cv_show_edit'),

    #ADD
    path('add_bio/<str:pk>', add_bio, name='add_bio'),
    path('add_lang/<str:pk>/<str:x>/<int:y>', add_lang, name='add_lang'),
    path('add_web/<str:pk>/<str:x>/<int:y>', add_web, name='add_web'),
    path('add_skill1/<str:pk>/<str:x>/<int:y>', add_skill1, name='add_skill1'),
    path('add_skill2/<str:pk>/<str:x>/<int:y>', add_skill2, name='add_skill2'),
    path('add_intro/<str:pk>/<str:x>/<int:y>', add_intro, name='add_intro'),

    path('add_job/<str:pk>/<str:x>/<int:y>', add_job, name='add_job'),
    path('add_job_r/<str:pk>/<str:x>/<int:y>', add_jobrole, name='add_jobrole'),
    path('add_jobb_r_c/<str:pk>/<str:x>/<int:y>', add_jobrolecat, name='add_jobrolecat'),

    path('add_edu/<str:pk>/<str:x>/<int:y>', add_edu, name='add_edu'),
    

    #ADD ONLY
    path('add_lang_/<str:pk>', add_lang_only, name='add_lang_only'),
    path('add_web_/<str:pk>', add_web_only, name='add_web_only'),
    path('add_skill1_/<str:pk>', add_skill1_only, name='add_skill1_only'),
    path('add_skill2_/<str:pk>', add_skill2_only, name='add_skill2_only'),
    path('add_intro_/<str:pk>', add_intro_only, name='add_intro_only'),

    path('add_job_/<str:pk>', add_job_only, name='add_job_only'),
    path('add_jr_/<str:pk>', add_jobrole_only, name='add_jobrole_only'),
    path('add_jrc_/<str:pk>', add_jobrolecat_only, name='add_jobrolecat_only'),

    path('add_edu_/<str:pk>', add_edu_only, name='add_edu_only'),

    #EDIT
    path('edit_color/<str:pk>', edit_color, name='edit_color'),
    path('edit_bio/<str:pk>', edit_bio, name='edit_bio'),
    path('edit_lang/<str:pk>', edit_lang, name='edit_lang'),
    path('edit_web/<str:pk>', edit_web, name='edit_web'),
    path('edit_skill1/<str:pk>', edit_skill1, name='edit_skill1'),
    path('edit_skill2/<str:pk>', edit_skill2, name='edit_skill2'),
    path('edit_intro/<str:pk>', edit_intro, name='edit_intro'),

    path('edit_job/<str:pk>', edit_job, name='edit_job'),
    path('edit_jr/<str:pk>', edit_jobrole, name='edit_jobrole'),
    path('edit_jrc/<str:pk>', edit_jobrolecat, name='edit_jobrolecat'),
    path('edit_edu/<str:pk>', edit_edu, name='edit_edu'),

    #DELETE
    path('delete_cv/<str:pk>', delete_cv, name='delete_cv'),
    path('delete_lang/<str:pk>', delete_lang, name='delete_lang'),
    path('delete_web/<str:pk>', delete_web, name='delete_web'),
    path('delete_skill1/<str:pk>', delete_skill1, name='delete_skill1'),
    path('delete_skill2/<str:pk>', delete_skill2, name='delete_skill2'),
    path('delete_intro/<str:pk>', delete_intro, name='delete_intro'),

    path('delete_j/<str:pk>', delete_job, name='delete_job'),
    path('delete_jr/<str:pk>', delete_jobrole, name='delete_jobrole'),
    path('delete_jrc/<str:pk>', delete_jobrolecat, name='delete_jobrolecat'),
    path('delete_edu/<str:pk>', delete_edu, name='delete_edu'),

    path('delete_intro/<str:pk>', delete_intro, name='delete_intro'),


   

]

'''    #ADD BACK
    
 
    path('add_jr_b/<str:pk>/<str:x>/<int:y>', add_jobrole_back, name='add_jobrole_back'),
    path('add_jrc_b/<str:pk>/<str:x>/<int:y>', add_jobrolecat_back, name='add_jobrolecat_back'),

    path('add_edu_b/<str:pk>/<str:x>/<int:y>', add_edu_back, name='add_edu_back'),
    path('add_bio_b/<str:pk>/<str:x>/<int:y>', add_bio_back, name='add_bio_back'),
'''