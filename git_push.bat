@echo off
echo ==========================================
echo 🚀 Auto-Push to GitHub
echo ==========================================

:: Check if git is initialized
if not exist .git (
    echo ⚠️  Git is not initialized. Initializing...
    git init
    git branch -M main
    echo Please add your remote origin manually:
    echo git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
    pause
    exit /b
)

:: Add all changes
echo 📦 Staging all changes...
git add .

:: Ask for commit message
set /p commit_msg="📝 Enter commit message (default: 'Update code'): "
if "%commit_msg%"=="" set commit_msg=Update code

:: Commit
echo 💾 Committing...
git commit -m "%commit_msg%"

:: Push
echo ☁️  Pushing to main...
git push -u origin main

echo ==========================================
echo ✅ Done!
echo ==========================================
pause
