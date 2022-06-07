from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import UserCreateForm, UserProfileEditForm, UserLoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from books.models import Book_Review
from .models import CustomUser



def index(request):
    return render(request, 'index.html')



def homePage(request):
    reviews = Book_Review.objects.all()
    p = Paginator(reviews, 4)
    page_from_request = request.GET.get('page')
    try:
        page = p.page(page_from_request)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)

    pages = range(1, p.num_pages+1)
    context = {'page': page, 'pages': pages}
    return render(request, 'home.html', context)



class RegisterView(View):
    def get(self, request):

        create_form = UserCreateForm(data=request.POST)
        context = {
            'form': create_form,
        }

        return render(request, 'users/register.html', context)
    
    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            user = create_form.save()
            login(request, user)
            messages.success(request, "Successfully Signed Up!")
            return redirect('users:profile-edit')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)



class LoginView(View):
    def get(self, request):
        login_form = UserLoginForm()
        context = {'form': login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):

        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('books:books-list')
        else:
            context = {'form': login_form}
            return render(request, 'users/login.html', context)



class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out!")
        return redirect('users:landing-page')



class UserProfilePageView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        
        context = {'user': user}
        return render(request, 'users/user_profile.html', context)



class UserProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        profile_edit_form = UserProfileEditForm(instance=request.user)
        context = {'form': profile_edit_form}
        return render(request, 'users/user_profile_edit.html', context)
    

    def post(self, request):
        profile_edit_form = UserProfileEditForm(request.POST, instance=request.user, files=request.FILES)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Profile successffully updated!')
            return redirect("users:user-profile", username=request.user.username)
        else:
            profile_edit_form = UserProfileEditForm(instance=request.user)
        context = {'form': profile_edit_form}
        return render(request, 'users/user_profile_edit.html', context)


class AuthorBooksPageView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        
        context = {'user': user}
        return render(request, 'users/author_books.html', context)