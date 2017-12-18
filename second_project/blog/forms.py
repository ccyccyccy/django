from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from .models import Author, Category, Tag, Post, Feedback


class AuthorForm(forms.ModelForm):
	
	class Meta:
		model = Author
		fields = '__all__'

	def clean_name(self):
		name = self.cleaned_data['name']
		if name.lower() in ('author', 'admin'):
			raise ValidationError("Author's name cannot be %s" % name)
		return name

	def clean_email(self):
		return self.cleaned_data['email'].lower()


class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
		fields = '__all__'

	def clean_name(self):
		n = self.cleaned_data['name']
		if n.lower() in ('tag', 'add', 'update'):
			raise ValidationError
		return n

	def clean_slug(self):
		return self.cleaned_data['slug'].lower()


class CategoryForm(forms.ModelForm):

	class Meta:
		model = Category
		fields = '__all__'

	def clean_name(self):
		n = cleaned_data['category']
		if n.lower() in ('tag', 'add', 'update'):
			raise ValidationError("Category name cannot be %s" % n)
		return n

	def clean_slug(self):
		return cleaned_data['slug'].lower()


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'content', 'category', 'tags',)

	# author is not recognised as part of Post field, need to add in manually in views
	author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)

	def clean_title(self):
		n = self.cleaned_data['title']
		if n.lower() in ('post', 'add', 'update'):
			raise ValidationError("Post's title cannot be %s" % n)
		return n

	def clean(self):
		cleaned_data = super().clean()
		title = cleaned_data.get('title')
		#if title exists create slug from title
		if title:
			cleaned_data['slug'] = slugify(title)
		return cleaned_data


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = '__all__'