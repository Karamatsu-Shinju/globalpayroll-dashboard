import { useState, useEffect } from 'react';
import { api, type DashboardData, type Employee, type PayrollRun } from '../lib/api';
import KPICards from '../components/KPICards';
import PayrollByCountryChart from '../components/PayrollByCountryChart';
import TaxBreakdownChart from '../components/TaxBreakdownChart';
import DepartmentChart from '../components/DepartmentChart';
import ComplianceStatus from '../components/ComplianceStatus';
import EmployeeTable from '../components/EmployeeTable';
import RecentPayrollRuns from '../components/RecentPayrollRuns';

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [payrollRuns, setPayrollRuns] = useState<PayrollRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.getDashboard(),
      api.getEmployees(),
      api.getPayrollRuns(),
    ])
      .then(([dash, emps, runs]) => {
        setData(dash);
        setEmployees(emps);
        setPayrollRuns(runs);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm text-slate-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Failed to load dashboard</p>
          <p className="text-xs text-slate-400">{error}</p>
          <p className="text-xs text-slate-400 mt-2">Make sure the Python backend is running: cd backend && uvicorn app.main:app --reload</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Dashboard</h2>
          <p className="text-sm text-slate-500">Global payroll overview — Q4 2024</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-slate-500">Live data</span>
        </div>
      </div>

      <KPICards kpis={data.kpis} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PayrollByCountryChart data={data.country_breakdowns} />
        <TaxBreakdownChart data={data.tax_breakdowns} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <DepartmentChart data={data.department_breakdowns} />
        <div className="lg:col-span-2">
          <ComplianceStatus data={data.country_breakdowns} />
        </div>
      </div>

      <EmployeeTable employees={employees} />
      <RecentPayrollRuns runs={payrollRuns} />
    </div>
  );
}
