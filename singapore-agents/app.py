"""Flask application for local development and testing of Singapore agents.

This app simulates the Azure Functions environment locally using Flask,
allowing for easier development and testing of the agent endpoints.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import logging
import os

try:
    from shared.trust_module import verify_agent_trust, get_agent_info, get_all_agents
except ImportError:
    # Fallback for different execution contexts
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from shared.trust_module import verify_agent_trust, get_agent_info, get_all_agents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)


def get_request_param(param_name, default=None):
    """Helper function to extract parameter from request.
    
    Args:
        param_name: Name of the parameter to extract
        default: Default value if parameter not found
        
    Returns:
        Parameter value or default
    """
    value = request.args.get(param_name)
    if value is None and request.is_json:
        value = request.json.get(param_name)
    return value if value is not None else default


@app.route('/')
def index():
    """Root endpoint showing available agents."""
    agents = get_all_agents()
    return jsonify({
        "message": "Singapore Multi-Agent System",
        "version": "1.0.0",
        "agents": agents,
        "endpoints": {
            "hawker": "/api/hawker",
            "psi": "/api/psi",
            "merlion": "/api/merlion"
        }
    })


@app.route('/api/hawker', methods=['GET', 'POST'])
def hawker_agent():
    """Hawker Agent endpoint."""
    logging.info('Hawker Agent: Processing request.')
    
    try:
        # Verify trust if requester info is provided
        requester = get_request_param('requester')
        if requester and not verify_agent_trust(requester):
            return jsonify({"error": "Requester not trusted"}), 403
        
        # Get query parameter
        query = get_request_param('query')
        
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
                    },
                    {
                        "name": "Old Airport Road Food Centre",
                        "location": "51 Old Airport Road",
                        "popular_stalls": ["Nam Sing Hokkien Fried Mee", "Roast Paradise"]
                    }
                ],
                "message": f"Found hawker centers matching: {query}"
            }
            return jsonify(response_data), 200
        else:
            return jsonify({
                "agent": get_agent_info("hawker"),
                "message": "Please provide a query parameter"
            }), 400
    except Exception as e:
        logging.error(f"Error in Hawker Agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/psi', methods=['GET', 'POST'])
def psi_agent():
    """PSI Agent endpoint."""
    logging.info('PSI Agent: Processing request.')
    
    try:
        # Verify trust if requester info is provided
        requester = get_request_param('requester')
        if requester and not verify_agent_trust(requester):
            return jsonify({"error": "Requester not trusted"}), 403
        
        # Get location parameter
        location = get_request_param('location', 'national')
        
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
        
        return jsonify(response_data), 200
    except Exception as e:
        logging.error(f"Error in PSI Agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/merlion', methods=['GET', 'POST'])
def merlion_agent():
    """Merlion Agent endpoint."""
    logging.info('Merlion Agent: Processing request.')
    
    try:
        # Verify trust if requester info is provided
        requester = get_request_param('requester')
        if requester and not verify_agent_trust(requester):
            return jsonify({"error": "Requester not trusted"}), 403
        
        # Get category parameter
        category = get_request_param('category', 'all')
        
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
        
        return jsonify(response_data), 200
    except Exception as e:
        logging.error(f"Error in Merlion Agent: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode should only be enabled in development environments
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=debug_mode
    )
