from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView
from django.views import View 
from django.urls import reverse_lazy
import os 
from django.db import IntegrityError
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Comment, Post
from .forms import PostForm, CommentForm

# Create your views here.
class AccountMixin(object):
    def dispatch(self, request, *args, **kwargs): 
        
        if request.user.is_authenticated:
            pass 
        else:
            messages.success(request, 'User should be logged-in before performing the operation.')
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)

class UpdateDeleteMixin(object):
    def dispatch(self, request, *args, **kwargs):  
        post_slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug = post_slug)
        print(post)
        if request.user.is_authenticated:
            if request.user.id==post.author.id:
                pass 
            else:
                messages.success(request, 'Failed to perform operation. Only the post owner is authorized to upate or delete post.')
                return redirect("blog:home")
        else:
            messages.success(request, 'User should be logged-in before performing the operation.')
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)

class HomeView(ListView):
    template_name = "blog/home.html"
    model = Post 
    context_object_name = "posts"
    ordering = ["-id"] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by("-id")
        paginator = Paginator(posts, 5, orphans=1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj 
        """ print("Paginator: ", paginator)
        print('Page number: ', page_number)
        print("Page_obj: ", page_obj)  """
        return context 

class PostDetailView(DetailView):
    template_name = "blog/post_detail.html"
    model = Post 
    slug_url_kwarg = 'slug' 
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.author.id==self.request.user.id:
            user_with_post = True
        else:
            user_with_post = False 
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        context['user_with_post'] = user_with_post
        return context


# @method_decorator(login_required, name="dispatch")
class PostCreateView(AccountMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create.html', {'form': form })

    def post(self, request):
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid(): 
            try: 
                t = form.cleaned_data['title']
                c = form.cleaned_data['content']
                img = form.cleaned_data['image'] 
                post = Post(title=t, content=c, image=img, author=request.user)
                post.save()
                return redirect("blog:home")  
            except IntegrityError as e:
                messages.success(request, "Failed to save! Try with another title.")
        return render(request, 'blog/post_create.html', {'form': form })


# @method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateDeleteMixin, UpdateView):
    template_name="blog/post_update.html"
    model = Post
    form_class = PostForm
    slug_url_kwargs="slug" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_slug'] = self.object.slug 
        return context

    def get_success_url(self): 
        post_slug = self.object.slug 
        return reverse_lazy("blog:post-detail", kwargs={'slug': post_slug})

class CommentHandleView(AccountMixin, View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post_slug = kwargs['slug'] 
            post = Post.objects.get(slug=post_slug)
            comment= Comment(content=content, author=request.user, post=post )  
            comment.save()
        return redirect(reverse_lazy("blog:post-detail", kwargs={'slug': post_slug}))
        
class VoteCountView(View):
    def post(self, request, slug):
        try:
            post = get_object_or_404(Post, slug=slug)   
            if request.user in post.voter.all():
                post.vote_count -= 1
                post.voter.remove(request.user)
                messages.success(request, "You unvoted the post.")
            else:
                post.vote_count += 1
                post.voter.add(request.user)
                messages.success(request, 'Voting success for the post.') 
            post.save()
            # return redirect(reverse_lazy("blog:post-detail", kwargs={'slug':slug})) 
        except Exception as e:
            print(e)
        return redirect("blog:post-detail", slug=slug)

class PostSearchView(View):
    def get(self, request):
        search_text = request.GET.get('keyword').strip()
        print(search_text)
        if search_text:
            posts = Post.objects.filter(Q(title__icontains=search_text) | Q(slug__icontains=search_text) | Q(content__icontains=search_text) | Q(author__username__icontains=search_text) ).order_by('-id')
        else:
            posts = Post.objects.all().order_by('-id')
        messages.success(request, f"{len(posts)} posts found in total that contains searched text \"f{search_text}\".")
        paginator = Paginator(posts, 5, orphans=1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number) 
        return render(request, 'blog/post_search.html', {'page_obj': page_obj, 'search_text': search_text})

# @method_decorator(login_required, name="dispatch")
class PostDeleteView(UpdateDeleteMixin, DeleteView):
    temlate_name = "blog/post_delete.html"
    model = Post 
    success_url = reverse_lazy("blog:home")
    