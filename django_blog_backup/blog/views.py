from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag 
from .forms import CommentForm
from django.urls import reverse_lazy
from django.db.models import Q

# Create your views here.
def register(request):
    if request.method == 'Post':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            form = UserRegisterForm()
        return render(request, 'blog/register.html', {'form': form})    


@login_required

def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.save()
    return render(request, 'blog/profile.html')        

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' #template location
    context_object_name = 'posts'
    ordering = ['-created_at'] #newest first

class PostDetailView(DetailView):
    model = Post 
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
#Create a comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self,form):
        form.instance.author = self.request.user
        post_id = self.kwargs['post_id']
        form.instance.post = get_object_or_404(Post, id= post_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.post.get_absolute_url()
    
#Update a Comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
        
    def get_success_url(self):
        return self.object.post.get_absolute_url()
    
#Delete a Comment

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    form_class = CommentForm 


    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()  
    

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query: 
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)

            ).distinct()
        return Post.objects.none()
    
def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    return render(request,'blog/posts_by_tag.html'), {'tag': tag, 'posts':posts}
    