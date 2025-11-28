# 🔄 Migration Guide: Single Container → Multi-Container

This guide helps you migrate from the old single-container setup to the new multi-container architecture.

## 📋 What's Changing?

### Old Setup (Single Container)
```yaml
services:
  mcp-app:
    build: .
    container_name: mcp-multi-agent-app
    ports:
      - "8501:8501"
```
- All services in one container
- Uses `start.sh` to run all services
- Any change requires full rebuild

### New Setup (Multi-Container)
```yaml
services:
  finance-server:
    build:
      dockerfile: Dockerfile.finance
    ports:
      - "8010:8010"
  
  hr-server:
    build:
      dockerfile: Dockerfile.hr
    ports:
      - "8011:8011"
  
  client-app:
    build:
      dockerfile: Dockerfile.client
    ports:
      - "8501:8501"
```
- Three separate containers
- Each service has its own Dockerfile
- Update only what you change

## 🚀 Migration Steps

### Step 1: Stop Old Container

```bash
# If using old docker-compose
docker-compose down

# Or if running manually
docker stop mcp-multi-agent-app
docker rm mcp-multi-agent-app
```

### Step 2: Backup Your Environment

```bash
# Backup your .env file if it exists
cp .env .env.backup
```

### Step 3: Update Your Files

The following files have been updated/created:

**Updated:**
- ✅ `docker-compose.yml` - Now defines 3 services
- ✅ `client_agent.py` - Now uses environment variables for server URLs

**New Files:**
- ✅ `Dockerfile.finance` - Finance server container
- ✅ `Dockerfile.hr` - HR server container
- ✅ `Dockerfile.client` - Client app container
- ✅ `.dockerignore` - Optimize builds
- ✅ `.env.example` - Environment template
- ✅ Documentation files (DOCKER_GUIDE.md, etc.)

**No Changes Needed:**
- ✅ `finance_mcp_server.py` - Works as-is
- ✅ `hr_mcp_server.py` - Works as-is
- ✅ `requirements.txt` - Same dependencies
- ✅ `.env` - Same format

### Step 4: Create Environment File

```bash
# If you don't have a .env file yet
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

### Step 5: Start New Multi-Container Setup

```bash
# Build and start all services
docker-compose up --build
```

### Step 6: Verify Everything Works

1. **Check service status:**
   ```bash
   docker-compose ps
   ```
   You should see 3 services running:
   - `mcp-finance-server` (healthy)
   - `mcp-hr-server` (healthy)
   - `mcp-client-app` (running)

2. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Access the UI:**
   - Open browser: http://localhost:8501
   - Verify Finance and HR servers are connected

4. **Test functionality:**
   - Try: "Generate invoice for customer 123"
   - Try: "Check employee details for emp001"

## 🎯 What You Gain

### Before Migration
- ❌ Full rebuild for any change
- ❌ All services restart together
- ❌ Hard to debug specific service
- ❌ Can't scale individual services

### After Migration
- ✅ Update only changed service
- ✅ Services restart independently
- ✅ Easy to debug with isolated logs
- ✅ Scale services individually
- ✅ Better fault tolerance
- ✅ Production-ready architecture

## 🔄 New Workflow Examples

### Example 1: Update Finance Logic

**Old Way:**
```bash
# Edit finance_mcp_server.py
docker-compose down
docker-compose up --build  # Rebuilds everything
```

**New Way:**
```bash
# Edit finance_mcp_server.py
docker-compose up --build -d finance-server  # Only rebuilds Finance
# HR and Client keep running! ✅
```

### Example 2: Update UI

**Old Way:**
```bash
# Edit client_agent.py
docker-compose down
docker-compose up --build  # Rebuilds everything
```

**New Way:**
```bash
# Edit client_agent.py
docker-compose up --build -d client-app  # Only rebuilds Client
# Finance and HR keep running! ✅
```

### Example 3: Debug a Service

**Old Way:**
```bash
docker-compose logs  # All logs mixed together
```

**New Way:**
```bash
docker-compose logs -f finance-server  # Only Finance logs
docker-compose logs -f hr-server       # Only HR logs
docker-compose logs -f client-app      # Only Client logs
```

## 📚 New Commands to Learn

```bash
# Start everything
docker-compose up --build

# Start in background
docker-compose up -d --build

# Update specific service
docker-compose up --build -d finance-server

# View specific logs
docker-compose logs -f finance-server

# Restart specific service
docker-compose restart hr-server

# Check status
docker-compose ps

# Stop everything
docker-compose down
```

## 🔍 Troubleshooting Migration

### Issue: "Port already in use"

**Solution:**
```bash
# Make sure old container is stopped
docker ps -a | grep mcp
docker stop <container-id>
docker rm <container-id>

# Then start new setup
docker-compose up --build
```

### Issue: "Client can't connect to servers"

**Solution:**
```bash
# Check if all services are healthy
docker-compose ps

# Restart client
docker-compose restart client-app
```

### Issue: "Environment variables not working"

**Solution:**
```bash
# Make sure .env file exists
ls -la .env

# Check docker-compose is reading it
docker-compose config

# Restart services
docker-compose down
docker-compose up
```

### Issue: "Want to go back to old setup"

**Solution:**
```bash
# Your old Dockerfile still exists
# Just use it directly:
docker build -t mcp-app .
docker run -p 8501:8501 --env-file .env mcp-app
```

## 📊 Comparison

| Aspect | Old Setup | New Setup |
|--------|-----------|-----------|
| Containers | 1 | 3 |
| Rebuild Time | ~2-3 min | ~30 sec (per service) |
| Update Finance | Rebuild all | Rebuild Finance only |
| Update HR | Rebuild all | Rebuild HR only |
| Update Client | Rebuild all | Rebuild Client only |
| Debugging | Mixed logs | Isolated logs |
| Scaling | Scale all | Scale individually |
| Fault Tolerance | Low | High |

## ✅ Migration Checklist

- [ ] Stop old container
- [ ] Backup .env file
- [ ] Pull latest code with new files
- [ ] Create .env file if needed
- [ ] Run `docker-compose up --build`
- [ ] Verify all 3 services are running
- [ ] Test Finance functionality
- [ ] Test HR functionality
- [ ] Test Client UI
- [ ] Read DOCKER_GUIDE.md
- [ ] Read QUICK_REFERENCE.md
- [ ] Celebrate! 🎉

## 🎓 Learning Resources

After migration, check out:

1. **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Overview of new architecture
2. **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Detailed guide
3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick commands
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual diagrams

## 🆘 Need Help?

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify services: `docker-compose ps`
3. Read troubleshooting section above
4. Check DOCKER_GUIDE.md for detailed help
5. Open an issue on GitHub

## 🎉 Success!

You've successfully migrated to the multi-container architecture!

**Next Steps:**
1. Try updating individual services
2. Experiment with the new commands
3. Enjoy faster development cycles
4. Deploy to production when ready

Happy coding! 🚀
