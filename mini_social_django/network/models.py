from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=160, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f"Profile({self.user.username})"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} -> {self.following}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Post({self.author.username}, {self.created:%Y-%m-%d %H:%M})"

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Comment({self.author} on {self.post_id})"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like({self.user} -> {self.post_id})"
