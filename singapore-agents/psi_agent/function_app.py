"""Azure Function entrypoint for PSI Agent.

This agent provides Pollutant Standards Index (PSI) information for Singapore.
"""

import azure.functions as func
import logging
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.trust_module import verify_agent_trust, get_agent_info

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="psi")
def psi_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for PSI Agent.
    
    Args:
        req: The HTTP request object
        
    Returns:
        HTTP response with PSI information
    """
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
        location = req.params.get('location')
        if not location:
            try:
                req_body = req.get_json()
                location = req_body.get('location')
            except ValueError:
                pass
        if not location:
            location = 'national'
        
        # Simulate PSI data
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
