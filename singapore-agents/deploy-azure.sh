#!/bin/bash

# Azure Deployment Script for Singapore Multi-Agent System
# This script sets up all necessary Azure resources and deploys the application

set -e  # Exit on error

echo "🚀 Singapore Multi-Agent System - Azure Deployment"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first:${NC}"
    echo "   https://learn.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  You are not logged in to Azure. Running 'az login'...${NC}"
    az login
fi

# Get current subscription
SUBSCRIPTION=$(az account show --query id -o tsv)
echo -e "${GREEN}✓ Using subscription: $SUBSCRIPTION${NC}"

# Prompt for configuration
read -p "Enter resource group name (default: rg-singapore-agents): " RESOURCE_GROUP
RESOURCE_GROUP=${RESOURCE_GROUP:-rg-singapore-agents}

read -p "Enter location (default: eastasia): " LOCATION
LOCATION=${LOCATION:-eastasia}

read -p "Enter function app name (default: singapore-agents-app): " FUNCTION_APP
FUNCTION_APP=${FUNCTION_APP:-singapore-agents-app}

read -p "Enter storage account name (default: stgsgagents$(date +%s | tail -c 6)): " STORAGE_ACCOUNT
STORAGE_ACCOUNT=${STORAGE_ACCOUNT:-stgsgagents$(date +%s | tail -c 6)}

echo ""
echo -e "${YELLOW}Configuration Summary:${NC}"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Function App: $FUNCTION_APP"
echo "  Storage Account: $STORAGE_ACCOUNT"
echo ""

read -p "Continue with deployment? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Step 1: Create Resource Group
echo ""
echo -e "${YELLOW}Step 1: Creating resource group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION
echo -e "${GREEN}✓ Resource group created${NC}"

# Step 2: Create Storage Account
echo ""
echo -e "${YELLOW}Step 2: Creating storage account...${NC}"
az storage account create \
    --name $STORAGE_ACCOUNT \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --sku Standard_LRS \
    --allow-shared-key-access true
echo -e "${GREEN}✓ Storage account created${NC}"

# Step 3: Create Function App
echo ""
echo -e "${YELLOW}Step 3: Creating function app...${NC}"
az functionapp create \
    --resource-group $RESOURCE_GROUP \
    --consumption-plan-location $LOCATION \
    --name $FUNCTION_APP \
    --storage-account $STORAGE_ACCOUNT \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --os-type Linux
echo -e "${GREEN}✓ Function app created${NC}"

# Step 4: Enable Application Insights
echo ""
echo -e "${YELLOW}Step 4: Enabling Application Insights...${NC}"
az monitor app-insights component create \
    --app $FUNCTION_APP \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --application-type web
echo -e "${GREEN}✓ Application Insights enabled${NC}"

# Step 5: Deploy code
echo ""
echo -e "${YELLOW}Step 5: Deploying code to Azure...${NC}"
echo "This may take 2-5 minutes..."
func azure functionapp publish $FUNCTION_APP --build remote
echo -e "${GREEN}✓ Code deployed${NC}"

# Step 6: Display deployment summary
echo ""
echo -e "${GREEN}=================================================="
echo "✓ Deployment Complete!${NC}"
echo ""
echo -e "${YELLOW}Your application is now live at:${NC}"
FUNCTION_URL="https://${FUNCTION_APP}.azurewebsites.net"
echo "  $FUNCTION_URL"
echo ""
echo -e "${YELLOW}API Endpoints:${NC}"
echo "  Root:    $FUNCTION_URL/api"
echo "  Hawker:  $FUNCTION_URL/api/hawker?query=food"
echo "  PSI:     $FUNCTION_URL/api/psi?location=central"
echo "  Merlion: $FUNCTION_URL/api/merlion?category=landmarks"
echo ""
echo -e "${YELLOW}View logs:${NC}"
echo "  func azure functionapp logstream $FUNCTION_APP"
echo ""
echo -e "${YELLOW}Save these details:${NC}"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Function App: $FUNCTION_APP"
echo "  Storage Account: $STORAGE_ACCOUNT"
echo ""
