from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')

def view_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    return render(request, 'webapp/view-record.html', {'record': record})

# - Register a user

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("my-login")
        else:
            # Add error messages for invalid form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

# - Login a user

def my_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'webapp/my-login.html', {'form': form})


# - Dashboard

@login_required
def dashboard(request):
    records = Record.objects.filter(user=request.user)  # Filter records by the logged-in user
    context = {'records': records}
    return render(request, 'webapp/dashboard.html', context)


# - Create a record 

@login_required
def create_record(request):
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user  # Set the user to the currently logged-in user
            record.save()
            return redirect('dashboard')
    else:
        form = CreateRecordForm()
    return render(request, 'webapp/create-record.html', {'form': form})


# - Update a record 

@login_required
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UpdateRecordForm(instance=record)
    return render(request, 'webapp/update-record.html', {'form': form})

# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)


# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my-login")





