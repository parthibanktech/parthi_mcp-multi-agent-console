# 🌐 Environment Variable Behavior - Explained

## The Code
```python
FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", "http://localhost:8010")
HR_SERVER_URL = os.getenv("HR_SERVER_URL", "http://localhost:8011")
```

## How `os.getenv()` Works

```python
os.getenv("VARIABLE_NAME", "default_value")
```

- **First argument**: Environment variable name to look for
- **Second argument**: Default/fallback value if variable not found

## 🎯 Behavior in Different Environments

### Scenario 1: Local Development (No Docker)

**Environment Variables:** None set

**Code Behavior:**
```python
FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", "http://localhost:8010")
# Environment variable not found → Uses default
# Result: "http://localhost:8010"

HR_SERVER_URL = os.getenv("HR_SERVER_URL", "http://localhost:8011")
# Environment variable not found → Uses default
# Result: "http://localhost:8011"
```

**What Happens:**
- Client connects to `http://localhost:8010` (Finance)
- Client connects to `http://localhost:8011` (HR)
- ✅ Works if you run servers locally

---

### Scenario 2: Docker Compose (Local Containers)

**Environment Variables:** Set by `docker-compose.yml`
```yaml
environment:
  - FINANCE_SERVER_URL=http://finance-server:8010
  - HR_SERVER_URL=http://hr-server:8011
```

**Code Behavior:**
```python
FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", "http://localhost:8010")
# Environment variable FOUND → Uses environment value
# Result: "http://finance-server:8010"

HR_SERVER_URL = os.getenv("HR_SERVER_URL", "http://localhost:8011")
# Environment variable FOUND → Uses environment value
# Result: "http://hr-server:8011"
```

**What Happens:**
- Client connects to `http://finance-server:8010` (Docker service name)
- Client connects to `http://hr-server:8011` (Docker service name)
- ✅ Works in Docker network
- ❌ localhost default is IGNORED

---

### Scenario 3: Render Cloud Deployment

**Environment Variables:** Set by `render.yaml`
```yaml
envVars:
  - key: FINANCE_SERVER_URL
    value: https://mcp-finance-server.onrender.com
  - key: HR_SERVER_URL
    value: https://mcp-hr-server.onrender.com
```

**Code Behavior:**
```python
FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", "http://localhost:8010")
# Environment variable FOUND → Uses environment value
# Result: "https://mcp-finance-server.onrender.com"

HR_SERVER_URL = os.getenv("HR_SERVER_URL", "http://localhost:8011")
# Environment variable FOUND → Uses environment value
# Result: "https://mcp-hr-server.onrender.com"
```

**What Happens:**
- Client connects to `https://mcp-finance-server.onrender.com`
- Client connects to `https://mcp-hr-server.onrender.com`
- ✅ Works in Render cloud
- ❌ localhost default is IGNORED

---

## 🔍 Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Python Code Execution                                       │
│                                                              │
│  FINANCE_SERVER_URL = os.getenv("FINANCE_SERVER_URL", ...)  │
│                                                              │
│  Step 1: Check if environment variable exists               │
│           ↓                                                  │
│     ┌─────┴─────┐                                           │
│     │  Exists?  │                                           │
│     └─────┬─────┘                                           │
│           │                                                  │
│     ┌─────┴──────────────────────┐                          │
│     │                            │                          │
│   YES                           NO                          │
│     │                            │                          │
│     ↓                            ↓                          │
│  Use environment value      Use default value               │
│  (from docker-compose       (http://localhost:8010)         │
│   or render.yaml)                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Comparison Table

| Environment | FINANCE_SERVER_URL Value | Source |
|-------------|-------------------------|--------|
| **Local (no Docker)** | `http://localhost:8010` | Default (hardcoded) |
| **Docker Compose** | `http://finance-server:8010` | docker-compose.yml |
| **Render Cloud** | `https://mcp-finance-server.onrender.com` | render.yaml |

## ✅ Why This Design is Good

### 1. **Flexibility**
- Works in any environment
- No code changes needed
- Just set environment variables

### 2. **Developer Friendly**
- New developers can run locally without setup
- No need to configure environment variables for local dev
- Just run the servers and it works

### 3. **Production Ready**
- Cloud deployments override defaults
- Secure (no hardcoded production URLs)
- Easy to change URLs without code changes

### 4. **Follows Best Practices**
- 12-Factor App methodology
- Environment-based configuration
- Separation of config from code

## 🎯 Real-World Example

### Developer A (Local Development)
```bash
# No environment variables set
python finance_mcp_server.py  # Runs on localhost:8010
python hr_mcp_server.py       # Runs on localhost:8011
streamlit run client_agent.py # Connects to localhost:8010, localhost:8011
# ✅ Works! Uses defaults
```

### Developer B (Docker Compose)
```bash
docker-compose up
# docker-compose.yml sets:
#   FINANCE_SERVER_URL=http://finance-server:8010
#   HR_SERVER_URL=http://hr-server:8011
# ✅ Works! Uses Docker service names
```

### Production (Render)
```bash
# render.yaml sets:
#   FINANCE_SERVER_URL=https://mcp-finance-server.onrender.com
#   HR_SERVER_URL=https://mcp-hr-server.onrender.com
# ✅ Works! Uses Render URLs
```

## 🔧 How to Override Locally (If Needed)

If you want to test with different URLs locally:

### Option 1: Set environment variables
```bash
# Windows PowerShell
$env:FINANCE_SERVER_URL="http://custom-url:8010"
$env:HR_SERVER_URL="http://custom-url:8011"
streamlit run client_agent.py
```

### Option 2: Use .env file
```env
# .env file
FINANCE_SERVER_URL=http://custom-url:8010
HR_SERVER_URL=http://custom-url:8011
```

The code already loads `.env` with `load_dotenv()`, so this will work!

## 🎓 Summary

**Question:** Why is localhost hardcoded?

**Answer:** It's NOT hardcoded in production! It's a **fallback default** for local development.

- **Local dev**: Uses `localhost` (default)
- **Docker**: Uses service names (from docker-compose.yml)
- **Render**: Uses cloud URLs (from render.yaml)

**The localhost value is ONLY used when no environment variable is set.**

This is a **best practice** called "sensible defaults" - the app works out of the box locally, but can be configured for any environment via environment variables.

## ✅ Your Setup is Correct!

When you deploy to Render:
1. ✅ `render.yaml` sets `FINANCE_SERVER_URL=https://mcp-finance-server.onrender.com`
2. ✅ `render.yaml` sets `HR_SERVER_URL=https://mcp-hr-server.onrender.com`
3. ✅ Client code reads these environment variables
4. ✅ localhost default is IGNORED
5. ✅ Everything works in the cloud!

**No code changes needed!** 🎉
