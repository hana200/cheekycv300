from django.db import models

from django.conf import settings

from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime, date, time
import calendar
from .random import randomN

from django.db import IntegrityError
from PIL import Image, ImageOps

import os



# ------------------- FUNCTIONS ------------------------------------------------------------

def resize(ih,iw,s,img,img_,a):
        if ih > s or iw > s:
            if ih > iw:                
                iw_=s
                ih_= iw * ih / iw_ 

                img.thumbnail((ih_, iw_))
                img=img.rotate(a, expand=True)
                img.save(img_)

            elif iw>ih:
                ih_= s 
                iw_= iw * ih / ih_  

                img.thumbnail((iw_, ih_))
                img=img.rotate(a, expand=True)     
                img.save(img_)

            else:
                ih_=s
                iw_=s

                img.thumbnail((ih_, iw_))                
                img.save(img)
def image_name():
    r = randomN()
    t = models.TimeField(auto_now_add = True)
    d = models.DateField(auto_now_add = True)
    name = str(r+'.jpg')
    return name
def path_and_rename(instance, filename):
    upload_to = 'pic/'+str(instance.user)
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        img = str(instance.user)+'_'+str(instance.num)
        filename = '{}.{}'.format(img, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_overwrite(instance, filename):
    upload_to = 'pic/'+str(instance.user)
    pp=os.path.join(settings.MEDIA_ROOT, 'pic/'+str(instance.user))
    
    # ext = filename.split('.')[-1]
    ext = "jpg"

    img = 'prof_img_1'
    img1 = str(instance.user)+'_1'

    filename = '{}.{}'.format(img, ext)
    
    return 'pic/'+str(instance.user)+'/prof_img_1.'+ext


def R(n):
    R=[]
    for i in range(n):
        k=i+1
        R.append((i,str(k)))
    return R
def cat():
    CH_M_ = [ 'Projects', 'Achievements', 'Responsibilities', 'Awards', 'Publications', 'Achievements', 'Performance', 'Acquisition', 'Participation']
    CH_M = [(CH_M_[i], CH_M_[i]) for i in range(len( CH_M_))]
    return CH_M
def ch_m():
    CH_M_ = [ 'Jan', 'Feb', 'March', 'Apr', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec','Present']
    CH_M = [(CH_M_[i], CH_M_[i]) for i in range(len( CH_M_))]
    return CH_M
def ch_y():
    return [(r,r) for r in range(1950, date.today().year+1)]
def current_m():
    pass
def current_y():
    CH_Y = [(str(i), str(i)) for i in range(1950,date.today().year+2)]
    CH_Y[-1] = ('Present', 'Present')
    return CH_Y

# ------------------- MODELS ------------------------------------------------------------

class CV(models.Model):
    id = models.CharField(primary_key=True,max_length =255, editable=False)
    title = models.CharField(null=False, blank=False, max_length=255)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='CV_user')
    color = models.CharField(null=True, blank=True, max_length=30)

    def save(self,*args,**kwargs):
        if self.id:
            super(CV, self).save(*args,**kwargs)
            return
        unique = False
        while not unique:
            try:              
                self.id = randomN()              
                super(CV, self).save(*args,**kwargs)
            except IntegrityError:
                self.id = randomN()               
            else:
                unique = True
   
    def __str__(self):

        #return str(self.user) + ' | '+ str(self.id)
        return str(self.user)

class Bio(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='BIO_cv')
    name = models.CharField(null=False, blank=False,max_length=50)
    surname = models.CharField(null=False, blank=False,max_length=50)
    email = models.CharField(null=False, blank=False,max_length=100)
    phone = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=False, blank=False,max_length=200)

    def __str__(self):
        return str(self.cv)

class Lang(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='LANG_cv')
    l1 = models.CharField(max_length=1024,null=False, blank=False)
    l2 = models.CharField(max_length=1024,null=True, blank=True)
    l3 = models.CharField(max_length=1024,null=True, blank=True)
    l4 = models.CharField(max_length=1024,null=True, blank=True)
    l5 = models.CharField(max_length=1024,null=True, blank=True)
    l6 = models.CharField(max_length=1024,null=True, blank=True)
    l7 = models.CharField(max_length=1024,null=True, blank=True)
    l8 = models.CharField(max_length=1024,null=True, blank=True)
    l9 = models.CharField(max_length=1024,null=True, blank=True)
    l10 = models.CharField(max_length=1024,null=True, blank=True)

    def __str__(self):
        return str(self.cv)

class Web(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='WEB_cv')
    wl1 = models.CharField(max_length=100,null=True, blank=True)
    wl2 = models.CharField(max_length=100,null=True, blank=True)
    wl3 = models.CharField(max_length=100,null=True, blank=True)
    wl4 = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.cv)

class Intro(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='INTRO_cv')
    intro_text = models.CharField(null=False, blank=False,max_length=1500)
    outro_text = models.CharField(null=True, blank=True,max_length=1500)

    def __str__(self):
        return str(self.cv)

class Skill1(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='SKILL1_cv')
    skill_w1 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w2 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w3 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w4 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w5 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w6 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w7 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w8 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w9 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w10 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w11 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w12 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w13 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w14 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w15 = models.CharField(max_length=1024,null=True, blank=True)

    def __str__(self):
        return str(self.cv)
