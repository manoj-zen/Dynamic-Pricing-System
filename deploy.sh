#!/bin/bash

# 🚀 Quick Deploy to Google Cloud Run
# This script automates the deployment process

set -e

echo "======================================"
echo "🚀 Dynamic Pricing - Cloud Deployment"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v gcloud &> /dev/null; then
    echo -e "${YELLOW}⚠️  Google Cloud SDK not found. Installing...${NC}"
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}ℹ️  Docker not found (optional for Cloud Build)${NC}"
fi

echo -e "${GREEN}✓ Prerequisites checked${NC}"
echo ""

# Get project details
echo -e "${BLUE}📝 Enter Google Cloud details:${NC}"

read -p "Enter Project ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID="dynamic-pricing-$(date +%s)"
    echo -e "${YELLOW}Creating new project: $PROJECT_ID${NC}"
    gcloud projects create "$PROJECT_ID" --name="Dynamic Pricing System"
fi

echo ""
echo -e "${BLUE}🔧 Configuring Google Cloud...${NC}"

# Set project
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✓ Project set to: $PROJECT_ID${NC}"

# Enable APIs
echo "Enabling APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable containerregistry.googleapis.com
echo -e "${GREEN}✓ APIs enabled${NC}"

echo ""
echo -e "${BLUE}🐳 Building and deploying to Cloud Run...${NC}"

# Deploy
SERVICE_NAME="dynamic-pricing"
REGION="us-central1"

gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300

echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format='value(status.url)')

echo "======================================"
echo -e "${GREEN}🎉 SUCCESS!${NC}"
echo "======================================"
echo ""
echo "📱 Your application is live at:"
echo -e "${BLUE}$SERVICE_URL${NC}"
echo ""
echo "📊 Dashboard: $SERVICE_URL"
echo "📚 API Docs: $SERVICE_URL/docs"
echo ""
echo "🔗 Share this link with anyone to access!"
echo ""
echo "======================================"
echo ""
echo "📝 Next steps:"
echo "1. Update frontend API URL in script.js if needed"
echo "2. Test the application"
echo "3. Monitor at: https://console.cloud.google.com/run"
echo ""
