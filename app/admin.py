from django.contrib import admin
from .models import  CV, Bio, Job, Edu,PImg, J_Role, J_Role_Cat
from .models import  Lang, Web, Intro, Skill1, Skill2
admin.site.register(CV)
admin.site.register(Bio)

admin.site.register(Job)
admin.site.register(J_Role)

class J_Role(admin.ModelAdmin):
    fields = ('job', 'user' )

admin.site.register(J_Role_Cat)
admin.site.register(Edu)
admin.site.register(PImg)

admin.site.register(Lang)
admin.site.register(Web)
admin.site.register(Intro)
admin.site.register(Skill1)
admin.site.register(Skill2)



