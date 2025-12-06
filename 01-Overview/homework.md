# Introduction to AI-Assisted Development
In this homework, we'll build an application with AI.

You can use any tool you want: ChatGPT, Claude, GitHub Copilot, Codex, Cursor, Antigravity, etc.

With chat-based applications you will need to copy code back-and-forth, so we recommend that you use an AI assistant in your IDE with agent mode.

We will build a TODO application in Django.

The app should be able to do the following:

Create, edit and delete TODOs
Assign due dates
Mark TODOs as resolved
You will only need Python to get started (we also recommend that you use uv).

You don't need to know Python or Django for doing this homework.

## Question 1: Install Django
We want to install Django. Ask AI to help you with that.

What's the command you used for that?
**pip install django**

Chat response:
```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install django
django-admin --version
pip freeze > requirements.txt
```

There could be multiple ways to do it. Put the one that AI suggested in the homework form.

## Question 2: Project and App
Now we need to create a project and an app for that.

Follow the instructions from AI to do it. At some point, you will need to include the app you created in the project.

Chat response:
```text
Here are the standard commands to create a Django project and a Django app, exactly as most AI assistants would suggest:

1. Create a new Django project

Run:

django-admin startproject myproject
django-admin startproject todo_app


This creates a folder called myproject/ with the project settings.

2. Create a new app inside the project

First, move into the project directory:

cd myproject


Then create an app (for example, called todo):

python manage.py startapp todo

3. Add the app to the project

Open:

myproject/settings.py


Find the list called INSTALLED_APPS and add your app:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'todo',   # ← add this
]
```

What's the file you need to edit for that?

**settings.py**
manage.py
urls.py
wsgi.py

## Question 3: Django Models
Let's now proceed to creating models - the mapping from python objects to a relational database.

For the TODO app, which models do we need? Implement them.

Chat Response:
```text
For a simple TODO application, we only need one model: a Todo (or Task) model.

A single TODO item needs:

A title – short text summarizing the task

A description – optional longer text

A due date – DateField or DateTimeField

A resolved flag – whether the task is completed

Auto-tracked metadata like created date and updated date

You can add more (e.g., users, categories), but for this assignment, one model is enough.
```

What's the next step you need to take?

Chat response:
```text
The next step after creating your models is:

✅ Run migrations

Django needs to create the database tables for the models you just defined.

From inside your project directory, run:

python manage.py makemigrations
python manage.py migrate

These commands will:

makemigrations — create migration files based on your model definitions

migrate — apply those migrations to the SQLite database (or whatever DB you use)

After this, your Todo model will have a real table in the database, and you can start building:

forms

views

URL routes

templates

admin integration

Run the application
Add the models to the admin panel
```

**Run migrations**
Create a makefile

## Question 4. TODO Logic
Let's now ask AI to implement the logic for the TODO app. Where do we put it?

Chat response:

```text
1. Create the Views (the “logic” lives here)

Open:

todo/views.py


Replace or add the following:

from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    todos = Todo.objects.all().order_by("resolved", "due_date")
    return render(request, "todo/todo_list.html", {"todos": todos})

def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoForm()
    return render(request, "todo/todo_form.html", {"form": form})

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todo/todo_form.html", {"form": form})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("todo_list")
    return render(request, "todo/todo_confirm_delete.html", {"todo": todo})

def todo_toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save()
    return redirect("todo_list")


This gives you:

list TODOs

create TODO

edit TODO

delete TODO

mark DONE/UNDONE

✅ 2. Create the Form

Create:

todo/forms.py


Add:

from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "due_date", "resolved"]

✅ 3. Wire up the URLs

Inside:

todo/urls.py


Create this file:

from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create/", views.todo_create, name="todo_create"),
    path("<int:pk>/edit/", views.todo_edit, name="todo_edit"),
    path("<int:pk>/delete/", views.todo_delete, name="todo_delete"),
    path("<int:pk>/toggle/", views.todo_toggle_resolved, name="todo_toggle"),
]


Then include it in your project:

Open:

myproject/urls.py


Add:

from django.urls import path, include

urlpatterns = [
    path("todo/", include("todo.urls")),
]

✅ 4. Create Templates

Create a folder:

todo/templates/todo/

todo_list.html
<h1>TODO List</h1>
<a href="{% url 'todo_create' %}">Create New</a>

<ul>
    {% for todo in todos %}
        <li>
            <a href="{% url 'todo_toggle' todo.pk %}">
                {% if todo.resolved %}✔{% else %}❌{% endif %}
            </a>
            {{ todo.title }} — Due: {{ todo.due_date }}

            <a href="{% url 'todo_edit' todo.pk %}">Edit</a>
            <a href="{% url 'todo_delete' todo.pk %}">Delete</a>
        </li>
    {% endfor %}
</ul>

todo_form.html
<h1>TODO Form</h1>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>

todo_confirm_delete.html
<h1>Delete TODO: {{ todo.title }}</h1>

<form method="POST">
    {% csrf_token %}
    <button type="submit">Confirm Delete</button>
</form>

📌 Where do I put everything?
File	Location
Models	todo/models.py
Logic (views)	todo/views.py
Form	todo/forms.py
App routes	todo/urls.py
Templates	todo/templates/todo/*.html
Add app to project routing	myproject/urls.py
Register app	myproject/settings.py → INSTALLED_APPS

```

