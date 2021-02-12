from django.contrib import admin

from .models import CallbackRequest, FeedbackRequest


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['datetime_created']
    search_fields = ['name', 'phone', 'comment']
    list_display = [
        'datetime_created',
        'phone',
        'name',
    ]


@admin.register(FeedbackRequest)
class FeedbackRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['datetime_created']
    search_fields = ['name', 'email', 'comment']
    list_filter = ['msg_type']
    list_display = [
        'datetime_created',
        'email',
        'name',
        'msg_type',
    ]