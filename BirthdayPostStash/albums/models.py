# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from users.models import User
from django.db import models
import datetime
# Create your models here.

import uuid
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill



class AlbumImage(models.Model):
    user = models.ForeignKey(User,unique=False)
    image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 70})
    # album = models.ForeignKey('album', on_delete=models.PROTECT, blank='True')
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.image.name

        # def on_save(self):
        #     pass

class People(models.Model):
    name = models.CharField(max_length=30,default='John Doe')
    created_by = models.ForeignKey(User,default=1)
    # propic = models.ForeignKey(AlbumImage, unique=False,related_name='thumb_pic')
    # thumb = ImageSpecField(source=get_propic(self), processors=[ResizeToFill(200,100)], format='JPEG',
    #                             options={'quality': 60})
    remind_on = models.DateField()
    event = models.TextField(default='No Event')
    associated_with = models.ManyToManyField(AlbumImage)
    favourite = models.ForeignKey(AlbumImage,related_name='fav',blank=True)

    def save(self):
        self.favourite = self.associated_with.all()[0]

    def change_fav(self,album):
        self.favourite = album


    def __str__(self):
        return self.name


    # class Album(models.Model):
#     title = models.CharField(max_length=70)
#     description = models.TextField(max_length=1024)
#     thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 90})
#     tags = models.CharField(max_length=250)
#     is_visible = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(max_length=50, unique=True)
#     people = models.ManyToManyField(People)


    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

        # def __unicode__(self):
        #     return self.title




