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
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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
        "documentation": "https://github.com/codess-aus/Merlion-Multi-Agent",
        "demo": "/api/demo"
    }
    
    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )

# Demo page endpoint
@app.route(route="demo")
def demo_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """Serve the demo HTML page."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Singapore Multi-Agent System - Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .agent-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .agent-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .agent-icon {
            font-size: 3em;
            margin-right: 15px;
        }
        
        .agent-title {
            flex: 1;
        }
        
        .agent-title h2 {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .agent-title p {
            color: #666;
            font-size: 0.9em;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            color: #555;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        input, select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .response {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .response.show {
            display: block;
        }
        
        .response-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        
        .response-content {
            background: white;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .error {
            color: #e74c3c;
            background: #fde8e8;
            border-left-color: #e74c3c;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 10px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
        
        footer a {
            color: white;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦁 Singapore Multi-Agent System</h1>
            <p class="subtitle">Explore Singapore through intelligent agents</p>
        </header>
        
        <div class="agents-grid">
            <!-- Hawker Agent -->
            <div class="agent-card">
                <div class="agent-header">
                    <div class="agent-icon">🍜</div>
                    <div class="agent-title">
                        <h2>Hawker Agent</h2>
                        <p>Find hawker centers & food</p>
                    </div>
                </div>
                
                <div class="input-group">
                    <label for="hawker-query">Search for:</label>
                    <input type="text" id="hawker-query" placeholder="e.g., chicken rice, noodles" value="chicken rice">
                </div>
                
                <button onclick="testHawker()">Search Hawker Centers</button>
                
                <div id="hawker-response" class="response"></div>
            </div>
            
            <!-- PSI Agent -->
            <div class="agent-card">
                <div class="agent-header">
                    <div class="agent-icon">💨</div>
                    <div class="agent-title">
                        <h2>PSI Agent</h2>
                        <p>Check air quality</p>
                    </div>
                </div>
                
                <div class="input-group">
                    <label for="psi-location">Location:</label>
                    <select id="psi-location">
                        <option value="national">National</option>
                        <option value="north">North</option>
                        <option value="south">South</option>
                        <option value="east">East</option>
                        <option value="west">West</option>
                        <option value="central" selected>Central</option>
                    </select>
                </div>
                
                <button onclick="testPSI()">Get Air Quality</button>
                
                <div id="psi-response" class="response"></div>
            </div>
            
            <!-- Merlion Agent -->
            <div class="agent-card">
                <div class="agent-header">
                    <div class="agent-icon">🏛️</div>
                    <div class="agent-title">
                        <h2>Merlion Agent</h2>
                        <p>Discover attractions</p>
                    </div>
                </div>
                
                <div class="input-group">
                    <label for="merlion-category">Category:</label>
                    <select id="merlion-category">
                        <option value="all">All Attractions</option>
                        <option value="landmarks" selected>Landmarks</option>
                        <option value="nature">Nature</option>
                        <option value="culture">Culture</option>
                    </select>
                </div>
                
                <button onclick="testMerlion()">Find Attractions</button>
                
                <div id="merlion-response" class="response"></div>
            </div>
        </div>
        
        <footer>
            <p>Powered by Azure Functions | <a href="https://github.com/codess-aus/Merlion-Multi-Agent" target="_blank">View on GitHub</a></p>
        </footer>
    </div>
    
    <script>
        // Use relative URLs since we're on the same domain
        const API_BASE_URL = '/api';
        
        async function callAPI(endpoint, params) {
            const url = new URL(`${API_BASE_URL}/${endpoint}`, window.location.origin);
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        }
        
        function showLoading(elementId) {
            const element = document.getElementById(elementId);
            element.className = 'response show';
            element.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
        }
        
        function showResponse(elementId, data) {
            const element = document.getElementById(elementId);
            element.className = 'response show';
            element.innerHTML = `
                <div class="response-title">✓ Response:</div>
                <div class="response-content">${JSON.stringify(data, null, 2)}</div>
            `;
        }
        
        function showError(elementId, error) {
            const element = document.getElementById(elementId);
            element.className = 'response show error';
            element.innerHTML = `
                <div class="response-title">✗ Error:</div>
                <div class="response-content">${error.message || error}</div>
            `;
        }
        
        async function testHawker() {
            const query = document.getElementById('hawker-query').value;
            if (!query) {
                alert('Please enter a search term');
                return;
            }
            
            showLoading('hawker-response');
            try {
                const data = await callAPI('hawker', { query });
                showResponse('hawker-response', data);
            } catch (error) {
                showError('hawker-response', error);
            }
        }
        
        async function testPSI() {
            const location = document.getElementById('psi-location').value;
            
            showLoading('psi-response');
            try {
                const data = await callAPI('psi', { location });
                showResponse('psi-response', data);
            } catch (error) {
                showError('psi-response', error);
            }
        }
        
        async function testMerlion() {
            const category = document.getElementById('merlion-category').value;
            
            showLoading('merlion-response');
            try {
                const data = await callAPI('merlion', { category });
                showResponse('merlion-response', data);
            } catch (error) {
                showError('merlion-response', error);
            }
        }
        
        // Allow Enter key to submit
        document.getElementById('hawker-query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') testHawker();
        });
    </script>
</body>
</html>"""
    
    return func.HttpResponse(
        html_content,
        status_code=200,
        mimetype="text/html"
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
