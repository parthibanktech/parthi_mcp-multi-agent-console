# 🤖 Multi-Agent MCP Console

A powerful **Model Context Protocol (MCP)** orchestration platform that unifies multiple AI agents (Finance & HR) into a single, cohesive Streamlit interface. This application demonstrates the power of the **MCP standard** by enabling a central LLM to dynamically query specialized micro-agents.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg) ![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🏗️ Architecture

This project uses a **microservices architecture** with three independent Docker containers:

```
┌─────────────────────────────────────────┐
│         Docker Network                   │
│                                          │
│  ┌──────────┐  ┌──────────┐            │
│  │ Finance  │  │    HR    │            │
│  │  :8010   │  │  :8011   │            │
│  └─────┬────┘  └────┬─────┘            │
│        │            │                   │
│        └─────┬──────┘                   │
│              │                          │
│         ┌────▼─────┐                    │
│         │  Client  │                    │
│         │  :8501   │                    │
│         └──────────┘                    │
└─────────────────────────────────────────┘
```

### Services:
- **Finance Server** (`mcp-finance-server`) - Port 8010
- **HR Server** (`mcp-hr-server`) - Port 8011  
- **Client App** (`mcp-client-app`) - Port 8501

## ✨ Features

*   **🤝 Multi-Agent Orchestration**: Seamlessly connects to multiple independent MCP servers (Finance & HR).
*   **🧠 Intelligent Routing**: Uses **LangChain** and **LangGraph** to intelligently route user queries to the correct domain agent.
*   **⚡ Real-time Interaction**: Built on **FastMCP** for high-performance, low-latency agent communication.
*   **🎨 Modern UI**: A sleek, dark-mode enabled **Streamlit** interface for easy interaction.
*   **🐳 Multi-Container Architecture**: Separate containers for each service, enabling independent updates and scaling.
*   **🔄 Independent Updates**: Update Finance, HR, or Client services without affecting others.
*   **💪 Fault Tolerant**: Service isolation ensures one failure doesn't crash the entire system.
*   **🔒 Secure**: Environment-variable based configuration for API keys.

## 🛠️ Technology Stack

*   **Frontend**: Streamlit
*   **Orchestration**: LangChain, LangGraph
*   **Protocol**: Model Context Protocol (MCP), FastMCP
*   **LLM**: OpenAI GPT-4o-mini
*   **Runtime**: Python 3.11
*   **Containerization**: Docker, Docker Compose
*   **Deployment**: Docker, Render

## 📋 Prerequisites

*   Python 3.10 - 3.12
*   OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
*   Docker & Docker Compose (for containerized deployment)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd updated_mcp_server_operation_team
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Open browser: http://localhost:8501

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Finance server** (Terminal 1)
   ```bash
   python finance_mcp_server.py
   ```

3. **Start HR server** (Terminal 2)
   ```bash
   python hr_mcp_server.py
   ```

4. **Start Streamlit client** (Terminal 3)
   ```bash
   streamlit run client_agent.py
   ```

## 📚 Documentation

- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Complete overview of the multi-container setup
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Comprehensive Docker guide with examples
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual architecture diagrams
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide

## 🔄 Working with Individual Services

### Update Finance Server Only
```bash
# 1. Edit finance_mcp_server.py
# 2. Rebuild only Finance:
docker-compose up --build -d finance-server
# HR and Client keep running! ✅
```

### Update HR Server Only
```bash
# 1. Edit hr_mcp_server.py
# 2. Rebuild only HR:
docker-compose up --build -d hr-server
# Finance and Client keep running! ✅
```

### Update Client Only
```bash
# 1. Edit client_agent.py
# 2. Rebuild only Client:
docker-compose up --build -d client-app
# Both servers keep running! ✅
```

## 🎯 Use Cases

### Finance Agent
- Generate invoices for customers
- Get budget summaries by department
- Financial reporting and analytics

### HR Agent
- Retrieve employee details
- Check leave balances
- HR data management

### Multi-Agent Queries
The system intelligently routes queries to the appropriate agent(s):
- "Generate invoice for customer 123" → Finance Agent
- "What's Alice's leave balance?" → HR Agent
- "Generate invoice for customer 456 and check employee 789's details" → Both Agents

## 🔍 Monitoring

### Check service status
```bash
docker-compose ps
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f finance-server
docker-compose logs -f hr-server
docker-compose logs -f client-app
```

### Restart a service
```bash
docker-compose restart finance-server
```

## 🌐 API Endpoints

- **Finance Server**: http://localhost:8010/mcp
- **HR Server**: http://localhost:8011/mcp
- **Client UI**: http://localhost:8501

## 🎨 Available Tools

### Finance Server Tools
- `generate_invoice(customer_id: str)` - Generate a new invoice
- `get_budget_summary(department: str)` - Get department budget overview

### HR Server Tools
- `get_employee_details(employee_id: str)` - Fetch employee information
- `check_leave_balance(employee_id: str)` - View employee leave balance

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Docker Compose automatically sets:
```env
FINANCE_SERVER_URL=http://finance-server:8010
HR_SERVER_URL=http://hr-server:8011
```

## 📊 Benefits of Multi-Container Architecture

| Feature | Single Container | Multi-Container |
|---------|-----------------|-----------------|
| Update Speed | Slow (rebuild all) | Fast (rebuild one) |
| Isolation | None | Full |
| Scalability | Limited | Excellent |
| Debugging | Hard | Easy |
| Resource Usage | High | Optimized |
| Fault Tolerance | Low | High |

## 🛠️ Development Workflow

1. **Make changes** to the service you want to update
2. **Rebuild only that service**:
   ```bash
   docker-compose up --build -d [service-name]
   ```
3. **Test your changes** - other services continue running
4. **Commit and deploy** when ready

## 🚢 Production Deployment

### Deploy to Render, Railway, or any cloud platform:

1. Each service can be deployed independently
2. Set environment variables for inter-service communication
3. Use health checks for reliability
4. Scale services based on load

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request

## 📝 Project Structure

```
updated_mcp_server_operation_team/
├── docker-compose.yml          # Orchestrates all services
├── Dockerfile.finance          # Finance server image
├── Dockerfile.hr               # HR server image
├── Dockerfile.client           # Client app image
├── finance_mcp_server.py       # Finance service
├── hr_mcp_server.py            # HR service
├── client_agent.py             # Streamlit UI
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
└── Documentation/
    ├── SETUP_SUMMARY.md
    ├── DOCKER_GUIDE.md
    ├── QUICK_REFERENCE.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

## 🐛 Troubleshooting

### Port already in use
```bash
docker-compose down
docker-compose up
```

### Service won't start
```bash
docker-compose logs [service-name]
docker-compose restart [service-name]
```

### Fresh start needed
```bash
docker-compose down -v
docker-compose up --build
```

## 📜 License

MIT License - feel free to use this project for learning and development.

## 🙏 Acknowledgments

- **FastMCP** - High-performance MCP implementation
- **LangChain** - LLM orchestration framework
- **Streamlit** - Beautiful web UI framework
- **Model Context Protocol** - Standardized AI agent communication

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using MCP, LangChain, and Streamlit**

🚀 **Ready to get started?** Run `docker-compose up --build` and visit http://localhost:8501
