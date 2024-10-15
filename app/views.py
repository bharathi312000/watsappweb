from pyexpat.errors import messages
from urllib import request
from django.shortcuts import redirect, render
from app.models import Mychats,UserProfile  # Import UserProfile model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Notification
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserCreationForm  # Import the custom form
# Create your views here.

 
@login_required
def home(request):
    """
    Handles the home page and chat logic.
    """

    frnd_name = request.GET.get('user', None)
    mychats_data = None
    frnd_profile_pic = None
    my_profile_pic = None

    # Retrieve the logged-in user's profile picture
    if UserProfile.objects.filter(user=request.user).exists():
        my_profile_pic = UserProfile.objects.get(user=request.user).profile_pic

    frnds_chats = []  # To store friends and their latest chat
    frnds = User.objects.exclude(pk=request.user.id)

    # Populate the friends' chats data
    for frnd in frnds:
        # Check if there's a chat thread with this friend
        if Mychats.objects.filter(me=request.user, frnd=frnd).exists():
            chat_data = Mychats.objects.get(me=request.user, frnd=frnd).chats
            # Sort the dictionary by keys and get the last message
            if chat_data:
                last_key = sorted(chat_data.keys())[-1]  # Get the last key
                last_message = chat_data[last_key]  # Get the last message using the last key
                frnds_chats.append({
                    'friend': frnd,
                    'last_message': last_message,
                })
        else:
            frnds_chats.append({
                'friend': frnd,
                'last_message': None,
            })

    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user, frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = Mychats.objects.get(me=request.user, frnd=frnd_).chats
            # print(mychats_data,"bbbb")

            # Retrieve the friend's profile picture
            if UserProfile.objects.filter(user=frnd_).exists():
                frnd_profile_pic = UserProfile.objects.get(user=frnd_).profile_pic
    else:
        frnd_profile_pic = None

    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'index.html', {
        'my': mychats_data,
        'frnds_chats': frnds_chats,  # Send friends with their last messages
        'my_profile_pic': my_profile_pic,  # Pass logged-in user's profile picture to the template
        'frnd_profile_pic': frnd_profile_pic,  # Pass friend's profile picture to the template
        'notifications_count': notifications,
    })

    
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')  # Redirect to the login page after logout
 
def login_view(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password.')  # Display error message

     return render(request, 'login.html')  # Render the login form template




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Create a UserProfile instance
            login(request, user)  # Automatically log in the user after registration
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your registration.')

    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

