import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
import os

class DynamicPricingModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['base_price', 'stock', 'sales_7', 'sales_30', 'day', 'demand_ratio', 'stock_ratio']
        
    def load_data(self, csv_path):
        """Load grocery data from CSV"""
        df = pd.read_csv(csv_path)
        return df
    
    def calculate_features(self, df):
        """Calculate additional features for pricing"""
        df['demand_ratio'] = df['sales_7'] / (df['sales_30'] + 1)  # 7-day to 30-day ratio
        df['stock_ratio'] = df['stock'] / (df['sales_7'] + 1)  # Days of inventory
        df['price_multiplier'] = 1.0
        return df
    
    def calculate_target(self, df):
        """Calculate optimal price multiplier based on demand and stock"""
        # High demand + low stock = increase price
        # Low demand + high stock = decrease price
        df['demand_pressure'] = (df['sales_7'] * 30) / (df['stock'] + 1)
        
        # Dynamic multiplier logic
        multipliers = []
        for _, row in df.iterrows():
            base_mult = 1.0
            
            # Demand-based adjustment
            if row['demand_pressure'] > 5:
                base_mult *= 1.15  # High demand, increase by 15%
            elif row['demand_pressure'] > 2:
                base_mult *= 1.08  # Medium demand, increase by 8%
            elif row['demand_pressure'] < 0.5:
                base_mult *= 0.90  # Low demand, decrease by 10%
            elif row['demand_pressure'] < 1:
                base_mult *= 0.95  # Low-medium demand, decrease by 5%
            
            # Seasonality adjustment (day of week)
            if row['day'] in [5, 6]:  # Weekend
                base_mult *= 1.05
            elif row['day'] in [0]:  # Monday (restocking day)
                base_mult *= 0.98
            
            multipliers.append(min(1.3, max(0.7, base_mult)))  # Cap between 0.7 and 1.3
        
        return np.array(multipliers)
    
    def train(self, csv_path, model_output_path='pricing_model.pkl'):
        """Train the pricing model"""
        df = self.load_data(csv_path)
        df = self.calculate_features(df)
        
        # Prepare features and target
        X = df[self.feature_names].values
        y = self.calculate_target(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Fit scaler
        self.scaler.fit(X_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Training Score: {train_score:.4f}")
        print(f"Testing Score: {test_score:.4f}")
        
        # Save model
        with open(model_output_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'features': self.feature_names
            }, f)
        
        print(f"Model saved to {model_output_path}")
        return train_score, test_score
    
    def load_model(self, model_path):
        """Load saved model"""
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['features']
    
    def predict_price_multiplier(self, base_price, stock, sales_7, sales_30, day):
        """Predict dynamic price multiplier for a product"""
        if self.model is None:
            raise ValueError("Model not loaded. Train or load the model first.")
        
        # Calculate derived features
        demand_ratio = sales_7 / (sales_30 + 1)
        stock_ratio = stock / (sales_7 + 1)
        
        # Create feature array
        features = np.array([[base_price, stock, sales_7, sales_30, day, demand_ratio, stock_ratio]])
        
        # Predict
        multiplier = self.model.predict(features)[0]
        multiplier = min(1.3, max(0.7, multiplier))  # Cap multiplier
        
        return float(multiplier)
    
    def predict_dynamic_price(self, base_price, stock, sales_7, sales_30, day):
        """Get dynamic price for a product"""
        multiplier = self.predict_price_multiplier(base_price, stock, sales_7, sales_30, day)
        dynamic_price = base_price * multiplier
        return {
            'base_price': base_price,
            'multiplier': round(multiplier, 3),
            'dynamic_price': round(dynamic_price, 2),
            'change_percent': round((multiplier - 1) * 100, 2)
        }


if __name__ == "__main__":
    # Initialize and train model
    pricing_model = DynamicPricingModel()
    csv_file = 'backend/data/groceries.csv'
    model_file = 'backend/pricing_model.pkl'
    
    if os.path.exists(csv_file):
        pricing_model.train(csv_file, model_file)
    else:
        print(f"CSV file not found at {csv_file}")
