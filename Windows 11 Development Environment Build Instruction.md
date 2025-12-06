# Windows 11 Development Environment Build Instructions

## Complete guide to building a development environment

 This guide will help build a complete X.com bookmarklet management tool development environment from scratch on Windows 11 with a technology stack that includes Next.js + Tailwind CSS (front-end), Python + FastAPI (back-end), Supabase (database), and Docker (containerization).
 
### System Requirements

- Windows 11 operating system
- Administrator privileges
- At least 16GB RAM (32GB recommended)
- At least 40GB of free disk space
- Stable Internet connection

## Basic Environment Installation

### Enabling WSL2

 WSL2 is the foundation for running Linux containers on Windows, and Docker Desktop relies on it to run. [^4](https://blog.codoplex.com/how-to-set-up-docker-desktop-with-wsl2-on-windows-for-fastapi-apps-step-by-step-guide/)

 Open PowerShell as administrator and execute the following command:

```powershell
wsl --install

```

 The system will automatically install the Ubuntu distribution, and you will need to reboot your computer after the installation is complete. The first time you open Ubuntu after the reboot, you need to create a Linux username and password (remember these credentials). [^4](https://dev.to/tigerfanxiao/build-python-docker-development-environment-on-win11-from-scratch-593d) 

 Verify the WSL2 installation:

```powershell
wsl --list --verbose

```

 Ensure that the Ubuntu version is displayed as 2. [^5](https://blog.codoplex.com/how-to-set-up-docker-desktop-with-wsl2-on-windows-for-fastapi-apps-step-by-step-guide/)

### Enable virtualization technology

 In Task Manager press Ctrl+Shift+Esc, click on the Performance tab, select CPU and check that "Virtualization: Enabled" is displayed at the bottom. [^5](https://blog.codoplex.com/how-to-set-up-docker-desktop-with-wsl2-on-windows-for-fastapi-apps-step-by-step-guide/)

 If it is not enabled, you need to reboot your computer into BIOS (usually press F2, DEL or ESC), find the Virtualization Technology (VT-x or AMD-V) option and enable it, save and exit. [^5](https://blog.codoplex.com/how-to-set-up-docker-desktop-with-wsl2-on-windows-for-fastapi-apps-step-by-step-guide/)

### Step 1: Install the base tools

### 1.1 Install Git

 Visit the Git official website to download the installer:

```bash
# Download address
<https://git-scm.com/download/win>

```

 Installation Steps:

- Download the 64-bit Windows version of the Git installer
- Run the installer and select the default options
- At the "Adjusting your PATH environment" step, select "Git from the command line and also from 3rd-party software".
- Select "Use bundled OpenSSH" in "Choosing the SSH executable".
- Choose "Use the OpenSSL library" for "Choosing the HTTPS transport backend".
- Leave the other options as  [default^3](https://code.visualstudio.com/docs/setup/windows)

 Verify the installation:

```bash
git --version

```

 Configure Git user information:

```bash
git config --global user.name "<Your Name>"
git config --global user.email "<Your email address>"

```

### 1.2 Installing Node.js and npm

 Visit the Node.js website to download the LTS version:

```bash
# Download address
<https://nodejs.org/>

```

 Installation Steps:

- Download the Windows Installer (.msi) LTS version (20.x or higher recommended).
- Run the installer
- Check the "Automatically install the necessary tools" box.
- Restart the command line terminal after the installation is complete [^4](https://code-b.dev/blog/tailwind-css-next-js)

 Verify the installation:

```bash
node -v
npm -v

```

### 1.3 Installing Python (Python 3.13.7 was automatically installed when Node.js was previously installed and pip has installed the latest version 25.2)

 Visit the official Python website to download the installer:

```bash
# Download address
<https://www.python.org/downloads/>

```

 Installation Steps:

- Download the Windows installer for Python version 3.11 or 3.12
- **Important**: When running the installer, check the "Add Python to PATH" box.
- Select "Install Now" for a standard installation.
- Restart the command line terminal after the installation is complete [^7](https://fastapi.tiangolo.com/deployment/docker/)

 Verify the installation:

```bash
python --version
pip --version

```

### 1.4 Installing Visual Studio Code

 Visit the VSCode website to download the installer:

```bash
# Download address
<https://code.visualstudio.com/>

```

 Installation Steps:

- Download the user installer for Windows (VSCodeUserSetup-{version}.exe)
- Run the installer
- Check in the installation options:
    - "Add to PATH" (important)
    - "Create a desktop icon" (optional)
    - "Register Code as an editor for supported file types"
    - "Add 'Open with Code' action to Windows Explorer file context menu"
    - "Add 'Open with Code' action to Windows Explorer directory context menu"
- Completing the installation [^8](https://code.visualstudio.com/docs/setup/windows)

 Verify the installation:

```bash
code --version

```

### 1.5 Installing Docker Desktop

 Visit the official Docker website to download the installer:

```bash
# Download address
<https://www.docker.com/products/docker-desktop/>

```

 Installation Steps:

- Download Docker Desktop for Windows
- Run the installer
- Check the "Use WSL 2 instead of Hyper-V" option (recommended).
- Restart your computer after the installation is complete
- Start Docker Desktop and complete the initial setup.
- Accept the Terms of  [Service^5](https://www.youtube.com/watch?v=mNpG1zg1QFc)

 Verify the installation:

```bash
docker --version
docker-compose --version

```

 Test Docker operation:

```bash
docker run hello-world

```

### Step 2: Configure the VSCode development environment

### 2.1 Install the required VSCode extensions

 Open VSCode and press `Ctrl+Shift+X` to open the extensions panel, search and install the following extensions:

**General Development Extensions**:

- `GitLens` - Git enhancement tool
- `Git Graph` - Git commit history visualization
- `Docker` - Docker container management
- `Remote - Containers` - In-container development support (this reads: Remote - Development (Extension Pack: WSL, Dev Containers))

**Front-end development extensions**:

- `ES7+ React/Redux/React-Native snippets` - React code snippets
- `Tailwind CSS IntelliSense` - Tailwind CSS IntelliSense
- `PostCSS Language Support` - PostCSS Syntax Support
- `Prettier - Code formatter` - Code formatting tool
- `ESLint` - JavaScript/TypeScript code inspections

**Python Development Extensions**:

- `Python` - Python Language Support (Official Microsoft)
- `Pylance` - Python High Level Language Server
- `Python Debugger` - Python debugging tool
- `Black Formatter` - Python code formatting tool
- `Ruff` - Fast Python linter

**Other useful extensions**:

- `Thunder Client` - API testing tool
- `Better Comments` - Enhanced comment display
- `Auto Rename Tag` - Automatic renaming of HTML/XML tags
- `Path Intellisense` - path auto-completion [^9](https://code.visualstudio.com/docs/setup/windows)

I've added the following plugins myself:

- Error Lens - highlights errors and warnings in the code, not only in the issue panel, but also directly in the editor
- Material Icon Theme - provides a nice icon theme for VSCode files and folders
- Rainbow CSV - Specialized for highlighting and analysis of CSV/TSV files.
- VSCode PDF - view PDF files directly inside VSCode

### 2.2 Configuring VSCode Settings

 Press `Ctrl+,to open` settings, or create/modify `.vscode/settings.json` file:

 Add in the settings JSON (Ctrl+Shift+P, type "Preferences: Open User Settings (JSON)")

I've modified the following file slightly

```json
{
  "editor.cursorBlinking": "expand",
  "editor.cursorSmoothCaretAnimation": "on",
  "editor.wordWrap": "on",
  "workbench.iconTheme": "material-icon-theme",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "editor.tabSize": 2,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.tabSize": 4
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": false,
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ],
  "explorer.confirmDragAndDrop": false,
  "explorer.confirmDelete": false,
  "git.enableSmartCommit": true,
  "python.terminal.useEnvFile": true
}

```

### Step 3: Create the project directory structure

### 3.1 Creating the Project Root Directory

```bash
# Open Command Prompt or PowerShell
mkdir C:\\Projects\\x-bookmark-manager
cd C:\\Projects\\x-bookmark-manager

# Initialize Git repository
git init

# Create .gitignore file
New-Item -Path .gitignore -ItemType File

```

 Edit the `.gitignore` file:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/

# Node
node_modules/
.next/
out/
.npm
.eslintcache

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Docker
*.log

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite

```

### Step 4: Build the backend development environment (Python + FastAPI)

### 4.1 Create the backend directory

```bash
mkdir backend
cd backend

```

### 4.2 Create a Python Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment（Windows PowerShell）
.\\venv\\Scripts\\Activate.ps1

# If you encounter an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use the Command Prompt (CMD) to activate：
.\\venv\\Scripts\\activate.bat

```

 Verify the virtual environment:

```bash
Get-Command python  # The Python path in the venv directory should be displayed, such as "C:\<Your Project>\backend\venv\Scripts\python.exe". If it is not, press Command + Shift + P, enter "Python: Select Interpreter" in the command palette, and VSCode will list all the Python interpreters it can find. Please select the one with the .venv path. It is usually marked as Recommended.

```

### 4.3 Install backend dependencies

 Create the `requirements.txt` file:

```
fastapi[standard]>=0.115.0,<0.116.0
uvicorn[standard]>=0.30.0,<0.31.0
tweepy>=4.14.0,<5.0.0
psycopg2-binary>=2.9.9,<3.0.0
python-dotenv>=1.0.0,<2.0.0
pydantic>=2.7.0,<3.0.0
pydantic-settings>=2.3.0,<3.0.0
httpx>=0.27.0,<0.28.0
python-multipart>=0.0.9,<0.1.0

```

 Install the dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

 Verify the installation:

```bash
pip list

```

### 4.4 Creating the back-end base file structure

```bash
# Create the following structure in the backend directory
mkdir app
mkdir app\\api
mkdir app\\core
mkdir app\\models
mkdir app\\services
mkdir app\\schemas

# Create initialization file
New-Item -Path app\\__init__.py -ItemType File
New-Item -Path app\\api\\__init__.py -ItemType File
New-Item -Path app\\core\\__init__.py -ItemType File
New-Item -Path app\\models\\__init__.py -ItemType File
New-Item -Path app\\services\\__init__.py -ItemType File
New-Item -Path app\\schemas\\__init__.py -ItemType File

```

### 4.5 Creating the base FastAPI application

 Creating `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="X Bookmark Manager API",
    description="API for managing X.com bookmarks",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "X Bookmark Manager API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Static frontend files will be mounted later
# if os.path.exists("../frontend/out"):
#     app.mount("/", StaticFiles(directory="../frontend/out", html=True), name="static")

```

 Creating the `.env` file:

```bash
# FastAPI Configuration
APP_NAME=X-Bookmark-Manager
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# X API Configuration
X_API_KEY=your_x_api_key_here
X_API_SECRET=your_x_api_secret_here
X_ACCESS_TOKEN=your_x_access_token_here
X_ACCESS_SECRET=your_x_access_secret_here
X_BEARER_TOKEN=your_x_bearer_token_here

```

 Creating `app/core/config.py`:

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="X-Bookmark-Manager")
    debug: bool = Field(default=True)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    supabase_url: str = Field(default="")
    supabase_key: str = Field(default="")

    x_api_key: str = Field(default="")
    x_api_secret: str = Field(default="")
    x_access_token: str = Field(default="")
    x_access_secret: str = Field(default="")
    x_bearer_token: str = Field(default="")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

```

### 4.6 Testing the backend run

```bash
# Ensure you are in the backend directory and the virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

 Access in browser:

- `http://localhost:8000` - view root path response
- `http://localhost:8000/docs` - view auto-generated API documentation (Swagger UI)
- `http://localhost:8000/redoc` - view ReDoc format documentation [^10](https://fastapi.tiangolo.com/deployment/docker/)

### Step 5: Build the front-end development environment (Next.js + Tailwind CSS)

### 5.1 Return to project root and create Next.js application

```bash
# Return to the project root directory
cd ..

# Create a Next.js application (using TypeScript and App Router)
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

```

 Options selection during installation:

- Would you like to use TypeScript?
- Would you like to use ESLint?
- Would you like to use Tailwind CSS?
- Would you like to use `src/` directory?
- Would you like to use App Router?
- Would you like to customize the default import alias (@/*)? →  [No^6](https://nextjs.org/docs/app/guides/tailwind-v3-css)

### 5.2 Entering the frontend directory and installing additional dependencies

```bash
cd frontend
npm install axios swr
npm install -D @types/node

```

### 5.3 Configuring Tailwind CSS

 Create `tailwind.config.ts`: (there is only one next.config.ts by default, so I created`tailwind.config.ts`myself)

```tsx
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
};
export default config;

```

 Verify that `src/app/globals.css` contains the Tailwind directive:

```css
@import "tailwindcss"; //In v4, if you need the complete Tailwind (including theme layer, preset reset Preflight, utility classes), keeping just this line is sufficient

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
}

```

### 5.4 Configuring Environment Variables

 Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000

```

### 5.5 Creating the API client

 Create `src/lib/api.ts:`

```tsx
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

```

### 5.6 Modify the homepage for testing

 Create `src/app/page.tsx`: (rename original page.tsx to page_original.tsx)

```tsx
'use client';

import { useEffect, useState } from 'react';
import apiClient from '@/lib/api';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...');

  useEffect(() => {
    apiClient.get('/health')
      .then(res => setApiStatus(`Backend connection successful: ${res.data.status}`))
      .catch(() => setApiStatus('Backend connection failed'));
  }, []);

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-4">X Bookmark Manager</h1>
      <p className="text-lg">{apiStatus}</p>
    </main>
  );
}

```

### 5.7 Test the front-end operation

```bash
# Run in the frontend directory
npm run dev

```

 Visit `http://localhost:3000` in your browser `and` you should see the page and display the backend connection status. [^11](https://nextjs.org/docs/app/guides/tailwind-v3-css)

### 5.8 Configure static export (for Docker deployment)

 Edit `next.config.ts`:

```tsx
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

```

 Test static export:

```bash
npm run build
# An `out` directory will be generated, containing all static files
```

### Step 6: Configure the Supabase database

### 6.1 Create a Supabase project

 Visit `https://supabase.com and register an account to` create a new project:

- Select an organization or create a new one
- Enter the project name: `x-bookmark-manager`
- Set the database password (be sure to save it)
- Select the region (the most recent region is recommended)
- Click on "Create new project"

### 6.2 Getting Connection Information

 Get the connection information in the project settings:

- Project URL (API URL)
- anon/public key (API Key)
- Update this information in the `backend/.env` file `.`

### 6.3 Creating the database table structure

 Execute it in the SQL editor of the Supabase console:

```sql
-- Create bookmark table
CREATE TABLE bookmarks (
    tweet_id TEXT PRIMARY KEY,
    text TEXT,
    author_id TEXT,
    author_name TEXT,
    author_handle TEXT,
    author_avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    bookmarked_at TIMESTAMP WITH TIME ZONE,
    original_url TEXT,
    media_urls JSONB,
    local_tags TEXT[],
    local_folder_id TEXT,
    local_notes TEXT,
    sync_status TEXT DEFAULT 'synced',
);

-- Create folder table
CREATE TABLE folders (
    folder_id TEXT PRIMARY KEY,
    folder_name TEXT NOT NULL,
    parent_folder_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create a bookmark table
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    tag_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes to optimize query performance
CREATE INDEX idx_bookmarks_author ON bookmarks(author_id);
CREATE INDEX idx_bookmarks_created_at ON bookmarks(created_at DESC);
CREATE INDEX idx_bookmarks_sync_status ON bookmarks(sync_status);
CREATE INDEX idx_bookmarks_local_tags ON bookmarks USING GIN(local_tags);

```

### 6.4 Install the Supabase Python client

 In the backend directory:

```bash
pip install "supabase>=2.0.0,<3.0.0"
pip freeze > requirements.txt

```

 Create `app/core/database.py`:

```python
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """Create Supabase client instance"""
    return create_client(settings.supabase_url, settings.supabase_key)

supabase_client = get_supabase_client()

```

### Step 7: Configure Docker Containerization

### 7.1 Create a Dockerfile in the project root directory

 Create `the Dockerfile`:

```docker
# Using the official Python 3.11 image as the base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy backend dependency files
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend ./backend

# Copy front-end build artifacts (requires local build first)
COPY frontend/out ./frontend/out

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=7860

# Start command
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]

```

### 7.2 Create .dockerignore

 Create `.dockerignore`:

```
# Python
**/__pycache__
**/*.pyc
**/*.pyo
**/*.pyd
**/.Python
**/venv
**/env
**/.venv

# Node
**/node_modules
**/.next
**/npm-debug.log*

# Git
.git
.gitignore

# IDE
.vscode
.idea
*.swp

# Environment
**/.env
**/.env.local

# Documentation
*.md
LICENSE

# Docker
Dockerfile
.dockerignore
docker-compose.yml

```

### 7.3 Creating docker-compose.yml (for local development)

 Creating `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "7860:7860"
    environment:
      - DEBUG=True
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - X_API_KEY=${X_API_KEY}
      - X_API_SECRET=${X_API_SECRET}
      - X_ACCESS_TOKEN=${X_ACCESS_TOKEN}
      - X_ACCESS_SECRET=${X_ACCESS_SECRET}
      - X_BEARER_TOKEN=${X_BEARER_TOKEN}
    env_file:
      - backend/.env
    volumes:
      - ./backend:/app/backend
    command: uvicorn backend.app.main:app --host 0.0.0.0 --port 7860 --reload

```

### 7.4 Testing Docker builds locally

```bash
# First, build the front-end static files
cd frontend
npm run build
cd ..

# Build the Docker image, please ensure Docker Desktop is running before proceeding
docker build -t x-bookmark-manager .

# Run Docker container
docker run -d -p 7860:7860 --env-file backend/.env --name x-bookmark-app x-bookmark-manager

# View Log
docker logs -f x-bookmark-app

# Stop container
docker stop x-bookmark-app

# Delete container
docker rm x-bookmark-app

```

 Or use docker-compose:

```bash
# Start service
docker-compose up --build

# Running in the background
docker-compose up -d

# Stop service
docker-compose down

```

 Visit `http://localhost:7860 Test application.`[^12^5](https://fastapi.tiangolo.com/deployment/docker/)

### Step 8: Configure X API and Tweepy

### 8.1 Get X API credentials

 Visit `https://developer.x.com and execute:`

- Apply for a developer account
- Create new projects and applications
- Generate API Keys and Tokens:
    - API Key
    - API Secret Key
    - Access Token
    - Access Token Secret
    - Bearer Token
- Ensure the application has Read and Write permissions
- Update the credentials to the `backend/.env` [file^2](https://www.notion.so/Xu-Qiu-Gui-Ge-Shuo-Ming-Shu-_-SRS.pdf)

### 8.2 Creating the Tweepy service module

 Create `app/services/twitter_service.py`:

```python
import tweepy
from typing import List, Dict, Optional
from app.core.config import settings

class TwitterService:
    def __init__(self):
        # OAuth 1.0a Authentication
        self.auth = tweepy.OAuthHandler(
            settings.x_api_key,
            settings.x_api_secret
        )
        self.auth.set_access_token(
            settings.x_access_token,
            settings.x_access_secret
        )

        # OAuth 2.0 Bearer Token Authentication
        self.client = tweepy.Client(
            bearer_token=settings.x_bearer_token,
            consumer_key=settings.x_api_key,
            consumer_secret=settings.x_api_secret,
            access_token=settings.x_access_token,
            access_token_secret=settings.x_access_secret,
            wait_on_rate_limit=True
        )

    async def get_bookmarks(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: Optional[str] = None
    ) -> Dict:
        """Get user bookmarks"""
        try:
            response = self.client.get_bookmarks(
                max_results=max_results,
                pagination_token=pagination_token,
                expansions=['author_id', 'attachments.media_keys'],
                tweet_fields=['created_at', 'text', 'author_id', 'entities'],
                user_fields=['name', 'username', 'profile_image_url'],
                media_fields=['url', 'preview_image_url']
            )
            return response
        except Exception as e:
            print(f"Error fetching bookmarks: {e}")
            return None

    async def delete_bookmark(self, tweet_id: str) -> bool:
        """Delete bookmark"""
        try:
            self.client.remove_bookmark(tweet_id)
            return True
        except Exception as e:
            print(f"Error deleting bookmark {tweet_id}: {e}")
            return False

# Create a singleton instance
twitter_service = TwitterService()

```

### 8.3 Creating the Bookmarks API Route

 Create `app/api/bookmarks.py`:

```python
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.twitter_service import twitter_service
from app.core.database import supabase_client
from typing import Optional

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])

@router.get("/")
async def get_all_bookmarks(
    limit: int = 100,
    offset: int = 0
):
    """Get all bookmarks stored locally"""
    try:
        response = supabase_client.table("bookmarks") \
            .select("*") \
            .order("bookmarked_at", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        return {"bookmarks": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/start")
async def start_sync(background_tasks: BackgroundTasks):
    """Start bookmark synchronization task"""
    # This will execute the synchronization logic in the background task
    return {"message": "Sync started", "status": "processing"}

@router.get("/sync/status")
async def get_sync_status():
    """Query synchronization task status"""
    return {"status": "idle", "progress": 0}

```

 Register the route in `app/main.py`:

```python
from app.api import bookmarks

app.include_router(bookmarks.router)

```

### Step 9: Create Development Workflow Scripts

### 9.1 Creating a Startup Script

 Create `scripts/start-dev.ps1` (PowerShell script):

```powershell
# Starting the development environment

Write-Host "Starting X Bookmark Manager Development Environment..." -ForegroundColor Green

# Start backend
Write-Host "`nStarting Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\\venv\\Scripts\\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait 2 seconds
Start-Sleep -Seconds 2

# Start frontend
Write-Host "`nStarting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`nDevelopment servers starting..." -ForegroundColor Green
Write-Host "Backend: <http://localhost:8000>" -ForegroundColor Cyan
Write-Host "Frontend: <http://localhost:3000>" -ForegroundColor Cyan
Write-Host "API Docs: <http://localhost:8000/docs>" -ForegroundColor Cyan

```

 Create `scripts/start-dev.bat` (batch script):

```
@echo off
echo Starting X Bookmark Manager Development Environment...

start cmd /k "cd backend && .\\venv\\Scripts\\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start cmd /k "cd frontend && npm run dev"

echo Development servers starting...
echo Backend: <http://localhost:8000>
echo Frontend: <http://localhost:3000>
echo API Docs: <http://localhost:8000/docs>

```

### 9.2 Creating build scripts

 Create `scripts/build.ps1`:

```powershell
# Building the complete application

Write-Host "Building X Bookmark Manager..." -ForegroundColor Green

# Building the frontend
Write-Host "`nBuilding Frontend..." -ForegroundColor Yellow
cd frontend
npm run build
cd ..

# Building Docker Image
Write-Host "`nBuilding Docker Image..." -ForegroundColor Yellow
docker build -t x-bookmark-manager:latest .

Write-Host "`nBuild completed successfully!" -ForegroundColor Green

```

### Step 10: Version Control and Git Workflow  (This part can be omitted)

### 10.1 Creating a Git repository structure

```bash
# In the project root directory
git add .
git commit -m "Initial commit: Project setup complete"

# Create development branch
git branch develop
git checkout develop

```

### 10.2 Creating a Remote Repository

 Create the remote repository in GitHub/GitLab, then:

```bash
git remote add origin https://github.com/joefeng2000/x-bookmark-manager.git
git push -u origin master
git push -u origin develop

```

### Step 11: Preparing for Hugging Face Spaces Deployment

### 11.1 [Creating the README.md](http://xn--readme-hn3jk46f.md/)

 Create the `README.md` in the project root directory:

```markdown
---
title: X Bookmark Manager
emoji: 🔖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# X Bookmark Manager

High-performance, private X.com bookmark management tool

```

### Step 12: Environment Validation Checklist

 After completing the above steps, verify the:

**Base environment**:

- [ ]  Git version is correct ( `git --version` )
- [ ]  Node.js version is correct ( `node -v`, should be 20.x or higher)
- [ ]  Python version is correct ( `python --version`, should be 3.11 or 3.12)
- [ ]  Docker is running properly ( `docker --version` )
- [ ]  VSCode is installed and extensions are configured

**Backend Environment**:

- [ ]  Python virtual environment has been created and activated
- [ ]  All backend dependencies are installed ( `pip list` )
- [ ]  FastAPI application is ready to run locally (visit `http://localhost:8000/docs)`
- [ ]  Supabase connection is configured correctly

**Front-end environment**:

- [ ]  Node modules are installed ( `frontend/node_modules` exist)
- [ ]  Next.js development server is working (visit `http://localhost:3000)`
- [ ]  Tailwind CSS works fine (styles are applied correctly)
- [ ]  Frontend can communicate with backend API

**Docker environment**:

- [ ]  Dockerfile build was successful ( `docker build` )
- [ ]  Container can run ( `docker run` )
- [ ]  The application inside the container can be accessed

**Database environment**:

- [ ]  Supabase project created
- [ ]  Database tables have been created
- [ ]  Connection credentials are configured

**API Environment**:

- [ ]  X Developer account has been requested
- [ ]  API credentials have been obtained and configured
- [ ]  Tweepy can connect to X API

### Troubleshooting

### Python virtual environment activation failed

 If you encounter a PowerShell execution policy error:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

### Docker Desktop failed to start

 Make sure:

- "Virtual Machine Platform" and "WSL 2" are enabled in the Windows features.
- Restart the computer and try again

### Port is occupied

 If port 3000 or 8000 is occupied:

```bash
# Find the process occupying the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# End process (using process ID)
taskkill /PID <Process ID> /F

```

### Node module installation failed

 Try clearing the cache:

```bash
npm cache clean --force
rm -rf node_modules
rm package-lock.json
npm install

```

### Development Environment Instructions

### Daily Development Process

1. **Start the development environment**:
    - Run `scripts/start-dev.ps1` or `scripts/start-dev.bat`
    - Or manually start the backend and frontend in two separate terminals
2. **Coding**:
    - Use VSCode to open the project root directory
    - Backend code is in `backend/app` directory
    - Frontend code in `frontend/src` directory
3. **Testing API**:
    - Visit `http://localhost:8000/docs使用Swagger` UI test
    - Or use the Thunder Client extension to test within VSCode
4. **View frontend**:
    - Visit `http://localhost:3000`
    - Automatic hot reloading after code changes
5. **Commit code**:

```bash
git add .
git commit -m "Descriptive commit message"
git push origin develop

```

### Build the production version

```bash
# Run the build script
.\\scripts\\build.ps1

# or execute manually
cd frontend
npm run build
cd ..
docker build -t x-bookmark-manager:latest .

```
