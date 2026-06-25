import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CountriesPage from './pages/CountriesPage';
import EmployeesPage from './pages/EmployeesPage';
import PayrollPage from './pages/PayrollPage';

export default function App() {
  const [activeView, setActiveView] = useState('dashboard');

  return (
    <div className="flex h-screen overflow-hidden" style={{ backgroundColor: '#f1f5f9' }}>
      <Sidebar activeView={activeView} onViewChange={setActiveView} />
      
      <main className="flex-1 overflow-y-auto">
        <div className="p-6 max-w-[1400px] mx-auto">
          {activeView === 'dashboard' && <Dashboard />}
          {activeView === 'countries' && <CountriesPage />}
          {activeView === 'employees' && <EmployeesPage />}
          {activeView === 'payroll' && <PayrollPage />}
        </div>
      </main>
    </div>
  );
}
