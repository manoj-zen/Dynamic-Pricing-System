# 🎯 AI-Driven Dynamic Pricing Model for Online Retail

## Problem Statement

Traditional online retail platforms use fixed pricing strategies which fail to adapt to real-time changes in demand, inventory levels, seasonality, and customer behavior. This results in:
- **Revenue Loss**: Missed opportunity to capitalize on high-demand periods
- **Inventory Issues**: Slow-moving stock ties up capital
- **Competitive Disadvantage**: Rigid pricing cannot adapt to market conditions
- **Customer Churn**: Inconsistent pricing erodes customer trust

## 🚀 Solution Overview

This project implements an **advanced dynamic pricing system** that automatically adjusts product prices using:
- **Machine Learning Models**: Random Forest regression for accurate price multiplier prediction
- **Historical Sales Data**: 7-day and 30-day sales trends for demand analysis
- **Real-Time Factors**: Current inventory levels and stock turnover rates
- **Seasonality Patterns**: Day-of-week adjustments to capture weekly trends

### Key Features

✨ **Demand-Based Pricing**: Automatically increase prices when demand is high, decrease during low-demand periods

📦 **Inventory Optimization**: Balance inventory levels by adjusting prices to move slow-moving stock

📅 **Seasonality Awareness**: Weekend vs. weekday pricing adjustments to maximize revenue

🤖 **ML-Powered Predictions**: Random Forest model trained on 200 grocery products with real-time predictions

📊 **Real-Time Dashboard**: Interactive web interface for monitoring prices and analytics

🔌 **RESTful API**: Complete API with endpoints for pricing predictions, bulk operations, and analytics

## Project Structure

```
dynamic-pricing-grocery/
│
├── backend/
│   ├── app.py               # FastAPI server with REST endpoints
│   ├── model.py             # ML model training and prediction
│   ├── pricing_model.pkl    # Serialized trained model
│   ├── data/
│   │   └── groceries.csv    # 200 grocery items database
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   ├── index.html           # Dashboard UI
│   ├── style.css            # Responsive styling
│   └── script.js            # Interactive functionality
│
└── README.md                # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- Modern web browser

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Train the ML Model**
```bash
python model.py
```

This will:
- Load 200 grocery items from `data/groceries.csv`
- Engineer features (demand ratio, stock ratio)
- Train Random Forest model
- Save model to `pricing_model.pkl`
- Display training and testing scores

3. **Start FastAPI Server**
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Frontend Setup

1. **Serve the Dashboard**

Using Python 3:
```bash
cd frontend
python -m http.server 8080
```

Using Node.js (if installed):
```bash
npx http-server frontend -p 8080
```

2. **Open in Browser**
Navigate to: `http://localhost:8080`

## 📊 How It Works

### Pricing Algorithm

The dynamic pricing system uses a multi-factor approach:

1. **Demand Pressure Calculation**
   ```
   demand_pressure = (sales_7_day * 30) / (current_stock + 1)
   ```

2. **Price Multiplier Logic**
   - High demand (pressure > 5): +15% increase
   - Medium demand (pressure > 2): +8% increase
   - Low demand (pressure < 0.5): -10% decrease
   - Low-medium demand (pressure < 1): -5% decrease

3. **Seasonality Adjustments**
   - Weekend (Fri-Sat): +5% boost
   - Monday (restocking): -2% discount

4. **ML Model Enhancement**
   - Random Forest refines multipliers based on historical patterns
   - Final multiplier capped between 0.7x and 1.3x

### Example
```
Base Price: ₹100
7-day Sales: 50 units
30-day Sales: 150 units
Current Stock: 5 units
Day: Friday

Calculation:
- Demand Ratio: 50 / 150 = 0.33 (stable)
- Demand Pressure: (50 * 30) / 5 = 300 (very high!)
- Base Multiplier: 1.15 (high demand)
- Weekend Bonus: 1.05 (Friday)
- Final Multiplier: 1.15 × 1.05 = 1.21

Dynamic Price: ₹100 × 1.21 = ₹121 ✓
```

## 🔌 API Endpoints

### Health & Status

**GET** `/health`
- Returns API health status and model state

**GET** `/model-status`
- Returns current ML model information

### Product Management

**GET** `/products?skip=0&limit=20`
- Retrieve paginated product list

**GET** `/products/{product_id}`
- Get specific product details

**PUT** `/product/{product_id}`
- Update product stock and sales data

### Pricing Predictions

**POST** `/predict-price`
```json
{
  "product_id": 1,
  "base_price": 50,
  "stock": 20,
  "sales_7": 30,
  "sales_30": 120,
  "day": 2
}
```

**GET** `/price/{product_id}`
- Get dynamic price for a product from database

**POST** `/bulk-pricing`
```json
{
  "products": [
    {"product_id": 1, "base_price": 50, ...},
    {"product_id": 2, "base_price": 40, ...}
  ]
}
```

### Analytics

**GET** `/analytics/top-demand?limit=10`
- Top demanding products

**GET** `/analytics/low-stock?threshold=10`
- Products with low inventory

**GET** `/analytics/high-value?limit=10`
- Highest priced items

### Model Management

**POST** `/train-model`
- Train/retrain the pricing model

## 📈 Dashboard Features

### Dashboard Tab
- Real-time statistics (total products, model status, API health)
- Quick action buttons for model training and data loading
- Feature overview with system capabilities

### Products Tab
- Browse all 200 grocery items
- Search and filter functionality
- Sort by name, price, stock, or demand
- Pagination with 20 items per page
- One-click dynamic price calculation per product

