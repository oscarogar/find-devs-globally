
from .models import Skills, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, user_profile, items_on_page):
    page = request.GET.get('page')
    paginator = Paginator(user_profile, items_on_page)
    try:
        user_profile = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        user_profile = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        user_profile = paginator.page(page)
    # the code below limits the number of pages in the event the pages displaying 
    # items on the website becomes too large for example. you have 1000 items pages
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 4)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    return custom_range, user_profile


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skills.objects.distinct().filter(name__icontains=search_query)
    user_profile = Profile.objects.filter(
        Q(name__icontains=search_query)|
        Q(short_intro__icontains=search_query)| 
        Q(name__in=skills)
    )
    return user_profile, search_query
