from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    introduction = models.TextField()
    #cover = models.ImageField()

    def __str__(self):
        return self.title

class Post(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded = models.DateTimeField(auto_now=True)
    temp = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.title

    def comments_count(self):
        return Comment.objects.filter(post=self).count() + Recomment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)
    

class Recomment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="recomments")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="recomments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recomments")
    content = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)


class Scrap(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="scraps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scraps")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    
