# Merlion Multi-Agent System

A distributed multi-agent system for Singapore-related services built with Azure Functions and Python. The system consists of three specialized agents that provide information about hawker centers, air quality, and tourist attractions.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Agents](#agents)
- [Installation](#installation)
- [Local Development](#local-development)
- [Azure Deployment](#azure-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Overview

The Merlion Multi-Agent System is a cloud-native application that leverages Azure Functions to provide a scalable, serverless multi-agent architecture. Each agent is an independent service that can be deployed, scaled, and managed separately while maintaining a unified interface for clients.

**Key Features:**
- ✅ Three specialized agents for different domains
- ✅ Trust-based inter-agent communication
- ✅ Serverless architecture (Azure Functions)
- ✅ Local development support (Flask)
- ✅ Comprehensive API endpoints
- ✅ Easy deployment to Azure
- ✅ Built-in monitoring with Application Insights

## Architecture

The system follows a distributed multi-agent pattern:

```
┌─────────────────────────────────────────────────┐
│         Azure Function App                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────┐│
│  │ Hawker Agent │  │  PSI Agent   │  │Merlion ││
│  │              │  │              │  │ Agent  ││
│  │  /api/hawker │  │  /api/psi    │  │ /api/  ││
│  │              │  │              │  │merlion ││
│  └──────────────┘  └──────────────┘  └────────┘│
│                                                 │
│  ┌────────────────────────────────────────────┐│
│  │  Shared Trust Module (Inter-agent comm)   ││
│  └────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

## Agents

### 1. Hawker Agent 🍜

**Purpose:** Provides information about hawker centers and food recommendations in Singapore

**Endpoint:** `/api/hawker`

**Parameters:**
- `query` (required): Search term for hawker centers (e.g., "food", "chicken rice", "noodles")
- `requester` (optional): Agent ID for trust verification

**Example Request:**
```bash
curl "http://localhost:7071/api/hawker?query=food"
```

**Example Response:**
```json
{
  "agent": {
    "id": "hawker",
    "name": "Hawker Agent",
    "description": "Provides information about hawker centers in Singapore",
    "trust_level": "high",
    "capabilities": ["hawker_search", "food_recommendations"]
  },
  "query": "food",
  "results": [
    {
      "name": "Maxwell Food Centre",
      "location": "1 Kadayanallur Street",
      "popular_stalls": ["Tian Tian Chicken Rice", "Zhen Zhen Porridge"]
    }
  ],
  "message": "Found hawker centers matching: food"
}
```

---

### 2. PSI Agent 💨

**Purpose:** Provides Pollutant Standards Index (PSI) readings and air quality information for Singapore

**Endpoint:** `/api/psi`

**Parameters:**
- `location` (optional): Region code - `north`, `south`, `east`, `west`, `central`, or `national` (default: `national`)
- `requester` (optional): Agent ID for trust verification

**Example Request:**
```bash
curl "http://localhost:7071/api/psi?location=central"
```

**Example Response:**
```json
{
  "agent": {
    "id": "psi",
    "name": "PSI Agent",
    "description": "Provides Pollutant Standards Index information",
    "trust_level": "high",
    "capabilities": ["psi_reading", "air_quality_advisory"]
  },
  "timestamp": "2026-01-03T17:18:27.717219",
  "location": "central",
  "psi_readings": {
    "north": 45,
    "south": 42,
    "east": 48,
    "west": 50,
    "central": 46,
    "national": 46
  },
  "air_quality": "Good",
  "health_advisory": "Air quality is satisfactory; air pollution poses little or no risk."
}
```

---

### 3. Merlion Agent 🦁

**Purpose:** Provides tourist attractions and travel information for Singapore

**Endpoint:** `/api/merlion`

**Parameters:**
- `category` (optional): Type of attraction - `landmarks`, `nature`, `culture`, or `all` (default: `all`)
- `requester` (optional): Agent ID for trust verification

**Example Request:**
```bash
curl "http://localhost:7071/api/merlion?category=landmarks"
```

**Example Response:**
```json
{
  "agent": {
    "id": "merlion",
    "name": "Merlion Agent",
    "description": "Provides tourist attractions and information",
    "trust_level": "high",
    "capabilities": ["attraction_search", "tourist_information"]
  },
  "category": "landmarks",
  "attractions": {
    "landmarks": [
      {
        "name": "Merlion Park",
        "description": "Iconic symbol of Singapore",
        "location": "One Fullerton"
      },
      {
        "name": "Marina Bay Sands",
        "description": "Integrated resort with iconic rooftop",
        "location": "10 Bayfront Avenue"
      }
    ]
  },
  "message": "Tourist attractions for category: landmarks"
}
```

---

## Installation

### Prerequisites

- Python 3.9+
- Azure CLI (for deployment)
- Azure Functions Core Tools v4
- Git

### Clone the Repository

```bash
git clone https://github.com/codess-aus/Merlion-Multi-Agent.git
cd Merlion-Multi-Agent/singapore-agents
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

- `azure-functions>=1.18.0` - Azure Functions SDK
- `Flask>=3.0.0` - For local development
- `python-dateutil>=2.8.2` - Date utilities
- `python-dotenv>=1.0.0` - Environment configuration
- `pytest>=7.4.0` - Testing framework (optional)

## Local Development

### Running with Azure Functions Core Tools

```bash
cd singapore-agents
func start
```

The server will start on `http://localhost:7071`

**Available Endpoints:**
- Root: `http://localhost:7071/api/`
- Hawker: `http://localhost:7071/api/hawker?query=<search>`
- PSI: `http://localhost:7071/api/psi?location=<region>`
- Merlion: `http://localhost:7071/api/merlion?category=<type>`

### Testing Endpoints Locally

Use the provided test script:

```bash
cd singapore-agents
bash test-api.sh http://localhost:7071/api
```

Or test individual endpoints:

```bash
# Test Hawker Agent
curl "http://localhost:7071/api/hawker?query=food"

# Test PSI Agent
curl "http://localhost:7071/api/psi?location=central"

# Test Merlion Agent
curl "http://localhost:7071/api/merlion?category=landmarks"
```

### Running with Flask (Alternative)

For traditional Flask development:

```bash
cd singapore-agents
python app.py
```

The server will run on `http://localhost:5000`

**Configuration:**
- `FLASK_DEBUG=true` - Enable debug mode (development only)
- `FLASK_PORT=8000` - Custom port number

Example:
```bash
FLASK_DEBUG=true FLASK_PORT=8000 python app.py
```

⚠️ **Security Note:** Never enable debug mode in production.

## Azure Deployment

### Prerequisites

1. **Azure Account:** Create a free account at [azure.microsoft.com](https://azure.microsoft.com)
2. **Azure CLI:** Install from [Microsoft docs](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Azure Functions Core Tools:** Install version 4

### Installation of Required Tools

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Azure Functions Core Tools (Linux)
sudo apt-get update
sudo apt-get install -y azure-functions-core-tools-4
```

### Verify Installation

```bash
az --version
func --version
```

### Deploy to Azure

From the `singapore-agents` directory:

```bash
./deploy-azure.sh
```

The script will:
1. ✅ Verify your Azure login
2. ✅ Prompt for configuration details
3. ✅ Create a resource group
4. ✅ Create a storage account
5. ✅ Create an Azure Function App
6. ✅ Set up Application Insights monitoring
7. ✅ Deploy your code
8. ✅ Display live URLs

**Configuration Prompts:**
```
Resource Group: rg-singapore-agents
Location: eastasia (or your preferred region)
Function App: singapore-agents-app
Storage Account: stgsgagents[timestamp]
```

### View Deployment

After successful deployment, access your application at:
```
https://<your-function-app-name>.azurewebsites.net/api/
```

### Monitor Logs

View real-time logs:

```bash
func azure functionapp logstream <your-function-app-name>
```

View in Azure Portal:
- Search for your Function App
- Select **Monitoring** → **Application Insights**

## API Documentation

### Root Endpoint

**GET** `/api/`

Returns information about all available agents and endpoints.

**Response:**
```json
{
  "message": "Singapore Multi-Agent System",
  "version": "1.0.0",
  "agents": [...],
  "endpoints": {
    "hawker": "/api/hawker?query=<search>",
    "psi": "/api/psi?location=<region>",
    "merlion": "/api/merlion?category=<type>"
  }
}
```

### Error Handling

All endpoints return appropriate HTTP status codes:

- **200 OK** - Request successful
- **400 Bad Request** - Missing required parameters
- **403 Forbidden** - Requester not trusted
- **500 Internal Server Error** - Server error

**Error Response Format:**
```json
{
  "error": "Error message describing what went wrong"
}
```

### Trust Verification

Optional parameter for inter-agent communication:

```bash
curl "http://localhost:7071/api/psi?location=central&requester=hawker"
```

Currently trusted agents:
- `hawker` - Hawker Agent
- `psi` - PSI Agent
- `merlion` - Merlion Agent

## Testing

### Unit Tests

Run the test suite:

```bash
cd singapore-agents
pytest
```

With coverage:

```bash
pytest --cov=shared --cov-report=html
```

### Manual Testing

Use provided test script:

```bash
bash test-api.sh http://localhost:7071/api
```

Or use curl directly:

```bash
# Test all endpoints
curl http://localhost:7071/api/
curl "http://localhost:7071/api/hawker?query=food"
curl "http://localhost:7071/api/psi?location=national"
curl "http://localhost:7071/api/merlion?category=all"
```

### Integration Testing

After deployment to Azure:

```bash
bash test-api.sh https://<your-function-app-name>.azurewebsites.net/api
```

## Project Structure

```
Merlion-Multi-Agent/
├── README.md                          # This file
├── singapore-agents/                  # Main application
│   ├── function_app.py               # Root Azure Functions entry point
│   ├── app.py                        # Flask development server
│   ├── requirements.txt               # Python dependencies
│   ├── local.settings.json           # Local Azure Functions config
│   ├── .funcignore                   # Files to ignore in deployment
│   ├── .gitignore                    # Git ignore rules
│   ├── deploy-azure.sh               # Azure deployment script
│   ├── test-api.sh                   # API testing script
│   ├── hawker_agent/                 # Hawker Agent
│   │   ├── __init__.py
│   │   └── function_app.py          # Hawker endpoint implementation
│   ├── psi_agent/                    # PSI Agent
│   │   ├── __init__.py
│   │   └── function_app.py          # PSI endpoint implementation
│   ├── merlion_agent/                # Merlion Agent
│   │   ├── __init__.py
│   │   └── function_app.py          # Merlion endpoint implementation
│   └── shared/                       # Shared utilities
│       ├── __init__.py
│       └── trust_module.py          # Trust verification & agent info
└── [other project files]
```

## How It Works

### Request Flow

1. **Client Request** → Azure Functions Endpoint
2. **Request Routing** → Appropriate Agent Handler
3. **Trust Verification** (if requester ID provided)
4. **Data Processing** → Agent Logic
5. **Response Formation** → JSON Response
6. **Return to Client** → HTTP Response

### Inter-Agent Communication

Agents can request information from each other using the trust module:

```python
from shared.trust_module import verify_agent_trust, get_agent_info

# Verify another agent is trusted
if verify_agent_trust("hawker"):
    # Process request from trusted agent
    pass

# Get information about an agent
agent_info = get_agent_info("psi")
```

## Scaling and Performance

- **Serverless Scaling:** Azure Functions automatically scales based on demand
- **Stateless Design:** Each request is independent, enabling horizontal scaling
- **Regional Deployment:** Can be deployed to any Azure region
- **Consumption Plan:** Pay only for compute time used

## Security Considerations

1. **Debug Mode:** Never enable in production
2. **Authentication:** Enable Azure AD or API key authentication for production
3. **HTTPS:** Always use HTTPS in production
4. **Environment Variables:** Use Azure Key Vault for sensitive data
5. **CORS:** Configure properly if accessed from web browsers

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Future Enhancements

- [ ] Database integration for persistent data
- [ ] Real-time PSI data integration with Singapore's NEA API
- [ ] Hawker center data from official sources
- [ ] User authentication and authorization
- [ ] Rate limiting and throttling
- [ ] Caching layer (Redis)
- [ ] GraphQL API support
- [ ] Mobile app integration
- [ ] Analytics and usage tracking

## Troubleshooting

### Azure Functions Not Starting Locally

```bash
# Check if func is installed
func --version

# Clear cache
rm -rf .python_packages/

# Try again
func start
```

### Import Errors

Ensure you're running from the correct directory:

```bash
cd singapore-agents
```

And dependencies are installed:

```bash
pip install -r requirements.txt
```

### Deployment Failures

1. Check Azure CLI login: `az login`
2. Verify subscription: `az account show`
3. Check available quota in region
4. Review script output for specific errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- 🐛 [Report bugs on GitHub](https://github.com/codess-aus/Merlion-Multi-Agent/issues)
- 💬 Start a discussion
- 📧 Contact the maintainers

## Quick Start Recap

**Local Testing:**
```bash
cd singapore-agents
func start
curl "http://localhost:7071/api/hawker?query=food"
```

**Deploy to Azure:**
```bash
./deploy-azure.sh
```

Happy coding! 🚀