from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard routes
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('finance/dashboard/', views.finance_dashboard, name='finance_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('notification/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('manager/approve_requests/', views.approve_requests, name='approve_requests'),
    path('manager/approved_requests/', views.approved_requests, name='approved_requests'),
    path('manager/rejected_requests/', views.rejected_requests, name='rejected_requests'),
    path('logout/', views.logout_view, name='logout'),
    
    path('manager/approve-reject-request/<int:request_id>/', views.approve_reject_request, name='approve_reject_request'),
    
    path('manager/request/<int:request_id>/', views.request_detail, name='request_detail'),
    # Add the view_status URL
    path('view-status/', views.view_status, name='view_status'),

    # Other URLs
    path('add-request/', views.add_request, name='add_request'),
    path('vendor/add/', views.add_vendor, name='add_vendor'),
    path('report/', views.report, name='report'),
    path('generate-report/', views.generate_report, name='generate_report'),  # Add this line
    path('chat/', views.chat_list_view, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail_view, name='chat_detail'),
    path('chat/send/', views.send_message, name='send_message'),
    path('new-requests/', views.new_requests, name='new_requests'),
    path('rejected-requests/', views.rejected_requests, name='rejected_requests'),
    path('approved-requests/', views.approved_requests, name='approved_requests'),
    path('hold-requests/', views.hold_requests, name='hold_requests'),

]
