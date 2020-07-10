from django.shortcuts import render, redirect
from .models import Blog

# Create your views here.

def home(request):
	blogs = Blog.objects
	return render(request, 'home.html', {'blogs' : blogs})

def new(request):
    return render(request, 'new.html')
 
def create(request):
    if(request.method == 'POST'):
        post = Blog()
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.save()
    return redirect('home')