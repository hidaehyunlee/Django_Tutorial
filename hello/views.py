from django.shortcuts import render
from .models import Blog

# Create your views here.

def home(request):
	blogs = Blog.objects
	return render(request, 'home.html', {'blogs' : blogs})
