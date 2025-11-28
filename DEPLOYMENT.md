# 🚀 Render Deployment Guide - Multi-Container Setup

## Overview

This guide explains how to deploy your multi-container MCP application to Render.com.

## 📋 What Gets Deployed

Your `render.yaml` now deploys **3 separate services**:

1. **mcp-finance-server** - Finance MCP Server (Port 8010)
2. **mcp-hr-server** - HR MCP Server (Port 8011)
3. **mcp-client-app** - Streamlit Client (Port 8501)

## 🏗️ Architecture on Render

```
┌─────────────────────────────────────────────────────┐
│                  Render.com                          │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  mcp-finance-server.onrender.com             │  │
│  │  (Finance MCP Server - Port 8010)            │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  mcp-hr-server.onrender.com                  │  │
│  │  (HR MCP Server - Port 8011)                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  mcp-client-app.onrender.com                 │  │
│  │  (Streamlit Client - Port 8501)              │  │
│  │  ↓ Connects to Finance & HR servers          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Multi-container MCP setup"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/your-repo.git

# Push to GitHub
git push -u origin main
```

### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`

### Step 3: Configure Environment Variables

Render will prompt you to set:

- **OPENAI_API_KEY** - Your OpenAI API key (required for client-app)

The other environment variables are automatically set in `render.yaml`.

### Step 4: Deploy

1. Click **"Apply"**
2. Render will deploy all 3 services simultaneously
3. Wait for all services to become "Live" (green status)

## 🌐 Access Your Application

After deployment, you'll have 3 URLs:

- **Finance Server**: `https://mcp-finance-server.onrender.com`
- **HR Server**: `https://mcp-hr-server.onrender.com`
- **Client App**: `https://mcp-client-app.onrender.com` ← **Main URL to use**

## 📊 Service Configuration

### Finance Server
```yaml
name: mcp-finance-server
dockerfile: Dockerfile.finance
port: 8010
environment:
  - PORT=8010
```

### HR Server
```yaml
name: mcp-hr-server
dockerfile: Dockerfile.hr
port: 8011
environment:
  - PORT=8011
```

### Client App
```yaml
name: mcp-client-app
dockerfile: Dockerfile.client
port: 8501
environment:
  - PORT=8501
  - OPENAI_API_KEY=<your-key>
  - FINANCE_SERVER_URL=https://mcp-finance-server.onrender.com
  - HR_SERVER_URL=https://mcp-hr-server.onrender.com
```

## 🔄 Updating Individual Services

### Update Finance Server Only

```bash
# 1. Edit finance_mcp_server.py
# 2. Commit and push
git add finance_mcp_server.py
git commit -m "Update Finance server"
git push

# Render will automatically redeploy only the Finance service
# HR and Client continue running! ✅
```

### Update HR Server Only

```bash
# 1. Edit hr_mcp_server.py
# 2. Commit and push
git add hr_mcp_server.py
git commit -m "Update HR server"
git push

# Render will automatically redeploy only the HR service
# Finance and Client continue running! ✅
```

### Update Client Only

```bash
# 1. Edit client_agent.py
# 2. Commit and push
git add client_agent.py
git commit -m "Update client UI"
git push

# Render will automatically redeploy only the Client
# Both servers continue running! ✅
```

## 💡 How Render Detects Changes

Render is smart about which services to redeploy:

- **Changes to `finance_mcp_server.py` or `Dockerfile.finance`** → Redeploys Finance only
- **Changes to `hr_mcp_server.py` or `Dockerfile.hr`** → Redeploys HR only
- **Changes to `client_agent.py` or `Dockerfile.client`** → Redeploys Client only
- **Changes to `requirements.txt`** → Redeploys all services (dependencies changed)

## 🔍 Monitoring on Render

### View Logs

1. Go to Render Dashboard
2. Click on a service (e.g., "mcp-finance-server")
3. Click **"Logs"** tab
4. View real-time logs for that service only

### Check Service Health

1. Go to Render Dashboard
2. All services should show **"Live"** status (green)
3. Click on each service to see details

### Manual Redeploy

If needed, you can manually redeploy a service:

1. Go to service in Render Dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## ⚠️ Important Notes

### Free Tier Limitations

On Render's free tier:

