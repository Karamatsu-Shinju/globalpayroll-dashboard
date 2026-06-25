import { useState, useEffect } from 'react';
import { api, type Country } from '../lib/api';
import { Globe, Users, DollarSign, FileText } from 'lucide-react';

export default function CountriesPage() {
  const [countries, setCountries] = useState<Country[]>([]);
  const [selected, setSelected] = useState<Country | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCountries().then((c) => { setCountries(c); setLoading(false); });
  }, []);

  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(n);
  const formatPct = (n: number) => `${(n * 100).toFixed(1)}%`;

  if (loading) return <p className="text-sm text-slate-500">Loading...</p>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Countries</h2>
        <p className="text-sm text-slate-500">Manage payroll compliance across {countries.length} countries</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Country List */}
        <div className="space-y-2">
          {countries.map((c) => (
            <button
              key={c.id}
              onClick={() => setSelected(c)}
              className={`w-full text-left p-3 rounded-xl border transition-all ${selected?.id === c.id ? 'border-blue-300 bg-blue-50' : 'border-slate-200 bg-white hover:border-slate-300'}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg flex items-center justify-center text-xs font-bold text-white flex-shrink-0" style={{ backgroundColor: c.compliance_status === 'compliant' ? '#059669' : '#d97706' }}>
                    {c.code}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-800">{c.name}</p>
                    <p className="text-[10px] text-slate-400">{c.currency} · {c.payroll_frequency}</p>
                  </div>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${c.compliance_status === 'compliant' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                  {c.compliance_status}
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* Country Detail */}
        <div className="lg:col-span-2">
          {selected ? (
            <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-xl flex items-center justify-center text-lg font-bold text-white" style={{ backgroundColor: '#2563eb' }}>
                    {selected.code}
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-slate-900">{selected.name}</h3>
                    <p className="text-sm text-slate-500">{selected.currency} ({selected.currency_symbol}) · {selected.payroll_frequency} payroll</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${selected.compliance_status === 'compliant' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                  {selected.compliance_status}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 rounded-lg bg-slate-50">
                  <Users size={16} className="text-slate-400 mb-2" />
                  <p className="text-xl font-bold text-slate-900">{selected.employee_count}</p>
                  <p className="text-xs text-slate-500">Employees</p>
                </div>
                <div className="p-4 rounded-lg bg-slate-50">
                  <DollarSign size={16} className="text-slate-400 mb-2" />
                  <p className="text-xl font-bold text-slate-900">{formatUSD(selected.total_payroll_usd)}</p>
                  <p className="text-xs text-slate-500">Monthly Payroll</p>
                </div>
                <div className="p-4 rounded-lg bg-slate-50">
                  <Globe size={16} className="text-slate-400 mb-2" />
                  <p className="text-xl font-bold text-slate-900">{formatPct(selected.avg_income_tax_rate)}</p>
                  <p className="text-xs text-slate-500">Avg Income Tax</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Social Security</p>
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-600">Employer rate</span>
                      <span className="font-medium text-slate-800">{formatPct(selected.employer_ss_rate)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-600">Employee rate</span>
                      <span className="font-medium text-slate-800">{formatPct(selected.employee_ss_rate)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Exchange Rate</p>
                  <p className="text-sm text-slate-600">1 USD = {selected.exchange_rate_to_usd} {selected.currency}</p>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase mb-2">Mandatory Benefits</p>
                <div className="flex flex-wrap gap-2">
                  {selected.mandatory_benefits.map((b) => (
                    <span key={b} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                      {b}
                    </span>
                  ))}
                </div>
              </div>

              {selected.notes && (
                <div className="flex gap-2 p-3 rounded-lg bg-slate-50">
                  <FileText size={14} className="text-slate-400 flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-slate-600 leading-relaxed">{selected.notes}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full min-h-[300px] bg-white rounded-xl border border-slate-200 border-dashed">
              <p className="text-sm text-slate-400">Select a country to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
