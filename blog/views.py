from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

def m_a(request):
    return render (request, 'blog/military_acronyms.html')

def home(request):
    return render (request, 'blog/home.html')

def FAQ(request):
    return render (request, 'blog/FAQ.html')

def guestbook(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/guestbook.html', context)

#view of all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/guestbook.html'  #browser looks in app > then model (post) > then viewtype 
    context_object_name = 'posts'
    #sets order of posts to by date, newest to oldest
    ordering =['-date_posted'] 
    #pages to show per page
    paginate_by = 6
   
#view for indiviual post object
class PostDetailView(DetailView):
    model = Post

#create new post object
#mixin django built-in to require user to be logged in to post comment
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/guestbook/'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#view posts by individual user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6
    #get user for show 404 error, display posts newest to oldest
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

#update post
#userpassestest check to only author (not all users) can update post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/guestbook/'


    def form_valid(self, form):
        #form instance author is set to current logged in user
        form.instance.author = self.request.user
        #vailidate the form, pass in the form as an arg
        return super().form_valid(form)

    def test_func(self):
        #get post that currently trying to update
        post = self.get_object()
        #check that current user is the same user as author
        if self.request.user == post.author:
            return True
        return False

#delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    #upon deletion send user to homepage
    success_url = '/guestbook/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def home(request):
    return render(request, 'blog/home.html', {'title': 'Home'})