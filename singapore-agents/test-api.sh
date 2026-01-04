#!/bin/bash

# API Testing Script for Singapore Multi-Agent System
# Tests all endpoints locally or remotely

BASE_URL="${1:-http://localhost:7071/api}"

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Singapore Multi-Agent System - API Test Suite       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Base URL: $BASE_URL"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_key="$3"
    
    echo -e "${BLUE}Testing $name...${NC}"
    
    response=$(curl -s -w "\n%{http_code}" "$url")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ] && echo "$body" | jq -e ".$expected_key" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        echo "$body" | jq -C . 2>/dev/null || echo "$body"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        echo "Response: $body"
        ((FAILED++))
    fi
    echo ""
}

# Test Hawker Agent
test_endpoint "Hawker Agent" "${BASE_URL}/hawker?query=food" "agent"

# Test PSI Agent
test_endpoint "PSI Agent" "${BASE_URL}/psi?location=central" "agent"

# Test Merlion Agent  
test_endpoint "Merlion Agent" "${BASE_URL}/merlion?category=landmarks" "agent"

# Summary
echo "═══════════════════════════════════════════════════════"
echo -e "Test Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "═══════════════════════════════════════════════════════"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed!${NC}"
    exit 1
fi
