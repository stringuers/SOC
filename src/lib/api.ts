import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Alert {
  id: number;
  title: string;
  description?: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  source?: string;
  source_ip?: string;
  timestamp: string;
  status: 'open' | 'investigating' | 'resolved' | 'false_positive';
  is_resolved: boolean;
  assigned_to?: string;
  category?: string;
  anomaly_score?: string;
}

export interface LogEntry {
  id: number;
  source_ip: string;
  destination_ip: string;
  timestamp: string;
  log_type: string;
  message: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  is_anomaly: boolean;
  anomaly_score?: string;
}

export interface AlertStats {
  total_alerts: number;
  unresolved: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

// API functions
export const apiService = {
  // Alerts
  getAlerts: async (params?: {
    skip?: number;
    limit?: number;
    severity?: string;
    status?: string;
    resolved?: boolean;
  }): Promise<Alert[]> => {
    const response = await api.get('/api/alerts', { params });
    return response.data;
  },

  getAlert: async (id: number): Promise<Alert> => {
    const response = await api.get(`/api/alerts/${id}`);
    return response.data;
  },

  updateAlert: async (id: number, data: {
    status?: string;
    assigned_to?: string;
    is_resolved?: boolean;
  }): Promise<Alert> => {
    const response = await api.patch(`/api/alerts/${id}`, data);
    return response.data;
  },

  resolveAlert: async (id: number): Promise<void> => {
    await api.patch(`/api/alerts/${id}/resolve`);
  },

  getAlertStats: async (): Promise<AlertStats> => {
    const response = await api.get('/api/alerts/stats/summary');
    return response.data;
  },

  // Logs
  getLogs: async (params?: {
    skip?: number;
    limit?: number;
    severity?: string;
  }): Promise<LogEntry[]> => {
    const response = await api.get('/api/logs', { params });
    return response.data;
  },

  ingestLog: async (log: {
    source_ip: string;
    destination_ip: string;
    log_type: string;
    raw_log: string;
    message?: string;
  }): Promise<LogEntry> => {
    const response = await api.post('/api/logs/ingest', log);
    return response.data;
  },

  getLog: async (id: number): Promise<LogEntry> => {
    const response = await api.get(`/api/logs/${id}`);
    return response.data;
  },
};

export default api;

