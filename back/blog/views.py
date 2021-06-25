from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Article, Comment, Tag
from blog.forms import CommentForm
# Create your views here.

def article_list(request):
    page_number = request.GET.get('page')
    context = {
        'title': 'ブログ一覧',
        'page_obj': Paginator(Article.objects.all(), 1).get_page(page_number),
        'page_number': page_number
    }
    return render(request, 'blog/index.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)

    if request.method == 'POST':
        if request.POST.get('like_count', None):
            article.count += 1
            article.save()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
            else:
                context['comment_errors'] = form.errors

    comments = Comment.objects.filter(article=article)
    context = {
        'article': article,
        'comments': comments,
    }

    return render(request, 'blog/detail.html', context)


def tagview(request, tag):
    tag = get_object_or_404(Tag, slug=tag)
    page_number = request.GET.get('page')
    context = {
        'title': '#タグ: {}'.format(tag.slug),
        'page_obj': Paginator(tag.article_set.all(), 2).get_page(page_number),
        'page_number': page_number
    }
    return render(request, 'blog/index.html', context)