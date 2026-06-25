import { CheckCircle, AlertTriangle } from 'lucide-react';
import type { CountryBreakdown } from '../lib/api';

interface Props {
  data: CountryBreakdown[];
}

export default function ComplianceStatus({ data }: Props) {
  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);
  const formatPct = (n: number) => `${(n * 100).toFixed(1)}%`;

  return (
    <div className="section-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Country Compliance</h3>
          <p className="text-xs text-slate-500 mt-0.5">Payroll & tax status per country</p>
        </div>
      </div>

      <div className="space-y-3">
        {data.map((c) => (
          <div key={c.country_code} className="flex items-center gap-3 py-2 px-3 rounded-lg hover:bg-slate-50 transition-colors">
            {/* Flag placeholder */}
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
              style={{ backgroundColor: c.tax_burden_pct > 40 ? '#dc2626' : c.tax_burden_pct > 30 ? '#d97706' : '#2563eb' }}
            >
              {c.country_code}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-slate-800">{c.country_name}</span>
                {c.tax_burden_pct > 40 ? (
                  <AlertTriangle size={14} className="text-amber-500 flex-shrink-0" />
                ) : (
                  <CheckCircle size={14} className="text-emerald-500 flex-shrink-0" />
                )}
              </div>
              <div className="flex items-center gap-3 mt-0.5">
                <span className="text-[10px] text-slate-400">{c.employee_count} employees</span>
                <span className="text-[10px] text-slate-400">{formatUSD(c.avg_salary_usd)} avg</span>
              </div>
            </div>

            <div className="text-right flex-shrink-0">
              <p className="text-sm font-semibold text-slate-800">{formatUSD(c.total_gross_usd)}</p>
              <p className="text-[10px] text-slate-400">{c.tax_burden_pct.toFixed(0)}% tax burden</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
