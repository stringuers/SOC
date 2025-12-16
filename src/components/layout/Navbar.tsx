import { cn } from '@/lib/utils';
import { 
  Shield, 
  LayoutDashboard, 
  AlertTriangle, 
  FileText, 
  Settings, 
  Search,
  Bell,
  User,
  Activity,
  Database,
  Zap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';

interface NavbarProps {
  className?: string;
}

export function Navbar({ className }: NavbarProps) {
  return (
    <nav className={cn('border-b border-border bg-card/50 backdrop-blur-xl', className)}>
      <div className="flex h-16 items-center justify-between px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
              <Shield className="h-6 w-6 text-primary-foreground" />
            </div>
            <div className="absolute -right-1 -top-1 h-3 w-3 rounded-full bg-success animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              <span className="text-gradient">Secure</span>
              <span className="text-foreground">Watch</span>
            </h1>
            <p className="text-xs text-muted-foreground">SOC Platform</p>
          </div>
        </div>

        {/* Navigation */}
        <div className="hidden md:flex items-center gap-1">
          <NavItem icon={LayoutDashboard} label="Dashboard" active />
          <NavItem icon={AlertTriangle} label="Alerts" badge={12} />
          <NavItem icon={Activity} label="Analytics" />
          <NavItem icon={Database} label="Logs" />
          <NavItem icon={Zap} label="Playbooks" />
          <NavItem icon={FileText} label="Reports" />
        </div>

        {/* Right section */}
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative hidden lg:block">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search alerts, IPs, domains..."
              className="w-72 pl-9 bg-secondary/50 border-border"
            />
            <kbd className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground bg-background px-2 py-0.5 rounded border border-border">
              ⌘K
            </kbd>
          </div>

          {/* Notifications */}
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-destructive text-xs text-destructive-foreground">
              3
            </span>
          </Button>

          {/* Settings */}
          <Button variant="ghost" size="icon">
            <Settings className="h-5 w-5" />
          </Button>

          {/* User */}
          <div className="flex items-center gap-3 border-l border-border pl-4">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium">John Smith</p>
              <p className="text-xs text-muted-foreground">SOC Analyst</p>
            </div>
            <div className="h-9 w-9 rounded-full bg-primary/20 flex items-center justify-center">
              <User className="h-5 w-5 text-primary" />
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

interface NavItemProps {
  icon: React.ElementType;
  label: string;
  active?: boolean;
  badge?: number;
}

function NavItem({ icon: Icon, label, active, badge }: NavItemProps) {
  return (
    <Button
      variant="ghost"
      className={cn(
        'relative gap-2 px-3',
        active && 'bg-secondary text-primary'
      )}
    >
      <Icon className="h-4 w-4" />
      <span>{label}</span>
      {badge && (
        <Badge variant="destructive" className="h-5 min-w-5 px-1.5 text-xs">
          {badge}
        </Badge>
      )}
      {active && (
        <span className="absolute bottom-0 left-1/2 h-0.5 w-8 -translate-x-1/2 rounded-full bg-primary" />
      )}
    </Button>
  );
}
