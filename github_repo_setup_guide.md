# Turning a Local Folder into a GitHub Repository

This document outlines the standard steps to initialize your local folder as a Git repository, commit your code, and push it to a new remote repository on GitHub.

## Prerequisites
1. **Git** is installed on your computer. (Check by running `git --version` in your terminal).
2. You have a **GitHub account**.

---

## Step 1: Initialize the Local Repository
First, you need to tell Git to start tracking the files in your current folder. 

1. Open your terminal (or command prompt/PowerShell).
2. Ensure you are in the project's root folder:
   ```bash
   cd c:\Users\alarc\Developer\Workspace\projects\InternshipScraper
   ```
3. Initialize the repository:
   ```bash
   git init
   ```
   *This creates a hidden `.git` folder in your project directory.*

## Step 2: Add and Commit Your Files
Next, stage your files (prepare them to be saved) and commit them (save a snapshot).

1. Before adding files, it's good practice to have a `.gitignore` file to ignore things like `__pycache__`, virtual environments (e.g., `venv/`), or sensitive `.env` files.
2. Stage all your project files:
   ```bash
   git add .
   ```
3. Commit the changes with a clear message:
   ```bash
   git commit -m "Initial commit: Set up project structure"
   ```

## Step 3: Create the Repository on GitHub
Now, create a destination for your code on the internet.

1. Go to [GitHub.com](https://github.com/) and log in.
2. Click the **"+"** icon in the top right corner and select **"New repository"**.
3. Name your repository (e.g., `InternshipScraper`).
4. Choose whether to make it **Public** or **Private**.
5. **DO NOT** check the boxes to initialize with a README, .gitignore, or license (since you already have an existing local repository).
6. Click **"Create repository"**.

## Step 4: Link Your Local Folder to GitHub
After creating the repository, GitHub will show you a page with specific URL links and instructions. You need to connect your local Git repo to this remote GitHub repo.

1. Copy the Git URL provided by GitHub (it will look like `https://github.com/LuisAlar/InternshipScraper.git`).
2. Run this command in your terminal to link them:
   ```bash
   git remote add origin https://github.com/LuisAlar/InternshipScraper.git
   ```

## Step 5: Push Your Code
Finally, upload your code to GitHub.

1. Ensure your primary branch is named `main` (the modern standard):
   ```bash
   git branch -M main
   ```
2. Push your code to the remote repository:
   ```bash
   git push -u origin main
   ```
   *Note: The `-u` flag sets the "upstream", meaning in the future, you will only need to type `git push`.*

---

## Summary of Commands (For Quick Copy-Pasting)
If you already created the empty repo on GitHub, you can just run these in order:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/LuisAlar/<Your-Repo-Name>.git
git push -u origin main
```
