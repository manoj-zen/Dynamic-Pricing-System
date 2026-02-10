from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from model import DynamicPricingModel
from datetime import datetime

app = FastAPI(title="Dynamic Pricing API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
pricing_model = DynamicPricingModel()
groceries_df = None
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "pricing_model.pkl")
csv_path = os.path.join(current_dir, "data", "groceries.csv")

# Load data on startup
def load_data():
    global groceries_df, pricing_model
    try:
        groceries_df = pd.read_csv(csv_path)
        if os.path.exists(model_path):
            pricing_model.load_model(model_path)
        else:
            print("Model not found. Please train the model first.")
    except Exception as e:
        print(f"Error loading data: {e}")

load_data()

# Pydantic models
class PricingRequest(BaseModel):
    product_id: int
    base_price: float
    stock: int
    sales_7: int
    sales_30: int
    day: int

class ProductUpdate(BaseModel):
    stock: int
    sales_7: int
    sales_30: int

class BulkPricingRequest(BaseModel):
    products: list[PricingRequest]

# Endpoints
@app.get("/")
def root():
    """Root endpoint with API info"""
    return {
        "name": "Dynamic Pricing API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "all_products": "/products",
            "product_price": "/price/{product_id}",
            "predict_price": "/predict-price",
            "bulk_pricing": "/bulk-pricing",
            "train_model": "/train-model",
            "model_status": "/model-status"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": pricing_model.model is not None,
        "products_loaded": len(groceries_df) if groceries_df is not None else 0
    }

@app.get("/products")
def get_all_products(skip: int = 0, limit: int = 20):
    """Get all products with pagination"""
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    products = groceries_df.iloc[skip:skip+limit].to_dict(orient='records')
    return {
        "total": len(groceries_df),
        "skip": skip,
        "limit": limit,
        "products": products
    }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Get specific product details"""
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    product = groceries_df[groceries_df['product_id'] == product_id]
    if product.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product.iloc[0].to_dict()

@app.post("/predict-price")
def predict_price(request: PricingRequest):
    """Predict dynamic price for a product"""
    if pricing_model.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model.")
    
    try:
        result = pricing_model.predict_dynamic_price(
            base_price=request.base_price,
            stock=request.stock,
            sales_7=request.sales_7,
            sales_30=request.sales_30,
            day=request.day
        )
        return {
            "product_id": request.product_id,
            **result,
            "recommendation": get_price_recommendation(result['change_percent'])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/price/{product_id}")
def get_product_dynamic_price(product_id: int):
    """Get dynamic price for a product from database"""
    if groceries_df is None or pricing_model.model is None:
        raise HTTPException(status_code=503, detail="Service unavailable")
    
    product = groceries_df[groceries_df['product_id'] == product_id]
    if product.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    
    prod = product.iloc[0]
    result = pricing_model.predict_dynamic_price(
        base_price=prod['base_price'],
        stock=prod['stock'],
        sales_7=prod['sales_7'],
        sales_30=prod['sales_30'],
        day=prod['day']
    )
    
    return {
        "product_id": product_id,
        "name": prod['name'],
        **result,
        "recommendation": get_price_recommendation(result['change_percent']),
        "stock": prod['stock'],
        "sales_7day": prod['sales_7'],
        "sales_30day": prod['sales_30']
    }

@app.post("/bulk-pricing")
def bulk_pricing(request: BulkPricingRequest):
    """Get dynamic prices for multiple products"""
    if pricing_model.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for product in request.products:
        try:
            result = pricing_model.predict_dynamic_price(
                base_price=product.base_price,
                stock=product.stock,
                sales_7=product.sales_7,
                sales_30=product.sales_30,
                day=product.day
            )
            results.append({
                "product_id": product.product_id,
                **result,
                "recommendation": get_price_recommendation(result['change_percent'])
            })
        except Exception as e:
            results.append({
                "product_id": product.product_id,
                "error": str(e)
            })
    
    return {
        "total_products": len(request.products),
        "successful": sum(1 for r in results if 'error' not in r),
        "results": results
    }

@app.post("/train-model")
def train_model():
    """Train the pricing model"""
    global pricing_model
    try:
        pricing_model = DynamicPricingModel()
        train_score, test_score = pricing_model.train(csv_path, model_path)
        return {
            "status": "success",
            "message": "Model trained successfully",
            "train_score": train_score,
            "test_score": test_score,
            "model_path": model_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/model-status")
def model_status():
    """Get model status and statistics"""
    if pricing_model.model is None:
        return {"status": "not_loaded", "model_loaded": False}
    
    return {
        "status": "loaded",
        "model_loaded": True,
        "model_type": type(pricing_model.model).__name__,
        "features": pricing_model.feature_names,
        "model_path": model_path
    }

@app.put("/product/{product_id}")
def update_product(product_id: int, update: ProductUpdate):
    """Update product stock and sales data"""
    global groceries_df
    
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    if product_id not in groceries_df['product_id'].values:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update data
    idx = groceries_df[groceries_df['product_id'] == product_id].index[0]
    groceries_df.loc[idx, 'stock'] = update.stock
    groceries_df.loc[idx, 'sales_7'] = update.sales_7
    groceries_df.loc[idx, 'sales_30'] = update.sales_30
    
    # Save to CSV
    groceries_df.to_csv(csv_path, index=False)
    
    return {
        "status": "updated",
        "product_id": product_id,
        "updated_fields": {
            "stock": update.stock,
            "sales_7": update.sales_7,
            "sales_30": update.sales_30
        }
    }

@app.get("/analytics/top-demand")
def top_demand_products(limit: int = 10):
    """Get top demanding products"""
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    top = groceries_df.nlargest(limit, 'sales_7')[['product_id', 'name', 'base_price', 'sales_7', 'sales_30']]
    return {"top_products": top.to_dict(orient='records')}

@app.get("/analytics/low-stock")
def low_stock_products(threshold: int = 10):
    """Get products with low stock"""
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    low = groceries_df[groceries_df['stock'] < threshold][['product_id', 'name', 'base_price', 'stock', 'sales_7']]
    return {"low_stock_products": low.to_dict(orient='records')}

@app.get("/analytics/high-value")
def high_value_products(limit: int = 10):
    """Get highest priced products"""
    if groceries_df is None:
        raise HTTPException(status_code=500, detail="Products data not loaded")
    
    high = groceries_df.nlargest(limit, 'base_price')[['product_id', 'name', 'base_price', 'stock']]
    return {"high_value_products": high.to_dict(orient='records')}

def get_price_recommendation(change_percent):
    """Get recommendation based on price change"""
    if change_percent > 10:
        return "PREMIUM - High demand detected"
    elif change_percent > 5:
        return "INCREASED - Moderate demand"
    elif change_percent < -10:
        return "CLEARANCE - Low demand, increase visibility"
    elif change_percent < -5:
        return "DISCOUNTED - Reduce to move inventory"
    else:
        return "OPTIMAL - Balanced pricing"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
