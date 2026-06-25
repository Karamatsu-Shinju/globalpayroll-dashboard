import { useState, useEffect } from 'react';
import { api, type Employee } from '../lib/api';
import EmployeeTable from '../components/EmployeeTable';

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getEmployees().then((e) => { setEmployees(e); setLoading(false); });
  }, []);

  if (loading) return <p className="text-sm text-slate-500">Loading...</p>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Employees</h2>
        <p className="text-sm text-slate-500">{employees.length} employees across the global workforce</p>
      </div>
      <EmployeeTable employees={employees} />
    </div>
  );
}
