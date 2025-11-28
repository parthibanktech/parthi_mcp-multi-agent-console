# MCP Multi-Container Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Docker Host Machine                          │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Docker Network: mcp-network                     │   │
│  │                    (Bridge Network)                          │   │
│  │                                                              │   │
│  │  ┌────────────────────┐  ┌────────────────────┐            │   │
│  │  │  Finance Server    │  │    HR Server       │            │   │
│  │  │ ┌────────────────┐ │  │ ┌────────────────┐ │            │   │
│  │  │ │finance_mcp_    │ │  │ │hr_mcp_server.py│ │            │   │
│  │  │ │server.py       │ │  │ │                │ │            │   │
│  │  │ │                │ │  │ │                │ │            │   │
│  │  │ │Port: 8010      │ │  │ │Port: 8011      │ │            │   │
│  │  │ └────────────────┘ │  │ └────────────────┘ │            │   │
│  │  │  Container:        │  │  Container:        │            │   │
│  │  │  mcp-finance-server│  │  mcp-hr-server     │            │   │
│  │  └─────────┬──────────┘  └──────────┬─────────┘            │   │
│  │            │                         │                      │   │
│  │            │  HTTP Requests          │                      │   │
│  │            │  (Internal Network)     │                      │   │
│  │            │                         │                      │   │
│  │            └────────────┬────────────┘                      │   │
│  │                         │                                   │   │
│  │                         ▼                                   │   │
│  │              ┌────────────────────┐                         │   │
│  │              │  Streamlit Client  │                         │   │
│  │              │ ┌────────────────┐ │                         │   │
│  │              │ │client_agent.py │ │                         │   │
│  │              │ │                │ │                         │   │
│  │              │ │Connects to:    │ │                         │   │
│  │              │ │- Finance Server│ │                         │   │
│  │              │ │- HR Server     │ │                         │   │
│  │              │ │                │ │                         │   │
│  │              │ │Port: 8501      │ │                         │   │
│  │              │ └────────────────┘ │                         │   │
│  │              │  Container:        │                         │   │
│  │              │  mcp-client-app    │                         │   │
│  │              └─────────┬──────────┘                         │   │
│  │                        │                                    │   │
│  └────────────────────────┼────────────────────────────────────┘   │
│                           │                                        │
│                           │ Port Mapping                           │
│                           │ 8501:8501                              │
│                           ▼                                        │
│                  ┌─────────────────┐                              │
│                  │   Host Ports    │                              │
│                  │  8010 → Finance │                              │
│                  │  8011 → HR      │                              │
│                  │  8501 → Client  │                              │
│                  └─────────────────┘                              │
│                           │                                        │
└───────────────────────────┼────────────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   Web Browser   │
                   │                 │
                   │ localhost:8501  │
                   └─────────────────┘
```

## Communication Flow

### 1. User Interaction
```
User → Browser (localhost:8501) → Client Container (port 8501)
```

### 2. Internal Service Communication
```
Client Container → Finance Server (http://finance-server:8010/mcp)
Client Container → HR Server (http://hr-server:8011/mcp)
```

### 3. Response Flow
```
Finance/HR Server → Client Container → Browser → User
```

## Service Dependencies

```
┌─────────────────┐
│  Client App     │  ← Depends on both servers being healthy
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Finance │ │   HR   │  ← Independent services
│Server  │ │ Server │
└────────┘ └────────┘
```

## Health Check Flow

```
Docker Compose
    │
    ├─► Start Finance Server
    │   └─► Health Check: Connect to port 8010
    │       └─► Status: Healthy ✓
    │
    ├─► Start HR Server
    │   └─► Health Check: Connect to port 8011
    │       └─► Status: Healthy ✓
    │
    └─► Start Client App (waits for both servers)
        └─► Connects to Finance & HR
            └─► Status: Running ✓
```

## Update Workflow

### Updating Finance Server Only

```
1. Edit finance_mcp_server.py
   │
   ▼
2. docker-compose up --build finance-server
   │
   ▼
3. Finance Container Rebuilds
   │
   ├─► HR Server: Still Running ✓
   └─► Client App: Still Running ✓
```

### Updating HR Server Only

```
1. Edit hr_mcp_server.py
   │
   ▼
2. docker-compose up --build hr-server
   │
   ▼
3. HR Container Rebuilds
   │
   ├─► Finance Server: Still Running ✓
   └─► Client App: Still Running ✓
```

### Updating Client Only

```
1. Edit client_agent.py
   │
   ▼
2. docker-compose up --build client-app
   │
   ▼
3. Client Container Rebuilds
   │
   ├─► Finance Server: Still Running ✓
   └─► HR Server: Still Running ✓
```

## Network Isolation

```
┌──────────────────────────────────────┐
│  mcp-network (Bridge)                │
│                                      │
│  ┌──────────┐  ┌──────────┐         │
│  │ Finance  │  │    HR    │         │
│  │ 8010     │  │   8011   │         │
│  └──────────┘  └──────────┘         │
│       ▲              ▲               │
│       │              │               │
│       └──────┬───────┘               │
│              │                       │
│         ┌────┴────┐                  │
│         │ Client  │                  │
│         │  8501   │                  │
│         └─────────┘                  │
│                                      │
└──────────────────────────────────────┘
         │ (Port Mapping)
         ▼
    Host Machine
    localhost:8501
```

## File Structure

```
updated_mcp_server_operation_team/
│
├── docker-compose.yml          ← Orchestrates all services
│
├── Dockerfile.finance          ← Finance server image
├── Dockerfile.hr               ← HR server image
├── Dockerfile.client           ← Client app image
│
├── finance_mcp_server.py       ← Finance service code
├── hr_mcp_server.py            ← HR service code
├── client_agent.py             ← Client UI code
│
├── requirements.txt            ← Python dependencies
├── .env                        ← Environment variables
│
└── Documentation
    ├── DOCKER_GUIDE.md         ← Detailed guide
    ├── QUICK_REFERENCE.md      ← Quick commands
    └── ARCHITECTURE.md         ← This file
```