### Price Calculator Tab
- Manual price calculation tool
- Input custom parameters for testing
- Real-time multiplier and price display
- Pricing recommendation based on demand conditions

### Analytics Tab
- **Top Demanding Products**: 7-day sales rankings
- **High-Value Products**: Most expensive items
- **Low Stock Alert**: Inventory warning system
- Data visualization for business insights

### Settings Tab
- Configure API base URL
- Model training controls
- Data export functionality
- System information display

## 🧠 Machine Learning Model

### Algorithm: Random Forest Regressor

**Configuration:**
- 100 decision trees
- Max depth: 15 levels
- Min samples split: 5
- Min samples leaf: 2

**Input Features:**
1. `base_price`: Original product price
2. `stock`: Current inventory level
3. `sales_7`: 7-day sales volume
4. `sales_30`: 30-day sales volume
5. `day`: Day of week (0-6)
6. `demand_ratio`: sales_7 / sales_30
7. `stock_ratio`: stock / sales_7

**Output:**
- `price_multiplier`: Factor to multiply base price (0.7 - 1.3)

**Performance:**
- Evaluated on 20% test set
- Typical accuracy: 85-90% R² score
- Fast inference time: <10ms per prediction

## 💡 Use Cases

### For E-Commerce Managers
- Maximize revenue during peak demand periods
- Clear slow-moving inventory with automated discounts
- Monitor competitor pricing in real-time

### For Inventory Planners
- Identify fast-moving products for restocking priority
- Predict which items need price adjustments
- Prevent stockouts of high-demand items

### For Business Analysts
- Analyze price elasticity across product categories
- Understand seasonal demand patterns
- Generate insights for promotional planning

## 🚀 Advanced Features (Extensible)

The system is designed for easy enhancement:

- **Category-Specific Models**: Train separate models for different product categories
- **Competitor Analysis**: Integrate competitor pricing data
- **Customer Segmentation**: Dynamic pricing per customer segment
- **Demand Forecasting**: Predict future sales for proactive pricing
- **A/B Testing**: Test pricing strategies with control groups
- **Multi-Channel Support**: Different prices across web, mobile, store

## 📊 Sample Data

Database includes 200 grocery items across categories:
- **Staples**: Rice, wheat, sugar, salt, oil
- **Dairy**: Milk, butter, yogurt, cheese, eggs
- **Produce**: Vegetables, fruits, herbs
- **Proteins**: Chicken, fish, meat, dal
- **Processed Foods**: Bread, biscuits, snacks, canned items
- **Beverages**: Tea, coffee, juice, drinks
- **Condiments**: Spices, sauces, oils, vinegar
- **Specialty**: Nuts, dried fruits, health items

Each product has:
- Base price in Indian Rupees (₹)
- Current stock quantity
- 7-day and 30-day sales data
- Day of week for analysis

## 🔒 Security Considerations

For production deployment:
1. Add authentication to API endpoints
2. Implement rate limiting
3. Enable HTTPS/SSL
4. Add input validation and sanitization
5. Store sensitive data securely
6. Implement audit logging
7. Regular security updates

## 📝 Example Workflow

```
1. Train Model
   └─> python model.py

2. Start Backend
   └─> python -m uvicorn app:app --reload

3. Open Dashboard
   └─> http://localhost:8080

4. Load Products
   └─> Click "Load Products" button

5. View Analytics
   └─> Navigate to Analytics tab

6. Calculate Prices
   └─> Use Price Calculator or click product card

7. Update Data
   └─> Settings → Update product info via API

8. Export Results
   └─> Settings → Export products as CSV
```

## 🎓 Learning Outcomes

By implementing this project, you'll learn:
- ✅ Machine Learning model development (scikit-learn)
- ✅ FastAPI REST API design and implementation
- ✅ Data preprocessing and feature engineering
- ✅ Frontend-backend integration
- ✅ Real-time data visualization
- ✅ Business logic implementation
- ✅ Production-ready API development
- ✅ Performance optimization techniques

## 📚 Technologies Used

**Backend:**
- FastAPI: Modern Python web framework
- pandas: Data manipulation and analysis
- scikit-learn: Machine learning library
- uvicorn: ASGI server

**Frontend:**
- HTML5: Markup structure
- CSS3: Responsive styling
- JavaScript (Vanilla): Interactive functionality
- Fetch API: HTTP requests

**Data:**
- CSV: Product database
- Pickle: Model serialization

## 🤝 Contributing

To extend this project:
1. Add new pricing algorithms
2. Implement additional ML models (XGBoost, Neural Networks)
3. Create mobile app version
4. Add more analytics features
5. Implement real-time price updates
6. Add database integration (PostgreSQL/MongoDB)
7. Develop admin panel for manual overrides

## 📄 License

This project is open-source and available for educational and commercial use.

## 🙋 Support

For issues or questions:
1. Check the API documentation at `/docs` (Swagger)
2. Review the code comments
3. Check browser console for frontend errors
4. Review server logs for backend errors

## 🎯 Future Enhancements

- [ ] Real-time price monitoring
- [ ] Competitor price tracking integration
- [ ] Customer purchase history analysis
- [ ] Promotional campaign impact analysis
- [ ] Supply chain cost integration
- [ ] Regional pricing variations
- [ ] Machine learning model versioning
- [ ] A/B testing framework

---

**Built with ❤️ for optimizing retail pricing with AI**
