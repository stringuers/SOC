import { useState } from 'react';
import { cn } from '@/lib/utils';
import { Alert } from '@/types/security';
import { apiService } from '@/lib/api';
import { 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  User, 
  ExternalLink,
  ChevronRight,
  Shield
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

interface AlertListProps {
  alerts: Alert[];
  className?: string;
}

const severityConfig = {
  critical: {
    badge: 'severity-critical',
    dot: 'bg-destructive',
    glow: 'shadow-[0_0_10px_hsl(var(--severity-critical)/0.5)]',
  },
  high: {
    badge: 'severity-high',
    dot: 'bg-severity-high',
    glow: '',
  },
  medium: {
    badge: 'severity-medium',
    dot: 'bg-severity-medium',
    glow: '',
  },
  low: {
    badge: 'severity-low',
    dot: 'bg-severity-low',
    glow: '',
  },
};

const statusConfig = {
  open: { icon: AlertTriangle, color: 'text-destructive', label: 'Open' },
  investigating: { icon: Clock, color: 'text-warning', label: 'Investigating' },
  resolved: { icon: CheckCircle2, color: 'text-success', label: 'Resolved' },
  false_positive: { icon: Shield, color: 'text-muted-foreground', label: 'False Positive' },
};

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function AlertList({ alerts, className }: AlertListProps) {
  const [selectedAlert, setSelectedAlert] = useState<string | null>(null);

  return (
    <div className={cn('rounded-lg border border-border bg-card', className)}>
      <div className="flex items-center justify-between border-b border-border p-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Active Alerts</h2>
          <Badge variant="secondary" className="ml-2">
            {alerts.filter(a => a.status === 'open').length} Open
          </Badge>
        </div>
        <Button variant="ghost" size="sm" className="text-primary hover:text-primary">
          View All <ChevronRight className="ml-1 h-4 w-4" />
        </Button>
      </div>

      <ScrollArea className="h-[400px]">
        <div className="divide-y divide-border">
          {alerts.map((alert, index) => {
            const severity = severityConfig[alert.severity];
            const status = statusConfig[alert.status];
            const StatusIcon = status.icon;
            const isSelected = selectedAlert === alert.id;

            return (
              <div
                key={alert.id}
                className={cn(
                  'group cursor-pointer p-4 transition-all duration-200 hover:bg-secondary/50',
                  isSelected && 'bg-secondary/30',
                  'animate-fade-in'
                )}
                style={{ animationDelay: `${index * 50}ms` }}
                onClick={() => setSelectedAlert(isSelected ? null : alert.id)}
              >
                <div className="flex items-start gap-3">
                  {/* Severity indicator */}
                  <div className="relative mt-1">
                    <div
                      className={cn(
                        'h-3 w-3 rounded-full',
                        severity.dot,
                        alert.severity === 'critical' && 'animate-pulse'
                      )}
                    />
                    {alert.severity === 'critical' && (
                      <div
                        className={cn(
                          'absolute inset-0 h-3 w-3 rounded-full animate-ping',
                          severity.dot
                        )}
                        style={{ opacity: 0.4 }}
                      />
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h3 className="font-medium text-foreground line-clamp-1">
                          {alert.title}
                        </h3>
                        <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                          {alert.description}
                        </p>
                      </div>
                      <Badge className={cn('shrink-0 text-xs', severity.badge)}>
                        {alert.severity.toUpperCase()}
                      </Badge>
                    </div>

                    {/* Meta info */}
                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <StatusIcon className={cn('h-3 w-3', status.color)} />
                        {status.label}
                      </span>
                      <span className="font-mono">{alert.sourceIp}</span>
                      <span>{alert.source}</span>
                      <span>{formatTimeAgo(alert.timestamp)}</span>
                      {alert.assignedTo && (
                        <span className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {alert.assignedTo}
                        </span>
                      )}
                    </div>

                    {/* Expanded content */}
                    {isSelected && (
                      <div className="mt-4 flex gap-2 animate-fade-in">
                        <Button 
                          size="sm" 
                          variant="default"
                          onClick={(e) => {
                            e.stopPropagation();
                            apiService.updateAlert(parseInt(alert.id), { status: 'investigating' });
                          }}
                        >
                          Investigate
                        </Button>
                        <Button 
                          size="sm" 
                          variant="secondary"
                          onClick={(e) => {
                            e.stopPropagation();
                            apiService.resolveAlert(parseInt(alert.id));
                          }}
                        >
                          Resolve
                        </Button>
                        <Button size="sm" variant="ghost">
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}
