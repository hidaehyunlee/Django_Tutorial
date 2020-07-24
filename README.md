# Django Cheatsheet

남진민



### 준비

#### 가상환경 만들기

```
$ python -m venv myvenv
```

#### 가상환경 실행

```
$ source myvenv/Scripts/activate
```

#### Django 설치

```
$ pip install django
```



### MTV개념

- #### Models

  데이터 관리

- #### Templates

  사용자가 보는 화면

- #### View

  데이터 처리, 중간관리자

  url요청 -> view(중간관리자) -> model(data관리) -> DB ->

  models-> views-> templates 



### 실습

1. ##### project 생성

   ```
   $ django-admin startproject firstsite
   ```

2. ##### project 폴더명 변경 후 경로로 이동

   ```
   $ cd firstsite_project
   ```

3. ##### app 생성

   ```
   $ python manage.py startapp blog
   ```

4. ##### project settings.py - INSTALLED_APPS에 app추가

   app 디렉토리의 apps.py에 정의된 class 명

   *이때 ','꼭 붙이기.

   ```
   'blog.apps.HelloConfig',
   ```

5. ##### Template 생성

   app 디렉토리 내에 templates 폴더 생성 후 html관리

   ```
   <h1>
       Hello, World!
   </h1>
   ```

6. ##### app views 함수 추가

   app 폴더 내의 views.py

   ```
   def blog(request):
       return render(request, 'blog.html')
   ```

7. ##### url과 view를 연결

   urls.py

   app 내의 views.py에 정의한 함수를 import

   ```
   import blog.views
   #import app이름.views
   ```

   urls.py의 urlpatterns에 path추가

   ```
   path('',blog.views.blog, name='blog'),
   #path('url뒤에 올 주소', app이름.views.함수이름, name='이름')
   ```

   path입력시 admin/과 같이 /를 마지막에 붙인다. (정규화)

8. ##### 서버 실행

   이때, 가상환경이 반드시 실행되어 있는 상태여야 한다.

   상위 디렉토리로 이동 후 가상환경 실행 후 다시 프로젝트 디렉토리로 이동 후 서버 실행

   ```
   $ python manage.py runserver
   ```

   

### model & admin

