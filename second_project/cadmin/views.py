from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from second_project.helpers import generate_activation_key, pg_records
from blog.forms import PostForm, CategoryForm, TagForm
from blog.models import Post, Author, Category, Tag
from .forms import CustomUserCreationForm



@login_required
def post_list(request):
	if request.user.is_superuser:
		posts = Post.objects.order_by('-id').all()
	else:
		posts = Post.objects.filter(
			author__user__username=request.user.username
			).order_by('-id')

	posts = pg_records(request, posts, 5)
	return render(request, 'cadmin/post_list.html', {'posts': posts})


@login_required
def post_add(request):
	#If request is POST, create a bound forms
	if request.method == 'POST':
		f = PostForm(request.POST)

		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				new_post = f.save(commit=False)
				author = Author.objects.get(user__username='staff')
				new_post.author = author
				new_post.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:				
				new_post = f.save()
		
			else:
				new_post = f.save(commit=False)
				new_post.author = Author.objects.get(user__username=request.user.username)
				new_post.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Post added')
			return redirect('post_add')

		else:
			print(f.errors)

	#if form is valid, save data to database, redirect back to post_add view
	
	#if request is GET, show unbound form
	else:
		f = PostForm()
	return render(request, 'cadmin/post_add.html', {'form': f})


@login_required
def post_update(request, pk):
	post = get_object_or_404(Post, pk=pk)

	if request.method == 'POST':
		f = PostForm(request.POST, instance=post)

		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				updated_post = f.save(commit=False)
				updated_post.author = Author.objects.get(user__username='staff')
				updated_post.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:				
				f.save()
		
			else:
				updated_post = f.save(commit=False)
				updated_post.author = Author.objects.get(user__username=request.user.username)
				updated_post.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Post updated')
			return redirect('post_update', pk=pk)

		else:
			print(f.errors)

	#If request is GET, prepopulate with current post data
	else:
		f = PostForm(instance=post)
	return render(request, 'cadmin/post_update.html', {'form': f, 'post':post})


@login_required
def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	next_page = request.GET['next']
	messages.add_message(request, messages.INFO, 'Post deleted')
	return redirect(next_page)


@login_required
def category_list(request):
	if request.user.is_superuser:
		categories = Category.objects.order_by('-id').all()
	else:
		categories = Category.objects.filter(author__user__username=request.user.username)

	categories = pg_records(request, categories, 5)

	return render(request, 'cadmin/category_list.html', {'categories': categories})


@login_required
def category_add(request):
	if request.method == 'POST':
		f = CategoryForm(request.POST)
		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				new_category = f.save(commit=False)
				new_category.author = Author.objects.get(user__username='staff')
				new_category.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:
				f.save()

			else:
				new_category = f.save(commit=False)
				new_category.author = Author.objects.get(user__username=request.user.username)
				new_category.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Category added')
			return redirect('category_add')

		else:
			print(f.errors)

	else:
		f = CategoryForm()
	return render(request, 'cadmin/category_add.html', {'form': f})


@login_required
def category_update(request, pk):
	category = get_object_or_404(Category, pk=pk)
	if request.method == 'POST':
		f = CategoryForm(request.POST, instance=category)
		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				updated_category = f.save(commit=False)
				updated_category.author = Author.objects.get(user__username='staff')
				updated_category.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:
				f.save()

			else:
				updated_category = f.save(commit=False)
				updated_category.author = Author.objects.get(user__username=request.user.username)
				updated_category.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Category updated')
			redirect('category_update', pk=pk)

		else:
			print(f.errors)

	else:
		f = CategoryForm(instance=category)

	return render(request, 'cadmin/category_update.html', {'form': f})


@login_required
def category_delete(request, pk):
	category = get_object_or_404(Category, pk=pk)
	category.delete()
	next_page = request.GET['next']
	messages.add_message(request, messages.INFO, 'Category deleted')
	return redirect(next_page)


@login_required
def tag_list(request):
	if request.user.is_superuser:
		tags = Tag.objects.order_by('-id').all()
	else:
		tags = Tag.objects.filter(author__user__username=request.user.username).order_by('-id')

	tags = pg_records(request, tags, 5)
	return render(request, 'cadmin/tag_list.html', {'tags': tags})


@login_required
def tag_add(request):
	if request.method == 'POST':
		f = TagForm(request.POST)
		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				new_tag = f.save(commit=False)
				new_tag.author = Author.objects.get(user__username='staff')
				new_tag.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:
				new_tag = f.save()

			else:
				new_tag = f.save(commit=False)
				new_tag.author = Author.objects.get(user__username=request.user.username)
				new_tag.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Tag added')
			return redirect('tag_add')

		else:
			print(f.errors)

	else:
		f = TagForm()

	return render(request, 'cadmin/tag_add.html', {'form': f})


@login_required
def tag_update(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	if request.method == 'POST':
		f = TagForm(request.POST, instance=tag)
		if f.is_valid():
			if request.POST.get('author') == '' and request.user.is_superuser:
				updated_tag = f.save(commit=False)
				updated_tag.author = Author.objects.get(user__username='staff')
				updated_tag.save()
				f.save_m2m()

			elif request.POST.get('author') and request.user.is_superuser:
				updated_tag = f.save()

			else:
				updated_tag = f.save(commit=False)
				updated_tag.author = Author.objects.get(user__username=request.user.username)
				updated_tag.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Tag updated')
			return redirect('tag_update', pk=pk)

		else:
			print(f.errors)

	else:
		f = TagForm(instance=tag)

	return render(request, 'cadmin/tag_update.html', {'form': f})


@login_required
def tag_delete(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	tag.delete()
	next_page = request.GET['next']
	messages.add_message(request, messages.INFO, 'Tag deleted')
	return redirect(next_page)


def login(request, **kwargs):
	if request.user.is_authenticated:
		return redirect('cadmin_post_list')
	else:
		return auth_views.login(request, **kwargs)


def register(request):
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST)
		if f.is_valid():
			# Send email verifications
			activation_key = generate_activation_key(username=request.POST['username'])
			subject = 'TheGreatDjangoBlog Account Verification'
			message = '''\n
			Please visit the following link to verify your account\n\n
			{0}://{1}/cadmin/activate/account/?key={2}
			'''.format(request.scheme, request.get_host(), activation_key)
			print(request.POST['email'])

			error = False
			try:
				send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
				messages.add_message(request, messages.INFO, 'Account created! Click on the link sent to your email to activate the account')

			except:
				error = True
				messages.add_message(request, messages.INFO, 'Unable to send email verification. Please try again')

			if not error:
				u = User.objects.create_user(
					username=request.POST['username'],
					email=request.POST['email'],
					password=request.POST['password1'],
					is_active=0,
				)

				author = Author()
				author.user = u
				author.activation_key = activation_key
				author.save()
				
			return redirect('register')

	else:
		f = CustomUserCreationForm()

	return render(request, 'cadmin/register.html', {'form': f})


@login_required
def account_info(request):
	return render(request, 'cadmin/account_info.html')


def activate_account(request):
	key = request.GET.get('key', False)
	if not key:
		raise Http404()
	author = get_object_or_404(Author, activation_key = key, email_validated=False)
	author.user.is_active = True
	author.user.save()
	author.email_validated = True
	author.save()

	return render(request, 'cadmin/activated.html')