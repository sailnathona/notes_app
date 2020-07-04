from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django import forms
#from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
#from notes_forms import LoginForm
from .models import Note, NoteForm
from django.forms.models import modelformset_factory


# In Django 1.8+, the template's render method takes a dictionary for the context parameter.
# Original code using RequestContext threw a TypeError at index.
# I got it to work first using locals() function
# It's a known trick that this can be used instead of the context dictionary but it's not recommended
# it works when all the data you need to pass to the template is stored in local variables
# locals() returns a dictionary holding the local variables names (as keys) and the current values (as values).
# I then built a small but explicit context_dictionary, instead of passing locals(),
# because down the line when I must build my data, I probably won't have such data in separate variables.
# see: https://stackoverflow.com/questions/1901525/django-template-and-the-locals-trick

#TODO: define a dict containing only what I want to pass through to the template instead of using locals()
# DONE!

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

@login_required(login_url="/notes/index/")
def dashboard(request):
    from django.forms.models import inlineformset_factory
    # InlineFormSet with parent_model=User and model=Note
    NoteFormSet = inlineformset_factory(User, Note,  exclude=['owner'], can_delete=True, extra=1, form=NoteForm)
    if request.method == 'POST':
        formset = NoteFormSet(request.POST, request.FILES, instance=request.user)
        if formset.is_valid():
            formset.save()
        return redirect("dashboard")
    else:
        formset = NoteFormSet(instance=request.user)
        template = loader.get_template('dashboard.html')
        context = {
            'form': NoteForm(),
            'formset': formset,
        }
        return HttpResponse(template.render(context, request=request))
        #return render_to_request("dashboard.html"), {'form':NoteForm(), 'formset':formset}, RequestContext(request))


@login_required(login_url="/notes/index/")
def dashboardold(request):
    if request.method == 'POST':
        # d dict is a copy of our request.Post because it's immutable and we need to add owner
        d = request.POST.copy()
        d.update({'owner': request.user.id})
        form = NoteForm(d)
        if not form.is_valid():
            template = loader.get_template('dashboard.html')
            context = {
                'form': form,
            }
            return HttpResponse(template.render(context, request=request))
        # overview of following code: save the note to the database
        # if the form is valid that is
        # save the new note to a variable, and associate it with the current user logged in, and save the changes to the database.
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        return redirect("dashboard")
    else:
        template = loader.get_template('dashboard.html')
        context = {
            'form': NoteForm(),
        }
        return HttpResponse(template.render(context, request=request))

#@csrf_exempt
def index(request):
    # this was the old direct pure python code way to return / send back the string
    # return HttpResponse("Hello, Notes")
    if request.method == 'POST':
        print("Received POST")
        form = LoginForm(request.POST)
        if form.is_valid():
            print("FORM is Valid")
            # proceed with registration
            username, pwd = request.POST.get("username", None), request.POST.get("password", None)
            if not username or not pwd:
                return HttpResponse("Username or password not present")
            try:
                user = User.objects.get(username_exact=username)
            except:
                print("Creating new user")
                user = User.objects.create_user(username, username, pwd)
            if user:
                print("authenticating")
                user = authenticate(username=username, password=pwd)
            #user = authenticate(username=username, password=pwd)
            print("logging in user")
            login(request, user)
            return redirect("dashboard")
        else:
            print("FORM is NOT VALID")
            # let the user know
            # send the correct instance of the form that has the information
            # send back a http response
            template = loader.get_template('index.html')
            context = {
                'username': 'Sinead Nic an Bháird',
                'form': form,
            }
            return HttpResponse(template.render(context, request=request))
    else:
        # load the template file
        template = loader.get_template('index.html')
        # Define template context: pass data to the template file
        # We change to static name and username for now
        context = {
           'username': 'Sinead Nic an Bháird',
            'form': LoginForm(),
        }
        return HttpResponse(template.render(context, request=request))


    #old code from tutorial that works with older Django
    #rc = RequestContext(request, {"user": request.user})
    #return HttpResponse(template.render(rc))

def dologout(request):
    logout(request)
    return redirect("index")

def example(request):
    # load the template file
    template = loader.get_template('example.html')
    temp = 80
    # Define template context: pass data to the template file
    # We change to static name and username for now
    context = {
        'fruits': ['apple', 'raspberry', 'orange', 'banana', 'apricot', 'tomato'],
        'username': 'Sinead Nic an Bháird',
        'temp': temp,
    }
    return HttpResponse(template.render(context))

