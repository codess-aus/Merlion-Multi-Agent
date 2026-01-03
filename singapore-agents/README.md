# Singapore Multi-Agent System

A multi-agent system for Singapore-related services, built with Azure Functions and Flask for local development.

## Architecture

The system consists of three specialized agents:

### 1. Hawker Agent
- **Purpose**: Provides information about hawker centers in Singapore
- **Endpoint**: `/api/hawker`
- **Capabilities**: 
  - Hawker center search
  - Food recommendations
- **Parameters**:
  - `query`: Search term for hawker centers
  - `requester` (optional): Agent ID for trust verification

### 2. PSI Agent
- **Purpose**: Provides Pollutant Standards Index (PSI) information
- **Endpoint**: `/api/psi`
- **Capabilities**:
  - PSI readings
  - Air quality advisory
- **Parameters**:
  - `location`: Region (north, south, east, west, central, national)
  - `requester` (optional): Agent ID for trust verification

### 3. Merlion Agent
- **Purpose**: Provides tourist attractions and information
- **Endpoint**: `/api/merlion`
- **Capabilities**:
  - Attraction search
  - Tourist information
- **Parameters**:
  - `category`: Type of attraction (landmarks, nature, culture, all)
  - `requester` (optional): Agent ID for trust verification

## Directory Structure

```
singapore-agents/
├── hawker_agent/
│   ├── __init__.py
│   └── function_app.py        # Azure Function entrypoint
├── psi_agent/
│   ├── __init__.py
│   └── function_app.py        # Azure Function entrypoint
├── merlion_agent/
│   ├── __init__.py
│   └── function_app.py        # Azure Function entrypoint
├── shared/
│   ├── __init__.py
│   └── trust_module.py        # Shared trust utilities
├── app.py                    # For local development/testing (Flask runner)
├── requirements.txt
└── README.md
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

Run the Flask development server:

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Environment Variables

For local development, you can configure the Flask app using environment variables:

- **FLASK_DEBUG**: Set to `true` to enable debug mode (default: `false` for security)
- **FLASK_PORT**: Port number for the Flask server (default: `5000`)

Example:
```bash
FLASK_DEBUG=true FLASK_PORT=8000 python app.py
```

**Security Note**: Never enable debug mode in production environments as it may allow attackers to execute arbitrary code.

### Testing Endpoints

**Root endpoint** - List all agents:
```bash
curl http://localhost:5000/
```

**Hawker Agent**:
```bash
curl "http://localhost:5000/api/hawker?query=food"
```

**PSI Agent**:
```bash
curl "http://localhost:5000/api/psi?location=north"
```

**Merlion Agent**:
```bash
curl "http://localhost:5000/api/merlion?category=landmarks"
```

## Trust Module

The `shared/trust_module.py` provides utilities for inter-agent communication:

- **`verify_agent_trust(agent_id)`**: Verify if an agent is trusted
- **`get_agent_info(agent_id)`**: Get information about a specific agent
- **`get_all_agents()`**: Get information about all registered agents
- **`validate_agent_capability(agent_id, capability)`**: Check if an agent has a specific capability
- **`get_trust_level(agent_id)`**: Get the trust level of an agent

### Trusted Agents

All three agents (hawker, psi, merlion) have a trust level of "high" and can communicate with each other securely.

## Azure Functions Deployment

Each agent has its own `function_app.py` that can be deployed as an Azure Function:

1. Deploy each agent folder as a separate Azure Function App
2. Configure the Function App settings
3. Use the Azure Functions authentication level (FUNCTION) for security

## API Response Format

All endpoints return JSON with the following structure:

```json
{
  "agent": {
    "id": "agent_name",
    "name": "Agent Display Name",
    "description": "Agent description",
    "trust_level": "high",
    "capabilities": ["capability1", "capability2"]
  },
  // ... agent-specific data
}
```

## Error Handling

- **400**: Missing required parameters
- **403**: Untrusted requester
- **500**: Internal server error

All errors return JSON:
```json
{
  "error": "Error description"
}
```

## Development Notes

- The Flask app (`app.py`) simulates the Azure Functions environment for local testing
- Each agent can operate independently
- Trust verification is optional but recommended for inter-agent communication
- All agents share the trust module for consistent security
