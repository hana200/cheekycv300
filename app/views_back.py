'''
#----------BACKS--------
def add_bio_back(request,pk,x,y):

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
        bio = Bio.objects.get(id = pk)
        cv = bio.cv
        user = cv.user
        # pk = user
        '''
        user = User.objects.get(username = pk)
        cv=CV.objects.get(user = user)
        bio = Bio.objects.get(cv = cv)
        '''         
       

        form_bio = BioForm(request.POST or None, instance = bio)
        form_cv = CVForm(request.POST or None, instance = cv)

        if request.method == 'POST':
            if form_bio.is_valid() and form_cv.is_valid():
                form_bio.save()
                form_cv.save()
                idd=form_bio.instance.id
                if request.POST.get("back"):
                    return redirect(reverse('add_job_back' ,  kwargs={'pk': y,'x':'bio','y':idd}))
            else:
                #back to myself
                return redirect(reverse('add_bio_back' , kwargs={'pk':pk,'x': x, 'y':y}))
        context["form_cv"] = form_cv
        context["form_bio"] = form_bio
        context["user_bio"] = user
    except:
        return redirect(reverse('error' ))

    return render(request, "cv/add_bio_back.html", context)    
# ADD JOB_BACK -----------------------------------------   
def add_job_back(request,pk,x,y):
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
        job = Job.objects.get(id = pk)
        cv = job.cv
        user = cv.user

        form_job = JobForm(request.POST or None, instance = job)

        if request.method == 'POST':
            if form_job.is_valid():
                form_job.save()
                idd = form_job.instance.id 
                if request.POST.get("save_next"):   
                    return redirect(reverse('add_jobrole' , kwargs={'pk': y,'x':'job','y':idd}))
                elif request.POST.get("back"): 
                    if x == 'role':
                        return redirect(reverse('add_jobrole_back' , kwargs={'pk': y,'x':'job','y':idd}))
                    elif x == 'bio':
                        return redirect(reverse('add_bio_back' , kwargs={'pk': y,'x':'job','y':idd}))                
            else:
                #back to myself
                return redirect(reverse('add_job_back' , kwargs={'pk':pk,'x': x, 'y':y}))
        
        context["form_job"] = form_job
        context["user_job"] = user

        
    except:
        return redirect(reverse('error'))
    return render(request, "cv/add_job_back.html", context)
def add_jobrole_back(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    try:      
        role = J_Role.objects.get(id = pk)
        user= role.user

        form_jobrole = J_RoleForm(request.POST or None, instance = role)

        if request.method == 'POST':
            if form_jobrole.is_valid():
                form_jobrole.save()
                idd = form_jobrole.instance.id            
            if request.POST.get("save_next"): 
                    return redirect(reverse('add_jobrolecat' , kwargs={'pk': y,'x':'role','y':idd}))
            elif request.POST.get("back"):
                if x == 'job':
                    return redirect(reverse('add_job_back' , kwargs={'pk': y,'x':'role','y':idd})) 
                elif x == 'cat':
                    return redirect(reverse('add_jobrolecat_back' , kwargs={'pk': y,'x':'role','y':idd}))                  
            else:
                #back to myself
                return redirect(reverse('add_jobrole_back' , kwargs={'pk':pk,'x': x, 'y':y}))
            
            context["form_jobrole"] = form_jobrole
            context["user_jobrole"] = user

        else:
            #back to myself
            return redirect(reverse('add_jobrole_back' , kwargs={'pk':pk,'x': x, 'y':y}))
    except:
        return redirect(reverse('error'))
    return render(request, "cv/add_jobrole_back.html", context)
def add_jobrolecat_back(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
    try:
        cat = J_Role_Cat.objects.get(id = pk)
        user= cat.user
        #job = cat.job 
        #role = cat.role

        form_jobrolecat = J_RoleForm(request.POST or None, instance = cat)

        if request.method == 'POST':
            if form_jobrolecat.is_valid():
                form_jobrolecat.save()
                idd = form_jobrolecat.instance.id 
            if request.POST.get("add_job"): 
                return redirect(reverse('add_job', kwargs={'pk': y,'x':'cat','y':idd}))
            elif request.POST.get("add_edu"): 
                return redirect(reverse('add_edu', kwargs={'pk': y,'x':'cat','y':idd})) 

            elif request.POST.get("back"): 
                if x =="edu":
                    return redirect(reverse('add_edu_back' , kwargs={'pk': y,'x':'cat','y':idd}))
                elif x == 'role':
                    return redirect(reverse('add_jobrole_back' , kwargs={'pk': y,'x':'cat','y':idd}))
                elif x == 'job':
                    return redirect(reverse('add_job_back' , kwargs={'pk': y,'x':'cat','y':idd}))
                           
            else:
                #back to myself
                return redirect(reverse('add_jobrolecat_back' , kwargs={'pk':pk,'x': x, 'y':y}))
            
            context["form_jobrolecat"] = form_jobrolecat
            context["user_jobrolecat"] = user

        else:
            #back to myself
            return redirect(reverse('add_jobrolecat_back' , kwargs={'pk':pk,'x': x, 'y':y}))
    except:
        return redirect(reverse('error'))
    return render(request, "cv/add_jobrolecat_back.html", context)
# ADD EDU_BACK -----------------------------------------   
def add_edu_back(request,pk,x,y):
    context={}
    context["cv_"] = 0
    context["img_p"] = 0

    if request.user.is_authenticated:
        img_p = model_check(request,PImg)
        cv = model_check(request,CV)
        context["cv_"] = cv
        context["img_p"] = img_p
        
    try: 
        edu = Edu.objects.get(id = pk)
        user=edu.cv.user
        form_edu = EduForm(request.POST or None, instance = edu)

        if request.method == 'POST':
            if form_edu.is_valid():
                form_edu.save()
                idd=form_edu.instance.id
                if request.POST.get("add_edu"): 
                    return redirect(reverse('add_edu' , kwargs={'pk':y,'x': 'edu', 'y':idd}))
                elif request.POST.get("save_home"):                 
                    return redirect(reverse('cv_show_edit' , kwargs={'pk':user}))
                elif request.POST.get("back"):              
                    if x == 'edu':
                        return redirect(reverse('add_edu_back' , kwargs={'pk': y,'x':'edu','y':idd}))
                    elif x == 'cat':
                        return redirect(reverse('add_jobrolecat_back' , kwargs={'pk': y,'x':'edu','y':idd}))
                    elif x == 'job':
                        return redirect(reverse('add_job_back' , kwargs={'pk': y,'x':'edu','y':idd}))
                else:
                    #back to myself
                    return redirect(reverse('add_edu_back' , kwargs={'pk':pk,'x': x, 'y':y}))
            
            context["form_edu"] = form_edu
            context["user_edu"] = user
        else:
            #back to myself
            return redirect(reverse('add_edu_back' , kwargs={'pk':pk,'x': x, 'y':y}))
    except:
        return redirect(reverse('error'))
    
    return render(request, "cv/add_edu_back.html", context)


'''
