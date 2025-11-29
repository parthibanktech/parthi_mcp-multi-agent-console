# 🚀 CI/CD & AWS EC2 Guide

This guide explains how to automate your development workflow and deploy to AWS EC2.

## 🤖 1. GitHub Actions (CI/CD)

We have created a workflow file at `.github/workflows/main.yml`.

### What it does:
1.  **Triggers** whenever you push code to the `main` branch.
2.  **Builds** your Docker images (Finance, HR, Client) to ensure there are no errors.
3.  **Verifies** your `docker-compose.yml` configuration.

### How to use it:
Just push your code to GitHub!
```bash
./git_push.bat
```
Go to the **Actions** tab in your GitHub repository to see the build progress.

---

## ☁️ 2. Moving to AWS EC2

If you decide to move from Render to AWS EC2, follow these steps:

### Step 1: Launch EC2 Instance
1.  Go to AWS Console > EC2 > Launch Instance.
2.  Choose **Ubuntu Server 22.04 LTS** (or Amazon Linux 2).
3.  Instance Type: **t2.small** or **t2.medium** (t2.micro might be too small for 3 containers).
4.  Create a Key Pair (e.g., `mcp-key.pem`) and download it.
5.  Allow HTTP (80), HTTPS (443), and Custom TCP ports **8010, 8011, 8501** in the Security Group.

### Step 2: Install Docker on EC2
SSH into your instance and run:
```bash
# Update and install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER
```
*Log out and log back in for group changes to take effect.*

### Step 3: Configure GitHub Secrets
To enable automatic deployment, go to your GitHub Repo > Settings > Secrets and Variables > Actions. Add:

| Secret Name | Value |
|-------------|-------|
| `EC2_HOST` | Public IP address of your EC2 instance (e.g., `54.123.45.67`) |
| `EC2_USER` | `ubuntu` (if using Ubuntu AMI) |
| `EC2_SSH_KEY` | Content of your `mcp-key.pem` file |

### Step 4: Enable Deployment Job
### Step 4: Verify Deployment Job
The `deploy-to-ec2` job has been added to `.github/workflows/main.yml`. It is configured to run automatically on pushes to `main` after the build job succeeds.

Ensure you have set the secrets in Step 3 correctly.

Now, every time you push to `main`, GitHub will:
1.  Test your code.
2.  SSH into your EC2 instance.
3.  Pull the latest code.
4.  Restart the containers with the new changes.

---

## 🛠️ 3. Auto-Push Script

We created `git_push.bat` to make saving changes easy.

**Usage:**
Double-click `git_push.bat` or run in terminal:
```cmd
git_push.bat
```
It will:
1.  `git add .` (Stage all files)
2.  Ask for a commit message.
3.  `git push origin main` (Upload to GitHub).

---

## ❓ Render vs. AWS EC2

| Feature | Render | AWS EC2 |
|---------|--------|---------|
| **Setup** | Easiest (Auto-detects `render.yaml`) | Moderate (Manual server setup) |
| **Cost** | Free tier available (sleeps) | Free tier (t2.micro) for 1 year |
| **Scaling** | Auto-scaling (Paid) | Manual or Auto Scaling Groups |
| **Control** | Managed Platform | Full Server Control (Root access) |
| **CI/CD** | Built-in (Auto-deploy) | Requires GitHub Actions (Setup above) |

**Recommendation:** Stick with **Render** for now if you want simplicity. Move to **EC2** if you need full control, persistent storage volumes, or cheaper 24/7 running costs for multiple services.
