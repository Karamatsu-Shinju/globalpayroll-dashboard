import type { CountryBreakdown } from '../lib/api';

interface Props {
  data: CountryBreakdown[];
}

const COLORS = ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed', '#0891b2', '#be123c', '#4338ca'];

export default function PayrollByCountryChart({ data }: Props) {
  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);
  
  const sorted = [...data].sort((a, b) => b.total_gross_usd - a.total_gross_usd);
  const max = sorted[0]?.total_gross_usd || 1;
  const barHeight = 28;
  const gap = 12;
  const leftPad = 120;
  const rightPad = 80;
  const chartWidth = 500;
  const totalWidth = leftPad + chartWidth + rightPad;
  const totalHeight = sorted.length * (barHeight + gap) + gap;

  return (
    <div className="section-card">
      <h3 className="text-sm font-semibold text-slate-900 mb-1">Payroll by Country</h3>
      <p className="text-xs text-slate-500 mb-5">Total gross payroll (USD) — latest run</p>
      
      <svg viewBox={`0 0 ${totalWidth} ${totalHeight}`} className="w-full" style={{ maxHeight: 360 }}>
        {sorted.map((d, i) => {
          const y = gap + i * (barHeight + gap);
          const w = (d.total_gross_usd / max) * chartWidth;
          const color = COLORS[i % COLORS.length];
          
          return (
            <g key={d.country_code}>
              <text x={leftPad - 8} y={y + barHeight / 2 + 4} textAnchor="end" fontSize="11" fill="#475569" fontWeight="500">
                {d.country_name}
              </text>
              <rect x={leftPad} y={y} width={w} height={barHeight} rx={4} fill={color} opacity={0.85} />
              <text x={leftPad + w + 8} y={y + barHeight / 2 + 4} fontSize="11" fill="#475569" fontWeight="600">
                {formatUSD(d.total_gross_usd)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
