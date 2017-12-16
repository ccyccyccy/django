from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.contrib import messages, auth
from .models import Author, Category, Tag, Post
from .forms import FeedbackForm
from second_project.helpers import pg_records


# display a list of posts, aka main page
def post_list(request):
	allPosts = get_list_or_404(Post.objects.order_by('-id').all())
	posts = pg_records(request, allPosts, 5)
	return render(request, 'blog/post_list.html', {'posts': posts})


# single post
def post_detail(request, pk, post_slug):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})


# display all posts in the category
def post_by_category(request, category_slug):
	category = get_object_or_404(Category, slug=category_slug)
	allPosts = get_list_or_404(Post.objects.order_by('-id'), category=category)
	posts = pg_records(request, allPosts, 5)
	context = {'posts': posts, 'category': category}
	return render(request, 'blog/post_by_category.html', context)


# display all posts of same tag
def post_by_tag(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = get_list_or_404(tag.post_set.all())
	context = {'posts': posts, 'tag': tag}
	return render(request, 'blog/post_by_tag.html', context)


def post_by_author(request, author_name):
	author = get_object_or_404(Author, name=author_name)
	posts = get_list_or_404(Post, author=author)
	context = {'author': author, 'posts': posts}
	return render(request, 'blog/post_by_author.html', context)


def feedback(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			sender = form.cleaned_data['email']
			subject = 'You have a new Feedback from %s:%s' % (name, sender)
			message = 'Subject: %s\n\nMessage: %s' % (form.cleaned_data['subject'], form.cleaned_data['message'])

			mail_admins(subject, message)
			form.save()
			return redirect('feedback')

	else:
		form = FeedbackForm()
	return render(request, 'blog/feedback.html', {'form':form})


def login(request):
	if request.user.is_authenticated:
		return redirect('admin_page')

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user:
			auth.login(request, user)
			return redirect('admin_page')

		else:
			messages.error(request, 'Error wrong username/password')

	return render(request, 'blog/login.html')


def logout(request):
	if not request.user.is_authenticated:
		return redirect('blog_login')

	auth.logout(request)
	return render(request, 'blog/logout.html')


def admin_page(request):
	if not request.user.is_authenticated:
		return redirect('blog_login')

	return render(request, 'blog/admin_page.html')