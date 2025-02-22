from django.utils import timezone
from rest_framework import serializers

from todo.models import Item
from todo.models import List


class ItemSerializer(serializers.ModelSerializer):
    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "due_date",
            "completed",
            "priority",
            "list",
        ]
        read_only_fields = ["created_at"]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = List
        fields = ["id", "title", "description", "created_at", "owner", "items"]
        read_only_fields = ["created_at"]
