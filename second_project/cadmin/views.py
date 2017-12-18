from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from second_project import helpers
from blog.forms import PostForm
from blog.models import Post, Author
from .forms import CustomUserCreationForm


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
				new_post = f.save(commit=False)
				author = f.cleaned_data['author']
				new_post.author = author
				new_post.save()
				f.save_m2m()
		
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
				updated_post = f.save()

			elif request.POST.get('author') and request.user.is_superuser:				
				updated_post = f.save(commit=False)
				author = f.cleaned_data['author']
				updated_post.author = author
				updated_post.save()
				f.save_m2m()
		
			else:
				updated_post = f.save(commit=False)
				updated_post.author = Author.objects.get(user__username=request.user.username)
				updated_post.save()
				f.save_m2m()

			messages.add_message(request, messages.INFO, 'Post updated')
			return redirect('post_update', pk=pk)

	#If request is GET, prepopulate with current post data
	else:
		f = PostForm(instance=post)
	return render(request, 'cadmin/post_update.html', {'form': f, 'post':post})

@login_required
def home(request):
	return render(request, 'cadmin/admin_page.html')


def login(request, **kwargs):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		return auth_views.login(request, **kwargs)


def register(request):
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST)
		if f.is_valid():
			# Send email verifications
			activation_key = helpers.generate_activation_key(username=request.POST['username'])
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