from feedbacks.models import Feedback
from django.contrib import admin


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["from_email", "create_date"]


admin.site.register(Feedback, FeedbackAdmin)