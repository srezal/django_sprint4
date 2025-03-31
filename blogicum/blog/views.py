from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Category, User, Comment
from .forms import PostForm, CommentForm, UserChangeForm
import datetime


def index(request):
    # five_last_posts = Post.objects.filter(
    #     pub_date__lte=datetime.date.today()
    # ).filter(
    #     is_published=True
    # ).filter(
    #     category__is_published=True
    # ).order_by('-pub_date')[:5]
    posts = Post.objects.filter(
        pub_date__lte=datetime.date.today()
    ).filter(
        is_published=True
    ).filter(
        category__is_published=True
    ).order_by(
        '-pub_date'
    ).annotate(comment_count=Count('comments'))
    paginator = Paginator(posts, 10)  # По 10 объектов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id
    )
    comments = post.comments.all()
    return render(request, 'blog/detail.html', {'post': post, 'form': CommentForm(), 'comments': comments})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category__id=category.id
    ).filter(
        is_published=True
    ).filter(
        pub_date__lte=datetime.date.today()
    ).filter(
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, 10)  # По 10 объектов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {'page_obj': page_obj, 'category': category}
    )


def profile(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    context.update({'profile': user})
    posts = Post.objects.filter(
        author__username=username
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, 10)  # По 10 объектов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'page_obj': page_obj
    })
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    instance = get_object_or_404(User, username=request.user.username)
    form = UserChangeForm(request.POST or None, instance=instance)
    if form.is_valid():
        user = form.save(commit=False)
        user.last_login = request.user.last_login
        user.date_joined = request.user.date_joined
        user.is_staff = request.user.is_staff
        user.is_superuser = request.user.is_superuser
        user.is_active = request.user.is_active
        user.save()
        return redirect('blog:profile', username=user.username)
    return render(request, 'blog/user.html', {'form': form})

@login_required
def create_or_edit_post(request, post_id=None):
    if post_id is not None:
        instance = get_object_or_404(Post, id=post_id)
    else: instance = None
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.POST:
        instance.delete()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', id=post.id)
    

@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        raise PermissionDenied()
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})
    

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    if comment.author != request.user:
        raise PermissionDenied()
    if request.POST:
        post.comments.delete(comment)
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
