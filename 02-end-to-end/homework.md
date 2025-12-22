# End-to-End Application Development

In this homework, we'll build an end-to-end application with AI.

You can use any tool you want: ChatGPT, Claude, GitHub Copilot, Codex, Cursor, Antigravity, etc.

With chat-based applications you will need to copy code back-and-forth, so we recommend that you use an AI assistant in your IDE with agent mode.

We will implement a platform for online coding interviews.

The app should be able to do the following:

- Create a link and share it with candidates
- Allow everyone who connects to edit code in the code panel
- Show real-time updates to all connected users
- Support syntax highlighting for multiple languages
- Execute code safely in the browser

You can choose any technologies you want. For example:

- Frontend: React + Vite
- Backend: Express.js

We recommend using JavaScript for frontend, because with other technologies, some of the homework requirements may be difficult to implement.

But you can experiment with alternatives, such as Streamlit.

You don't need to know these technologies for doing this homework.


## Question 1: Initial Implementation

Ask AI to implement both frontend and backend - in one prompt.

Note: you can also follow the same path as in the videos and make it in 3 steps:

1. Frontend
2. OpenAPI specs
3. Backend

What's the initial prompt you gave to AI to start the implementation?

Copy and paste it in the homework form.

```text
create a platform for online coding interviews. It will have the following functionalities: create a link and share it with candidates,allow everyone who connects to edit code in the code panel, show real-time updates to all connected users, support syntax highlighting for multiple languages, execute code safely in the browser. Add mockups for those functionalities and also for log in. everything should be interactive. Make sure that all the logic is covered with unit tests.
Create the frontend with React and Javascript. Don't implement backend, so everything is mocked. But centralize all the calls to the backend in one place

API Specification prompt
analyse the content of the frontend client app (frontend folder) for code interviewing and create an OpenAPI specs based on what it needs. later we want to implement backend based on these specs.

Backend
based on the OpenAPI specs, create fastapi backend (backend folder)for now use a mock database, which we will later replace with a real one create tests to make sure the implementation Works.
follow the guidelines in AGENTS.md. And implement a verify_api.py script that tests the running server to ensure all endpoints work correctly.
```

## Question 2: Integration Tests

Maybe at this point your application will already function. Maybe not. But it's always a good idea to cover it with tests.

We usually do it even before trying to run the application because it helps to resurface all the problems with implementation.

Ask AI to write integration tests that check that the interaction between client and server works.

Also it's a good idea to ask it to start creating a `README.md` file with all the commands for running and testing your application.

```text
We now have backend. Lets connect it to frontend. Prompt:

Make frontend use backend. use OpenAPI specs for guidance follow the guidelines in AGENTS.md.We also need a way to run them both at the same tile
```

What's the terminal command you use for executing tests?
**npm run test:integration**

## Question 3: Running Both Client and Server

Now let's make it possible to run both client and server at the same time. Use `concurrently` for that.

```text
How can I run both frontend and backend at the same time? Let's use concurrently instead of our own script

 "dev": "concurrently \"npm run server\" \"npm run client\" --names \"SERVER,CLIENT\" --prefix-colors \"blue,green\" --kill-others",
    "server": "cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
    "client": "cd frontend && npm run dev",
    "test": "echo \"Error: no test specified\" && exit 1"
```

What's the command you have in `package.json` for `npm dev` for running both?

```text
 "dev": "concurrently \"npm run server\" \"npm run client\" --names \"SERVER,CLIENT\" --prefix-colors \"blue,green\" --kill-others",
```

## Question 4: Syntax Highlighting

Let's now add support for syntax highlighting for JavaScript and Python.

```text
Now, add support for syntax highlighting for JavaScript and Python on the frontend app.And follow the guidelines in AGENTS.md

I have created a plan to add syntax highlighting using prismjs and react-simple-code-editor. Please review the implementation plan.
```

Which library did AI use for it?
**Prism.js**

## Question 5: Code Execution

Now let's add code execution.

For security reasons, we don't want to execute code directly on the server. Instead, let's use WASM to execute the code only in the browser.

Which library did AI use for compiling Python to WASM?
**py2wasm**

## Question 6: Containerization

Now let's containerize our application. Ask AI to help you create a Dockerfile for the application. Put both backend and frontend in one container.

```text
Now let's containerize our application. Create a Dockerfile for the application. Put both backend and frontend in one container and also use postgres as the database for our backend server.  we can serve frontend with nginx or whatever you recommend. And follow the guidelines in AGENTS.md.
```

What's the base image you used for your Dockerfile?
**node:20-alpine**


## Question 7: Deployment

Now let's deploy it. Choose a service to deploy your application.

```text
For deployment we need to put together backend and frontend in one container. I want to deploy it to the cloud now. what are the options
```
Which service did you use for deployment?
**Render**

## Homework URL

Commit your code to GitHub. You can create a repository for this course. Within the repository, create a folder, e.g. "02-coding-interview", where you put the code.

## Tip

You can copy-paste the homework description into the AI system of your choice. But make sure you understand (and follow) all the steps in the response.
