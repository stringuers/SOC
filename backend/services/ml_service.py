import numpy as np
from typing import Dict
from datetime import datetime
import os

# Try to load the ML model, but handle gracefully if not available
try:
    import joblib
    
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml-engine', 'anomaly_detector.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml-engine', 'scaler.pkl')
    
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        MODEL_AVAILABLE = True
    else:
        MODEL_AVAILABLE = False
        print("Warning: ML model files not found. Using rule-based detection.")
except ImportError:
    MODEL_AVAILABLE = False
    print("Warning: joblib not available. Using rule-based detection.")

def ip_to_int(ip: str) -> int:
    """Convert IP address to integer"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return 0
        return sum(int(part) * (256 ** (3 - i)) for i, part in enumerate(parts))
    except:
        return 0

def extract_features(log_entry: Dict) -> Dict:
    """Extract features from log entry for ML analysis"""
    timestamp = log_entry.get('timestamp')
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            timestamp = datetime.utcnow()
    elif not isinstance(timestamp, datetime):
        timestamp = datetime.utcnow()
    
    raw_log = log_entry.get('raw_log', '').lower()
    
    features = {
        'hour': timestamp.hour,
        'day_of_week': timestamp.weekday(),
        'source_ip_int': ip_to_int(log_entry.get('source_ip', '0.0.0.0')),
        'dest_ip_int': ip_to_int(log_entry.get('destination_ip', '0.0.0.0')),
        'log_length': len(log_entry.get('raw_log', '')),
        'has_sql_keywords': int(any(kw in raw_log for kw in ['select', 'union', 'drop', 'delete', 'insert', 'update', "' or '1'='1", '--'])),
        'has_script_tags': int('<script>' in raw_log or 'javascript:' in raw_log),
        'failed_login': int('failed login' in raw_log or 'authentication failed' in raw_log or 'unauthorized' in raw_log),
    }
    return features

class AnomalyDetector:
    def __init__(self):
        self.model_available = MODEL_AVAILABLE
        if MODEL_AVAILABLE:
            self.model = model
            self.scaler = scaler
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict if log entry is anomalous
        Returns: {
            'is_anomaly': bool,
            'anomaly_score': float,
            'confidence': float
        }
        """
        if self.model_available:
            try:
                feature_vector = np.array([[
                    features['hour'],
                    features['day_of_week'],
                    features['source_ip_int'],
                    features['dest_ip_int'],
                    features['log_length'],
                    features['has_sql_keywords'],
                    features['has_script_tags'],
                    features['failed_login']
                ]])
                
                scaled_features = self.scaler.transform(feature_vector)
                prediction = self.model.predict(scaled_features)[0]
                score = self.model.score_samples(scaled_features)[0]
                
                return {
                    'is_anomaly': prediction == -1,
                    'anomaly_score': float(score),
                    'confidence': abs(float(score))
                }
            except Exception as e:
                print(f"ML prediction error: {e}, falling back to rule-based")
        
        # Rule-based fallback detection
        return self._rule_based_detection(features)
    
    def _rule_based_detection(self, features: Dict) -> Dict:
        """Rule-based anomaly detection as fallback"""
        score = 0.0
        confidence = 0.0
        
        # SQL injection indicators
        if features['has_sql_keywords']:
            score -= 0.5
            confidence += 0.6
        
        # Script injection
        if features['has_script_tags']:
            score -= 0.4
            confidence += 0.5
        
        # Failed login attempts
        if features['failed_login']:
            score -= 0.3
            confidence += 0.4
        
        # Unusual log length
        if features['log_length'] > 500:
            score -= 0.2
            confidence += 0.3
        
        # Unusual hour (3-5 AM)
        if 3 <= features['hour'] <= 5:
            score -= 0.1
            confidence += 0.2
        
        is_anomaly = score < -0.3 or confidence > 0.5
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_score': score,
            'confidence': min(confidence, 1.0)
        }

# Create global detector instance
detector = AnomalyDetector()

