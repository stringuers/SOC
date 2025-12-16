import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Navbar } from '@/components/layout/Navbar';
import { MetricsGrid } from '@/components/dashboard/MetricCards';
import { AlertList } from '@/components/dashboard/AlertList';
import { LogStream } from '@/components/dashboard/LogStream';
import { ThreatChart } from '@/components/dashboard/ThreatChart';
import { SecurityScoreCard } from '@/components/dashboard/SecurityScoreCard';
import { apiService, Alert, LogEntry } from '@/lib/api';
import { 
  mockThreatData, 
  mockSecurityScore
} from '@/data/mockData';

const Index = () => {
  // Fetch alerts
  const { data: alerts = [], isLoading: alertsLoading } = useQuery<Alert[]>({
    queryKey: ['alerts'],
    queryFn: () => apiService.getAlerts({ limit: 50 }),
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  // Fetch logs
  const { data: logs = [], isLoading: logsLoading } = useQuery<LogEntry[]>({
    queryKey: ['logs'],
    queryFn: () => apiService.getLogs({ limit: 100 }),
    refetchInterval: 3000, // Refresh every 3 seconds
  });

  // Fetch stats
  const { data: stats } = useQuery({
    queryKey: ['alertStats'],
    queryFn: () => apiService.getAlertStats(),
    refetchInterval: 10000, // Refresh every 10 seconds
  });

  // Convert API alerts to component format
  const formattedAlerts = alerts.map(alert => ({
    id: alert.id.toString(),
    title: alert.title,
    description: alert.description || '',
    severity: alert.severity,
    source: alert.source || 'Unknown',
    sourceIp: alert.source_ip || 'Unknown',
    timestamp: new Date(alert.timestamp),
    status: alert.status,
    assignedTo: alert.assigned_to,
    category: alert.category || 'Security',
  }));

  // Convert API logs to component format
  const formattedLogs = logs.map(log => ({
    id: log.id.toString(),
    timestamp: new Date(log.timestamp),
    sourceIp: log.source_ip,
    destinationIp: log.destination_ip,
    logType: log.log_type,
    message: log.message,
    severity: log.severity,
  }));

  const unresolvedAlerts = formattedAlerts.filter(a => a.status === 'open' || a.status === 'investigating');
  const criticalAlerts = formattedAlerts.filter(a => a.severity === 'critical');

  return (
    <div className="min-h-screen bg-background">
      {/* Background grid pattern */}
      <div className="fixed inset-0 bg-grid-pattern bg-grid opacity-[0.02] pointer-events-none" />
      
      {/* Gradient orb effects */}
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 right-1/4 w-96 h-96 bg-destructive/5 rounded-full blur-3xl pointer-events-none" />

      <Navbar />

      <main className="relative container mx-auto px-4 py-6 space-y-6">
        {/* Status bar */}
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Security Operations Center</h2>
            <p className="text-muted-foreground">Real-time threat monitoring and response</p>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-success/10 border border-success/20">
              <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
              <span className="text-success font-medium">All Systems Operational</span>
            </div>
            <span className="text-muted-foreground">
              Last updated: {new Date().toLocaleTimeString()}
            </span>
          </div>
        </div>

        {/* Metrics */}
        <MetricsGrid
          totalAlerts={stats?.total_alerts || 0}
          unresolvedAlerts={stats?.unresolved || 0}
          criticalAlerts={stats?.critical || 0}
          eventsPerMinute={Math.floor(formattedLogs.length / 2) || 0}
        />

        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Alerts - takes 2 columns */}
          <div className="lg:col-span-2">
            {alertsLoading ? (
              <div className="rounded-lg border border-border bg-card p-6">
                <p className="text-muted-foreground">Loading alerts...</p>
              </div>
            ) : (
              <AlertList alerts={formattedAlerts} />
            )}
          </div>

          {/* Security Score */}
          <div className="space-y-6">
            <SecurityScoreCard score={mockSecurityScore} />
          </div>
        </div>

        {/* Threat Chart */}
        <ThreatChart data={mockThreatData} />

        {/* Log Stream */}
        {logsLoading ? (
          <div className="rounded-lg border border-border bg-card p-6">
            <p className="text-muted-foreground">Loading logs...</p>
          </div>
        ) : (
          <LogStream logs={formattedLogs} />
        )}
      </main>
    </div>
  );
};

export default Index;
