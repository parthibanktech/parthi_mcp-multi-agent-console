# Multi-Container MCP Architecture Guide

## 🏗️ Architecture Overview

This application uses a **microservices architecture** with three separate Docker containers:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                    (mcp-network)                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Finance    │  │      HR      │  │   Streamlit  │  │
│  │    Server    │  │    Server    │  │    Client    │  │
│  │  Port: 8010  │  │  Port: 8011  │  │  Port: 8501  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         ▲                 ▲                 │           │
│         └─────────────────┴─────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

### Services:

1. **finance-server** (`mcp-finance-server`)
   - Runs `finance_mcp_server.py`
   - Exposed on port `8010`
   - Provides finance-related tools (invoices, budgets)

2. **hr-server** (`mcp-hr-server`)
   - Runs `hr_mcp_server.py`
   - Exposed on port `8011`
   - Provides HR tools (employee details, leave balance)

3. **client-app** (`mcp-client-app`)
   - Runs `client_agent.py` (Streamlit UI)
   - Exposed on port `8501`
   - Connects to both Finance and HR servers
   - Waits for both servers to be healthy before starting

## 🚀 How to Use

### Starting All Services

```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### Stopping All Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Working with Individual Services

#### Start only Finance server:
```bash
docker-compose up finance-server
```

#### Start only HR server:
```bash
docker-compose up hr-server
```

#### Restart a specific service:
```bash
docker-compose restart finance-server
```

#### View logs for a specific service:
```bash
docker-compose logs -f finance-server
```

#### Rebuild a specific service:
```bash
docker-compose up --build finance-server
```

## 🔄 How Changes Work

### When you modify Finance server (`finance_mcp_server.py`):

1. **Stop only the Finance service:**
   ```bash
   docker-compose stop finance-server
   ```

2. **Rebuild and restart it:**
   ```bash
   docker-compose up --build finance-server
   ```

3. **HR server and Client continue running!** ✅

### When you modify HR server (`hr_mcp_server.py`):

1. **Stop only the HR service:**
   ```bash
   docker-compose stop hr-server
   ```

2. **Rebuild and restart it:**
   ```bash
   docker-compose up --build hr-server
   ```

3. **Finance server and Client continue running!** ✅

### When you modify Client (`client_agent.py`):

1. **Stop only the Client:**
   ```bash
   docker-compose stop client-app
   ```

2. **Rebuild and restart it:**
   ```bash
   docker-compose up --build client-app
   ```

3. **Both MCP servers continue running!** ✅

## 🔍 Monitoring & Debugging

### Check service status:
```bash
docker-compose ps
```

### View all logs:
```bash
docker-compose logs -f
```

### View specific service logs:
```bash
docker-compose logs -f finance-server
docker-compose logs -f hr-server
docker-compose logs -f client-app
```

### Execute commands in a running container:
```bash
# Access Finance server shell
docker-compose exec finance-server bash

# Access HR server shell
docker-compose exec hr-server bash

# Access Client shell
docker-compose exec client-app bash
```

### Check container health:
```bash
docker-compose ps
```
Look for "healthy" status in the State column.

## 🌐 Network Communication

- **Internal Communication**: Services communicate using Docker service names
  - Finance: `http://finance-server:8010`
  - HR: `http://hr-server:8011`

- **External Access** (from your host machine):
  - Finance: `http://localhost:8010`
  - HR: `http://localhost:8011`
  - Client UI: `http://localhost:8501`

## 📝 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The client will automatically use:
- `FINANCE_SERVER_URL=http://finance-server:8010` (set by docker-compose)
- `HR_SERVER_URL=http://hr-server:8011` (set by docker-compose)

## 🔧 Development Workflow

### Scenario 1: Adding a new Finance tool

1. Edit `finance_mcp_server.py`
2. Add your new tool function with `@mcp.tool()` decorator
3. Rebuild only Finance:
   ```bash
   docker-compose up --build -d finance-server
   ```
4. The client will automatically detect the new tool!

### Scenario 2: Adding a new HR tool

1. Edit `hr_mcp_server.py`
2. Add your new tool function with `@mcp.tool()` decorator
3. Rebuild only HR:
   ```bash
   docker-compose up --build -d hr-server
   ```
4. The client will automatically detect the new tool!

### Scenario 3: Updating the UI

1. Edit `client_agent.py`
2. Rebuild only the client:
   ```bash
   docker-compose up --build -d client-app
   ```
3. Refresh your browser at `http://localhost:8501`

## 🎯 Benefits of This Architecture

✅ **Isolation**: Each service runs independently
✅ **Scalability**: Can scale services individually
✅ **Faster Updates**: Only rebuild what changed
✅ **Better Debugging**: Isolated logs per service
✅ **Health Checks**: Automatic service health monitoring
✅ **Fault Tolerance**: If one server fails, others continue
✅ **Resource Efficiency**: Services use only needed resources

## 🛠️ Troubleshooting

### Service won't start:
```bash
# Check logs
docker-compose logs finance-server

# Remove and rebuild
docker-compose rm -f finance-server
docker-compose up --build finance-server
```

### Port already in use:
```bash
# Find what's using the port
netstat -ano | findstr :8010

# Stop all containers
docker-compose down

# Start again
docker-compose up
```

### Client can't connect to servers:
```bash
# Check if servers are healthy
docker-compose ps

# Restart client
docker-compose restart client-app
```

## 📦 Production Deployment

For production, you can deploy each service separately:

- Deploy Finance server to one instance
- Deploy HR server to another instance
- Deploy Client with environment variables pointing to server URLs

Example production `.env`:
```env
FINANCE_SERVER_URL=https://finance.yourdomain.com
HR_SERVER_URL=https://hr.yourdomain.com
OPENAI_API_KEY=your_production_key
```
