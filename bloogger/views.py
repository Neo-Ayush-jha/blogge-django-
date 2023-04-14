from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import CreateView,View,ListView,FormView
from .models import *
from .forms import *
from .decorators import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self,req):
        data={
            "post":Post.objects.all(),
            "categorys":Category.objects.all(),
        }
        return render(req,"home.html",data)

class SingUp(View):
    def get(self,req):
        return render(req,"Form/select_user_type.html")
class AdminView(CreateView):
    model = User
    form_class = AdminCreateForm
    template_name="Form/singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']='Admin'
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect("home") 

class PrivateView(CreateView):
    model = User
    form_class = PrivateCreateForm
    template_name="Form/singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']='Private'
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect("home") 

class PublicView(CreateView):
    model=User
    form_class=PublicCreateForm
    template_name="Form/singup.html"
    success_url="/"
    def get_context_data(self,**kwargs):
        kwargs['user_type']='Public'
        return super().get_context_data(**kwargs)
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        return redirect("home")

class insertPostAsPrivate(CreateView):
    template_name="./Form/post.html"
    model=Post
    fields="__all__"
    def post(self,req):
        pass


class LoginView(FormView):
    template_name="Form/login.html"
    form_class=AuthenticationForm
    success_url="/"
    def post(self,req):
        username=req.POST.get("username")
        password=req.POST.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(req,user)
                back=req.GET.get("next","/")
                return redirect(back)
            else:
                return HttpResponse("inactivated")
        else:
            return HttpResponse("login cheeking is fail")
    
@method_decorator([login_required, public_required],name='dispatch')
class LinOut(View):
    def get(self,req):
        logout(req)
        return redirect("login")

@login_required
@public_required
def postCreate(req):
    form=PostCreateForm(req.POST or None, req.FILES or None)
    data={
        "form":form,
        "category":CategoryCreateForm
    }
    if req.method=="POST":
        if form.is_valid():
            p=form.save(commit=False)
            p.author=req.user
            p.save()
            return redirect("home")
    return render(req,"Form/post.html",data)

@login_required
@private_required
def categoryView(req):
    form=CategoryCreateForm(req.POST or None)
    if req.method=="POST":
        if form.is_valid():
            form.save()
            return redirect(postCreate)
    return render(req,"Form/category.html",{"form":form})
        