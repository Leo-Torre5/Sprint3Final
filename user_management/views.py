# user_management/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from MelodyMatrix.forms import LoanAlbumForm, AlbumForm, SearchForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from user_management.models import UserProfile
from django.contrib import messages
from user_management.forms import UserCreationForm, ProfileUpdateForm, UserUpdateForm
from .forms import RegisterForm
from django.contrib import messages



class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_management/user_list.html'

class UserCreateView(CreateView):
    model = get_user_model()
    form_class = RegisterForm  # Use your existing registration form
    template_name = 'user_management/user_create_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm()
        return context

class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'user_management/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm(instance=self.object.userprofile)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update user profile
        profile_form = ProfileUpdateForm(self.request.POST, instance=self.object.userprofile)
        if profile_form.is_valid():
            profile_form.save()
        return response

class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'user_management/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


def profile(request):
    User = get_user_model()

    # Ensure there is a UserProfile instance for the user
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('view_profile')
        else:
            print(u_form.errors)
            print(p_form.errors)
            messages.error(request, 'Error updating your profile. Please check the form.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context)


def view_profile(request):
    # Retrieve the user profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Retrieve success message from the session
    success_messages = messages.get_messages(request)
    success_message = None
    for message in success_messages:
        success_message = message

    # Create a context dictionary
    context = {
        'user_profile': user_profile,
        'success_message': success_message,
    }

    # Render the template with the context
    return render(request, 'view_profile.html', context)

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    try:
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been deleted successfully.')
    except ProtectedError:
        messages.error(request, f'User "{user.username}" cannot be deleted.')

    return redirect('user_list')



