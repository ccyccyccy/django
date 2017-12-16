from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Author(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	phone = models.IntegerField(blank=True, default=1)
	activation_key = models.CharField(max_length=255, default=1)
	email_validated = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('post_by_author', args=[self.user.username])


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('post_by_category', args=[self.slug])


class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('post_by_tag', args=[self.slug])


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True, help_text='Slug will be generated automatically from the title')
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		#parentSaveMethod = models.Model.save
		#self.parentSaveMethod(*args, **kwargs)
		super().save(*args, **kwargs) #This works the same as above 2 lines

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk, 'post_slug': self.slug})


class Feedback(models.Model):
	name = models.CharField(max_length=100, help_text='Name of sender')
	email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Feedback"

	def __str__(self):
		return self.name + '-' + self.email

	def get_absolute_url(self):
		return reverse('feedback')