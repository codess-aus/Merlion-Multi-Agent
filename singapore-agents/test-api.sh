#!/bin/bash

# API Testing Script for Singapore Multi-Agent System
# Tests all endpoints locally or remotely

BASE_URL="${1:-http://localhost:7071/api}"

echo "Testing Singapore Multi-Agent System API"
echo "========================================"
echo "Base URL: $BASE_URL"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test root endpoint
echo -e "${YELLOW}Testing Root Endpoint...${NC}"
curl -s "${BASE_URL}" | jq . || echo "Failed to reach root endpoint"
echo ""

# Test Hawker Agent
echo -e "${YELLOW}Testing Hawker Agent...${NC}"
curl -s "${BASE_URL}/hawker?query=food" | jq . || echo "Failed"
echo ""

# Test PSI Agent
echo -e "${YELLOW}Testing PSI Agent...${NC}"
curl -s "${BASE_URL}/psi?location=central" | jq . || echo "Failed"
echo ""

# Test Merlion Agent
echo -e "${YELLOW}Testing Merlion Agent...${NC}"
curl -s "${BASE_URL}/merlion?category=landmarks" | jq . || echo "Failed"
echo ""

echo -e "${GREEN}Testing complete!${NC}"
