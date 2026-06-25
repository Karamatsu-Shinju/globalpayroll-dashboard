import type { DepartmentBreakdown } from '../lib/api';

interface Props {
  data: DepartmentBreakdown[];
}

const COLORS = ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed', '#0891b2', '#be123c', '#4338ca'];

export default function DepartmentChart({ data }: Props) {
  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);
  const sorted = [...data].sort((a, b) => b.total_payroll_usd - a.total_payroll_usd);
  const total = sorted.reduce((s, d) => s + d.total_payroll_usd, 0);
  
  const size = 160;
  const cx = size / 2;
  const cy = size / 2;
  const radius = size * 0.38;
  const innerRadius = size * 0.24;
  
  let angleOffset = -Math.PI / 2;
  const segments = sorted.map((d, i) => {
    const frac = d.total_payroll_usd / total;
    const angle = frac * Math.PI * 2;
    const start = angleOffset;
    const end = angleOffset + angle;
    angleOffset = end;
    
    const x1 = cx + radius * Math.cos(start);
    const y1 = cy + radius * Math.sin(start);
    const x2 = cx + radius * Math.cos(end);
    const y2 = cy + radius * Math.sin(end);
    const lx1 = cx + innerRadius * Math.cos(start);
    const ly1 = cy + innerRadius * Math.sin(start);
    const lx2 = cx + innerRadius * Math.cos(end);
    const ly2 = cy + innerRadius * Math.sin(end);
    const largeArc = angle > Math.PI ? 1 : 0;
    
    return {
      ...d,
      color: COLORS[i % COLORS.length],
      path: `M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} L ${lx2} ${ly2} A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${lx1} ${ly1} Z`,
      midAngle: start + angle / 2,
    };
  });

  return (
    <div className="section-card">
      <h3 className="text-sm font-semibold text-slate-900 mb-1">Payroll by Department</h3>
      <p className="text-xs text-slate-500 mb-4">Distribution of payroll spend</p>
      
      <div className="flex items-center gap-6">
        <svg viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0" style={{ width: 140, height: 140 }}>
          {segments.map((s) => (
            <path key={s.department} d={s.path} fill={s.color} opacity={0.85} />
          ))}
          <text x={cx} y={cy - 4} textAnchor="middle" fontSize="14" fontWeight="700" fill="#0f172a">
            {sorted.length}
          </text>
          <text x={cx} y={cy + 10} textAnchor="middle" fontSize="8" fill="#64748b">
            Departments
          </text>
        </svg>
        
        <div className="space-y-2 flex-1">
          {sorted.map((d, i) => (
            <div key={d.department} className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                <span className="text-xs text-slate-600 truncate">{d.department}</span>
              </div>
              <span className="text-xs font-semibold text-slate-700 flex-shrink-0">{formatUSD(d.total_payroll_usd)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
