from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Comment, Like, Follow

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def feed_view(request):
    # Posts from me + people I follow
    following_ids = list(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    qs = Post.objects.filter(author_id__in=following_ids + [request.user.id])
    form = PostForm()
    return render(request, 'network/feed.html', {'posts': qs.select_related('author'), 'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'network/post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    comments = post.comments.select_related('author')
    cform = CommentForm()
    return render(request, 'network/post_detail.html', {'post': post, 'comments': comments, 'cform': cform})

@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        cm = form.save(commit=False)
        cm.post = post
        cm.author = request.user
        cm.save()
    return redirect(post.get_absolute_url())

@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    followers = user.followers_set.count()
    following = user.following_set.count()
    return render(request, 'network/profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'followers': followers,
        'following': following
    })

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'network/profile_edit.html', {'form': form})

@login_required
@require_POST
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        raise Http404("Cannot follow yourself.")
    obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        obj.delete()
        following = False
    else:
        following = True
    return JsonResponse({'following': following, 'followers': target.followers_set.count()})
