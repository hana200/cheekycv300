import os
from django.conf import settings
from django import forms
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse
import json
from django.core.exceptions import ValidationError

from django.http import HttpResponse, Http404, HttpRequest
from datetime import datetime, date, time
from django.db import IntegrityError

#PDF--------------

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#-----------------

from django.contrib.auth.models import User

from .models import   CV, Bio, Job, Edu,  PImg, J_Role, J_Role_Cat
from .models import  Lang, Web, Intro, Skill1, Skill2

from .forms import CVForm, BioForm, JobForm, EduForm, ColorForm
from .forms import J_RoleForm, J_Role_CatForm, LangForm, WebForm, IntroForm, Skill1Form, Skill2Form
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView




'''
print(review)  # Print so I can see in cmd prompt that something posts as it should
            try:
                review.save()
            except IntegrityError:
                return redirect('name-of-some-view')
'''

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

#------------VIEWSSSS--------------------------

def home(request):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    context["home"] = 1
    css_=os.path.join(settings.STATIC_ROOT, 'css')
    js_=os.path.join(settings.STATIC_ROOT, 'js')
    context["css_"] = css_
    context["js_"] = js_

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    img = PImg.objects.all()
    cvs = CV.objects.all()
    CVS=[]
    for cv in cvs:
        try:
            user_=cv.user
            img_ = PImg.objects.get(user = user_ )
            lista_=[cv,img_.image.url]
        except:
            lista_=[cv,0]
        CVS.append(lista_)
    # CVS.reverse()
    context['img'] = img
    context['CVS'] = CVS

    return render(request, 'home.html',context)
def error(request):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        user = request.user
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p      
    return render(request,'error.html', context)
def error_deleted(request):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        user = request.user
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    return render(request,'error_deleted.html', context)

#PDF -------------------

def pdf_(request):
    # create bytestream buffer
    buf = io.BytesIO()
    # create canvas
    c = canvas.Canvas(buf, pagesize = letter, bottomup = 0)
    c1 = canvas.Canvas(buf, pagesize = letter, bottomup = 0)
    #create text object
    textob = c.beginText()
    textob.setTextOrigin(50, 50)
    textob.setFont("Helvetica", 11)

    textob1 = c1.beginText()
    textob1.setTextOrigin(20, 50)
    textob1.setFont("Helvetica", 11)



    #add some line of text

   
    lines1 = [
        "Line aksknsknds adnad asd adjna sd 1",
        "Line aksknsknds adnad asd adjna sd 2",
        "Line aksknsknds adnad asd adjna sd 3",
        "Line aksknsknds adnad asd adjna sd 4",
        "Line aksknsknds adnad asd adjna sd 5",
    ]
   
    #designate the model:

    users = User.objects.all()
    cvs = CV.objects.all()

    lines=[]
    lines1=[]
    for user in users:
        lines.append(user.username)
        lines.append(user.email)
        k=0
        for cv in cvs:           
            tit=""
            if cv.user.username == user.username:
                k=1
                tit = cv.title
                lines.append("CV title: "+tit)

        if k==0:
            lines.append("No CV")
        lines.append("  ")

    #append lines as obj 

    for line in lines:
        textob.textLine(line)
    for line in lines1:
        textob1.textLine(line1)

    c.drawText(textob1)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True, filename = "MyCheekyCV.pdf")


#---------------- CV SHOW / SHOW EDIT

