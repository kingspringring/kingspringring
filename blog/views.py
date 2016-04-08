# -*- coding:utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.conf import settings
from blog.models import Category, Article, Ad, Comment, Tag, User
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Count
from .forms import CommentForm, LoginForm, RegForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password


def global_set(request):
    category_list = Category.objects.all()
    ad_list = Ad.objects.all()
    archive_list = Article.objects.distinct_date()

    #comment_list = Comment.objects.values('article').annotate(Count('article')).order_by('-article__count')[:5]
    #article_comment_list = [Article.objects.get(pk=c['article']) for c in comment_list]
    article_comment_list = Article.objects.annotate(num_comment=Count('comment')).order_by('-num_comment')[:5]

    article_click_list = Article.objects.order_by('-click_count')[:5]

    article_is_recommend = Article.objects.filter(is_recommend=True).order_by('-click_count')

    tag_list = Tag.objects.all()

    return {
        'category_list': category_list,
        'ad_list': ad_list,
        'archive_list': archive_list,
        'article_comment_list': article_comment_list,
        'article_click_list': article_click_list,
        'article_is_recommend': article_is_recommend,
        'tag_list': tag_list,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
        'SITE_URL': settings.SITE_URL,
    }

logger = logging.getLogger('blog.views')


def index(request):

    # print locals()
    # print globals()
    try:
        article_list = get_page_list(request, Article.objects.all())
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


def archive(request):
    now = timezone.now()
    year = request.GET.get('year', now.year)
    month = request.GET.get('month', now.month)
    article_list = get_page_list(request, Article.objects.filter(date_publish__icontains=year+'-'+month))
    return render(request, 'archive.html', locals())


def tag(request):
    tag_name = request.GET.get('tag_name', '2015')
    article_list = get_page_list(request, Article.objects.filter(tag__name=tag_name))
    return render(request, 'tag.html', locals())


def category(request):
    category_id = request.GET.get('cid', 0)
    category = get_object_or_404(Category, pk=category_id)
    article_list = get_page_list(request, Article.objects.filter(category__id=category_id))
    return render(request, 'category.html', locals())


def article(request):
    article_id = request.GET.get('id', None)
    #article = get_object_or_404(Article, pk=article_id)
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist as e:
        print(e)
        return render(request, 'failure.html', {'reason': '文章不存在'})

    comment_list = article.comment_set.filter(pid=None)

    comment_form = CommentForm(
        {'author': request.user.username,
        'email': request.user.email,
        'url': request.user.url,
        'article': article_id} if request.user.is_authenticated() else{'article': article_id}
    )

    for i in dir(request.user):
        print(i)
    print(request.user.is_authenticated())
    print(request.GET)
    return render(request, 'article.html', locals())


def comment_post(request):
    if request.method == "POST":
        try:
            cf = CommentForm(request.POST)
            if cf.is_valid():
                comment = Comment.objects.create(
                    username=cf.cleaned_data['author'],
                    content=cf.cleaned_data['comment'],
                    url=cf.cleaned_data['url'],
                    email=cf.cleaned_data['email'],
                    article_id=cf.cleaned_data['article'],
                    user=request.user if request.user.is_authenticated() else None
                )
                print(comment, '******************************************')
                comment.save()
            else:
                render(request, 'failure.html', {'reason': cf.errors})
        except Exception as e:
            logger.error(e)
        for i in request.META:
            print(request.META[i])
        return redirect(request.META['HTTP_REFERER'])


def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                print("有效 *************************")
                print(reg_form.cleaned_data['username'],make_password(reg_form.cleaned_data['password']),reg_form.cleaned_data['email'],reg_form.cleaned_data['url'])
                user = User.objects.create(
                    username=reg_form.cleaned_data['username'],
                    password=make_password(reg_form.cleaned_data['password']),
                    email=reg_form.cleaned_data['email'],
                    url=reg_form.cleaned_data['url'],
                )
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                print(request.POST.get('source_url'))
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', locals())
        else:
            reg_form = RegForm()
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'reg.html', locals())


def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_login(request):
    try:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    print('pass authenticate**************************')
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    print(request.META['HTTP_REFERER'] + "**************")
                    for i in request.POST:
                        print(i, request.POST[i])
                    return redirect(request.POST.get('source_url'))
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
            else:
                return render(request, 'failure.html', {"reason": login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'login.html', locals())


def get_page_list(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger, ValueError):
        article_list = paginator.page(1)
    return article_list