**views.py**
urls.py
admin.py
tests.py

## Question 5. Templates
Next step is creating the templates. You will need at least two: the base one and the home one. Let's call them base.html and home.html.

Where do you need to register the directory with the templates?

**INSTALLED_APPS in project's settings.py**
TEMPLATES['DIRS'] in project's settings.py
TEMPLATES['APP_DIRS'] in project's settings.py
In the app's urls.py

## Question 6. Tests
Now let's ask AI to cover our functionality with tests.

Ask it which scenarios we should cover
Make sure they make sense
Let it implement it and run them
Probably it will require a few iterations to make sure that tests pass and evertyhing is working.

Chat response:
```text
Scenarios You Should Cover

These tests should make sense for your app and match the logic we implemented earlier.

1. Creating a TODO

A valid POST request creates a new Todo.

After creation, the user is redirected to the list page.

2. Listing TODOs

The list view returns a 200 OK.

Created TODOs appear in the response context.

3. Editing a TODO

A POST request updates the title, description, due date, resolved.

Redirects correctly after saving.

4. Deleting a TODO

POST request deletes the item.

Redirects correctly to the list view.

5. Toggling "resolved" state

Hitting /toggle/ flips resolved from False → True and True → False.

6. Correct templates are used

List view uses todo_list.html

Form view uses todo_form.html

Delete confirmation uses todo_confirm_delete.html
```

What's the command you use for running tests in the terminal?
Chat response:
```text
Run:

python manage.py test
```

pytest
**python manage.py test**
python -m django run_tests
django-admin test
Running the app

Now the application is developed and tested. Run it:
```bash
python manage.py runserver
```

Since we asked AI to test everything, it should just work. If it doesn't, iterate with AI until it works.

## Homework URL
Commit your code to GitHub. You can create a repository for this course. Within the repository, create a folder, e.g. "01-todo", where you put the code.

Use the link to this folder in the homework submission form.

## Tip
You can copy-paste the homework description into the AI system of your choice. But make sure you understand (and follow) all the steps in the response.

## Submission
Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2025/homework/hw1

## Learning in Public
We encourage everyone to share what they learned. This is called "learning in public".

Learning in public is one of the most effective ways to accelerate your growth. Here's why:

Accountability: Sharing your progress creates commitment and motivation to continue
Feedback: The community can provide valuable suggestions and corrections
Networking: You'll connect with like-minded people and potential collaborators
Documentation: Your posts become a learning journal you can reference later
Opportunities: Employers and clients often discover talent through public learning
Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

Example post for LinkedIn:
🚀 Week 1 of AI Dev Tools Zoomcamp by @DataTalksClub complete!

Just built a Django TODO application using AI assistants - without knowing Django beforehand!

Today I learned how to:

✅ Set up Django projects and apps
✅ Create database models and migrations
✅ Implement views and templates
✅ Write comprehensive tests with AI help
Here's my repo:

Following along with this amazing course - who else is exploring AI development tools?

You can sign up here: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/

Example post for Twitter/X:
🤖 Built a Django app with AI in @Al_Grigor's AI Dev Tools Zoomcamp!

✨ TODO app from scratch
📝 Models & migrations
🎨 Views and templates
✅ Tests
My repo:

Zero Django knowledge → working app in one session!

Join me: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/

