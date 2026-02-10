# 🌐 Deploy to Google Cloud - Complete Guide

This guide will help you deploy the Dynamic Pricing System to Google Cloud Run so anyone can access it via a public URL.

## 📋 Prerequisites

1. **Google Cloud Account** - [Create free account](https://cloud.google.com/free)
2. **Google Cloud CLI** - [Download gcloud CLI](https://cloud.google.com/sdk/docs/install)
3. **Docker** - [Download Docker](https://www.docker.com/products/docker-desktop) (optional, Cloud Build handles it)

## 🚀 Step-by-Step Deployment

### Step 1: Set Up Google Cloud Project

```bash
# 1. Create a new Google Cloud Project
# Go to: https://console.cloud.google.com/projectcreate
# Or use gcloud CLI:
gcloud projects create dynamic-pricing-system --name="Dynamic Pricing System"

# 2. Set your project as default
gcloud config set project dynamic-pricing-system

# 3. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Configure Authentication

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set up Docker authentication
gcloud auth configure-docker
```

### Step 3: Deploy Backend to Cloud Run

```bash
# Navigate to project directory
cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery

# Deploy using Cloud Build (easiest method)
gcloud run deploy dynamic-pricing \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PORT=8080

# This will:
# 1. Build Docker image automatically
# 2. Push to Google Container Registry
# 3. Deploy to Cloud Run
# 4. Generate a public URL
```

**Expected Output:**
```
Service [dynamic-pricing] revision [dynamic-pricing-00001] has been deployed.
URL: https://dynamic-pricing-abc123-uc.a.run.app
```

### Step 4: Deploy Frontend

#### Option A: Deploy with Backend (Recommended)

The frontend is already included in the Docker image. After backend deployment, access it at the Cloud Run URL.

#### Option B: Deploy Frontend to Firebase Hosting

```bash
# 1. Install Firebase CLI
npm install -g firebase-tools

# 2. Login to Firebase
firebase login

# 3. Initialize Firebase project
cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery
firebase init hosting

# 4. Update firebase.json
# Configure "public" to point to "frontend" directory

# 5. Deploy frontend
firebase deploy
```

### Step 5: Update API Configuration

After deployment, update the frontend to use the correct API URL:

1. Note your Cloud Run URL: `https://dynamic-pricing-abc123-uc.a.run.app`

2. Update `frontend/script.js`:
```javascript
const API_BASE_URL = 'https://dynamic-pricing-abc123-uc.a.run.app';
```

3. Or update via dashboard Settings → API Configuration

## 🔗 Accessing Your Application

### Backend API
- **Base URL**: `https://dynamic-pricing-abc123-uc.a.run.app`
- **API Docs**: `https://dynamic-pricing-abc123-uc.a.run.app/docs`
- **ReDoc**: `https://dynamic-pricing-abc123-uc.a.run.app/redoc`

### Frontend Dashboard
- **URL**: `https://dynamic-pricing-abc123-uc.a.run.app` (if deployed as single service)
- **Or separate Firebase URL** (if deployed to Firebase)

## 📊 Example API Calls (Public URLs)

```bash
# Check health
curl https://dynamic-pricing-abc123-uc.a.run.app/health

# Get all products
curl https://dynamic-pricing-abc123-uc.a.run.app/products

# Get dynamic price
curl https://dynamic-pricing-abc123-uc.a.run.app/price/1

# Predict price (POST)
curl -X POST https://dynamic-pricing-abc123-uc.a.run.app/predict-price \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "base_price": 50,
    "stock": 20,
    "sales_7": 30,
    "sales_30": 120,
    "day": 2
  }'
```

## 🔧 Advanced Deployment Options

### Option 1: Deploy with Cloud Build (Recommended for CI/CD)

```bash
# Build and deploy using Cloud Build
gcloud builds submit --config=cloudbuild.yaml

# Monitor build progress
gcloud builds list --limit=1 --format='value(ID)' | xargs gcloud builds log
```

### Option 2: Manual Docker Build and Deploy

```bash
# Build Docker image locally
docker build -t dynamic-pricing:latest .

# Tag for Google Container Registry
docker tag dynamic-pricing:latest gcr.io/PROJECT_ID/dynamic-pricing:latest

# Push to registry
docker push gcr.io/PROJECT_ID/dynamic-pricing:latest

# Deploy from image
gcloud run deploy dynamic-pricing \
  --image gcr.io/PROJECT_ID/dynamic-pricing:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Deploy with Custom Domain

```bash
# Map custom domain to Cloud Run service
gcloud run services update-traffic dynamic-pricing --to-revisions LATEST=100 --region us-central1

# Set up custom domain in Cloud Run console
# 1. Go to https://console.cloud.google.com/run
# 2. Click on "dynamic-pricing" service
# 3. Click "Manage Custom Domains"
# 4. Add your domain
```

## 🔒 Security Best Practices

### 1. Restrict Access (Optional)

```bash
# Remove public access
gcloud run services update dynamic-pricing \
  --no-allow-unauthenticated \
  --region us-central1

# Add specific users
gcloud run services add-iam-policy-binding dynamic-pricing \
  --member=user:EMAIL@example.com \
  --role=roles/run.invoker \
  --region us-central1
```

### 2. Environment Variables

```bash
# Set environment variables
gcloud run services update dynamic-pricing \
  --set-env-vars KEY=value \
  --region us-central1
```

### 3. Enable Cloud Armor (DDoS Protection)

```bash
# Requires setting up load balancer
# See: https://cloud.google.com/run/docs/securing/cloud-armor
```

## 📈 Monitoring and Logging

### View Logs

```bash
# Real-time logs
gcloud run services logs read dynamic-pricing --follow --limit 50

# Specific revision logs
gcloud run revisions describe REVISION_NAME --region us-central1
```

### Monitor Performance

Go to: https://console.cloud.google.com/run/detail/REGION/dynamic-pricing/logs

## 💰 Cost Estimation (Free Tier)

Google Cloud Run provides:
- ✅ **2 million requests/month** - FREE
- ✅ **365,000 GB-seconds/month** - FREE
- ✅ **24/7 always-on capability**

For this project: **Completely FREE** during free tier!

After free tier:
- ~$0.40 per million requests
- ~$0.00001667 per GB-second
- Typical cost: $5-20/month for moderate usage

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Cloud Run automatically assigns PORT environment variable
# Dockerfile and app.py handle this automatically
```

### Issue: "Module not found"
```bash
# Ensure all requirements are in requirements.txt
# Rebuild and redeploy:
gcloud run deploy dynamic-pricing --source . --region us-central1
```

### Issue: "Permission denied"
```bash
# Check IAM permissions
gcloud projects get-iam-policy dynamic-pricing-system

# Grant necessary permissions
gcloud projects add-iam-policy-binding dynamic-pricing-system \
  --member=serviceAccount:YOUR_SA@PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/run.admin
```

### Issue: "File not found" (CSV/Model)
```bash
# Ensure Dockerfile copies data files:
# COPY backend/data/ data/

# Rebuild Docker image
docker build --no-cache -t dynamic-pricing:latest .
```

## 🔄 Continuous Deployment (CI/CD)

### Setup GitHub Integration

```bash
# 1. Create GitHub repository
# 2. Connect to Cloud Build
#    https://console.cloud.google.com/cloud-build/github

# 3. Create cloudbuild.yaml in repo root (already provided)

# 4. On each push, Cloud Build automatically:
#    - Builds Docker image
#    - Runs tests
#    - Deploys to Cloud Run
```

## 📱 Share Public Link

After deployment, share this link with anyone:

```
https://dynamic-pricing-abc123-uc.a.run.app
```

They can:
- ✅ View live dashboard
- ✅ Load products
- ✅ Calculate prices
- ✅ View analytics
- ✅ Use API endpoints

## 🎯 Next Steps

1. **Deploy**: Follow Step 1-3 above
2. **Share**: Send the Cloud Run URL to anyone
3. **Monitor**: Check logs and performance
4. **Scale**: Adjust resources as needed
5. **Secure**: Add authentication if needed

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Deploying Python Apps](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)

---

**Your application will be live globally in ~5 minutes!** 🚀
