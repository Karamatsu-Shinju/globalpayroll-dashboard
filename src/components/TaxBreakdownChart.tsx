import type { TaxBreakdown } from '../lib/api';

interface Props {
  data: TaxBreakdown[];
}

export default function TaxBreakdownChart({ data }: Props) {
  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);
  
  const sorted = [...data].sort((a, b) => b.total_tax_usd - a.total_tax_usd).slice(0, 8);
  const max = sorted[0]?.total_tax_usd || 1;
  const barHeight = 24;
  const gap = 14;
  const leftPad = 110;
  const rightPad = 10;
  const chartWidth = 400;
  const totalWidth = leftPad + chartWidth + rightPad;
  const totalHeight = sorted.length * (barHeight + gap) + gap + 30;

  return (
    <div className="section-card">
      <h3 className="text-sm font-semibold text-slate-900 mb-1">Tax & Contributions</h3>
      <p className="text-xs text-slate-500 mb-4">Breakdown by type — monthly total</p>
      
      {/* Legend */}
      <div className="flex gap-4 mb-4">
        <div className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm" style={{background:'#2563eb'}} /><span className="text-[10px] text-slate-500">Income Tax</span></div>
        <div className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm" style={{background:'#059669'}} /><span className="text-[10px] text-slate-500">Employee SS</span></div>
        <div className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm" style={{background:'#d97706'}} /><span className="text-[10px] text-slate-500">Employer SS</span></div>
      </div>

      <svg viewBox={`0 0 ${totalWidth} ${totalHeight}`} className="w-full" style={{ maxHeight: 340 }}>
        {sorted.map((d, i) => {
          const y = gap + 30 + i * (barHeight + gap);
          const incW = (d.income_tax_usd / max) * chartWidth;
          const empW = (d.employee_ss_usd / max) * chartWidth;
          const emprW = (d.employer_ss_usd / max) * chartWidth;
          
          return (
            <g key={d.country_name}>
              <text x={leftPad - 6} y={y + barHeight / 2 + 4} textAnchor="end" fontSize="10" fill="#475569" fontWeight="500">
                {d.country_name.length > 12 ? d.country_name.slice(0, 12) + '...' : d.country_name}
              </text>
              <rect x={leftPad} y={y} width={incW} height={barHeight} rx={3} fill="#2563eb" opacity={0.85} />
              <rect x={leftPad + incW} y={y} width={empW} height={barHeight} rx={3} fill="#059669" opacity={0.85} />
              <rect x={leftPad + incW + empW} y={y} width={emprW} height={barHeight} rx={3} fill="#d97706" opacity={0.85} />
              <text x={leftPad + incW + empW + emprW + 6} y={y + barHeight / 2 + 4} fontSize="10" fill="#475569" fontWeight="600">
                {formatUSD(d.total_tax_usd)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
