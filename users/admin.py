from django.contrib import admin
from .models import CustomUser, PhoneNumber, SpamAction, UserContact

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "spam_likelihood"]

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone_number", "is_superuser"]

class UserContactAdmin(admin.ModelAdmin):
    list_display = ["user", "contact_name", "phone_number"] 

class SpamActionAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "is_marked_as_spam"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(SpamAction, SpamActionAdmin)
admin.site.register(UserContact, UserContactAdmin)
