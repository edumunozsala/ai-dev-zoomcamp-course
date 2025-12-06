# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Todo
from datetime import date

class TodoTests(TestCase):

    def test_todo_list_view(self):
        Todo.objects.create(title="Test Task")
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_create_todo(self):
        response = self.client.post(reverse("todo_create"), {
            "title": "New Task",
            "description": "Details",
            "due_date": "2025-01-01",
            "resolved": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, "New Task")

    def test_edit_todo(self):
        todo = Todo.objects.create(title="Old Title")
        response = self.client.post(reverse("todo_edit", args=[todo.pk]), {
            "title": "Updated Title",
            "description": "",
            "due_date": "",
            "resolved": False,
        })
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Updated Title")

    def test_delete_todo(self):
        todo = Todo.objects.create(title="To Delete")
        response = self.client.post(reverse("todo_delete", args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle_resolved(self):
        todo = Todo.objects.create(title="Toggle Me", resolved=False)
        response = self.client.get(reverse("todo_toggle", args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)

        # Toggle back
        self.client.get(reverse("todo_toggle", args=[todo.pk]))
        todo.refresh_from_db()
        self.assertFalse(todo.resolved)
