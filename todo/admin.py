from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from todo.models import Item
from todo.models import List
from todo.models import Priority


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "item_count", "created_at"]
    list_filter = ["owner", "created_at"]
    search_fields = ["title", "description", "owner__username"]
    readonly_fields = ["created_at"]

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Number of Items"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "todo_list",
        "priority_badge",
        "due_date_status",
        "completed",
        "created_at",
    ]
    list_filter = ["completed", "priority", "todo_list", "created_at"]
    search_fields = ["title", "description", "todo_list__title"]
    readonly_fields = ["created_at"]
    list_editable = ["completed"]
    ordering = ["due_date", "-priority"]

    def priority_badge(self, obj):
        colors = {
            Priority.HIGH: "red",
            Priority.MEDIUM: "orange",
            Priority.LOW: "green",
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',  # noqa
            colors[obj.priority],
            obj.get_priority_display(),
        )

    priority_badge.short_description = "Priority"

    def due_date_status(self, obj):
        if not obj.due_date:
            return "-"
        if obj.completed:
            return "Completed"

        now = timezone.now()
        if obj.due_date < now:
            return format_html('<span style="color: red;">Overdue</span>')
        elif obj.due_date.date() == now.date():
            return format_html('<span style="color: orange;">Due today</span>')
        return format_html('<span style="color: green;">Upcoming</span>')

    due_date_status.short_description = "Status"

    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "todo_list")}),
        ("Status", {"fields": ("completed", "priority", "due_date")}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(todo_list__owner=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "todo_list" and not request.user.is_superuser:
            kwargs["queryset"] = List.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
