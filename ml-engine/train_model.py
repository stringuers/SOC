"""
Train anomaly detection model for SecureWatch
This script creates a simple model for demonstration purposes.
In production, you would train on real historical data.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta

def ip_to_int(ip):
    """Convert IP address to integer"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return 0
        return sum(int(part) * (256 ** (3 - i)) for i, part in enumerate(parts))
    except:
        return 0

def generate_training_data(num_samples=10000):
    """Generate synthetic training data"""
    data = []
    
    for i in range(num_samples):
        # 85% normal traffic, 15% anomalous
        is_anomaly = np.random.random() < 0.15
        
        if is_anomaly:
            # Anomalous traffic patterns
            hour = np.random.choice([2, 3, 4, 5])  # Unusual hours
            source_ip = f"203.0.113.{np.random.randint(1, 254)}"
            dest_ip = "192.168.1.10"
            log_length = np.random.randint(200, 1000)
            has_sql = 1
            has_script = np.random.choice([0, 1])
            failed_login = np.random.choice([0, 1])
        else:
            # Normal traffic patterns
            hour = np.random.randint(8, 20)  # Business hours
            source_ip = f"192.168.1.{np.random.randint(1, 254)}"
            dest_ip = f"10.0.0.{np.random.randint(1, 254)}"
            log_length = np.random.randint(20, 200)
            has_sql = 0
            has_script = 0
            failed_login = 0
        
        data.append({
            'hour': hour,
            'day_of_week': np.random.randint(0, 7),
            'source_ip_int': ip_to_int(source_ip),
            'dest_ip_int': ip_to_int(dest_ip),
            'log_length': log_length,
            'has_sql_keywords': has_sql,
            'has_script_tags': has_script,
            'failed_login': failed_login,
            'is_anomaly': 1 if is_anomaly else 0
        })
    
    return pd.DataFrame(data)

def train_model():
    """Train the anomaly detection model"""
    print("Generating training data...")
    df = generate_training_data(10000)
    
    # Features for training
    features = ['hour', 'day_of_week', 'source_ip_int', 'dest_ip_int', 
                'log_length', 'has_sql_keywords', 'has_script_tags', 'failed_login']
    
    X = df[features].values
    
    # Normalize features
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest
    print("Training Isolation Forest model...")
    model = IsolationForest(
        contamination=0.15,  # Expect 15% anomalies
        random_state=42,
        n_estimators=100,
        max_samples='auto'
    )
    model.fit(X_scaled)
    
    # Save model and scaler
    os.makedirs('ml-engine', exist_ok=True)
    model_path = 'ml-engine/anomaly_detector.pkl'
    scaler_path = 'ml-engine/scaler.pkl'
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")
    
    # Evaluate on training data
    predictions = model.predict(X_scaled)
    anomalies = (predictions == -1).sum()
    print(f"\nModel evaluation:")
    print(f"Total samples: {len(df)}")
    print(f"Detected anomalies: {anomalies} ({anomalies/len(df)*100:.2f}%)")
    print(f"Actual anomalies: {df['is_anomaly'].sum()} ({df['is_anomaly'].sum()/len(df)*100:.2f}%)")
    
    return model, scaler

if __name__ == "__main__":
    print("Training SecureWatch Anomaly Detection Model")
    print("=" * 50)
    train_model()
    print("\nTraining complete!")

