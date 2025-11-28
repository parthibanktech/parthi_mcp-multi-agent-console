# 🚀 Quick Reference - Multi-Container MCP

## Start Everything
```bash
docker-compose up --build
```

## Update Only Finance Server
```bash
# 1. Edit finance_mcp_server.py
# 2. Run:
docker-compose up --build -d finance-server
```

## Update Only HR Server
```bash
# 1. Edit hr_mcp_server.py
# 2. Run:
docker-compose up --build -d hr-server
```

## Update Only Client
```bash
# 1. Edit client_agent.py
# 2. Run:
docker-compose up --build -d client-app
```

## View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f finance-server
docker-compose logs -f hr-server
docker-compose logs -f client-app
```

## Check Status
```bash
docker-compose ps
```

## Stop Everything
```bash
docker-compose down
```

## Restart a Service
```bash
docker-compose restart finance-server
docker-compose restart hr-server
docker-compose restart client-app
```

## Access URLs
- **Client UI**: http://localhost:8501
- **Finance Server**: http://localhost:8010
- **HR Server**: http://localhost:8011

## Common Issues

### Port already in use?
```bash
docker-compose down
docker-compose up
```

### Service won't start?
```bash
docker-compose logs [service-name]
docker-compose restart [service-name]
```

### Need fresh start?
```bash
docker-compose down -v
docker-compose up --build
```
