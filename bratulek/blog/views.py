from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.utils import timezone
from .models import Post, Board, Comment
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.contrib.sites.models import Site
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.utils.six.moves.urllib.parse import urlparse
from django.contrib.syndication.views import Feed


def board_list(request):
    boards = Board.objects.all()
    if not boards:
        Board.objects.create(name="Free Board")
        boards = Board.objects.all()
    return render(request, 'blog/board_list.html', {'boards': boards})

def board_detail(request, pk):
    boards = Board.objects.all()
    if not boards:
        Board.objects.create(name="Free Board")
        boards = Board.objects.all()
    posts = Post.objects.filter(board=pk).order_by('-published_date')
    board = Board.objects.get(pk=pk)
    return render(request, 'blog/post_list.html', {'posts': posts, 'board':board, 'boards': boards})

def post_new(request, bd):
        board_get=Board.objects.get(pk=bd)
        if request.method == "POST":
            form = PostForm(request.POST  or None, request.FILES or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.board = board_get
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    boards = Board.objects.all()
    comments = Comment.objects.filter(post=pk).order_by('-published_date')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(text=form.cleaned_data['text'], post=get_object_or_404(Post, pk=pk),
                                  published_date=timezone.now())
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments' : comments, 'boards': boards, 'form' : form})


def e404(request):
    return render(request, 'blog/404.html', {}, status=404)