- ##### Migration

  model.py에 정의된 모델을 생성 및 변경 내역 관리, DB에 적용

  ```
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

- ##### admin

  DB 접근 권한을 가진 유저

  1. admin계정 만들기

     migration단계가 진행된 후 실행

     ```
     $ python manage.py createsuperuser
     ```



- ##### 실습

  1. ###### models.py에 class 생성(글쓰기)

     ```
     from django.db import models
     
     class Blog(models.Model):
         title = models.CharField(max_length=200)
         created_at = models.DateTimeField(auto_now_add=True)
         updated_at = models.DateTimeField(auto_now=True)
         body = models.TextField()
     
         def __str__(self): 
             return self.title
             #제목으로 표시되게
     ```

  2. ###### 생성 후에는 저장 후 migrate단계를 거친다.

     ```
     $ python manage.py makemigrations
     $ python manage.py migrate
     ```

  3. ###### admin.py 에 import

     admin사이트에서 적용되어야 한다.

     ```
     from django.contrib import admin
     from .models import Blog
     
     #admin사이트에 등록
     admin.site.register(Blog)
     ```

     

### queryset & method

1. ##### admin페이지가 아닌 메인 페이지에 데이터가 나오기 위해 view에서 데이터 처리

   ```
   from django.shortcuts import render
   from .models import Blog
   #models.py의 Blog class import
   
   def blog(request):
       blogs = Blog.objects
       return render(request, 'blog.html', {'blogs':blogs})
   ```

2. ##### 홈화면의 html파일에 쿼리셋 메소드 사용

   이때, models.py에서 정의된 각 객체의 이름과 동일하게 변수명을 입력 해야 함.

   ```
   {% for blog in blogs.all %}
       <h1>{{blog.title}}</h1>
       <p>{{blog.created_at}}</p>
       <p>{{blog.body}}</p>
       <br><br>
   {%endfor%}
   ```



### CRUD

​	Create, Read, Update, Delete

- #### Create & Read

  홈 화면에서 글 목록, 글쓰기 버튼

1. ##### blog.html

   ```
   <h1>
       게시판
   </h1>
   <br>
   <a href="{% url 'new' %}">글쓰기</a>
   
   {% for blog in blogs.all %}
   <div>
       <h1>{{blog.title}}</h1>
       <p>{{blog.created_at}}</p>
       <p>{{blog.body}}</p>
   </div>
   {%endfor%}
   ```

2. ##### new.html 생성

   ```
   <form action="{% url 'create' %}" method="post">
       {% csrf_token %}
       <div>
         <label for="title">제목</label><br>
         <input type="text" name="title" id="title">
       </div>
       <div>
           <label for="content">내용</label><br>
         <textarea name="body" id="body" cols="30" rows="10"></textarea>
       </div>
       <input type="submit" value="글쓰기">
     </form>
   ```

3. ##### 위에서 쓰인 url들 지정하기

   ```
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', blog.views.blog, name='blog'),
       path('new/',blog.views.new, name='new'),
       path('create/',blog.views.create, name='create'),
   ]
   ```

4. ##### path에 지정된 views.py에 함수 생성.

   ```
   from django.shortcuts import render, redirect
   from .models import Blog
   # Create your views here.
   def blog(request):
       blogs = Blog.objects
       return render(request, 'blog.html', {'blogs':blogs})
   
   def new(request):
       return render(request, 'new.html')
   
   def create(request):
       print(request.method)
       if(request.method=='POST'):
           post = Blog()
           post.title = request.POST['title']
           post.body = request.POST['body']
           post.save()
       return redirect('blog')
   ```

5. ##### 함수에 작성된 html(템플릿 폴더 내)



- #### Detail 페이지

  1. ##### 페이지 html 만들기

     ```
     <h1>제목 : {{blog.title}}</h1>
     <p>작성 시간 : {{blog.created_at}}</p>
     <p>내용 : {{blog.body}}</p>
      
     <a href="{% url 'blog' %}">홈으로</a>
     ```

  2. ##### urls.py

     ```
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', blog.views.blog, name='blog'),
         path('new/',blog.views.new, name='new'),
         path('create/',blog.views.create, name='create'),
         path('detail/<int:post_id'>,blog.views.detail, name='detail'),
     ]
     ```

  3. ##### views.py

     ```
     from django.shortcuts import render,redirect,get_object_or_404
     
     def detail(request, post_id):
         blog = get_object_or_404(Blog, pk = post_id)
         return render(request, 'detail.html', {'blog':blog})
     ```

  4. ##### blog.html 수정

     ```
     <h1>
         게시판
     </h1>
     <br>
     <a href="{% url 'new' %}">글쓰기</a>
     
     {% for blog in blogs.all %}
     <div>
         <h1><a href="{% url 'detail' blog.id %}">제목 : {{blog.title}}</a></h1>
         <p>{{blog.created_at}}</p>
         <p>{{blog.body}}</p>
     </div>
     {%endfor%}
     ```

     

### Update & Delete

- #### Update

  ##### 글 수정

  1. ###### detail.html 수정버튼 생성

     ```
     <a href="{% url 'edit' blog.id %}">수정</a>
     ```

  2. ###### urls.py

     ```
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', blog.views.blog, name='blog'),
         path('new/',blog.views.new, name='new'),
         path('create/',blog.views.create, name='create'),
         path('detail/<int:post_id>',blog.views.detail, name="detail"),
         path('edit/<int:post_id>',blog.views.edit, name="edit"),
     ]
     ```

  3. ###### views.py

     ```
     def edit(request, post_id):
         blog = get_object_or_404(Blog, pk=post_id)
         return render(request, 'edit.html',{'blog':blog})
     ```

  4. ###### edit.html

     ```
     <form action="{% url 'update' blog.id %}" method="POST">
         {% csrf_token %}
         <label for="title">제목</label> <br>
         <input type="text" name="title" id="title" value="{{blog.title}}">
         <br><br>
     
         <label for="body">내용</label> <br>
         <textarea name="body" id="body" cols="30" rows="20">{{blog.body}}</textarea> 
         <br><br>
     
         <button type="submit">수정하기</button>
     
     </form>
     
     <a href="{% url 'detail' blog.id %}">돌아가기</a>
     ```

  5. ###### urls.py ----- update

     ```
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', blog.views.blog, name='blog'),
         path('new/',blog.views.new, name='new'),
         path('create/',blog.views.create, name='create'),
         path('detail/<int:post_id>',blog.views.detail, name="detail"),
         path('edit/<int:post_id>',blog.views.edit, name="edit"),
         path('update/<int:post_id>',blog.views.update, name="update"),
     ]
     ```

  6. ###### views.py ----- update

     ```
     def update(request, post_id):
         blog = get_object_or_404(Blog, pk=post_id)
         blog.title = request.POST['title']
         blog.body = request.POST['body']
         blog.save()
         return redirect('/detail/'+str(post_id))
     ```

- #### delete

  1. ###### urls.py

     ```
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', blog.views.blog, name='blog'),
         path('new/',blog.views.new, name='new'),
         path('create/',blog.views.create, name='create'),
         path('detail/<int:post_id>',blog.views.detail, name="detail"),
         path('edit/<int:post_id>',blog.views.edit, name="edit"),
         path('update/<int:post_id>',blog.views.update, name="update"),
         path('delete/<int:post_id>',blog.views.delete,name="delete"),    
     ]
     ```

  2. ###### views.py

     ```
     def delete(request, post_id):
         delete=get_object_or_404(Blog, pk=post_id)
         delete.delete()
         return redirect('blog')
     ```

  3. ###### detail.html 삭제 추가

     ```
     <a href="{% url 'delete' blog.id %}">삭제</a>
     ```



### URL 관리

​	urls.py에 정의된 path가 많아 복잡해짐에 따라 기능 단위를 app으로 나누어 구현.

​	이에 따라서 기능 단위 별, 즉 app별로 url을 관리한다.

1. ##### app별로 urls.py를 생성하여 프로젝트 폴더의 urls.py내용 중 기능 별로 분류한다.

   (불필요한 admin과 같은 코드 제거)

   ```
   urlpatterns = [
       path('', blog.views.blog, name='blog'),
       path('new/',blog.views.new, name='new'),
       path('create/',blog.views.create, name='create'),
       path('detail/<int:post_id>',blog.views.detail, name="detail"),
       path('edit/<int:post_id>',blog.views.edit, name="edit"),
       path('update/<int:post_id>',blog.views.update, name="update"),
       path('delete/<int:post_id>',blog.views.delete,name="delete"),   
   ]
   ```

2. ##### project 폴더의 urls.py를 수정.

   앱의 urls.py로 안내하여 실질적인 url관리는 앱 내에서 이루어지게 한다.

   이때 경로는 blog/detail/1과 같이 나타난다.

   ```
   from django.contrib import admin
   from django.urls import path,include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('blog/',include('hello.urls'))
   ]
   ```

   

