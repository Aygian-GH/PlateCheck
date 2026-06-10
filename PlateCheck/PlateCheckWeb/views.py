from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# ---------------------------------------------------------------------------
# Custom Forms
# ---------------------------------------------------------------------------

class UsernameOnlySignupForm(UserCreationForm):
    """
    Strips email from the default UserCreationForm.
    Only requires username + password.
    """
    class Meta(UserCreationForm.Meta):
        fields = ('username',)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def home(request):
    """
    Landing page. Surfaces Sign Up, Login, Image Upload, and Dashboard links.
    When the user is authenticated, Sign Up and Login are replaced by Log Out.
    """
    return render(request, 'home.html')


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def signup_view(request):
    """
    Open registration — no existing account required.
    GET  – renders the sign-up form (username + password only, no email).
    POST – creates the account and logs the user in, then redirects to dashboard.
    Already-authenticated users are redirected to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsernameOnlySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UsernameOnlySignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """
    Handles user login.
    GET  – renders the login form.
    POST – authenticates credentials; redirects to dashboard on success.
    Already-authenticated users are redirected to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    """
    Logs the user out and returns them to the home page.
    Uses POST to protect against CSRF-based forced logouts.
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You've been logged out.")
    return redirect('home')


# ---------------------------------------------------------------------------
# Image Upload  (nutrition analysis)
# ---------------------------------------------------------------------------

@login_required(login_url='signup')
def image_upload_view(request):
    """
    Lets users upload a food photo for nutrition analysis.
    GET  – renders the upload form.
    POST – validates and saves the image, then hands off to the analysis pipeline.
    Unauthenticated users are redirected to sign up.

    Expects a model like FoodImage with fields: user, image, uploaded_at.
    Replace the stub below with your actual model import and processing logic.
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('food_image')
        if not uploaded_file:
            messages.error(request, "Please select an image before uploading.")
            return render(request, 'image_upload.html')

        # Placeholder: persist the image and kick off analysis
        # food_image = FoodImage.objects.create(user=request.user, image=uploaded_file)
        # run_nutrition_analysis.delay(food_image.id)   # e.g. a Celery task

        messages.success(request, "Image uploaded! Analysis will appear on your dashboard shortly.")
        return redirect('dashboard')

    return render(request, 'image_upload.html')


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@login_required(login_url='signup')
def dashboard_view(request):
    """
    Main dashboard: shows the user's nutrition log, recent uploads, and stats.
    Unauthenticated users are redirected to sign up.

    Populate `context` with real queryset data once your models are ready.
    """
    context = {
        'user': request.user,
        # TODO: add real data, e.g.:
        # 'recent_logs': NutritionLog.objects.filter(user=request.user).order_by('-date')[:7],
        # 'today_summary': get_today_summary(request.user),
    }
    return render(request, 'dashboard.html', context)