- Services **sleep after 15 minutes of inactivity**
- First request after sleep takes ~30-60 seconds (cold start)
- All 3 services count toward your free tier limit

### Cold Start Handling

When services wake up from sleep:

1. Finance and HR servers start first
2. Client waits for both servers to be healthy
3. First request may take longer

### Service URLs

The URLs in `render.yaml` assume your services will be named:
- `mcp-finance-server`
- `mcp-hr-server`
- `mcp-client-app`

If Render assigns different URLs, update the environment variables:

```yaml
envVars:
  - key: FINANCE_SERVER_URL
    value: https://your-actual-finance-url.onrender.com
  - key: HR_SERVER_URL
    value: https://your-actual-hr-url.onrender.com
```

## 🎯 Best Practices

### 1. Use Environment Variables

Never hardcode URLs. Always use environment variables:

```python
FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", "http://localhost:8010")
```

### 2. Health Checks

Each service has a health check configured:

```yaml
healthCheckPath: /
```

This ensures Render knows when services are ready.

### 3. Separate Commits

For cleaner deployments, commit changes to individual services separately:

```bash
# Good: Separate commits
git commit -m "Add new Finance tool"
git commit -m "Update HR logic"

# Less ideal: Combined commit
git commit -m "Update Finance and HR"
```

### 4. Monitor Logs

After deployment, always check logs:

```
Render Dashboard → Service → Logs
```

## 🔧 Troubleshooting

### Issue: Client can't connect to servers

**Solution:**
1. Check if Finance and HR services are "Live"
2. Verify URLs in environment variables match actual Render URLs
3. Check logs for connection errors

### Issue: Service fails to deploy

**Solution:**
1. Check build logs in Render Dashboard
2. Verify Dockerfile path is correct
3. Ensure all dependencies are in `requirements.txt`

### Issue: All services redeploy on every change

**Solution:**
1. Make sure you're using separate Dockerfiles
2. Commit only the files that changed
3. Check Render's build logs to see why it's rebuilding

### Issue: Environment variables not working

**Solution:**
1. Go to Render Dashboard → Service → Environment
2. Verify all variables are set correctly
3. Redeploy the service

## 📊 Cost Optimization

### Free Tier Strategy

To stay within free tier limits:

1. **Use 3 free services** (Finance, HR, Client)
2. **Accept sleep behavior** (services sleep after 15 min)
3. **Optimize cold starts** (keep services lightweight)

### Paid Tier Benefits

If you upgrade to paid tier:

- No sleep behavior
- Faster performance
- More resources per service
- Can scale services independently

## 🎓 Alternative Deployment Options

If you prefer not to use Render's multi-service approach:

### Option 1: Deploy Client Only

Deploy just the client, and run Finance/HR locally or elsewhere:

```yaml
services:
  - type: web
    name: mcp-client-app
    env: docker
    dockerfilePath: ./Dockerfile.client
    envVars:
      - key: FINANCE_SERVER_URL
        value: https://your-finance-server.com
      - key: HR_SERVER_URL
        value: https://your-hr-server.com
```

### Option 2: Use Docker Compose on a VPS

Deploy the entire `docker-compose.yml` to a VPS:

```bash
# On your VPS
git clone your-repo
cd your-repo
docker-compose up -d
```

### Option 3: Use Kubernetes

For production at scale, consider Kubernetes with separate deployments for each service.

## 📝 Deployment Checklist

Before deploying to Render:

- [ ] Push latest code to GitHub
- [ ] Verify `render.yaml` is configured correctly
- [ ] Set OPENAI_API_KEY in Render Dashboard
- [ ] Check all Dockerfiles exist
- [ ] Verify environment variables in `render.yaml`
- [ ] Test locally with `docker-compose up`
- [ ] Monitor deployment in Render Dashboard
- [ ] Test all services after deployment
- [ ] Check logs for any errors

## 🎉 Success!

Once deployed, you'll have:

- ✅ 3 independent services on Render
- ✅ Automatic deployments on git push
- ✅ Individual service updates
- ✅ Production-ready MCP application

**Main URL:** `https://mcp-client-app.onrender.com`

---

**Questions?** Check Render's [documentation](https://render.com/docs) or open an issue on GitHub.
