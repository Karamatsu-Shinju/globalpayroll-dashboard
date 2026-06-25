import { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import type { Employee } from '../lib/api';

interface Props {
  employees: Employee[];
}

export default function EmployeeTable({ employees }: Props) {
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('');

  const formatUSD = (n: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);
  const formatLocal = (n: number, sym: string) => `${sym}${new Intl.NumberFormat('en-US').format(n)}`;

  const depts = [...new Set(employees.map((e) => e.department))].sort();

  const filtered = employees.filter((e) => {
    const matchesSearch = `${e.first_name} ${e.last_name} ${e.email} ${e.role}`.toLowerCase().includes(search.toLowerCase());
    const matchesDept = !deptFilter || e.department === deptFilter;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="section-card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Employees</h3>
          <p className="text-xs text-slate-500 mt-0.5">{filtered.length} of {employees.length} employees</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-48"
            />
          </div>
          <select
            value={deptFilter}
            onChange={(e) => setDeptFilter(e.target.value)}
            className="text-xs border border-slate-200 rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Departments</option>
            {depts.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="data-table w-full">
          <thead>
            <tr>
              <th>Name</th>
              <th>Role</th>
              <th>Department</th>
              <th>Country</th>
              <th>Salary (Local)</th>
              <th>Salary (USD)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((e) => (
              <tr key={e.id} className="hover:bg-slate-50 transition-colors">
                <td>
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-semibold text-white flex-shrink-0" style={{ backgroundColor: '#2563eb' }}>
                      {e.first_name[0]}{e.last_name[0]}
                    </div>
                    <div>
                      <p className="font-medium text-slate-800">{e.first_name} {e.last_name}</p>
                      <p className="text-[10px] text-slate-400">{e.email}</p>
                    </div>
                  </div>
                </td>
                <td>{e.role}</td>
                <td>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-600">
                    {e.department}
                  </span>
                </td>
                <td>
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold text-slate-500">{e.country_code}</span>
                    <span className="text-xs text-slate-400">{e.currency}</span>
                  </div>
                </td>
                <td className="font-mono text-xs">{formatLocal(e.salary_local, e.country_code === 'GB' ? '£' : e.currency === 'EUR' ? '€' : e.currency === 'INR' ? '₹' : e.currency === 'BRL' ? 'R$' : e.currency === 'AUD' ? 'A$' : e.currency === 'CAD' ? 'C$' : '$')}</td>
                <td className="font-mono text-xs font-medium">{formatUSD(e.salary_usd)}</td>
                <td>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium ${e.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                    {e.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