def cv_show(request, pk):
    context={}
    context["show"] = 1
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p



    user = User.objects.get(username = pk)
    user_req = request.user
    context["user_req"] = user_req
    context["user_"] = user
    try: 
        CV.objects.get(user = user)
        cv = get_object_or_404(CV, user = user)
        bio = get_object_or_404(Bio, cv = cv)   

        try:
           pic = PImg.objects.get(user = user)
           context["pic"] = pic.image.url
           context["pic_id"] = pic.id
        except:
            pass   
        try:
            lang = Lang.objects.get(cv = cv)
            context["lang"] = lang
        except:
            pass
        try:
           web = Web.objects.get(cv = cv)
           context["web"] = web
        except:
            pass
        try:
           skill1 = Skill1.objects.get(cv = cv)
           context["skill1"] = skill1
        except:
            pass
        try:
           skill2 = Skill2.objects.get(cv = cv)
           context["skill2"] = skill2
        except:
            pass
        try:
           intro = Intro.objects.get(cv = cv)
           context["intro"] = intro
        except:
            pass
         
        try:
            jobs = Job.objects.filter(cv = cv)
            roles = J_Role.objects.filter(user = user)
            edus = Edu.objects.filter(cv = cv)
            roles = []
            cats = []
            for job in jobs:
                role = J_Role.objects.filter(user = user,job = job)
                cats_=[]
                roles.append(role)
                for r in role:
                    c = J_Role_Cat.objects.filter(user = user,job = job, role = r)
                    cats_.append(c)
                cats.append(cats_)

                #--------
            zipp=[]

            for i in range(len(jobs)):
                job = jobs[i]
                r=[]
                c=[]
                for j in range(len(roles[i])):
                    role = roles[i][j]
                    c_=[]
                    for k in range(len(cats[i][j])):
                        cat = cats[i][j][k]
                        c_.append(cat)
                    c.append(c_)
                    r.append([role,c_])
                zipp.append([job,r])

        except:
            raise Http404

        if cv.color == None:
            cv.color = '#9e9e9e'

        context["color"] = cv.color
        context["cv"] = cv
        context["bio"] = bio

        context["jobs"] = jobs
        context["edus"] = edus
        context["jobs_num"] = len(jobs)
        context["edus_num"] = len(edus)

        context["zipp"] = zipp


    except:
            return redirect(reverse('error_deleted'))

    context["user_cv"] = user
    return render(request, 'cv/cv_show.html', context)

# try: 
#         bio = Bio.objects.get(id = pk)           
#         #bio = get_object_or_404(Bio, id = pk)
#         user=bio.cv.user

#         form_bio = BioForm(request.POST or None, instance = bio)

#         if request.method == 'POST':
#             if form_bio.is_valid():
#                 form_bio.save()
#                 return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
#             else:
#                 raise ValidationError([
#                     ('Error! Please try again.'),
#                 ])      

#         context["form_bio"] = form_bio
#         context["user_bio"] = user
#     except:
#         return redirect(reverse('error' ))

def cv_show_edit(request, pk):
    context={}
    context["show"] = 1
    context["show_edit"] = 1
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    user = User.objects.get(username = pk)
    user_req = request.user
    try: 
        CV.objects.get(user = user)
        cv = get_object_or_404(CV, user = user)
        bio = get_object_or_404(Bio, cv = cv)   

        try:
           pic = PImg.objects.get(user = user)
           context["pic"] = pic.image.url
        except:
            pass   
        try:
            lang = Lang.objects.get(cv = cv)
            context["lang"] = lang
        except:
            pass
        try:
           web = Web.objects.get(cv = cv)
           context["web"] = web
        except:
            pass
        try:
           skill1 = Skill1.objects.get(cv = cv)
           context["skill1"] = skill1
        except:
            pass
        try:
           skill2 = Skill2.objects.get(cv = cv)
           context["skill2"] = skill2
        except:
            pass
        try:
           intro = Intro.objects.get(cv = cv)
           context["intro"] = intro
        except:
            pass
         
        try:
            jobs = Job.objects.filter(cv = cv)
            roles = J_Role.objects.filter(user = user)
            edus = Edu.objects.filter(cv = cv)
            roles = []
            cats = []
            for job in jobs:
                role = J_Role.objects.filter(user = user,job = job)
                cats_=[]
                roles.append(role)
                for r in role:
                    c = J_Role_Cat.objects.filter(user = user,job = job, role = r)
                    cats_.append(c)
                cats.append(cats_)
            zipp=[]

            for i in range(len(jobs)):
                job = jobs[i]
                r=[]
                c=[]
                for j in range(len(roles[i])):
                    role = roles[i][j]
                    c_=[]
                    for k in range(len(cats[i][j])):
                        cat = cats[i][j][k]
                        c_.append(cat)
                    c.append(c_)
                    r.append([role,c_])
                zipp.append([job,r])

        except:
            raise Http404

        if cv.color == None:
            cv.color = '#9e9e9e'

        context["cv"] = cv
        context["color"] = cv.color
        context["bio"] = bio

        context["jobs"] = jobs
        context["edus"] = edus
        context["jobs_num"] = len(jobs)
        context["edus_num"] = len(edus)

        context["zipp"] = zipp

    except:
            return redirect(reverse('error_deleted'))

    context["user_cv"] = user
    return render(request, 'cv/cv_show_edit.html', context)

