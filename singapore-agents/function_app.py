"""Root Azure Functions entrypoint for Singapore Multi-Agent System.

This file consolidates all agent function apps into a single entry point
for Azure Functions deployment.
"""

import azure.functions as func
import logging
import json
from datetime import datetime

try:
    from shared.trust_module import verify_agent_trust, get_agent_info, get_all_agents
except ImportError:
    # Fallback for different execution contexts
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from shared.trust_module import verify_agent_trust, get_agent_info, get_all_agents

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main function app
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Root endpoint to display available APIs
@app.route(route="")
def root_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Root endpoint showing available agents and their endpoints."""
    response = {
        "message": "Singapore Multi-Agent System",
        "version": "1.0.0",
        "agents": get_all_agents(),
        "endpoints": {
            "hawker": "/api/hawker?query=<search_term>",
            "psi": "/api/psi?location=<north|south|east|west|central|national>",
            "merlion": "/api/merlion?category=<landmarks|nature|culture|all>"
        },
        "documentation": "https://github.com/codess-aus/Merlion-Multi-Agent"
    }
    
    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )

# Hawker Agent endpoint
@app.route(route="hawker")
def hawker_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for Hawker Agent."""
    logging.info('Hawker Agent: Processing HTTP request.')
    
    try:
        # Verify trust if requester info is provided
        requester = req.params.get('requester')
        if requester and not verify_agent_trust(requester):
            return func.HttpResponse(
                json.dumps({"error": "Requester not trusted"}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Get query parameter
        query = req.params.get('query')
        if not query:
            try:
                req_body = req.get_json()
                query = req_body.get('query')
            except ValueError:
                pass
        
        if query:
            response_data = {
                "agent": get_agent_info("hawker"),
                "query": query,
                "results": [
                    {
                        "name": "Maxwell Food Centre",
                        "location": "1 Kadayanallur Street",
                        "popular_stalls": ["Tian Tian Chicken Rice", "Zhen Zhen Porridge"]
                    },
                    {
                        "name": "Lau Pa Sat",
                        "location": "18 Raffles Quay",
                        "popular_stalls": ["Satay Street", "Various seafood stalls"]
                    }
                ],
                "message": f"Found hawker centers matching: {query}"
            }
            
            return func.HttpResponse(
                json.dumps(response_data),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({
                    "agent": get_agent_info("hawker"),
                    "message": "Please provide a query parameter"
                }),
                status_code=400,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error in Hawker Agent: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# PSI Agent endpoint
@app.route(route="psi")
def psi_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for PSI Agent."""
    logging.info('PSI Agent: Processing HTTP request.')
    
    try:
        # Verify trust if requester info is provided
        requester = req.params.get('requester')
        if requester and not verify_agent_trust(requester):
            return func.HttpResponse(
                json.dumps({"error": "Requester not trusted"}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Get location parameter
        location = req.params.get('location', 'national')
        if not location:
            try:
                req_body = req.get_json()
                location = req_body.get('location', 'national')
            except ValueError:
                location = 'national'
        
        response_data = {
            "agent": get_agent_info("psi"),
            "timestamp": datetime.utcnow().isoformat(),
            "location": location,
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
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error in PSI Agent: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# Merlion Agent endpoint
@app.route(route="merlion")
def merlion_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for Merlion Agent."""
    logging.info('Merlion Agent: Processing HTTP request.')
    
    try:
        # Verify trust if requester info is provided
        requester = req.params.get('requester')
        if requester and not verify_agent_trust(requester):
            return func.HttpResponse(
                json.dumps({"error": "Requester not trusted"}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Get category parameter
        category = req.params.get('category', 'all')
        if not category:
            try:
                req_body = req.get_json()
                category = req_body.get('category', 'all')
            except ValueError:
                category = 'all'
        
        # Simulate tourist attraction data
        attractions = {
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
            ],
            "nature": [
                {
                    "name": "Gardens by the Bay",
                    "description": "Nature park with Supertrees",
                    "location": "18 Marina Gardens Drive"
                },
                {
                    "name": "Singapore Botanic Gardens",
                    "description": "UNESCO World Heritage site",
                    "location": "1 Cluny Road"
                }
            ],
            "culture": [
                {
                    "name": "Chinatown",
                    "description": "Historic ethnic neighborhood",
                    "location": "Chinatown district"
                },
                {
                    "name": "Little India",
                    "description": "Vibrant Indian cultural district",
                    "location": "Little India district"
                }
            ]
        }
        
        if category == 'all':
            results = attractions
        else:
            results = {category: attractions.get(category, [])}
        
        response_data = {
            "agent": get_agent_info("merlion"),
            "category": category,
            "attractions": results,
            "message": f"Tourist attractions for category: {category}"
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error in Merlion Agent: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
