from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Finance', 'Finance'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# Request model to handle payment requests made by employees
class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Hold', 'Hold'),
    ]

    VENDOR_TYPE_CHOICES = [
        ('existing_vendor', 'Existing Vendor'),
        ('new_vendor', 'New Vendor'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Employee'})
    vendor_name = models.CharField(max_length=255)
    type_of_vendor = models.CharField(max_length=50, choices=VENDOR_TYPE_CHOICES)  # Dropdown for vendor type
    vendor_code = models.CharField(max_length=100)
    basis_of_request = models.CharField(max_length=255)
    details_of_request = models.TextField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    requested_date_of_payment = models.DateField()
    invoice_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager_approval_at = models.DateTimeField(null=True, blank=True)
    manager_note = models.TextField(blank=True, null=True)
    finance_approval_at = models.DateTimeField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)  # Field for urgency
    notes = models.TextField(blank=True, null=True)
    invoice = models.FileField(upload_to='attachments/', blank=True, null=True)
    ticket_number = models.PositiveIntegerField(unique=True, null=True, blank=True)  # Allow null for initial save

    def save(self, *args, **kwargs):
        # Only assign a ticket number if the object is being created
        if self._state.adding and self.ticket_number is None:
            last_request = Request.objects.order_by('-ticket_number').first()
            
            if last_request and last_request.ticket_number:
                self.ticket_number = last_request.ticket_number + 1
            else:
                self.ticket_number = 10000  # Start ticket numbering from 10000 if no records exist
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request by {self.employee.username} - Status: {self.status}"


# Vendor model to track vendors added by finance or admin
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=100, unique=True)  # Ensure vendor ID is unique
    type_of_vendor = models.CharField(max_length=100)
    branch = models.CharField(max_length=255)
    vendor_banking_name = models.CharField(max_length=255)
    vendor_bank = models.CharField(max_length=255)
    vendor_ifsc = models.CharField(max_length=11)
    vendor_account_number = models.CharField(max_length=50, unique=True)  # Ensure uniqueness
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['Finance', 'Admin']})
    document = models.FileField(upload_to='vendor_docs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor_name} (ID: {self.vendor_id})"


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Custom user model
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username}'






from django.db import models
from django.conf import settings

class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {', '.join([str(p) for p in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
