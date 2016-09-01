from urllib import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, 'Successfully created.')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'form' : form
	}

	return render(request, 'post_form.html', context)


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)

	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string = quote_plus(instance.content)
	context = {
		'instance' : instance,
		'title' : instance.title,
		'share_string' : share_string
	}
	return render(request, 'post_detail.html', context)


def post_list(request):
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	else:
		queryset_list = Post.objects.active()

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query)
		).distinct()

	paginator = Paginator(queryset_list, 2)
	page_request = 'page'
	page = request.GET.get(page_request)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		'object_list' : queryset,
		'title' : 'List',
		'page_request': page_request
	}

	return render(request, 'post_list.html', context)


def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)

	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, 'Post saved.')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'instance' : instance,
		'title' : instance.title,
		'form' : form
	}
	return render(request, 'post_form.html', context)


def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, id=id)
	instance.delete()

	context = {
		'title': 'Delete'
	}
	messages.success(request, 'Post deleted.')
	return redirect('posts:list')
