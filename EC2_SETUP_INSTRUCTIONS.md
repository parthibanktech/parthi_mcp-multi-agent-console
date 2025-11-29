# 🚀 Moving Your Docker Images to Your EC2 Instance

Based on your screenshot, here are the specific steps to connect your GitHub pipeline to your new AWS EC2 instance.

**Instance Details:**
- **Public IP:** `13.51.206.121`
- **Instance Type:** `t3.micro`

---

## ✅ Step 1: Configure GitHub Secrets
Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

Add these exact values:

| Name | Value |
| :--- | :--- |
| `EC2_HOST` | `51.20.51.57` |
| `EC2_USER` | `ubuntu` (Since you likely chose Ubuntu, otherwise try `ec2-user`) |
| `EC2_SSH_KEY` | Open your `.pem` key file (that you downloaded when creating the instance) with a text editor (like Notepad) and copy the **entire** content. |
| `DOCKER_PASSWORD` | Your Docker Hub password. |

---

## 💻 Step 2: Prepare Your EC2 Instance
You need to install Docker on your new instance so it can run the images.

1. **Connect to your instance** (using SSH or EC2 Instance Connect in the AWS Console).
2. **Run these commands** to install Docker:

```bash
# 1. Update the package database
sudo apt-get update

# 2. Install Docker and Docker Compose
sudo apt-get install -y docker.io docker-compose

# 3. Start Docker and enable it to run on boot
sudo systemctl start docker
sudo systemctl enable docker

# 4. Add the 'ubuntu' user to the docker group (avoids using 'sudo' for every docker command)
sudo usermod -aG docker ubuntu
```

*Note: You might need to log out and log back in for the group change to take effect.*

---

## 🚀 Step 3: Trigger the Move
Once Step 1 and Step 2 are done, you don't need to manually move files.

1. **Push any change** to your `main` branch on GitHub.
   - You can simply run `git_push.bat` from your local folder.
2. **Watch the Magic**:
   - GitHub Actions will build your code.
   - It will push the images to Docker Hub.
   - It will log in to your EC2.
   - It will pull the new images and start them.

## 🔍 Troubleshooting
- **Security Groups**: Ensure your EC2 Security Group allows **Inbound Traffic** on ports `8010`, `8011`, and `8501` so you can access the app.
- **Accessing the App**: Once deployed, your app will be available at:
  - Client App: `http://51.20.51.57:8501`
