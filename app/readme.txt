<!DOCTYPE html>
<html lang="en">
  {% load static %}
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Chat App with Sidebar</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN"
      crossorigin="anonymous"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    />
    <link rel="stylesheet" href="{% static 'images/app/style.css' %}" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
  </head>
  <body class="light-mode">
    <div class="grid">
      <!-- App background -->
      <div class="top"></div>
      <div class="bottom"></div>
      <!-- App -->
      <div class="app">
        <div class="sidebar">
          <div class="sidebar-header">
            {% if my_profile_pic %}
            <img
              src="{{ my_profile_pic.url }}"
              alt="My Profile Picture"
              class="profile-pic"
            />
            {% else %}
            <img
              src="/media/profile_pics/default_profile_pic.jpg"
              alt="Default Profile Picture"
              class="profile-pic"
            />
            <!-- Fallback default profile pic -->
            {% endif %}
            <div class="sidebar-header-icons">
              <img src="{% static  'images/app/status.svg' %} " />
              <img src="{% static  'images/app/message-icon.svg' %} " />
              <ul class="navbar-nav ms-auto">
                <!-- Image Dropdown Trigger -->
                <li class="nav-item dropdown">
                  <!-- Image as a trigger for the dropdown menu -->
                  <a
                    class="nav-link dropdown-toggle"
                    href="#"
                    id="menuDropdown"
                    role="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    <img
                      src="{% static 'images/app/menu-icon.svg' %}"
                      alt="Menu"
                      style="width: 30px; height: 30px"
                    />
                  </a>

                  <!-- Dropdown Menu -->
                  <ul
                    class="dropdown-menu dropdown-menu-end"
                    aria-labelledby="menuDropdown"
                  >
                    <!-- Show the logged-in user's username -->
                    <li class="dropdown-item disabled">
                      {{ user.username }}
                      <!-- Display the logged-in username -->
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <!-- Logout Button -->
                    <li>
                      <form method="POST" action="{% url 'logout' %}">
                        {% csrf_token %}
                        <button type="submit" class="dropdown-item">
                          Logout
                        </button>
                      </form>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
          <div
            class="toggle-container"
            style="text-align: center; margin-top: 20px"
          >
            <button id="toggle-button" class="btn btn-secondary">
              Toggle Dark/Light Mode
            </button>
          </div>
          <div class="sidebar-notifications">
            <img src="{% static  'images/app/notifications.svg' %} " />
            <div class="sidebar-notifications-message">
              <span>Get Notified of New Messages</span>
              <a href="#"
                >Turn on desktop notifications
                <img src="{% static  'images/app/gt-arrow.svg' %} "
              /></a>
            </div>
          </div>
          <div class="search-chat">
            <div class="search-bar">
              <img
                class="search-icon"
                src="{% static  'images/app/search-icon.svg' %} "
              />
              <input type="text" placeholder="Search or start new chat" />
            </div>
          </div>
          <div class="chats">
            {% for frnd_chat in frnds_chats %}
            <!-- Study group -->
            <a
              class="chat"
              href="/?user={{ frnd_chat.friend.username }}&image={{ frnd_chat.friend.profile.profile_pic.url | urlencode }}"
              role="tab"
              aria-controls="v-pills-home"
              aria-selected="false"
              style="text-decoration: none; color: gray"
            >
              <div class="chat-left">
                {% if frnd_chat.friend.profile.profile_pic %}
                <img
                  src="{{ frnd_chat.friend.profile.profile_pic.url }}"
                  alt="Friend's Profile Picture"
                  class="profile-pic"
                />
                {% else %}
                <img
                  src="/media/profile_pics/default_profile_pic.jpg"
                  alt="Default Profile Picture"
                  class="profile-pic"
                />
                {% endif %}
              </div>
              <div class="chat-right">
                <div class="chat-right-top">
                  <span class="contact-name"
                    >{{ frnd_chat.friend.username }}</span
                  >
                </div>

                <div class="chat-right-bottom">
                  <!-- Show the latest message here -->
                  {% if frnd_chat.last_message %}
                  <p class="chat-message">{{ frnd_chat.last_message.msg }}</p>
                  <span class="chat-date"
                    >{{ frnd_chat.last_message.time_sent }}</span
                  >
                  {% else %}
                  <p class="chat-message">No messages yet</p>
                  {% endif %}
                </div>

                <div class="chat-right-bottom-right">
                  <span class="unread-messages-number" id="unreadCountDisplay"
                    >{{ frnd_chat.friend.unreadCount }}</span
                  >
                  <span class="chat-options">
                    <img src="{% static 'images/app/down-arrow.svg' %}" />
                  </span>
                </div>
              </div>
            </a>
            {% endfor %}
          </div>
        </div>
        <div class="main">
          <div class="chat-window-header">
            <div class="chat-window-header-left">
              <img
                class="chat-window-contact-image"
                id="profileImage"
                src="{% static  'images/timmy-m-harley.jpg' %} "
              />
              <div class="contact-name-and-status-container">
                <span id="username" class="chat-window-contact-name"></span>
                <span class="status chat-window-contact-status" id="status-user"
                  >Online</span
                >
              </div>
            </div>
            <div class="chat-window-header-right">
              <img
                class="chat-window-search-icon"
                src="{% static  'images/app/search-icon.svg' %} "
              />
              <img
                class="chat-window-menu-icon"
                src="{% static  'images/app/menu-icon.svg' %} "
              />
            </div>
          </div>
          <div class="chat-window">
            {% for key, chat  in chats.items %}
            {% if chat.user == 'me' %}
            <div class="sender chat-card"  data-message-id="{{ key }}">
              <span class="sender-message-tail"><img src="{% static  'images/app/message-tail-sender.svg' %} "></span>
              <span class="chat-card" data-message-id="{{ key }}">{{ chat.msg }}</span>
              <span class="message-time chat-time">{{ chat.time_sent }}</span>
              <span class="message-status"><img src="{% static  'images/app/double-check-seen.svg' %} "></span>
            </div>
            {% else %}
            <div class="receiver otherchat" data-message-id="{{ key }}">
              <span class="receiver-message-tail"><img src="{% static  'images/app/message-tail-receiver.svg' %} "></span>
              <span class=" otherchat" data-message-id="{{ key }}">{{ chat.msg  }}</span>
              <span class="message-time">{{ chat.time_sent }}</span>
            </div>
            {% endif %}
            {% endfor %}
          </div>
          <div class="type-message-bar">
            <div class="type-message-bar-left">
              <img src="{% static  'images/app/icons.svg' %} " />
              <img src="{% static  'images/app/attach-icon.svg' %} " />
            </div>
            <div class="type-message-bar-center">
              <input
                class="message-input"
                type="text"
                placeholder="Type a message"
              />
            </div>
            <div class="type-message-bar-right">
              <img src="{% static  'images/app/audio-icon.svg' %} " />
            </div>
            <button class="send-button">
              <img
                width="24"
                height="24"
                src="https://img.icons8.com/material/24/sent--v1.png"
                alt="sent--v1"
              />
            </button>
          </div>
        </div>
      </div>
    </div>

    <script>
      document.addEventListener("DOMContentLoaded", async function () {
        // Get the query parameter 'user' from the URL
        const queryParams = new URLSearchParams(window.location.search);
        const user = queryParams.get("user");
        console.log(user);
        document.getElementById("username").textContent = user;
        const imageUrl = queryParams.get("image");
        // Activate the tab based on the 'user' query parameter
        const tab = document.querySelector(
          `[href="/?user=${user}&image=${encodeURIComponent(imageUrl)}"]`
        );
        if (tab) {
          tab.classList.add("active");
          tab.setAttribute("aria-selected", "true");
          document.getElementById("username").textContent = user;
          console.log(user, "user");
        }
        // If there's an image URL in the query params, update the image source
        if (imageUrl) {
          const imgElement = document.getElementById("profileImage");
          imgElement.src = decodeURIComponent(imageUrl);
        }

        if (user === null) {
          const chatContent = document.querySelector(".main");
          chatContent.style.display = "none";
        }
        var sendButton = document.querySelector(".send-button");
        var textarea = document.querySelector(".message-input");
        var chatMessages = document.querySelector(".chat-window");

        var ws;

        // Initialize unread message count
        let unreadMessageCount = 0;
        // Function to append a message to chat messages
        function appendMessage(user, message, status, messageId) {
          const chatCard = document.createElement("div");
          chatCard.classList.add(user === "me" ? "chat-card" : "otherchat");
          const timestamp = new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          });
          // Display ticks based on status
          let ticks = "";
          if (status === "unread") {
            return (ticks = "✔️"); // One tick for sent
          } else if (status === "read") {
            return (ticks = "✔️✔️"); // Two ticks for read
          }
          chatCard.innerHTML = `<p>${message} <span class="timestamp">${timestamp} </span> ${ticks}</p>`;
          chatCard.addEventListener("dblclick", function () {
            console.log(`Message "${message}" was double-clicked.`);
            markMessageAsRead(messageId);
          });
          chatMessages.appendChild(chatCard);
          chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // const toggleButton = document.getElementById("toggle-button");
        // toggleButton.addEventListener("click", function() {
        //   document.body.classList.toggle("dark-mode");
        //});

        // Function to mark message as read
        function markMessageAsRead(messageId) {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(
              JSON.stringify({ action: "mark_as_read", message_id: messageId })
            );

            // Assuming you have a way to update the status of the message in the UI
            const chatCards = document.querySelectorAll(".chat-card"); // Select all messages sent by the user
            chatCards.forEach((card) => {
              // Add a condition to match the messageId
              if (card.dataset.messageId === messageId) {
                // Update the status to read
                const timestamp = new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                });
                card.innerHTML = card.innerHTML.replace("✔️", "✔️✔️"); // Change to double ticks
                card.querySelector(
                  ".timestamp"
                ).textContent = `${timestamp} ✔️✔️`; // Update the timestamp with the new status
              }
            });
          }
        }
        // Function to send a message via WebSocket
        function sendMessage(message) {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ user: user, msg: message }));
          }
        }
        // Create a single WebSocket connection
        ws = new WebSocket("ws://127.0.0.1:8000/ws/wsc/");
        // Handle WebSocket connection open
        ws.addEventListener("open", function () {
          console.log("WebSocket connection opened.");
          updateUserStatus(true);
        });
        // Handle WebSocket message received
        ws.addEventListener("message", function (event) {
          console.log("Message received:", event.data);
          // Parse the received message JSON
          const data = JSON.parse(event.data);
          // Check if the message exists and append it to the chat
          if (data.msg) {
            appendMessage("frnd", data.msg || "unread"); // Append received message to chat
            unreadMessageCount++;
            updateUnreadCountDisplay();
          }
        });
        // Handle WebSocket connection close
        ws.addEventListener("close", function () {
          console.log("WebSocket connection closed.");
          updateUserStatus(false);
        });
        // Function to update user status based on WebSocket connection
        function updateUserStatus(isOnline) {
          const statusElement = document.getElementById("status-user");
          statusElement.textContent = isOnline ? "Online" : "Offline";
          statusElement.className = `status ${isOnline ? "online" : "offline"}`; // Update class for styling
        }
        // Initialize message count
        let messageCount = 0;
        const username = "User";
        // Event listener for send button click
        sendButton.addEventListener("click", sendHandler);
        // Event listener for 'Enter' key press to send message
        textarea.addEventListener("keypress", function (event) {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault(); // Prevent a new line in the textarea
            sendHandler();
          }
        });
        // Function to handle sending a message
        function sendHandler() {
          const messageText = textarea.value.trim(); // Trim whitespace from message
          if (messageText !== "") {
            sendMessage(messageText);
            appendMessage("me", messageText, true);
            messageCount++;
            // Update notification element with message count
            const notificationElement = document.getElementById("notification");
            if (notificationElement) {
              notificationElement.textContent = `${username}, your message has been sent! Total messages sent: ${messageCount}`;
            } else {
              console.error("Notification element not found");
            }
            textarea.value = ""; // Clear the textarea for the next message
          } else {
            console.warn("Message is empty, not sending.");
          }
        }

        // Function to update the unread message count display
        function updateUnreadCountDisplay() {
          const unreadCountDisplay =
            document.getElementById("unreadCountDisplay");
          if (unreadMessageCount > 0) {
            unreadCountDisplay.textContent = unreadMessageCount; // Show the count
            unreadCountDisplay.style.display = "block"; // Make it visible
          } else {
            unreadCountDisplay.style.display = "none"; // Hide it if count is 0
          }

          console.log("Unread message count:", unreadMessageCount); // Debug log
        }
        updateUnreadCountDisplay();
      });

      const toggleButton = document.getElementById("toggle-button");
      toggleButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
      });
    </script>
    <!-- Add Bootstrap JS at the bottom of your template for dropdown functionality -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>









