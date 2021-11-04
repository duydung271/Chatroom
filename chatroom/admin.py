from django.contrib import admin

from chatroom.models import Message, Room

# Register your models here.
class TaskInline(admin.TabularInline):
    model = Message
    extra = 3

class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Room",{'fields': ['room_name','participants','password','host']}),
    ]
    inlines = [TaskInline]

admin.site.register(Room, RoomAdmin)