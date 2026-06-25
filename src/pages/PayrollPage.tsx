import { useState, useEffect } from 'react';
import { api, type PayrollRun } from '../lib/api';
import RecentPayrollRuns from '../components/RecentPayrollRuns';

export default function PayrollPage() {
  const [runs, setRuns] = useState<PayrollRun[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getPayrollRuns().then((r) => { setRuns(r); setLoading(false); });
  }, []);

  if (loading) return <p className="text-sm text-slate-500">Loading...</p>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Payroll Runs</h2>
        <p className="text-sm text-slate-500">Processing history and status</p>
      </div>
      <RecentPayrollRuns runs={runs} />
    </div>
  );
}
