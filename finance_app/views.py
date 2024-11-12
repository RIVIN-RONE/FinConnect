from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Vendor, User
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Vendor, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import Vendor
import logging

# Setup a logger for debugging
logger = logging.getLogger(__name__)

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the appropriate dashboard based on the user's role
            if user.role == 'Employee':
                return redirect('employee_dashboard')
            elif user.role == 'Manager':
                return redirect('manager_dashboard')
            elif user.role == 'Finance':
                return redirect('finance_dashboard')
            elif user.role == 'Admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Employee Dashboard
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request, Notification
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def employee_dashboard(request):
    if request.user.role != 'Employee':
        messages.error(request, 'Unauthorized access')
        return redirect('login')

    # Fetch all the requests made by the employee
    requests = Request.objects.filter(employee=request.user)

    total_requests = requests.count()
    approved_by_manager = requests.filter(status='Approved').count()
    approved_by_finance = requests.filter(status='Approved by Finance').count()
    pending_requests = requests.filter(status='Pending').count()
    hold_requests = requests.filter(status='Hold').count()
    rejected_requests = requests.filter(status='Rejected').count()

    return render(request, 'employee_dashboard.html', {
        'total_requests': total_requests,
        'approved_by_manager': approved_by_manager,
        'approved_by_finance': approved_by_finance,
        'pending_requests': pending_requests,
        'hold_requests': hold_requests,
        'rejected_requests': rejected_requests,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Notification

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Notification

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Notification

from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, Notification
from django.contrib.auth.decorators import login_required
from .forms import RequestForm  # Assuming you have a RequestForm for handling the request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Request, Vendor, Notification, User
from .forms import RequestForm

@login_required
def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.employee = request.user  # Assign the logged-in user as the employee
            new_request.save()

            # Notify all managers when a new request is added
            managers = User.objects.filter(role='Manager')
            for manager in managers:
                Notification.objects.create(
                    user=manager,
                    message=f"New request submitted by {request.user.username}.",
                )

            return redirect('employee_dashboard')  # Redirect to employee dashboard or appropriate view
    else:
        form = RequestForm()

    return render(request, 'add_request.html', {'form': form})

@login_required
def manager_dashboard(request):
    if request.user.role != 'Manager':
        return redirect('home')

    notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = notifications.count()

    total_approved = Request.objects.filter(status='Approved').count()
    total_rejected = Request.objects.filter(status='Rejected').count()
    total_pending = Request.objects.filter(status='Pending').count()

    data = {
        'total_approved': total_approved,
        'total_rejected': total_rejected,
        'total_pending': total_pending,
    }

    return render(request, 'manager_dashboard.html', {
        'data': data,
        'unread_notifications_count': unread_notifications_count,
        'notifications': notifications,
    })

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()

    return redirect('manager_dashboard')


#####################################################################################################
#####################################################################################################
#####################################################################################################

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

@login_required
def request_detail(request, request_id):
    if request.user.role != 'Manager':
        return redirect('home')

    req = get_object_or_404(Request, id=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'Approved':
            req.status = 'Approved'
            req.manager_approval_at = timezone.now()
            req.save()
            return redirect('approve_requests')
        elif action == 'Rejected':
            req.status = 'Rejected'
            req.save()
            return redirect('approve_requests')

    return render(request, 'request_detail.html', {
        'request_detail': req
    })


#####################################################################################################
#####################################################################################################
#####################################################################################################


# views.py
from django.utils import timezone
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request, User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Request, Notification
from django.urls import reverse
from django.contrib import messages

# Approve requests view for manager
@login_required
def approve_requests(request):
    if request.user.role != 'Manager':
        return redirect('home')  # Ensure only managers can access this view

    # Fetch all pending requests
    pending_requests = Request.objects.filter(status='Pending')

    return render(request, 'approve_requests.html', {
        'requests': pending_requests
    })

# Detailed view for approving/rejecting a request
@login_required
def approve_reject_request(request, request_id):
    if request.user.role != 'Manager':
        return redirect('home')  # Ensure only managers can access this view

    request_obj = get_object_or_404(Request, id=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('manager_note')  # Make sure you get the correct form field name

        if action == 'Approved':
            request_obj.status = 'Approved'
            request_obj.notes = notes  # Store the manager's note
            request_obj.save()

            # Create a notification for the finance team (if required)
            finance_users = Notification.objects.filter(user__role='Finance')
            for finance_user in finance_users:
                Notification.objects.create(user=finance_user.user, message=f"Request {request_obj.ticket_number} has been approved.")

            messages.success(request, f"Request {request_obj.ticket_number} has been approved.")

        elif action == 'Rejected':
            request_obj.status = 'Rejected'
            request_obj.notes = notes  # Store the rejection note
            request_obj.save()

            # Notify the employee about the rejection (if required)
            Notification.objects.create(user=request_obj.employee, message=f"Your request {request_obj.ticket_number} has been rejected with the note: {notes}")

            messages.error(request, f"Request {request_obj.ticket_number} has been rejected.")

        return redirect('approve_requests')

    return render(request, 'approve_reject_request.html', {
        'request_obj': request_obj
    })


@login_required
def finance_dashboard(request):
    if request.user.role != 'Finance':
        return redirect('home')

    requests = Request.objects.filter(status='Approved')

    return render(request, 'finance_dashboard.html', {
        'requests': requests
    })


@login_required
def view_status(request):
    if request.user.role != 'Employee':
        return redirect('home')

    requests = Request.objects.filter(employee=request.user, status='Rejected')

    return render(request, 'view_status.html', {
        'requests': requests
    })


@login_required
def approved_requests(request):
    if request.user.role != 'Manager':
        return redirect('home')

    # Filter approved requests
    requests = Request.objects.filter(status='Approved')
    return render(request, 'approved_requests.html', {'requests': requests})


@login_required
def rejected_requests(request):
    if request.user.role != 'Manager':
        return redirect('home')

    # Filter rejected requests
    requests = Request.objects.filter(status='Rejected')
    return render(request, 'rejected_requests.html', {'requests': requests})



# Finance Dashboard
@login_required
def finance_dashboard(request):
    if request.user.role != 'Finance':
        messages.error(request, 'Unauthorized access')
        return redirect('login')

    # Fetch unread notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    # Mark notifications as read
    notifications.update(is_read=True)

    # Filter requests that are approved by the manager only
    requests = Request.objects.filter(status='Approved')

    approved_count = requests.filter(status='Approved').count()
    rejected_count = requests.filter(status='Rejected').count()
    pending_count = requests.filter(status='Pending').count()
    hold_count = requests.filter(status='Hold').count()

    urgent_requests = Request.objects.filter(is_urgent=True, status='Pending')

    context = {
        'requests': requests,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'hold_count': hold_count,
        'urgent_requests': urgent_requests,
        'notifications': notifications,  # Add notifications to context
    }

    return render(request, 'finance_dashboard.html', context)


# Admin Dashboard
@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        return redirect('home')

    users = User.objects.all()

    if request.method == 'POST':
        # Handle user management logic (Add/Update/Set permissions)
        username = request.POST.get('username')
        role = request.POST.get('role')
        password = request.POST.get('password')

        if username and role and password:
            new_user = User.objects.create_user(username=username, role=role)
            new_user.set_password(password)
            new_user.save()
            messages.success(request, 'New user added successfully!')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'admin_dashboard.html', {
        'users': users
    })

# Add new vendor (Finance/Admin only)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

@login_required
def add_vendor(request):
    if request.user.role not in ['Employee', 'Finance', 'Admin']:
        messages.error(request, 'Unauthorized access.')
        return redirect('home')

    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        vendor_id = request.POST.get('vendor_id')
        type_of_vendor = request.POST.get('type_of_vendor')
        branch = request.POST.get('branch')
        vendor_banking_name = request.POST.get('vendor_banking_name')
        vendor_bank = request.POST.get('vendor_bank')
        vendor_ifsc = request.POST.get('vendor_ifsc')
        vendor_account_number = request.POST.get('vendor_account_number')
        document = request.FILES.get('document')

        # Ensure all fields are filled
        if all([vendor_name, vendor_id, type_of_vendor, branch, vendor_banking_name, vendor_bank, vendor_ifsc, vendor_account_number, document]):
            # Check for the uniqueness of vendor_id and vendor_account_number
            if Vendor.objects.filter(vendor_id=vendor_id).exists():
                messages.error(request, 'Vendor ID already exists. Please use a unique Vendor ID.')
            elif Vendor.objects.filter(vendor_account_number=vendor_account_number).exists():
                messages.error(request, 'Vendor account number already exists. Please use a unique account number.')
            else:
                try:
                    vendor = Vendor.objects.create(
                        vendor_name=vendor_name,
                        vendor_id=vendor_id,
                        type_of_vendor=type_of_vendor,
                        branch=branch,
                        vendor_banking_name=vendor_banking_name,
                        vendor_bank=vendor_bank,
                        vendor_ifsc=vendor_ifsc,
                        vendor_account_number=vendor_account_number,
                        added_by=request.user,
                        document=document
                    )
                    vendor.save()
                    messages.success(request, 'Vendor added successfully!')
                    return redirect('employee_dashboard' if request.user.role == 'Employee' else 'finance_dashboard')
                except IntegrityError:
                    # Fallback in case of any other integrity errors
                    messages.error(request, 'An error occurred while adding the vendor. Please try again.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'add_vendor.html')

# Vendor List (For Finance and Admin)
@login_required
def vendor_list(request):
    if request.user.role not in ['Finance', 'Admin']:
        return redirect('home')

    vendors = Vendor.objects.all()

    return render(request, 'vendor_list.html', {
        'vendors': vendors
    })

# Edit Vendor
@login_required
def edit_vendor(request, vendor_id):
    if request.user.role not in ['Finance', 'Admin']:
        return redirect('home')

    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        document = request.FILES.get('document')

        if vendor_name:
            vendor.vendor_name = vendor_name
        
        if document:
            vendor.document = document
        
        vendor.save()
        messages.success(request, 'Vendor details updated successfully!')
        return redirect('vendor_list')

    return render(request, 'edit_vendor.html', {
        'vendor': vendor
    })

# Vendor Details (Finance/Admin can view vendor details)
@login_required
def vendor_detail(request, vendor_id):
    if request.user.role not in ['Finance', 'Admin']:
        return redirect('home')

    vendor = get_object_or_404(Vendor, id=vendor_id)

    return render(request, 'vendor_detail.html', {
        'vendor': vendor
    })
from django.shortcuts import render, get_object_or_404
from .models import Request

# Request Progress Tracker View
def request_progress(request, request_id):
    payment_request = get_object_or_404(Request, id=request_id)
    return render(request, 'request_progress.html', {'request': payment_request})



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RequestForm

from .models import Request, Notification, User
from .models import Request, Notification, User

@login_required
def add_vendor(request):
    if request.user.role not in ['Employee', 'Finance', 'Admin']:
        messages.error(request, 'Unauthorized access.')
        return redirect('home')

    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        vendor_id = request.POST.get('vendor_id')
        type_of_vendor = request.POST.get('type_of_vendor')
        branch = request.POST.get('branch')
        vendor_banking_name = request.POST.get('vendor_banking_name')
        vendor_bank = request.POST.get('vendor_bank')
        vendor_ifsc = request.POST.get('vendor_ifsc')
        vendor_account_number = request.POST.get('vendor_account_number')
        document = request.FILES.get('document')

        if all([vendor_name, vendor_id, type_of_vendor, branch, vendor_banking_name, vendor_bank, vendor_ifsc, vendor_account_number, document]):
            try:
                vendor = Vendor.objects.create(
                    vendor_name=vendor_name, 
                    vendor_id=vendor_id, 
                    type_of_vendor=type_of_vendor,
                    branch=branch,
                    vendor_banking_name=vendor_banking_name,
                    vendor_bank=vendor_bank,
                    vendor_ifsc=vendor_ifsc,
                    vendor_account_number=vendor_account_number,
                    added_by=request.user, 
                    document=document
                )
                vendor.save()
                messages.success(request, 'Vendor added successfully!')
                return redirect('employee_dashboard' if request.user.role == 'Employee' else 'finance_dashboard')

            except IntegrityError:
                # Handle the case where the vendor_id is not unique
                messages.error(request, 'Vendor ID already exists. Please use a unique Vendor ID.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'add_vendor.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Request

@login_required
def view_status(request):
    if request.user.role != 'Employee':
        messages.error(request, 'Unauthorized access')
        return redirect('login')

    # Fetch all requests made by the logged-in user
    requests = Request.objects.filter(employee=request.user).order_by('-created_at')

    return render(request, 'view_status.html', {
        'requests': requests
    })

@login_required
def report(request):
    reports = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        # Filter requests based on date range and status
        reports = Request.objects.filter(
            date_submitted__range=[start_date, end_date]
        )
        
        if status != 'All':
            reports = reports.filter(status=status)

    return render(request, 'reports.html', {'reports': reports})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Request

@login_required

@login_required
def generate_report(request):
    reports = Request.objects.all()  # Start with all requests

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        ticket_number = request.POST.get('ticket_number')

        # Filter by date range if both start_date and end_date are provided
        if start_date and end_date:
            reports = reports.filter(created_at__range=[start_date, end_date])
        elif start_date:  # If only start_date is provided
            reports = reports.filter(created_at__gte=start_date)
        elif end_date:  # If only end_date is provided
            reports = reports.filter(created_at__lte=end_date)

        # Filter by status if a specific status is selected
        if status and status != 'All':
            reports = reports.filter(status=status)

        # Filter by ticket number if provided
        if ticket_number:
            reports = reports.filter(ticket_number=ticket_number)

    # Add pagination
    paginator = Paginator(reports, 15)  # Show 15 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reports.html', {'page_obj': page_obj})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat, Message, User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Chat, Message, User
from django.utils import timezone
import json

# View for listing users to chat with
@login_required
def chat_list_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude current user from chat list
    return render(request, 'chat_list.html', {'users': users})

# View for handling the chat between two users
@login_required
def chat_detail_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Retrieve the chat between the logged-in user and the selected other user
    chat = Chat.objects.filter(participants__in=[request.user, other_user]).distinct()

    if not chat.exists():
        # If no chat exists between the users, create a new chat
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    else:
        chat = chat.first()

    # Retrieve only the messages that are between the logged-in user and the selected other user
    messages = Message.objects.filter(
        chat=chat, 
        sender__in=[request.user, other_user], 
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    return render(request, 'chat_detail.html', {
        'other_user': other_user,
        'messages': messages,
    })

import json
from django.http import JsonResponse

@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            message_text = data.get('message')
            receiver_id = data.get('receiver_id')

            if not message_text or not receiver_id:
                return JsonResponse({'status': 'failed', 'error': 'Invalid data'})

            receiver = get_object_or_404(User, id=receiver_id)
            chat = Chat.objects.filter(participants__in=[request.user, receiver]).distinct()

            if not chat.exists():
                chat = Chat.objects.create()
                chat.participants.add(request.user, receiver)
            else:
                chat = chat.first()

            Message.objects.create(
                chat=chat,
                sender=request.user,
                receiver=receiver,
                text=message_text,
                created_at=timezone.now()
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'status': 'failed'})


#==============================================================================================================================================================
#=================================================================================================================================================================
#=========================================================================================================================================================================
#==============================================================================================================================================================
#=================================================================================================================================================================
#=========================================================================================================================================================================
@login_required
def new_requests(request):
    if request.user.role not in ['Manager', 'Finance']:
        messages.error(request, 'Unauthorized access')
        return redirect('home')

    requests = Request.objects.filter(status='Pending')  # Filter requests with pending status
    return render(request, 'new_requests.html', {'requests': requests})

@login_required
def rejected_requests(request):
    if request.user.role not in ['Manager', 'Finance']:
        messages.error(request, 'Unauthorized access')
        return redirect('home')

    requests = Request.objects.filter(status='Rejected')
    return render(request, 'rejected_requestss.html', {'requests': requests})
@login_required
def approved_requests(request):
    if request.user.role not in ['Manager', 'Finance']:
        messages.error(request, 'Unauthorized access')
        return redirect('home')

    requests = Request.objects.filter(status='Approved')
    return render(request, 'approved_requestss.html', {'requests': requests})
@login_required
def hold_requests(request):
    if request.user.role not in ['Manager', 'Finance']:
        messages.error(request, 'Unauthorized access')
        return redirect('home')

    requests = Request.objects.filter(status='Hold')
    return render(request, 'hold_requests.html', {'requests': requests})
