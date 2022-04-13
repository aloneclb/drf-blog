from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utils.slugger import slugger # for slug
from utils.image_tools import image_size_converter, image_deleter # for image 
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
import os
from core.settings import BASE_DIR
from django.template.defaultfilters import slugify


def path_and_rename(instance, filename):
    # Product.image file name convert
    upload_to = 'post/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(slugify(filename), ext)
    return os.path.join(upload_to, filename)



class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.title


class PostObjects(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    CHOICES = (
        ('draft', 'Taslak'),
        ('published', 'Yayında'),
    )
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, related_name='category_posts', default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    tags = models.ManyToManyField(Tag, related_name='tag_posts', blank=True)
    # TODO: likes, images
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    image = models.ImageField(upload_to = path_and_rename, default='post/default.png') 
    content = models.TextField()
    slug = models.SlugField(unique=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10, choices=CHOICES, default='published')

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name='replies')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField(max_length=250)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return 'Comment by {} - {} '.format(self.author, self.body)



@receiver(pre_save, sender=Category)
def category_slug(instance, *args, **kwargs):
    slugger(instance)
    

@receiver(pre_save, sender=Tag)
def tag_slug(instance, *args, **kwargs):
    slugger(instance)


@receiver(pre_save, sender=Post)
def post_slug(instance, *args, **kwargs):
    slugger(instance)


@receiver(m2m_changed, sender=Post.tags.through)
def tag_slug(instance, *args, **kwargs):
    # This is posted by Many-to-Many fields
    if instance.tags.count() > 5:
        raise ValidationError("En fazla 5 tane tag atayabilirsiniz...")


@receiver(post_save, sender=Post)
def img_size_convert(instance, *args, **kwargs):
    image_size_converter(instance) 


@receiver(post_delete, sender = Post)
def delete_image_product(instance, *args, **kwargs):
    image_deleter(instance)
