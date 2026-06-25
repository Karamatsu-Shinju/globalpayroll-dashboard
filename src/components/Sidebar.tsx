import { useState } from 'react';
import { LayoutDashboard, Globe, Users, Receipt, Settings, ChevronLeft, ChevronRight, Shield } from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
}

export default function Sidebar({ activeView, onViewChange }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'countries', label: 'Countries', icon: Globe },
    { id: 'employees', label: 'Employees', icon: Users },
    { id: 'payroll', label: 'Payroll Runs', icon: Receipt },
  ];

  return (
    <aside
      className="flex flex-col h-screen transition-all duration-300 relative"
      style={{
        width: collapsed ? 64 : 240,
        backgroundColor: '#0f172a',
        minWidth: collapsed ? 64 : 240,
      }}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-slate-700/50">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style={{ backgroundColor: '#2563eb' }}>
          <Shield size={18} className="text-white" />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-white font-semibold text-sm leading-tight">GlobalPayroll</h1>
            <p className="text-slate-400 text-[10px] leading-tight">Dashboard</p>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onViewChange(item.id)}
            className={`sidebar-link w-full ${activeView === item.id ? 'active' : ''}`}
            title={collapsed ? item.label : ''}
          >
            <item.icon size={18} />
            {!collapsed && <span>{item.label}</span>}
          </button>
        ))}
      </nav>

      {/* Bottom */}
      <div className="px-2 py-4 border-t border-slate-700/50">
        <button className="sidebar-link w-full" title={collapsed ? 'Settings' : ''}>
          <Settings size={18} />
          {!collapsed && <span>Settings</span>}
        </button>
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-20 w-6 h-6 rounded-full flex items-center justify-center text-xs"
        style={{ backgroundColor: '#1e293b', border: '1px solid #334155', color: '#94a3b8' }}
      >
        {collapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
      </button>
    </aside>
  );
}