#--------------ADD----------------------------------------

# ADD BIO ------------------------------
def add_bio(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    user = User.objects.get(username = pk)

    if CV.objects.filter(user = user):
         return redirect(reverse('error' ))
    else:

        if request.method == 'POST': 
            cv_form = CVForm(request.POST)
            cv_form.instance.user = user      
            cv=cv_form.instance.id

            bio_form = BioForm(request.POST)
            bio_form.instance.cv = cv_form.instance 
                        
            if cv_form.is_valid() and bio_form.is_valid():
                cv_form.save()
                bio_form.save()
                idd=bio_form.instance.id
                cv=bio_form.instance.cv
                if request.POST.get("save_next"):
                    return redirect(reverse('add_lang' , kwargs={'pk':user,'x': 'bio', 'y':idd}))
                elif request.POST.get("save_home"):
                    return redirect(reverse('home'))
                
            else:
                return redirect(reverse('add_bio' , kwargs={'pk':pk})) 

        else:
            cv_form = CVForm()
            bio_form = BioForm()

        context["cv_form"] = cv_form
        context["bio_form"] = bio_form
        context["user_cv"] = user

    return render(request, 'cv/add/add_bio.html', context)
# ADD LANG -----------------------------
def add_lang(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    user = User.objects.get(username = pk)
    cv = CV.objects.get(user = user.id)
    if request.method == 'POST': 
        lang_form = LangForm(request.POST)
        lang_form.instance.cv = cv                        
        if lang_form.is_valid():
            lang_form.save()
            idd=lang_form.instance.id
            if request.POST.get("save_next"):
                return redirect(reverse('add_web' , kwargs={'pk':user,'x': 'lang', 'y':idd}))
            elif request.POST.get("save_home"):
                return redirect(reverse('home'))          
        else:
            return redirect(reverse('add_lang' , kwargs={'pk':pk})) 
    else:
        lang_form = LangForm()

    context["lang_form"] = lang_form
    context["lang_user"] = user
    return render(request, 'cv/add/add_lang.html', context)

# ADD WEB -------------------------------
def add_web(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    user = User.objects.get(username = pk)
    cv = CV.objects.get(user = user.id)

    if request.method == 'POST': 
        web_form = WebForm(request.POST)
        web_form.instance.cv = cv                        
        if web_form.is_valid():
            web_form.save()
            idd=web_form.instance.id
            if request.POST.get("save_next"):
                return redirect(reverse('add_skill1' , kwargs={'pk':user,'x': 'web', 'y':idd}))
            elif request.POST.get("save_home"):
                return redirect(reverse('home'))          
        else:
            return redirect(reverse('add_web' , kwargs={'pk':pk})) 
    else:
        web_form = WebForm()

    context["web_form"] = web_form
    context["web_user"] = user
    return render(request, 'cv/add/add_web.html', context)  

# ADD SKILL ------------------------------
def add_skill1(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    user = User.objects.get(username = pk)
    cv = CV.objects.get(user = user.id)

    if request.method == 'POST': 
        skill_form = Skill1Form(request.POST)
        skill_form.instance.cv = cv                        
        if skill_form.is_valid():
            skill_form.save()
            idd=skill_form.instance.id
            if request.POST.get("save_next"):
                return redirect(reverse('add_skill2' , kwargs={'pk':user,'x': 'skill', 'y':idd}))
            elif request.POST.get("save_home"):
                return redirect(reverse('home'))          
        else:
            return redirect(reverse('add_skill1' , kwargs={'pk':pk})) 
    else:
        skill_form = Skill1Form()

    context["skill_form"] = skill_form
    context["skill_user"] = user 
    return render(request, 'cv/add/add_skill1.html', context)  

def add_skill2(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    user = User.objects.get(username = pk)
    cv = CV.objects.get(user = user.id)

    if request.method == 'POST': 
        skill_form = Skill2Form(request.POST)
        skill_form.instance.cv = cv                        
        if skill_form.is_valid():
            skill_form.save()
            idd=skill_form.instance.id
            if request.POST.get("save_next"):
                return redirect(reverse('add_intro' , kwargs={'pk':user,'x': 'skill', 'y':idd}))
            elif request.POST.get("save_home"):
                return redirect(reverse('home'))          
        else:
            return redirect(reverse('add_skill2' , kwargs={'pk':pk})) 
    else:
        skill_form = Skill2Form()

    context["skill_form"] = skill_form
    context["skill_user"] = user 
    return render(request, 'cv/add/add_skill2.html', context)  

# ADD INTRO -------------------------------
def add_intro(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    
    user = User.objects.get(username = pk)
    cv = CV.objects.get(user = user.id)

    if request.method == 'POST': 
        intro_form = IntroForm(request.POST)
        intro_form.instance.cv = cv                        
        if intro_form.is_valid():
            intro_form.save()
            idd=intro_form.instance.id
            if request.POST.get("save_next"):
                return redirect(reverse('add_job' , kwargs={'pk':user,'x': 'intro', 'y':idd}))
            elif request.POST.get("save_home"):
                return redirect(reverse('home'))          
        else:
            return redirect(reverse('add_intro' , kwargs={'pk':pk})) 
    else:
        intro_form = IntroForm()

    context["intro_form"] = intro_form
    context["intro_user"] = user 
    return render(request, 'cv/add/add_intro.html', context)  
    
# ADD JOB ---------------------------------

def add_job(request,pk,x,y):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p       

        if x == "intro":
            user = User.objects.get(username = pk)
            cv = CV.objects.get(user = user.id)

        elif x == "cat":
            cat = J_Role_Cat.objects.get(id = y)
            cv = cat.job.cv
            user = cat.user
        elif x == "role":
            role = J_Role.objects.get(id = y)
            cv = role.job.cv
            user = role.user

        job_form = JobForm(request.POST or None)

        if request.method == 'POST':
            job_form = JobForm(request.POST)
            job_form.instance.cv = cv         
            if job_form.is_valid():
                job_form.save()
                idd=job_form.instance.id          
                if request.POST.get("save_next"):               
                    return redirect(reverse('add_jobrole' , kwargs={'pk':y,'x': 'job', 'y':idd}))
                elif request.POST.get("save_home"):
                        return redirect(reverse('home'))
                elif request.POST.get("back"):                
                    if x=='bio':                
                        return redirect(reverse('add_bio_back' ,  kwargs={'pk':y,'x':'job','y':idd})) 
                    elif x == 'cat':
                        return redireSct(reverse('add_jobrolecat_back' ,  kwargs={'pk':y,'x':'job','y':idd})) 
            else:
                #back to myself
                return redirect(reverse('add_job' , kwargs={'pk':pk,'x': x, 'y':y}))           
        else:
            job_form = JobForm()

    context["job_form"] = job_form
    context["user_job"] = user

    return render(request, 'cv/add/add_job.html', context)

def add_jobrole(request,pk,x,y):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        try:
            # pk = y
            job = Job.objects.get(id = y)
            cv = job.cv
            user = cv.user

            jrole_form = J_RoleForm(request.POST or None)

            if request.method == 'POST': 
                jrole_form = J_RoleForm(request.POST)
                jrole_form.instance.user = user
                jrole_form.instance.job = job        
                if jrole_form.is_valid():
                    jrole_form.save()
                    idd=jrole_form.instance.id
                    if request.POST.get("save_next"):
                        return redirect(reverse('add_jobrolecat' , kwargs={'pk':y,'x': 'role', 'y':idd}))
                    elif request.POST.get("add_job"):
                        return redirect(reverse('add_job' , kwargs={'pk':y,'x': 'role', 'y':idd}))
                    elif request.POST.get("add_edu"):
                        return redirect(reverse('add_edu' , kwargs={'pk':y,'x': 'role', 'y':idd}))
                    elif request.POST.get("save_home"):
                        return redirect(reverse('home'))
                    elif request.POST.get("back"):              
                        return redirect(reverse('add_job_back' ,  kwargs={'pk':y,'x':'role','y':idd}))
                else:
                    #back to myself
                    return redirect(reverse('add_jobrole' , kwargs={'pk':pk,'x': x, 'y':y}))
        except:
            return redirect(reverse('error' ))

    else:
        jrole_form = J_RoleForm()

    context["jrole_form"] = jrole_form
    context["user_jrole"] = user
    return render(request, 'cv/add/add_jobrole.html', context)

def add_jobrolecat(request,pk,x,y):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        try:
            # pk = y

            role = J_Role.objects.get(id = y)
            job = role.job
            user = role.user

            jrolecat_form = J_Role_CatForm(request.POST or None)
            # pk = user
            '''
            role = J_Role.objects.get(id = y)
            user = User.objects.get(username = pk)           
            '''
            if request.method == 'POST': 
                jrolecat_form = J_Role_CatForm(request.POST)
                jrolecat_form.instance.role = role
                jrolecat_form.instance.user = user
                jrolecat_form.instance.job = job
                if jrolecat_form.is_valid():
                    jrolecat_form.save()
                    idd=jrolecat_form.instance.id
                    if request.POST.get("save_next"):
                        return redirect(reverse('add_edu' , kwargs={'pk':y,'x': 'cat', 'y':idd}))
                    elif request.POST.get("add_job"):
                        return redirect(reverse('add_job' , kwargs={'pk':y,'x': 'cat', 'y':idd}))
                    if request.POST.get("add_jobrolecat"):
                        return redirect(reverse('add_jobrolecat' , kwargs={'pk':pk,'x': 'cat', 'y':y}))
                    elif request.POST.get("back"):              
                        return redirect(reverse('add_jobrole_back' ,  kwargs={'pk':y,'x':'cat','y':idd}))
                    elif request.POST.get("save_home"):
                        return redirect(reverse('home'))
                else:
                    #back to myself
                    return redirect(reverse('add_jobrolecat' , kwargs={'pk':pk,'x': x, 'y':y}))
        except:
            return redirect(reverse('error' ))

            
    else:
        jrolecat_form = J_Role_CatForm()

    context["jrolecat_form"] = jrolecat_form
    context["user_jrolecat"] = user
    return render(request, 'cv/add/add_jobrolecat.html', context)
# ADD EDU -----------------------------------

def add_edu(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        if x == 'cat':
            cat = J_Role_Cat.objects.get(id = y)
            user = cat.user
            cv = CV.objects.get(user = user)
        elif x == 'edu':
            edu = Edu.objects.get(id = y)
            cv = edu.cv
            user = cv.user
        elif x == 'role':
            role = J_Role.objects.get(id = y)
            cv = role.job.cv
            user = role.user

        edu_form = EduForm(request.POST or None)

        if request.method == 'POST': 
            edu_form = EduForm(request.POST)
            edu_form.instance.cv = cv         
            if edu_form.is_valid():
                edu_form.save()
                idd = edu_form.instance.id
                if request.POST.get("add_edu"): 
                     return redirect(reverse('add_edu' , kwargs={'pk':y,'x': 'edu', 'y':idd}))
                elif request.POST.get("save_next"):
                    return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
                elif request.POST.get("save_home"):
                    return redirect(reverse('home'))
                elif request.POST.get("back"):
                    if x=='edu':                
                        return redirect(reverse('add_edu_back' ,  kwargs={'pk':y,'x':'edu','y':idd})) 
                    elif x == 'job':
                        return redirect(reverse('add_job_back' ,  kwargs={'pk':y,'x':'edu','y':idd}))
            else:
                #back to myself
                return redirect(reverse('add_job' , kwargs={'pk':pk,'x': x, 'y':y}))
        else:
            edu_form = EduForm()

    context["edu_form"] = edu_form
    context["user_edu"] = user
    return render(request, 'cv/add/add_edu.html', context)

# ADD_ONLY ---------------------------------------------------------------

def add_lang_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                lang_form = LangForm(request.POST)
                lang_form.instance.cv = cv         
                if lang_form.is_valid():
                    lang_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            lang_form = LangForm()

        context["lang_form"] = lang_form
        context["lang_user"] = user

    return render(request, 'cv/add_only/add_lang_only.html', context) 

def add_web_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                web_form = WebForm(request.POST)
                web_form.instance.cv = cv         
                if web_form.is_valid():
                    web_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            web_form = WebForm()

        context["web_form"] = web_form
        context["web_user"] = user

    return render(request, 'cv/add_only/add_web_only.html', context) 

def add_intro_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                intro_form = IntroForm(request.POST)
                intro_form.instance.cv = cv         
                if intro_form.is_valid():
                    intro_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            intro_form = IntroForm()

        context["intro_form"] = intro_form
        context["intro_user"] = user

    return render(request, 'cv/add_only/add_intro_only.html', context) 

def add_skill1_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                skill1_form = Skill1Form(request.POST)
                skill1_form.instance.cv = cv         
                if skill1_form.is_valid():
                    skill1_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            skill1_form = Skill1Form()

        context["skill1_form"] = skill1_form
        context["skill1_user"] = user

    return render(request, 'cv/add_only/add_skill1_only.html', context) 
def add_skill2_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                skill2_form = Skill2Form(request.POST)
                skill2_form.instance.cv = cv         
                if skill2_form.is_valid():
                    skill2_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            skill2_form = Skill2Form()

        context["skill2_form"] = skill2_form
        context["skill2_user"] = user

    return render(request, 'cv/add_only/add_skill2_only.html', context) 

def add_job_only(request,pk):

    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user

        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                job_form = JobForm(request.POST)
                job_form.instance.cv = cv         
                if job_form.is_valid():
                    job_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            job_form = JobForm()

        context["job_form"] = job_form
        context["user_job"] = user

    return render(request, 'cv/add_only/add_job_only.html', context) 

def add_jobrole_only(request,pk):
    #pk is job.id
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        job=Job.objects.get(id = pk)
        user=job.cv.user

        if request.method == 'POST':
            jrole_form = J_RoleForm(request.POST)
            jrole_form.instance.user = user
            jrole_form.instance.job = job    
            if jrole_form.is_valid():
                jrole_form.save() 
                idd = jrole_form.instance.id                         
                if request.POST.get("save_back"): 
                    return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))


        else:
            jrole_form = J_RoleForm()

        context["jrole_form"] = jrole_form
        context["jrole_user"] = user

    return render(request, 'cv/add_only/add_jobrole_only.html', context)

def add_jobrolecat_only(request,pk):

    #pk is role.id
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        role=J_Role.objects.get(id = pk)
        user=role.user
        job = role.job

        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                jrolecat_form = J_Role_CatForm(request.POST)
                jrolecat_form.instance.role = role 
                jrolecat_form.instance.user = user 
                jrolecat_form.instance.job = job  
                if jrolecat_form.is_valid():
                    jrolecat_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            jrolecat_form = J_Role_CatForm()

        context["jrolecat_form"] = jrolecat_form
        context["jrolecat_user"] = user

    return render(request, 'cv/add_only/add_jobrolecat_only.html', context)

def add_edu_only(request,pk):
    #pk is CV
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

        cv=CV.objects.get(id = pk)
        user=cv.user
        
        if request.method == 'POST': 
            if request.POST.get("save_next"): 
                edu_form = EduForm(request.POST)
                edu_form.instance.cv = cv         
                if edu_form.is_valid():
                    edu_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))

        else:
            edu_form = EduForm()

        context["edu_form"] = edu_form
        context["user_edu"] = user

    return render(request, 'cv/add_only/add_edu_only.html', context) 

#--------------EDITS--------------------------------------------------------

#----ABOUT-----------
def edit_color(request, pk):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        user = User.objects.get(username = pk)
        cv = CV.objects.get(user = user)  
          
        

        form_color = ColorForm(request.POST or None, instance = cv)

        if request.method == 'POST':
            if form_color.is_valid():
                form_color.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])
    except:
         return redirect(reverse('error' ))

    context["form_color"] = form_color
    context["user_color"] = user


    return render(request, "cv/edit/edit_color.html", context)    
def edit_color1(request, pk):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try: 
        cv = CV.objects.get(id = pk)
        user=cv.user

        form_color = ColorForm(request.POST or None, instance = cv)

        if request.method == 'POST':
            if form_color.is_valid():
                form_color.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["form_color"] = form_color
        context["user_color"] = user
    except:
        return redirect(reverse('error' ))

    return render(request, "cv/edit/edit_color.html", context) 
def edit_bio(request, pk):

    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try: 
        bio = Bio.objects.get(id = pk)           
        #bio = get_object_or_404(Bio, id = pk)
        user=bio.cv.user

        form_bio = BioForm(request.POST or None, instance = bio)

        if request.method == 'POST':
            if form_bio.is_valid():
                form_bio.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["form_bio"] = form_bio
        context["user_bio"] = user
    except:
        return redirect(reverse('error' ))

    return render(request, "cv/edit/edit_bio.html", context)    

def edit_lang(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        lang = Lang.objects.get(id = pk)
        #lang = get_object_or_404(Lang, id = pk)
        user=lang.cv.user

        lang_form = LangForm(request.POST or None, instance = lang)

        if request.method == 'POST':
            if lang_form.is_valid():
                lang_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["lang_form"] = lang_form
        context["lang_user"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_lang.html", context)

def edit_web(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        web= Web.objects.get(id = pk)
        #web = get_object_or_404(Web, id = pk)
        user=web.cv.user

        web_form = WebForm(request.POST or None, instance = web)

        if request.method == 'POST':
            if web_form.is_valid():
                web_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["web_form"] = web_form
        context["web_user"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_web.html", context)

def edit_skill1(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        skill = Skill1.objects.get(id = pk)
        #lang = get_object_or_404(Lang, id = pk)
        user=skill.cv.user

        skill1_form = Skill1Form(request.POST or None, instance = skill)

        if request.method == 'POST':
            if skill1_form.is_valid():
                skill1_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["skill1_form"] = skill1_form
        context["skill1_user"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_skill1.html", context)

def edit_skill2(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        skill = Skill2.objects.get(id = pk)
        #lang = get_object_or_404(Lang, id = pk)
        user=skill.cv.user

        skill2_form = Skill2Form(request.POST or None, instance = skill)

        if request.method == 'POST':
            if skill2_form.is_valid():
                skill2_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["skill2_form"] = skill2_form
        context["skill2_user"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_skill2.html", context)

def edit_intro(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        intro = Intro.objects.get(id = pk)
        #lang = get_object_or_404(Lang, id = pk)
        user=intro.cv.user

        intro_form = IntroForm(request.POST or None, instance = intro)

        if request.method == 'POST':
            if intro_form.is_valid():
                intro_form.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["intro_form"] = intro_form
        context["intro_user"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_intro.html", context)

#----EDU-----------

def edit_edu(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        Edu.objects.get(id = pk)
        edu = get_object_or_404(Edu, id = pk)
        user=edu.cv.user

        form_edu = EduForm(request.POST or None, instance = edu)

        if request.method == 'POST':
            if form_edu.is_valid():
                form_edu.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["form_edu"] = form_edu
        context["user_edu"] = user
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/edit/edit_edu.html", context)

#----JOB-----------

def edit_job(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        Job.objects.get(id = pk)
        job = get_object_or_404(Job, id = pk)
        user=job.cv.user

        form_job = JobForm(request.POST or None, instance = job)

        if request.method == 'POST':
            if form_job.is_valid():
                form_job.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                raise ValidationError([
                    ('Error! Please try again.'),
                ])      

        context["form_job"] = form_job
        context["user_job"] = user

    except:
        return redirect(reverse('error'))
    return render(request, "cv/edit/edit_job.html", context)

def edit_jobrole(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        J_Role.objects.get(id = pk)
        role = get_object_or_404(J_Role, id = pk)
        user=role.user

        form_jobrole = J_RoleForm(request.POST or None, instance = role)

        if request.method == 'POST':
            if form_jobrole.is_valid():
                form_jobrole.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                #back to myself
                return redirect(reverse('edit_jobrole' , kwargs={'pk':pk}))
       

        context["form_jobrole"] = form_jobrole
        context["user_jobrole"] = user

    except:
        return redirect(reverse('error'))
    return render(request, "cv/edit/edit_jrole.html", context)

def edit_jobrolecat(request, pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        J_Role_Cat.objects.get(id = pk)
        cat = get_object_or_404(J_Role_Cat, id = pk)
        user=cat.user

        form_jobrolecat = J_Role_CatForm(request.POST or None, instance = cat)

        if request.method == 'POST':
            if form_jobrolecat.is_valid():
                form_jobrolecat.save()
                return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
            else:
                #back to myself
                return redirect(reverse('edit_jobrolecat' , kwargs={'pk':pk}))
       

        context["form_jobrolecat"] = form_jobrolecat
        context["user_jobrolecat"] = user

    except:
        return redirect(reverse('error'))
    return render(request, "cv/edit/edit_jrolecat.html", context)

#--------------DELETES--------------------------------------------------------

def delete_cv(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0
    user = request.user

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        cv = CV.objects.get(id = pk)
        #cv = get_object_or_404(CV, id = pk)
        user=cv.user

        if request.method == 'POST':
            cv.delete()
            return redirect(reverse('home' ))
        context["user_cv"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_cv.html", context)

#----ABOUT-----------

def delete_lang(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        lang = Lang.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=lang.cv.user

        if request.method == 'POST':
            lang.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["lang_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_lang.html", context)

def delete_intro(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        intro = Intro.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=intro.cv.user

        if request.method == 'POST':
            intro.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["intro_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_intro.html", context)

def delete_web(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        web = Web.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=web.cv.user

        if request.method == 'POST':
            web.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["web_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_web.html", context)



def delete_skill1(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        skill1 = Skill1.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=skill1.cv.user

        if request.method == 'POST':
            skill1.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["skill1_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_skill1.html", context)

def delete_skill2(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        skill2 = Skill2.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=skill2.cv.user

        if request.method == 'POST':
            skill2.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["skill2_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_skill2.html", context)

def delete_intro(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        intro = Intro.objects.get(id = pk)
        #job = get_object_or_404(Job, id = pk)
        user=intro.cv.user

        if request.method == 'POST':
            intro.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["intro_user"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_intro.html", context)

#----JOB-----------

def delete_job(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        Job.objects.get(id = pk)
        job = get_object_or_404(Job, id = pk)
        user=job.cv.user
        context['job'] = job.job_o

        if request.method == 'POST':
            job.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["user_job"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_job.html", context) 

def delete_jobrole(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        J_Role.objects.get(id = pk)
        role = get_object_or_404(J_Role, id = pk)
        user=role.user
        context['role'] = role.role_r

        if request.method == 'POST':
            role.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["user_jobrole"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_jobrole.html", context)

def delete_jobrolecat(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p

    try:
        J_Role_Cat.objects.get(id = pk)
        cat = get_object_or_404(J_Role_Cat, id = pk)
        user=cat.user
        context['cat'] = cat.cat

        if request.method == 'POST':
            cat.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["user_jobrolecat"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_jobrolecat.html", context)

#----EDU-----------

def delete_edu(request,pk):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    try:
        Edu.objects.get(id = pk)
        edu = get_object_or_404(Edu, id = pk)
        user=edu.cv.user
        context['edu'] = edu.edu_s

        if request.method == 'POST':
            edu.delete()
            return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
        context["user_edu"] = user
    except:
        return redirect(reverse('error'))
    return render(request, "cv/delete/delete_edu.html", context)




