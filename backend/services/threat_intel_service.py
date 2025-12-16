from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class ThreatIntelligence:
    def __init__(self):
        # These would be real API keys in production
        self.abuse_ipdb_key = os.getenv("ABUSE_IPDB_KEY", "")
        self.virustotal_key = os.getenv("VIRUSTOTAL_KEY", "")
        self.enabled = bool(self.abuse_ipdb_key or self.virustotal_key)
    
    def check_ip_reputation(self, ip: str) -> Dict:
        """Check IP against threat intelligence sources"""
        if not self.enabled:
            # Return mock data when API keys are not configured
            return {
                'ip': ip,
                'is_malicious': False,
                'abuse_score': 0,
                'country': 'Unknown',
                'reports': 0,
                'source': 'mock'
            }
        
        # In production, this would call real APIs
        # For now, we'll use a simple heuristic based on IP ranges
        try:
            # Check if IP is in known malicious ranges (example)
            ip_parts = ip.split('.')
            if len(ip_parts) == 4:
                first_octet = int(ip_parts[0])
                # Example: 203.0.113.x is a test range that we'll mark as suspicious
                if first_octet == 203 and int(ip_parts[1]) == 0:
                    return {
                        'ip': ip,
                        'is_malicious': True,
                        'abuse_score': 75,
                        'country': 'Unknown',
                        'reports': 5,
                        'source': 'heuristic'
                    }
        except:
            pass
        
        return {
            'ip': ip,
            'is_malicious': False,
            'abuse_score': 0,
            'country': 'Unknown',
            'reports': 0,
            'source': 'heuristic'
        }
    
    def enrich_alert(self, alert_data: Dict) -> Dict:
        """Enrich alert with threat intelligence"""
        source_ip = alert_data.get('source_ip')
        
        if source_ip:
            intel = self.check_ip_reputation(source_ip)
            alert_data['threat_intel'] = intel
        
        return alert_data

