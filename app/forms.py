from django import forms
from .models import CV, Bio, Job, Edu, J_Role, J_Role_Cat
from .models import  Lang, Web, Intro, Skill1, Skill2
from django.utils.safestring import mark_safe
from datetime import datetime, date, time


def ch_y():
    return [(r,r) for r in range(1950, date.today().year+1)]

def current_m():
    return date.today().month

def current_y():
    return date.today().year

#------forms


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        exclude = ['user','color']
        widgets = {
        'title' : forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
        "title": "Title * ",}
class ColorForm(forms.ModelForm):
    class Meta:
        model = CV
        exclude = ['user','title']
        widgets = {
        'color' : forms.TextInput(attrs={'class': 'form-control','placeholder':'#e3e3e3'}),
        }
        labels = {
        "color": "Set New Color - use HEX form",}
#------------BIO FORMS--------------------------------------
class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        exclude = ['cv']
        widgets = {
        'name' : forms.TextInput(attrs={'class': 'form-control','placeholder':'John'}),
        'surname' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Smith'}),
        'email' : forms.TextInput(attrs={'class': 'form-control','placeholder':'mail@mail.com'}),
        'phone' : forms.TextInput(attrs={'class': 'form-control','placeholder':'+1 00 555 555'}),
        'location' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Amsterdam, NL'}),
		}

        labels = {  
        'name': 'Name * ',
         'surname': 'Surname * ',
         'email':'Email * ',
         'location': 'Location * ' 
         }

class LangForm(forms.ModelForm):
    class Meta:
        model = Lang
        fields = ('l1','l2','l3','l4','l5','l6','l7','l8','l9','l10')
        widgets = {
        'l1' : forms.TextInput(attrs={'class': 'form-control','placeholder':'English'}),
        'l2' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Spanish'}),
        'l3' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Mandarin'}),
        'l4' : forms.TextInput(attrs={'class': 'form-control','placeholder':'French'}),
        'l5' : forms.TextInput(attrs={'class': 'form-control','placeholder':'German'}),
        'l6' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Russian'}),
        'l7' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Portugese'}),
        'l8' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Arabic'}),
        'l9' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Italian'}),
        'l10' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Polish'}),
        }

        labels = {
        'l1' : "Language 1 * ",
        'l2' : "Language 2",
        'l3' : "Language 3",
        'l4' : "Language 4",
        'l5' : "Language 5",
        'l6' : "Language 6",
        'l7' : "Language 7",
        'l8' : "Language 8",
        'l9' : "Language 9",
        'l10' : "Language 10",
        }

class WebForm(forms.ModelForm):
    class Meta:
        model = Web
        fields = ('wl1','wl2','wl3','wl4')
        widgets = {
        'wl1' : forms.TextInput(attrs={'class': 'form-control','placeholder':'http://mywebsite.com'}),
        'wl2' : forms.TextInput(attrs={'class': 'form-control','placeholder':'http://mywebsite.com'}),
        'wl3' : forms.TextInput(attrs={'class': 'form-control','placeholder':'http://mywebsite.com'}),
        'wl4' : forms.TextInput(attrs={'class': 'form-control','placeholder':'http://mywebsite.com'}),
        }

        labels = {
        "wl1":"Linkedin", "wl2":"Pdf Link", "wl3":"Website 1", "wl4":"Website 2",
        }
class IntroForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = ('intro_text','outro_text')
        widgets = {
        'intro_text' : forms.Textarea(attrs={'class':'form-control','placeholder':'Something about me...'}),
        'outro_text' : forms.Textarea(attrs={'class':'form-control','placeholder':'When I am not working I am...'}),
        } 
        labels = {
        "intro_text": "Intro text * ", "outro_text": "Outro text",
        }

class Skill1Form(forms.ModelForm):
    class Meta:
        model = Skill1
        exclude = ['cv']
        widgets = {
        'skill_w1' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Team Management'}),
        }
        labels ={
        "skill_w1": "Skill 1 * ",
        }
        
        for x in range(2, 16):
            widgets["skill_w{0}".format(x)] = forms.TextInput(attrs={'class': 'form-control','placeholder':'Team Management'})
            labels["skill_w{0}".format(x)] = 'Skill ' + str(x) 
class Skill2Form(forms.ModelForm):
    class Meta:
        model = Skill2
        exclude = ['cv']
        widgets = {
        'skill_w1' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Microsoft Office'}),
        }
        labels ={
        "skill_w1": "Skill 1 * ",
        }
        for x in range(2, 16):
            widgets["skill_w{0}".format(x)] = forms.TextInput(attrs={'class': 'form-control','placeholder':'Microsoft Office'})
            labels["skill_w{0}".format(x)] = 'Skill ' + str(x)  +'*'      

#------------JOB FORMS--------------------------------------
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('job_o','job_ws','job_l','job_sdm','job_sdy','job_edm','job_edy')
        widgets = {
        'job_o' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Amazon'}),
        'job_ws' : forms.TextInput(attrs={'class': 'form-control','placeholder':'http://amazon.com'}),
        'job_l' : forms.TextInput(attrs={'class': 'form-control','placeholder':'London, UK'}),
        }

        labels = {
        "job_o": "Office Name * ",
        "job_ws": "Office Website",
        "job_l": "Office Location * ",

        "job_sdm": "Start Month ",
        "job_sdy": "Start Year * ",
        "job_edm": " End Month ",
        "job_edy": "End Year * ",
        }

class J_RoleForm(forms.ModelForm):
    class Meta:
        model = J_Role
        fields = ('role_r','role_l','role_d','role_sdm','role_sdy','role_edm','role_edy')
        widgets = {
        'role_r' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Project Manager'}),
        'role_l' : forms.TextInput(attrs={'class': 'form-control','placeholder':'London, UK'}),
        'role_d' : forms.Textarea(attrs={'class': 'form-control','placeholder': 'My role as a project manager involved...'}),
        }

        labels = {
        'role_r' : "Role * ",
        'role_l' : "Location",
        'role_d' : "description",

        'role_sdm' : "Start Month",
        'role_sdy' : "Start Year",
        'role_edm' : "End Month",
        'role_edy' : "End Year",
        }

class J_Role_CatForm(forms.ModelForm):
    class Meta:
        model = J_Role_Cat
        exclude = ['role','user','job']
        widgets ={}
        labels ={}
        for x in range(1, 21):
            widgets["cat_p{0}".format(x)] = forms.TextInput(attrs={'class': 'form-control','placeholder':'Project X'})
            if x==1:
                labels["cat_p{0}".format(x)] = 'Category Item ' + str(x)+' * '
            else:
                labels["cat_p{0}".format(x)] = 'Category Item ' + str(x)

#------------EDU FORMS--------------------------------------

class EduForm(forms.ModelForm):
    class Meta:
        model = Edu
        exclude = ['cv']
        widgets = {
        'edu_s' : forms.TextInput(attrs={'class': 'form-control','placeholder':'MIT, Department of Mathematics'}),
        'edu_d' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Master od Sciences'}),
        'edu_l' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Boston, MA'}),
    
        }
        labels = {
        "edu_s": "Educational Institution",
        "edu_d": "Degree",
        "edu_sdy": "Start Year",
        "edu_edy": "End Year",
        'edu_l' : "Location",
        }

#--related to add_img view ---------------
'''
class ImgForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['image',]

'''