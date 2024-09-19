from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, HttpResponse
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from .models import TodoItem, UserProfile
from .forms import TodoItemForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST

# Create your views here.


def todo(request):
    now = datetime.datetime.now()
    time = "<h1>The time is now %s <h1/>" % now
    return HttpResponse(time)


def home(request):
    return render(request, "home.html", {})


def join(request):
    user = get_user_model()
    if request.method == "POST":
        # Create a UserCreationForm instance
        form = UserCreationForm(request.POST)

        # Check if the form is valid (validates username, password, etc.)
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Redirect to success page (e.g., profile)
            return redirect("login")

        # If form is not valid, return the form with errors in the template
        else:
            return render(request, "join.html", {"form": form})
    else:
        # If the request is not POST, render the join form template with an empty form
        form = UserCreationForm()
        return render(request, "join.html", {"form": form})


def check_username(request):
    username = request.GET.get("username", None)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"exists": True})
    else:
        return JsonResponse({"exists": False})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({"success": True, "redirect_url": "/welcome/"})
            else:
                return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": False})
    else:
        form = LoginForm()
        csrf_token = get_token(request)
    return render(request, "login.html", {"form": form, "csrf_token": csrf_token})


@login_required
def welcome(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    search_query = request.GET.get("search", "")
    if search_query:
        items = TodoItem.objects.filter(user=request.user, title__icontains=search_query)
    else:
        items = TodoItem.objects.filter(user=request.user)

    important_items = TodoItem.objects.filter(user=request.user, important=True)
    item_id = request.GET.get("item_id")

    if item_id:
        item = get_object_or_404(TodoItem, id=item_id, user=request.user)
    else:
        item = None

    if request.method == "POST":
        if "avatar" in request.FILES:
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, "avatar_url": user_profile.avatar.url})
            else:
                return JsonResponse({"success": False, "error": form.errors})
        elif item:
            form = TodoItemForm(request.POST, instance=item)
        else:
            form = TodoItemForm(request.POST)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect("welcome")
    else:
        if item:
            form = TodoItemForm(instance=item)
        else:
            form = TodoItemForm()

    context = {
        "items": items,
        "form": form,
        "editing_item": item,
        "last_login": request.user.last_login,
        "user_profile": user_profile,
        "profile_form": UserProfileForm(instance=user_profile),
        "search_query": search_query,
        "important_items": important_items,  # Pass important items to the template
    }
    return render(request, "welcome.html", context)



@login_required
def delete_item(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("welcome")
    return render(request, "confirm_delete.html", {"item": item})




@require_POST
@csrf_exempt
def update_importance(request, item_id, importance):
    importance = True if importance.lower() == 'true' else False

    try:
        item = TodoItem.objects.get(id=item_id, user=request.user)
        item.important = importance
        item.save()
        return JsonResponse({"success": True})
    except TodoItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Item not found"})




"""
@csrf_exempt
def update_importance(request, item_id):
    if request.method == 'POST':
        try:
            item = TodoItem.objects.get(id=item_id)
            data = json.loads(request.body)
            item.important = data['important']
            item.save()
            return JsonResponse({'success': True})
        except TodoItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
"""
