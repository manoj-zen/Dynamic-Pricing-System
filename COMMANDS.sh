#!/bin/bash

# ============================================================================
# 🚀 COMMAND REFERENCE - Copy & Paste Ready Commands
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║            DYNAMIC PRICING DEPLOYMENT COMMAND REFERENCE           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# 1. INSTALL GOOGLE CLOUD SDK
# ============================================================================

echo "1️⃣  INSTALL GOOGLE CLOUD SDK"
echo "   Download from: https://cloud.google.com/sdk/docs/install"
echo "   Or run:"
echo "   $ curl https://sdk.cloud.google.com | bash"
echo ""

# ============================================================================
# 2. VERIFY INSTALLATION
# ============================================================================

echo "2️⃣  VERIFY GCLOUD IS INSTALLED"
echo "   $ gcloud --version"
echo ""

# ============================================================================
# 3. AUTHENTICATE
# ============================================================================

echo "3️⃣  AUTHENTICATE WITH GOOGLE CLOUD"
echo "   $ gcloud auth login"
echo "   (Browser will open - authorize access)"
echo ""

# ============================================================================
# 4. DEPLOY COMMAND (FASTEST)
# ============================================================================

echo "4️⃣  DEPLOY TO CLOUD RUN (ONE COMMAND)"
echo ""
echo "   $ cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery"
echo ""
echo "   $ gcloud run deploy dynamic-pricing \\"
echo "     --source . \\"
echo "     --platform managed \\"
echo "     --region us-central1 \\"
echo "     --allow-unauthenticated"
echo ""
echo "   ⏱️  Wait 2-5 minutes..."
echo ""

# ============================================================================
# 5. GET SERVICE URL
# ============================================================================

echo "5️⃣  GET YOUR PUBLIC URL"
echo "   $ gcloud run services describe dynamic-pricing \\"
echo "     --region us-central1 \\"
echo "     --format='value(status.url)'"
echo ""

# ============================================================================
# 6. VIEW LOGS
# ============================================================================

echo "6️⃣  VIEW DEPLOYMENT LOGS (REAL-TIME)"
echo "   $ gcloud run services logs read dynamic-pricing --follow"
echo ""

# ============================================================================
# 7. UPDATE DEPLOYMENT
# ============================================================================

echo "7️⃣  UPDATE DEPLOYMENT (After code changes)"
echo "   $ cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery"
echo "   $ gcloud run deploy dynamic-pricing --source . --region us-central1"
echo ""

# ============================================================================
# 8. ALTERNATIVE: USING AUTOMATED SCRIPT
# ============================================================================

echo "8️⃣  ALTERNATIVE: USE DEPLOYMENT SCRIPT"
echo "   $ cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery"
echo "   $ chmod +x deploy.sh"
echo "   $ ./deploy.sh"
echo ""

# ============================================================================
# 9. BUILD LOCALLY (OPTIONAL)
# ============================================================================

echo "9️⃣  BUILD DOCKER IMAGE LOCALLY (OPTIONAL)"
echo "   $ cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery"
echo "   $ docker build -t dynamic-pricing:latest ."
echo "   $ docker run -p 5000:8080 dynamic-pricing:latest"
echo ""

# ============================================================================
# 10. TRAIN MODEL LOCALLY (OPTIONAL)
# ============================================================================

echo "🔟 TRAIN ML MODEL LOCALLY"
echo "   $ cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery"
echo "   $ source .venv/bin/activate"
echo "   $ python backend/model.py"
echo ""

# ============================================================================
# ADDITIONAL HELPFUL COMMANDS
# ============================================================================

echo "════════════════════════════════════════════════════════════════════"
echo "📝 ADDITIONAL COMMANDS"
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "List all Cloud Run services:"
echo "   $ gcloud run services list --region us-central1"
echo ""

echo "Delete the service:"
echo "   $ gcloud run services delete dynamic-pricing --region us-central1"
echo ""

echo "Monitor service:"
echo "   $ gcloud run services describe dynamic-pricing --region us-central1"
echo ""

echo "Update service configuration:"
echo "   $ gcloud run services update dynamic-pricing --region us-central1 \\"
echo "     --memory 512Mi --cpu 1"
echo ""

echo "Set environment variables:"
echo "   $ gcloud run services update dynamic-pricing --region us-central1 \\"
echo "     --set-env-vars KEY=value"
echo ""

echo "Add custom domain:"
echo "   $ gcloud run domain-mappings create --service dynamic-pricing \\"
echo "     --domain yourdomain.com --region us-central1"
echo ""

# ============================================================================
# QUICK COPY-PASTE DEPLOY
# ============================================================================

echo "════════════════════════════════════════════════════════════════════"
echo "⚡ QUICK COPY-PASTE (Replace placeholder values)"
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "FASTEST WAY TO DEPLOY:"
echo ""
echo "gcloud auth login && cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery && gcloud run deploy dynamic-pricing --source . --platform managed --region us-central1 --allow-unauthenticated && gcloud run services describe dynamic-pricing --region us-central1 --format='value(status.url)'"
echo ""

# ============================================================================
# TROUBLESHOOTING COMMANDS
# ============================================================================

echo "════════════════════════════════════════════════════════════════════"
echo "🐛 TROUBLESHOOTING COMMANDS"
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "Check if gcloud is installed:"
echo "   $ which gcloud"
echo ""

echo "Check Python version:"
echo "   $ python --version"
echo ""

echo "Check Docker is installed:"
echo "   $ docker --version"
echo ""

echo "View recent build logs:"
echo "   $ gcloud builds list --limit=5"
echo ""

echo "View specific build log:"
echo "   $ gcloud builds log BUILD_ID"
echo ""

echo "Test API locally before deploying:"
echo "   $ curl http://localhost:5000/health"
echo ""

# ============================================================================
# END
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "✅ For step-by-step guide, read: PUBLIC_LINK_GUIDE.md"
echo "════════════════════════════════════════════════════════════════════"
echo ""

