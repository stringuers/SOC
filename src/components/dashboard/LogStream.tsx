import { useEffect, useState, useRef } from 'react';
import { cn } from '@/lib/utils';
import { LogEntry } from '@/types/security';
import { Terminal, Pause, Play, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface LogStreamProps {
  logs: LogEntry[];
  onNewLog?: (log: LogEntry) => void;
  className?: string;
}

const severityColors = {
  critical: 'text-destructive',
  high: 'text-severity-high',
  medium: 'text-warning',
  low: 'text-muted-foreground',
};

const typeColors: Record<string, string> = {
  HTTP: 'text-info',
  SSH: 'text-warning',
  DNS: 'text-primary',
  Security: 'text-destructive',
  System: 'text-success',
  Firewall: 'text-severity-high',
};

function formatTimestamp(date: Date): string {
  const time = date.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  const ms = date.getMilliseconds().toString().padStart(3, '0');
  return `${time}.${ms}`;
}

export function LogStream({ logs, className }: LogStreamProps) {
  const [isPaused, setIsPaused] = useState(false);
  const [visibleLogs, setVisibleLogs] = useState<LogEntry[]>(logs);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isPaused) {
      setVisibleLogs(logs);
    }
  }, [logs, isPaused]);

  useEffect(() => {
    if (!isPaused && scrollRef.current) {
      scrollRef.current.scrollTop = 0;
    }
  }, [visibleLogs, isPaused]);

  return (
    <div className={cn('rounded-lg border border-border bg-card', className)}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border p-4">
        <div className="flex items-center gap-2">
          <Terminal className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Live Log Stream</h2>
          <div className="ml-2 flex items-center gap-1">
            <div className={cn(
              'h-2 w-2 rounded-full',
              isPaused ? 'bg-warning' : 'bg-success animate-pulse'
            )} />
            <span className="text-xs text-muted-foreground">
              {isPaused ? 'Paused' : 'Live'}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsPaused(!isPaused)}
          >
            {isPaused ? (
              <Play className="h-4 w-4 mr-1" />
            ) : (
              <Pause className="h-4 w-4 mr-1" />
            )}
            {isPaused ? 'Resume' : 'Pause'}
          </Button>
          <Button variant="ghost" size="sm">
            <Filter className="h-4 w-4 mr-1" />
            Filter
          </Button>
        </div>
      </div>

      {/* Log entries */}
      <div
        ref={scrollRef}
        className="h-[300px] overflow-auto bg-background/50 font-mono text-sm"
      >
        <div className="scan-line absolute inset-0 pointer-events-none h-full" />
        <table className="w-full">
          <tbody>
            {visibleLogs.map((log, index) => (
              <tr
                key={log.id}
                className={cn(
                  'border-b border-border/30 hover:bg-secondary/30 transition-colors',
                  'animate-slide-in'
                )}
                style={{ animationDelay: `${index * 30}ms` }}
              >
                <td className="whitespace-nowrap px-3 py-2 text-muted-foreground">
                  {formatTimestamp(log.timestamp)}
                </td>
                <td className="px-3 py-2">
                  <Badge
                    variant="outline"
                    className={cn(
                      'font-mono text-xs',
                      typeColors[log.logType] || 'text-muted-foreground'
                    )}
                  >
                    {log.logType}
                  </Badge>
                </td>
                <td className="whitespace-nowrap px-3 py-2 text-xs text-muted-foreground">
                  <span className="text-foreground/70">{log.sourceIp}</span>
                  <span className="mx-2">→</span>
                  <span className="text-foreground/70">{log.destinationIp}</span>
                </td>
                <td className={cn('px-3 py-2', severityColors[log.severity])}>
                  {log.message}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
