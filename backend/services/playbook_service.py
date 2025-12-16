from typing import Dict, List

class PlaybookEngine:
    def __init__(self):
        self.playbooks = {
            'sql_injection': [
                {'action': 'block_ip', 'params': {'duration': 3600}},
                {'action': 'alert_admin', 'params': {'priority': 'high'}},
                {'action': 'log_incident', 'params': {}},
            ],
            'brute_force': [
                {'action': 'rate_limit_ip', 'params': {'max_attempts': 3}},
                {'action': 'enable_captcha', 'params': {}},
                {'action': 'alert_admin', 'params': {'priority': 'medium'}},
            ],
            'data_exfiltration': [
                {'action': 'block_ip', 'params': {'duration': 7200}},
                {'action': 'isolate_host', 'params': {}},
                {'action': 'alert_admin', 'params': {'priority': 'critical'}},
                {'action': 'capture_traffic', 'params': {'duration': 300}},
            ],
            'port_scan': [
                {'action': 'block_ip', 'params': {'duration': 1800}},
                {'action': 'alert_admin', 'params': {'priority': 'medium'}},
            ]
        }
    
    def execute_playbook(self, threat_type: str, context: Dict) -> Dict:
        """Execute automated response playbook"""
        if threat_type not in self.playbooks:
            return {'status': 'no_playbook_found', 'threat_type': threat_type}
        
        results = []
        for step in self.playbooks[threat_type]:
            result = self._execute_action(step['action'], step['params'], context)
            results.append(result)
        
        return {'status': 'completed', 'results': results, 'threat_type': threat_type}
    
    def _execute_action(self, action: str, params: Dict, context: Dict) -> Dict:
        """Execute a single playbook action"""
        actions = {
            'block_ip': self._block_ip,
            'alert_admin': self._alert_admin,
            'log_incident': self._log_incident,
            'rate_limit_ip': self._rate_limit_ip,
            'enable_captcha': self._enable_captcha,
            'isolate_host': self._isolate_host,
            'capture_traffic': self._capture_traffic,
        }
        
        if action in actions:
            return actions[action](params, context)
        
        return {'action': action, 'status': 'not_implemented'}
    
    def _block_ip(self, params: Dict, context: Dict) -> Dict:
        """Block IP address"""
        ip = context.get('source_ip')
        duration = params.get('duration', 3600)
        # In production, this would integrate with firewall API
        print(f"[PLAYBOOK] Blocking IP {ip} for {duration} seconds")
        return {'action': 'block_ip', 'ip': ip, 'duration': duration, 'status': 'blocked'}
    
    def _alert_admin(self, params: Dict, context: Dict) -> Dict:
        """Send alert to admin"""
        priority = params.get('priority', 'medium')
        # In production, this would send email/Slack notification
        print(f"[PLAYBOOK] Alerting admin with priority {priority}")
        return {'action': 'alert_admin', 'priority': priority, 'status': 'sent'}
    
    def _log_incident(self, params: Dict, context: Dict) -> Dict:
        """Log incident"""
        # In production, this would create an incident record
        print(f"[PLAYBOOK] Logging incident for alert {context.get('alert_id')}")
        return {'action': 'log_incident', 'status': 'logged'}
    
    def _rate_limit_ip(self, params: Dict, context: Dict) -> Dict:
        """Apply rate limiting to IP"""
        ip = context.get('source_ip')
        max_attempts = params.get('max_attempts', 3)
        print(f"[PLAYBOOK] Rate limiting IP {ip} to {max_attempts} attempts")
        return {'action': 'rate_limit_ip', 'ip': ip, 'max_attempts': max_attempts, 'status': 'applied'}
    
    def _enable_captcha(self, params: Dict, context: Dict) -> Dict:
        """Enable CAPTCHA"""
        print(f"[PLAYBOOK] Enabling CAPTCHA")
        return {'action': 'enable_captcha', 'status': 'enabled'}
    
    def _isolate_host(self, params: Dict, context: Dict) -> Dict:
        """Isolate host"""
        ip = context.get('source_ip')
        print(f"[PLAYBOOK] Isolating host {ip}")
        return {'action': 'isolate_host', 'ip': ip, 'status': 'isolated'}
    
    def _capture_traffic(self, params: Dict, context: Dict) -> Dict:
        """Capture network traffic"""
        duration = params.get('duration', 300)
        print(f"[PLAYBOOK] Capturing traffic for {duration} seconds")
        return {'action': 'capture_traffic', 'duration': duration, 'status': 'capturing'}

