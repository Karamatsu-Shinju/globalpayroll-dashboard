const API_BASE = '/api';

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface Country {
  id: number;
  name: string;
  code: string;
  currency: string;
  currency_symbol: string;
  exchange_rate_to_usd: number;
  employer_ss_rate: number;
  employee_ss_rate: number;
  avg_income_tax_rate: number;
  payroll_frequency: string;
  compliance_status: string;
  mandatory_benefits: string[];
  notes?: string;
  employee_count: number;
  total_payroll_usd: number;
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  country_id: number;
  role: string;
  department: string;
  salary_local: number;
  salary_usd: number;
  employment_type: string;
  hire_date: string;
  status: string;
  tax_class?: string;
  country_name: string;
  country_code: string;
  currency: string;
}

export interface DashboardKPIs {
  total_employees: number;
  total_countries: number;
  total_monthly_payroll_usd: number;
  avg_employee_cost_usd: number;
  compliance_rate: number;
  yoy_growth: number;
}

export interface CountryBreakdown {
  country_name: string;
  country_code: string;
  currency: string;
  employee_count: number;
  total_gross_usd: number;
  total_employer_ss_usd: number;
  total_net_usd: number;
  avg_salary_usd: number;
  tax_burden_pct: number;
}

export interface MonthlyTrend {
  month: string;
  total_payroll_usd: number;
  total_employees: number;
}

export interface DepartmentBreakdown {
  department: string;
  employee_count: number;
  avg_salary_usd: number;
  total_payroll_usd: number;
}

export interface TaxBreakdown {
  country_name: string;
  income_tax_usd: number;
  employee_ss_usd: number;
  employer_ss_usd: number;
  total_tax_usd: number;
}

export interface DashboardData {
  kpis: DashboardKPIs;
  country_breakdowns: CountryBreakdown[];
  monthly_trends: MonthlyTrend[];
  department_breakdowns: DepartmentBreakdown[];
  tax_breakdowns: TaxBreakdown[];
}

export interface PayrollRun {
  id: number;
  name: string;
  month: number;
  year: number;
  status: string;
  total_employees: number;
  total_gross_usd: number;
  total_deductions_usd: number;
  total_net_usd: number;
  created_at: string;
}

export const api = {
  getDashboard: () => fetchJson<DashboardData>('/dashboard/'),
  getCountries: () => fetchJson<Country[]>('/countries/'),
  getEmployees: () => fetchJson<Employee[]>('/employees/'),
  getPayrollRuns: () => fetchJson<PayrollRun[]>('/payroll/runs'),
  getHealth: () => fetchJson<{ status: string }>('/health'),
};