class Skill2(models.Model):
    cv = models.OneToOneField(CV,on_delete=models.CASCADE,related_name='SKILL2_cv')

    skill_w1 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w2 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w3 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w4 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w5 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w6 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w7 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w8 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w9 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w10 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w11 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w12 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w13 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w14 = models.CharField(max_length=1024,null=True, blank=True)
    skill_w15 = models.CharField(max_length=1024,null=True, blank=True)

    def __str__(self):
        return str(self.cv)

class Job(models.Model):
    #id = models.CharField(primary_key=True,max_length =255, editable=False)
    cv = models.ForeignKey(CV,on_delete=models.CASCADE,related_name='JOB_cv')

    job_o = models.CharField(max_length=50,null=False, blank=False)
    job_ws = models.CharField(max_length=200,null=True, blank=True)
    job_l = models.CharField(max_length=50,null=False, blank=False)
   
    #datetime
    job_sdm = models.CharField(max_length=9,choices=ch_m(),null=False, blank=False, default= 'Jan')
    job_sdy = models.CharField(max_length=9,choices=current_y(),null=False, blank=False, default=str(date.today().year))
    job_edm = models.CharField(max_length=9,choices=ch_m(),null=False, blank=False, default= 'Jan')
    job_edy = models.CharField(max_length=9,choices=current_y(),null=False, blank=False, default=str(date.today().year))

    def __str__(self):
        return str(self.cv.user)

class J_Role(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ROLE_user')
    #id = models.CharField(primary_key=True,max_length =255, editable=False)
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='ROLE_job')  

    role_r = models.CharField(max_length=50,null=False, blank=False)
    role_l = models.CharField(max_length=50,null=True, blank=True)
    role_d = models.CharField(max_length=1024,null=True, blank=True)

    #datetime
    role_sdm = models.CharField(max_length=9,choices=ch_m(),null=True, blank=True,default='Jan')
    role_sdy = models.CharField(max_length=9,choices=current_y(),null=True, blank=True,default=str(date.today().year))
    role_edm = models.CharField(max_length=9,choices=ch_m(),null=True, blank=True, default='Jan')
    role_edy = models.CharField(max_length=9,choices=current_y(),null=True, blank=True,default=str(date.today().year))
    
    def __str__(self):
        return str(self.job)

class J_Role_Cat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CAT_user') 
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='CAT_job')    
    role = models.ForeignKey(J_Role,on_delete=models.CASCADE,related_name='CAT_role')    
    #cat = models.CharField(max_length=1024,null=False, blank=False, help_text="Category name ")
    cat = models.CharField(max_length=20,choices=cat(),null=True, blank=True, default= 'Projects')
    cat_p1 = models.CharField(max_length=1024,null=False, blank=False)
    cat_p2 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p3 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p4 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p5 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p6 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p7 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p8 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p9 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p10 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p11 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p12 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p13 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p14 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p15 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p16 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p17 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p18 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p19 = models.CharField(max_length=1024,null=True, blank=True)
    cat_p20 = models.CharField(max_length=1024,null=True, blank=True)


    #cat_p = models.CharField(max_length=1024,null=False, blank=False, help_text="Please separate elements with a comma")

    def __str__(self):
        return str(self.role) + '|' + str(self.job)

class Edu(models.Model):
    cv = models.ForeignKey(CV,on_delete=models.CASCADE,related_name='EDU_cv')
    
    edu_s = models.CharField(max_length=100,null=False, blank=False)
    edu_d = models.CharField(max_length=100,null=False, blank=False)
    edu_l = models.CharField(max_length=100,null=True, blank=True)
    
    
    #datetime   
    edu_sdy = models.CharField(max_length=9,choices=current_y(),null=False, blank=False, default=str(date.today().year))  
    edu_edy = models.CharField(max_length=9,choices=current_y(),null=False, blank=False, default=str(date.today().year))

    def __str__(self):
        return str(self.cv.user)

class PImg(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(null = True, blank = True, upload_to=path_and_rename_overwrite, max_length=255,)


    # def delete1(self, using=None, keep_parents=False):
    #     aa=settings.MEDIA_ROOT+self.image.url 
    #     self.image.storage.delete(aa)
    #     super().delete()
    def delete(self,using=None, keep_parents=False):
        try:
            this = PImg.objects.get(id=self.id)
            this.image.delete()
            this.image.storage.delete()
        except: pass

        super(PImg, self).delete()

    def save(self, *args, **kwargs):

        try:
            this = PImg.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
                this.image.storage.delete()
        except: pass

        super(PImg, self).save(*args, **kwargs)

        #-----------------
      

        img = Image.open(self.image.path)
        img = ImageOps.exif_transpose(img)
        width, height = img.size  # Get dimensions
        if width > 1 and height > 1:

            if width > 300 and height > 300:
                # keep ratio but shrink down
                img.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                img.thumbnail((300, 300))

            img.save(self.image.path)
        else:
            super(PImg, self).delete() 



        #-----------------


        #--------------------

        #im = PImage.open('path_and_rename_overwrite') 
        #im = im.crop((left, top, right, bottom)) 
       

        '''

        img_ = self.image.path
        img = Image.open(img_)

        ih = img.height
        iw = img.width

        s=200 
        a=90

        resize(ih,iw,s,img,img_,a)
        '''

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self): 
        return reverse('home')


'''
profile_image = models.ImageField(upload_to='profile_images', default='profile_images/icon.png')
profile_icon = ImageSpecField(source='profile_image',
                              processors=[
                                  processors.Transpose(),
                                  processors.Thumbnail(width=72, height=72, crop=True)
                              ],
                              format='JPEG',

'''