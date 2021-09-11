from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import *
from users.models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView

@login_required(login_url='login')
def post_home_view(request):
    user = request.user
    posts = PostModel.objects.all()
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = user
            new_post.save()

    context = {
        'post_list': posts,
        'form': form,
        'user': user,
    }

    return render(request, 'home/home.html', context)

@login_required(login_url='login')
def post_detail_view(request, pk):
    logged_in_user = request.user
    post = PostModel.objects.get(id=pk)
    author = post.author
    author_profile = ProfileModel.objects.get(user=author)
    comments = CommentModel.objects.filter(post=post)

    form = CommentForm(request.POST,)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.author = logged_in_user
        new_comment.save()

    context = {
        'post': post,
        'comments': comments,
        'author': author,
        'author_profile': author_profile,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


class PostDetailView(LoginRequiredMixin, View):
    @login_required(login_url='login')
    def get(self, request, pk, *args, **kwargs):
        post = PostModel.objects.get(pk=pk)
        form = CommentForm()

        comments = CommentModel.objects.filter(post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'posts/post_detail.html', context)
    @login_required(login_url='login')
    def post(self, request, pk, *args, **kwargs):
        post = PostModel.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = CommentModel.objects.filter(post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'posts/post_detail.html', context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostModel
    fields = ['body']
    template_name = 'posts/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostModel
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommentModel
    template_name = 'posts/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
