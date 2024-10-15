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

    frnd_name = request.GET.get('user',None)
    mychats_data = None
    frnd_profile_pic = None
    my_profile_pic = None

    # Retrieve the logged-in user's profile picture
    if UserProfile.objects.filter(user=request.user).exists():
        my_profile_pic = UserProfile.objects.get(user=request.user).profile_pic

        

    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = Mychats.objects.get(me=request.user,frnd=frnd_).chats

            # Retrieve the friend's profile picture
              # Retrieve the friend's profile picture
            if UserProfile.objects.filter(user=frnd_).exists():
                frnd_profile_pic = UserProfile.objects.get(user=frnd_).profile_pic
    else:
        frnd_profile = None


    frnds = User.objects.exclude(pk=request.user.id)
    # Fetch notifications for the logged-in user
     # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request,'index.html',{
        'my':mychats_data,
        'chats': mychats_data,
        'frnds':frnds,
        'my_profile_pic': my_profile_pic,  # Pass logged-in user's profile picture to the template
        'frnd_profile_pic': frnd_profile_pic,  # Pass friend's profile picture to the template
        'notifications_count': notifications,
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




 <div class="chats">
            {% for frnd in frnds %}
            <!-- Study group -->
            <a class="chat" href="/?user={{ frnd.username }}&image={{ frnd.profile.profile_pic.url | urlencode }}" role="tab" aria-controls="v-pills-home" aria-selected="false" style="text-decoration: none; color:gray" >
              <div class="chat-left">
                {% if frnd.profile.profile_pic %}
               <img src="{{ frnd.profile.profile_pic.url }}" alt="Friend's Profile Picture" class="profile-pic">
                  {% else %}
                   <img src="/media/profile_pics/default_profile_pic.jpg" alt="Default Profile Picture" class="profile-pic">  <!-- Fallback default profile pic -->
              {% endif %}
              </div>
              <div class="chat-right">
                <div class="chat-right-top">
                  <span class="contact-name">{{frnd.username}}</span>
                  <!-- <span class="chat-date">11:20</span> -->
                </div>
                {% for key, chat in chats.items %}
                    {% if forloop.last %}
                        {% if chat.user == 'me' %}
                            <div class="chat-message-group" data-message-id="{{ key }}">
                                <p>{{ chat.msg }}</p>
                                <div>
                                  <div>
                                    <p class="chat-date">
                                      {{ chat.time_sent }}
                                  </p>
                                  </div>

                                </div>
                            </div>
                        {% else %}
                            <div class="otherchatlist" data-message-id="{{ key }}">
                                <p>{{ chat.msg }}</p>
                                <p class="chat-timelist">{{ chat.time_sent }}</p>
                            </div>
                        {% endif %}
                    {% endif %}
                  {% endfor %}
                
                <div class="chat-right-bottom">
                  <div class="chat-right-bottom-right">
                    <span class="unread-messages-number" id="unreadCountDisplay">{{frnd.unreadCount}}</span>
                    <span class="chat-options"
                      ><img src="{% static  'images/app/down-arrow.svg' %} "
                    /></span>
                  </div>
                </div>
              </div>
            </a>
            {% endfor %}
          </div>





          surya frnd
          <div class="chat-window">
            {% for chat in frnds_chats %}
            
            {% if chat.last_message.user == 'me' %}
            <div class="chat-card sender" data-message-id="{{ chat.last_message.time_sent }}">
              <span class="sender-message-tail">
                <img src="{% static 'images/app/message-tail-sender.svg' %}">
              </span>
              <span class="chat-card" data-message-id="{{ chat.last_message.time_sent }}">{{ chat.last_message.msg }}</span>
              <span class="message-time chat-time">{{ chat.last_message.time_sent }}</span>
              <span class="message-status">
                <img src="{% static 'images/app/double-check-seen.svg' %}">
              </span>
            </div>
            {% else %}
            <div class="otherchat receiver" data-message-id="{{ chat.last_message.time_sent }}">
              <span class="receiver-message-tail">
                <img src="{% static 'images/app/message-tail-receiver.svg' %}">
              </span>
              <span class="otherchat" data-message-id="{{ chat.last_message.time_sent }}">{{ chat.last_message.msg }}</span>
              <span class="message-time">{{ chat.last_message.time_sent }}</span>
            </div>
            {% endif %}
            
            {% endfor %}
          </div>