views.pye
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

    # Fetch notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'index.html', {
        'my': mychats_data,
        'frnds_chats': frnds_chats,  # Send friends with their last messages
        'my_profile_pic': my_profile_pic,
        'notifications_count': notifications,
    })


# Retrieve the logged-in user's profile picture
    # if UserProfile.objects.filter(user=request.user).exists():
    #     my_profile_pic = UserProfile.objects.get(user=request.user).profile_pic

        

    # if frnd_name:
    #     if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
    #         frnd_ = User.objects.get(username=frnd_name)
    #         mychats_data = Mychats.objects.get(me=request.user,frnd=frnd_).chats

    #         # Retrieve the friend's profile picture
    #           # Retrieve the friend's profile picture
    #         if UserProfile.objects.filter(user=frnd_).exists():
    #             frnd_profile_pic = UserProfile.objects.get(user=frnd_).profile_pic
    # else:
    #     frnd_profile = None


    # frnds = User.objects.exclude(pk=request.user.id)
    # # Fetch notifications for the logged-in user
    #  # Fetch notifications for the logged-in user
    # notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    # return render(request,'index.html',{
    #     'my':mychats_data,
    #     'chats': mychats_data,
    #     'frnds':frnds,
    #     'my_profile_pic': my_profile_pic,  # Pass logged-in user's profile picture to the template
    #     'frnd_profile_pic': frnd_profile_pic,  # Pass friend's profile picture to the template
    #     'notifications_count': notifications,
    #      'notifications_count': notifications,
    #     })



    
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

