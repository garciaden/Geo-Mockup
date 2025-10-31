# Lab Software Mockup

This is a basic Flask web application that serves as a UI and workflow template for our senior design lab software project. It demonstrates a modular Flask structure, Bootstrap-based UI, and Docker-based development workflow.

## Features

- Modular Flask app using blueprints (`main`, `auth`, `projects`)
- Bootstrap 5 styling and responsive layout
- Project listing and detail views (mock data)
- User authentication form (mockup)
- Example navigation and dashboard
- Ready for Docker and VS Code Dev Containers

## Project Structure


```
├── app/
│   ├── __init__.py
│   ├── main/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── main/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── auth/
│   ├── projects/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── projects/
│   ├── samples/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── samples/
│   ├── static/
│   │   ├── favicon.png
│   │   └── logo.png
│   └── templates/
│       ├── base.html
│       └── _nav.html
├── config.py
├── myapp.py
├── requirements.txt
├── Dockerfile
├── .devcontainer/
├── .vscode/
└── example.env
```

- **app/**: Main application package (blueprints, templates, static files)
- **config.py**: Configuration classes (uses `.env` if present)
- **myapp.py**: Entrypoint for running the app
- **requirements.txt**: Python dependencies
- **Dockerfile**: Container setup for development/production
- **example.env**: Example environment variables

## Getting Started


### Prerequisites

> **For a complete and up-to-date guide on using Dev Containers in VS Code, including system requirements, installation, and troubleshooting, see the official documentation:**
>
> [VS Code Dev Containers Documentation — Getting Started, System Requirements, and Installation](https://code.visualstudio.com/docs/devcontainers/containers)

#### 1. Visual Studio Code

- [Visual Studio Code (VS Code)](https://code.visualstudio.com/)
   - **Extensions:**
      - [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) <br> (required)
      - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) <br>(recommended for Python syntax highlighting and tools)
      - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) <br> (optional, for Docker integration)

#### 2. Docker (must be installed and running)

<details>
<summary><strong>Platform-specific Docker requirements</strong></summary>

- **Windows:** Docker Desktop 2.0+ on Windows 10 Pro/Enterprise. Windows 10 Home (2004+) requires Docker Desktop 2.3+ and the WSL 2 back-end. (Docker Toolbox is not supported. Windows container images are not supported.)
- **macOS:** Docker Desktop 2.0+.
- **Linux:** Docker CE/EE 18.06+ and Docker Compose 1.21+. (The Ubuntu snap package is not supported.)
- **Remote hosts:** 1 GB RAM is required, but at least 2 GB RAM and a 2-core CPU is recommended.

</details>

> **Note:** You do NOT need to install Python manually. All Python dependencies are handled automatically inside the Dev Container, but Docker must be installed and running on your system.

### VS Code Dev Container (RECOMMENDED)

If you have the Dev Containers extension installed:

1. Open the project folder in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Select **"Dev Containers: Reopen in Container"**.
4. The container will build and VS Code will reload the workspace inside the container.
5. **Set environment variables:**
   - Copy `example.env` to `.env` and edit as needed. This is required for the app to load environment variables, even inside the Dev Container.
6. Open a terminal in VS Code and run:
   ```sh
   python myapp.py
   ```
7. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Local Development

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd lab_software_mockup
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```sh
   python myapp.py
   ```
   - The app will start the Flask development server and be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).
   - You can access it by opening your browser and navigating to `http://127.0.0.1:5000`.

## Customization

- **Add routes:** In the appropriate blueprint’s `routes.py`.
- **Add templates:** Place in `app/templates/` for site-wide templates or the template folder inside of each blueprint subdiretory.
- **Add static files:** Place in `app/static/`.
- **Environment config:** Add a `.env` file for secrets and settings.
