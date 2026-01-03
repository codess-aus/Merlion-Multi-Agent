"""Azure Function entrypoint for Hawker Agent.

This agent provides information about hawker centers in Singapore.
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

@app.route(route="hawker")
def hawker_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for Hawker Agent.
    
    Args:
        req: The HTTP request object
        
    Returns:
        HTTP response with hawker center information
    """
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
            # Simulate hawker center data
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
