import { cn } from '@/lib/utils';
import { SecurityScore } from '@/types/security';
import { Shield, Wifi, Monitor, User, Database } from 'lucide-react';
import { LucideIcon } from 'lucide-react';

interface SecurityScoreCardProps {
  score: SecurityScore;
  className?: string;
}

interface ScoreItemProps {
  label: string;
  value: number;
  icon: LucideIcon;
}

function getScoreColor(score: number): string {
  if (score >= 80) return 'text-success';
  if (score >= 60) return 'text-warning';
  return 'text-destructive';
}

function getScoreGradient(score: number): string {
  if (score >= 80) return 'from-success/20 to-success/5';
  if (score >= 60) return 'from-warning/20 to-warning/5';
  return 'from-destructive/20 to-destructive/5';
}

function ScoreItem({ label, value, icon: Icon }: ScoreItemProps) {
  return (
    <div className="flex items-center justify-between py-2">
      <div className="flex items-center gap-2">
        <Icon className="h-4 w-4 text-muted-foreground" />
        <span className="text-sm text-muted-foreground">{label}</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-24 h-2 rounded-full bg-secondary overflow-hidden">
          <div
            className={cn(
              'h-full rounded-full transition-all duration-1000',
              value >= 80 ? 'bg-success' : value >= 60 ? 'bg-warning' : 'bg-destructive'
            )}
            style={{ width: `${value}%` }}
          />
        </div>
        <span className={cn('font-mono text-sm font-medium w-8 text-right', getScoreColor(value))}>
          {value}
        </span>
      </div>
    </div>
  );
}

export function SecurityScoreCard({ score, className }: SecurityScoreCardProps) {
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (score.overall / 100) * circumference;

  return (
    <div className={cn('rounded-lg border border-border bg-card p-4', className)}>
      <div className="flex items-center gap-2 mb-4">
        <Shield className="h-5 w-5 text-primary" />
        <h2 className="font-semibold">Security Score</h2>
      </div>

      <div className="flex items-center gap-6">
        {/* Circular score */}
        <div className="relative flex items-center justify-center">
          <svg className="w-28 h-28 -rotate-90">
            {/* Background circle */}
            <circle
              cx="56"
              cy="56"
              r="45"
              stroke="hsl(var(--secondary))"
              strokeWidth="8"
              fill="none"
            />
            {/* Progress circle */}
            <circle
              cx="56"
              cy="56"
              r="45"
              stroke={
                score.overall >= 80
                  ? 'hsl(var(--success))'
                  : score.overall >= 60
                  ? 'hsl(var(--warning))'
                  : 'hsl(var(--destructive))'
              }
              strokeWidth="8"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute flex flex-col items-center">
            <span className={cn('text-3xl font-bold', getScoreColor(score.overall))}>
              {score.overall}
            </span>
            <span className="text-xs text-muted-foreground">/ 100</span>
          </div>
        </div>

        {/* Score breakdown */}
        <div className="flex-1 space-y-1">
          <ScoreItem label="Network" value={score.network} icon={Wifi} />
          <ScoreItem label="Endpoint" value={score.endpoint} icon={Monitor} />
          <ScoreItem label="Identity" value={score.identity} icon={User} />
          <ScoreItem label="Data" value={score.data} icon={Database} />
        </div>
      </div>
    </div>
  );
}
