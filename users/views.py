from django.shortcuts import render, redirect
from .models import Profile, Message
from django.contrib.auth import login, authenticate, logout
from .forms import SkillForm, UserRegistrationForm, ProfileForm, MessageForm
from .models import Profile, Skills
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
# Create your views here.

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account' )
        else:
            messages.error(request,'username or password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successful!!')
    return redirect('login')
 
def registerUser(request):
    page = 'register'
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration Successful')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request,'username or password is incorrect')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)
    

def profiles(request):
    user_profile, search_query = searchProfiles(request)
    custom_range, user_profile = paginateProfiles(request, user_profile, 6)

    context = {'user_profile': user_profile, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profile.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skills_set.exclude(description__exact="")
    other_skills = profile.skills_set.filter(description="")
    context = {'profile':profile,'top_skills':top_skills,'other_skills':other_skills }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skills_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def createSKill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill Created Successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)




@login_required(login_url='login')
def updateSKill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save(commit=False)
            form.save()
            messages.success(request, 'Skill Updated Successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def deleteSKill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted Successfully')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messsageRequest = profile.messages.all()
    unread_count = messsageRequest.filter(is_read=False).count()
    context = {'messsageRequest':messsageRequest, 'unread_count':unread_count }
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message }
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender 
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,'Message Sent Successfully')
            return redirect('user-profile', pk=recipient.id)
    form = MessageForm()
    context = {'form':form, 'recipient':recipient}
    return render(request, 'users/message_form.html', context)
