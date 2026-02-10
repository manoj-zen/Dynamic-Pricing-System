# 🌐 Google Cloud Deployment - Quick Start

Your Dynamic Pricing System is ready to be deployed globally! Here are the quickest ways to get a public, shareable link.

## ⚡ Fastest Method: 3 Steps

### Step 1: Install Google Cloud CLI
```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install

# Verify installation
gcloud --version
```

### Step 2: Authenticate
```bash
# Sign in to Google Cloud
gcloud auth login

# A browser window will open - authorize access
```

### Step 3: Deploy to Cloud Run
```bash
# Navigate to project folder
cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery

# One-command deployment
gcloud run deploy dynamic-pricing \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# That's it! ✅ You'll get a public URL
```

**Result:** You'll see something like:
```
Service [dynamic-pricing] revision [dynamic-pricing-00001] has been deployed.
URL: https://dynamic-pricing-abc123-uc.a.run.app
```

## 📱 Share Your Link!

Your public link: `https://dynamic-pricing-abc123-uc.a.run.app`

Anyone with this link can:
- ✅ View the dashboard
- ✅ Load products
- ✅ Calculate dynamic prices
- ✅ View analytics
- ✅ Use the API

## 🎯 Alternative: Use Deployment Script

```bash
# Make script executable
chmod +x /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery/deploy.sh

# Run the script
./deploy.sh

# Follow prompts and deploy!
```

## 📊 What Gets Deployed

- ✅ **Backend API** - FastAPI server with ML model
- ✅ **Frontend Dashboard** - Interactive web UI
- ✅ **ML Model** - Pre-trained Random Forest
- ✅ **Database** - 200 grocery items data
- ✅ **API Endpoints** - All 15+ endpoints live

## 🔗 What You Get

| Component | URL |
|-----------|-----|
| Dashboard | https://dynamic-pricing-xxx-uc.a.run.app |
| API Base | https://dynamic-pricing-xxx-uc.a.run.app |
| Swagger Docs | https://dynamic-pricing-xxx-uc.a.run.app/docs |
| ReDoc | https://dynamic-pricing-xxx-uc.a.run.app/redoc |

## 💰 Cost

**Completely FREE!**
- 2 million requests/month free
- 365,000 GB-seconds/month free
- This project will cost $0 during free tier

## 🔒 Security

The deployment is:
- ✅ Public and accessible
- ✅ Auto-scaling (handles traffic)
- ✅ HTTPS encrypted
- ✅ Google-managed infrastructure

## 📝 API Usage Examples

```bash
# Get all products
curl https://dynamic-pricing-xxx-uc.a.run.app/products

# Get product price
curl https://dynamic-pricing-xxx-uc.a.run.app/price/1

# Predict dynamic price
curl -X POST https://dynamic-pricing-xxx-uc.a.run.app/predict-price \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "base_price": 50, "stock": 20, "sales_7": 30, "sales_30": 120, "day": 2}'
```

## ✨ Features Available Publicly

1. **Dashboard Tab**
   - View system statistics
   - Train model
   - Load products

2. **Products Tab**
   - Browse 200 grocery items
   - Search and filter
   - View pricing

3. **Price Calculator**
   - Calculate dynamic prices
   - Get recommendations

4. **Analytics Tab**
   - Top demanding products
   - Low stock alerts
   - High-value items

5. **Settings Tab**
   - Configure API URL
   - Export data
   - View system info

## 🚨 Troubleshooting

**"Command not found: gcloud"**
- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install

**"Permission denied"**
- Run: `gcloud auth login`
- Authorize in browser when prompted

**"Port already in use"**
- Cloud Run handles ports automatically
- No conflicts with local port 8000

**"Build failed"**
- Check requirements.txt is complete
- Verify Dockerfile exists
- View logs: `gcloud run logs read dynamic-pricing --follow`

## 📈 Next Steps After Deployment

1. **Test the URL** - Open in browser, load products, test API
2. **Share** - Give the link to anyone globally
3. **Monitor** - Check logs: `gcloud run logs read dynamic-pricing --follow`
4. **Update** - Push code changes, auto-deploys from GitHub (with CI/CD setup)
5. **Scale** - Adjust resources if needed

## 🔄 Update Deployment

```bash
# After making changes, redeploy:
cd /Users/vimalraj/Desktop/manoj/dynamic-pricing-grocery

gcloud run deploy dynamic-pricing \
  --source . \
  --region us-central1
```

## 📚 Full Deployment Guide

See `DEPLOYMENT_GUIDE.md` for advanced options including:
- Custom domains
- Database integration
- GitHub CI/CD
- Cloud Armor security
- Cost optimization

## 🎊 You're All Set!

Your Global URL: `https://dynamic-pricing-xxx-uc.a.run.app`

**Share it anywhere, anyone can access it!** 🚀
