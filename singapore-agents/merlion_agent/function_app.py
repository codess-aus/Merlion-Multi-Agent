"""Azure Function entrypoint for Merlion Agent.

This agent provides tourist information and attractions in Singapore.
"""

import azure.functions as func
import logging
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.trust_module import verify_agent_trust, get_agent_info

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="merlion")
def merlion_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for Merlion Agent.
    
    Args:
        req: The HTTP request object
        
    Returns:
        HTTP response with tourist attraction information
    """
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
        category = req.params.get('category')
        if not category:
            try:
                req_body = req.get_json()
                category = req_body.get('category')
            except ValueError:
                pass
        if not category:
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
