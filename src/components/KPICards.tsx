import { Users, Globe, DollarSign, TrendingUp, AlertTriangle } from 'lucide-react';
import type { DashboardKPIs } from '../lib/api';

interface KPICardsProps {
  kpis: DashboardKPIs;
}

export default function KPICards({ kpis }: KPICardsProps) {
  const formatUSD = (n: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

  const cards = [
    {
      label: 'Total Employees',
      value: kpis.total_employees.toString(),
      sub: `Across ${kpis.total_countries} countries`,
      icon: Users,
      color: '#2563eb',
      bg: '#eff6ff',
    },
    {
      label: 'Monthly Payroll',
      value: formatUSD(kpis.total_monthly_payroll_usd),
      sub: `Avg ${formatUSD(kpis.avg_employee_cost_usd)}/employee`,
      icon: DollarSign,
      color: '#059669',
      bg: '#ecfdf5',
    },
    {
      label: 'Compliance Rate',
      value: `${kpis.compliance_rate}%`,
      sub: kpis.compliance_rate === 100 ? 'All countries compliant' : 'Some countries need attention',
      icon: kpis.compliance_rate === 100 ? TrendingUp : AlertTriangle,
      color: kpis.compliance_rate === 100 ? '#059669' : '#d97706',
      bg: kpis.compliance_rate === 100 ? '#ecfdf5' : '#fffbeb',
    },
    {
      label: 'Payroll Growth',
      value: `${kpis.yoy_growth > 0 ? '+' : ''}${kpis.yoy_growth}%`,
      sub: 'Month-over-month change',
      icon: TrendingUp,
      color: kpis.yoy_growth >= 0 ? '#059669' : '#dc2626',
      bg: kpis.yoy_growth >= 0 ? '#ecfdf5' : '#fef2f2',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div key={card.label} className="kpi-card">
          <div className="flex items-start justify-between mb-3">
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: card.bg }}
            >
              <card.icon size={20} style={{ color: card.color }} />
            </div>
          </div>
          <p className="text-2xl font-bold text-slate-900">{card.value}</p>
          <p className="text-sm font-medium text-slate-900 mt-0.5">{card.label}</p>
          <p className="text-xs text-slate-500 mt-1">{card.sub}</p>
        </div>
      ))}
    </div>
  );
}
