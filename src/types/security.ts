export type SeverityLevel = 'critical' | 'high' | 'medium' | 'low';

export type AlertStatus = 'open' | 'investigating' | 'resolved' | 'false_positive';

export interface Alert {
  id: string;
  title: string;
  description: string;
  severity: SeverityLevel;
  source: string;
  sourceIp: string;
  timestamp: Date;
  status: AlertStatus;
  assignedTo?: string;
  category: string;
}

export interface LogEntry {
  id: string;
  timestamp: Date;
  sourceIp: string;
  destinationIp: string;
  logType: string;
  message: string;
  severity: SeverityLevel;
}

export interface Metric {
  label: string;
  value: number;
  change?: number;
  trend?: 'up' | 'down' | 'stable';
}

export interface ThreatData {
  time: string;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface SecurityScore {
  overall: number;
  network: number;
  endpoint: number;
  identity: number;
  data: number;
}
