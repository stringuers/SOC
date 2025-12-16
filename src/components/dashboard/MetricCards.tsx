import { cn } from '@/lib/utils';
import { LucideIcon, Shield, AlertTriangle, Activity, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'stable';
  icon: LucideIcon;
  variant?: 'default' | 'critical' | 'warning' | 'success';
  className?: string;
}

export function MetricCard({
  title,
  value,
  change,
  trend,
  icon: Icon,
  variant = 'default',
  className,
}: MetricCardProps) {
  const variantStyles = {
    default: 'border-border bg-card',
    critical: 'border-destructive/50 bg-destructive/5',
    warning: 'border-warning/50 bg-warning/5',
    success: 'border-success/50 bg-success/5',
  };

  const iconStyles = {
    default: 'bg-primary/10 text-primary',
    critical: 'bg-destructive/20 text-destructive',
    warning: 'bg-warning/20 text-warning',
    success: 'bg-success/20 text-success',
  };

  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;
  const trendColor = trend === 'up' ? 'text-destructive' : trend === 'down' ? 'text-success' : 'text-muted-foreground';

  return (
    <div
      className={cn(
        'relative overflow-hidden rounded-lg border p-6 transition-all duration-300 hover:border-primary/50',
        variantStyles[variant],
        className
      )}
    >
      {/* Subtle glow effect for critical */}
      {variant === 'critical' && (
        <div className="absolute inset-0 bg-gradient-radial from-destructive/10 to-transparent" />
      )}
      
      <div className="relative flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold tracking-tight animate-counter">{value}</p>
          
          {change !== undefined && (
            <div className={cn('flex items-center gap-1 text-sm', trendColor)}>
              <TrendIcon className="h-4 w-4" />
              <span>{Math.abs(change)}% from last hour</span>
            </div>
          )}
        </div>
        
        <div className={cn('rounded-lg p-3', iconStyles[variant])}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
}

interface MetricsGridProps {
  totalAlerts: number;
  unresolvedAlerts: number;
  criticalAlerts: number;
  eventsPerMinute: number;
}

export function MetricsGrid({
  totalAlerts,
  unresolvedAlerts,
  criticalAlerts,
  eventsPerMinute,
}: MetricsGridProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        title="Total Alerts"
        value={totalAlerts}
        change={12}
        trend="up"
        icon={Shield}
      />
      <MetricCard
        title="Unresolved"
        value={unresolvedAlerts}
        change={5}
        trend="up"
        icon={AlertTriangle}
        variant="warning"
      />
      <MetricCard
        title="Critical"
        value={criticalAlerts}
        change={8}
        trend="up"
        icon={Activity}
        variant="critical"
      />
      <MetricCard
        title="Events/min"
        value={eventsPerMinute}
        change={3}
        trend="down"
        icon={TrendingUp}
        variant="success"
      />
    </div>
  );
}
