from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING,)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    createTime = models.DateTimeField()

from django.forms import ModelForm

class NoteForm(ModelForm):
    class Meta:
        model = Note
        #fields = '__all__'
        #fields = ['title', 'text', 'createTime']
        exclude = ['owner']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization = Authorization()

