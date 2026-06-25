import { CheckCircle, Clock } from 'lucide-react';
import type { PayrollRun } from '../lib/api';

interface Props {
  runs: PayrollRun[];
}

export default function RecentPayrollRuns({ runs }: Props) {
  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);

  const sorted = [...runs].sort((a, b) => {
    if (a.year !== b.year) return b.year - a.year;
    return b.month - a.month;
  });

  return (
    <div className="section-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Recent Payroll Runs</h3>
          <p className="text-xs text-slate-500 mt-0.5">Latest processing cycles</p>
        </div>
      </div>

      <div className="space-y-3">
        {sorted.map((run) => (
          <div key={run.id} className="flex items-center gap-4 p-3 rounded-lg border border-slate-100 hover:border-slate-200 transition-colors">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${run.status === 'completed' ? 'bg-emerald-50' : 'bg-amber-50'}`}>
              {run.status === 'completed' ? (
                <CheckCircle size={18} className="text-emerald-600" />
              ) : (
                <Clock size={18} className="text-amber-600" />
              )}
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-800">{run.name}</p>
              <p className="text-[10px] text-slate-400">{run.total_employees} employees processed</p>
            </div>

            <div className="text-right flex-shrink-0">
              <p className="text-sm font-semibold text-slate-800">{formatUSD(run.total_gross_usd)}</p>
              <p className="text-[10px] text-slate-400">{formatUSD(run.total_net_usd)} net</p>
            </div>

            <div className="flex-shrink-0">
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${run.status === 'completed' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                {run.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
