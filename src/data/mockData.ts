import { Alert, LogEntry, ThreatData, SecurityScore } from '@/types/security';

export const mockAlerts: Alert[] = [
  {
    id: '1',
    title: 'SQL Injection Attempt Detected',
    description: 'Multiple SQL injection patterns detected from external IP targeting the authentication endpoint.',
    severity: 'critical',
    source: 'WAF',
    sourceIp: '203.0.113.42',
    timestamp: new Date(Date.now() - 1000 * 60 * 5),
    status: 'open',
    category: 'Web Attack',
  },
  {
    id: '2',
    title: 'Brute Force Attack on SSH',
    description: '847 failed login attempts detected on SSH service within 10 minutes.',
    severity: 'high',
    source: 'IDS',
    sourceIp: '198.51.100.78',
    timestamp: new Date(Date.now() - 1000 * 60 * 12),
    status: 'investigating',
    assignedTo: 'John Smith',
    category: 'Authentication',
  },
  {
    id: '3',
    title: 'Unusual Data Exfiltration',
    description: 'Large outbound data transfer (2.3GB) detected from internal server to unknown external host.',
    severity: 'critical',
    source: 'DLP',
    sourceIp: '192.168.1.105',
    timestamp: new Date(Date.now() - 1000 * 60 * 23),
    status: 'open',
    category: 'Data Loss',
  },
  {
    id: '4',
    title: 'Suspicious PowerShell Execution',
    description: 'Encoded PowerShell command executed with potential malicious payload.',
    severity: 'high',
    source: 'EDR',
    sourceIp: '192.168.1.42',
    timestamp: new Date(Date.now() - 1000 * 60 * 45),
    status: 'open',
    category: 'Endpoint',
  },
  {
    id: '5',
    title: 'Port Scan Detected',
    description: 'Sequential port scanning detected from external IP targeting DMZ network.',
    severity: 'medium',
    source: 'Firewall',
    sourceIp: '203.0.113.99',
    timestamp: new Date(Date.now() - 1000 * 60 * 60),
    status: 'resolved',
    assignedTo: 'Jane Doe',
    category: 'Reconnaissance',
  },
  {
    id: '6',
    title: 'TLS Certificate Expiring',
    description: 'SSL certificate for api.company.com expires in 7 days.',
    severity: 'low',
    source: 'Certificate Monitor',
    sourceIp: '10.0.0.15',
    timestamp: new Date(Date.now() - 1000 * 60 * 120),
    status: 'open',
    category: 'Compliance',
  },
];

export const mockLogs: LogEntry[] = [
  {
    id: '1',
    timestamp: new Date(),
    sourceIp: '192.168.1.45',
    destinationIp: '10.0.0.12',
    logType: 'HTTP',
    message: 'GET /api/users HTTP/1.1 200 OK',
    severity: 'low',
  },
  {
    id: '2',
    timestamp: new Date(Date.now() - 1000),
    sourceIp: '203.0.113.42',
    destinationIp: '192.168.1.10',
    logType: 'Security',
    message: "SQL injection attempt: ' OR '1'='1' --",
    severity: 'critical',
  },
  {
    id: '3',
    timestamp: new Date(Date.now() - 2000),
    sourceIp: '198.51.100.78',
    destinationIp: '192.168.1.22',
    logType: 'SSH',
    message: 'Failed password for root from 198.51.100.78 port 54321 ssh2',
    severity: 'high',
  },
  {
    id: '4',
    timestamp: new Date(Date.now() - 3000),
    sourceIp: '192.168.1.100',
    destinationIp: '8.8.8.8',
    logType: 'DNS',
    message: 'Query: suspicious-domain.xyz A record',
    severity: 'medium',
  },
  {
    id: '5',
    timestamp: new Date(Date.now() - 4000),
    sourceIp: '192.168.1.55',
    destinationIp: '10.0.0.5',
    logType: 'HTTP',
    message: 'POST /api/login HTTP/1.1 401 Unauthorized',
    severity: 'medium',
  },
  {
    id: '6',
    timestamp: new Date(Date.now() - 5000),
    sourceIp: '10.0.0.8',
    destinationIp: '192.168.1.1',
    logType: 'System',
    message: 'Service nginx restarted successfully',
    severity: 'low',
  },
];

export const mockThreatData: ThreatData[] = [
  { time: '00:00', critical: 2, high: 5, medium: 12, low: 24 },
  { time: '04:00', critical: 1, high: 3, medium: 8, low: 18 },
  { time: '08:00', critical: 4, high: 8, medium: 15, low: 32 },
  { time: '12:00', critical: 6, high: 12, medium: 22, low: 45 },
  { time: '16:00', critical: 3, high: 7, medium: 18, low: 38 },
  { time: '20:00', critical: 5, high: 9, medium: 14, low: 28 },
  { time: 'Now', critical: 4, high: 6, medium: 11, low: 22 },
];

export const mockSecurityScore: SecurityScore = {
  overall: 78,
  network: 85,
  endpoint: 72,
  identity: 81,
  data: 74,
};

export const generateNewLog = (): LogEntry => {
  const types = ['HTTP', 'SSH', 'DNS', 'Security', 'System', 'Firewall'];
  const severities: Array<'critical' | 'high' | 'medium' | 'low'> = ['low', 'low', 'low', 'medium', 'medium', 'high', 'critical'];
  const messages = [
    'GET /api/health HTTP/1.1 200 OK',
    'Connection established from 192.168.1.x',
    'Query: google.com A record resolved',
    'Firewall rule matched: ALLOW TCP 443',
    'User authentication successful',
    'Rate limit exceeded for API endpoint',
    'Suspicious pattern detected in request',
  ];

  return {
    id: Date.now().toString(),
    timestamp: new Date(),
    sourceIp: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    destinationIp: `10.0.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
    logType: types[Math.floor(Math.random() * types.length)],
    message: messages[Math.floor(Math.random() * messages.length)],
    severity: severities[Math.floor(Math.random() * severities.length)],
  };
};
