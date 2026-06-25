from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date, datetime


class CountryBase(BaseModel):
    name: str
    code: str
    currency: str
    currency_symbol: str
    exchange_rate_to_usd: float
    employer_ss_rate: float
    employee_ss_rate: float
    avg_income_tax_rate: float
    payroll_frequency: str
    compliance_status: str
    mandatory_benefits: List[str]
    notes: Optional[str] = None


class CountryResponse(CountryBase):
    id: int
    employee_count: int = 0
    total_payroll_usd: float = 0.0

    class Config:
        from_attributes = True


class CountryDetail(CountryResponse):
    employees: List["EmployeeResponse"] = []

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    country_id: int
    role: str
    department: str
    salary_local: float
    salary_usd: float
    employment_type: str = "full_time"
    hire_date: date
    status: str = "active"
    tax_class: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    country_name: str = ""
    country_code: str = ""
    currency: str = ""

    class Config:
        from_attributes = True


class PayrollEntryResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str = ""
    gross_salary_usd: float
    employer_ss_amount: float
    employee_ss_amount: float
    income_tax_amount: float
    other_deductions: float
    net_salary_usd: float

    class Config:
        from_attributes = True


class PayrollRunResponse(BaseModel):
    id: int
    name: str
    month: int
    year: int
    status: str
    total_employees: int
    total_gross_usd: float
    total_deductions_usd: float
    total_net_usd: float
    created_at: datetime

    class Config:
        from_attributes = True


class PayrollRunDetail(PayrollRunResponse):
    entries: List[PayrollEntryResponse] = []

    class Config:
        from_attributes = True


class DashboardKPIs(BaseModel):
    total_employees: int
    total_countries: int
    total_monthly_payroll_usd: float
    avg_employee_cost_usd: float
    compliance_rate: float
    yoy_growth: float


class CountryPayrollBreakdown(BaseModel):
    country_name: str
    country_code: str
    currency: str
    employee_count: int
    total_gross_usd: float
    total_employer_ss_usd: float
    total_net_usd: float
    avg_salary_usd: float
    tax_burden_pct: float


class MonthlyTrend(BaseModel):
    month: str
    total_payroll_usd: float
    total_employees: int


class DepartmentBreakdown(BaseModel):
    department: str
    employee_count: int
    avg_salary_usd: float
    total_payroll_usd: float


class TaxBreakdown(BaseModel):
    country_name: str
    income_tax_usd: float
    employee_ss_usd: float
    employer_ss_usd: float
    total_tax_usd: float


class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    country_breakdowns: List[CountryPayrollBreakdown]
    monthly_trends: List[MonthlyTrend]
    department_breakdowns: List[DepartmentBreakdown]
    tax_breakdowns: List[TaxBreakdown]


class FilterParams(BaseModel):
    country_id: Optional[int] = None
    department: Optional[str] = None
    status: Optional[str] = None
    role: Optional[str] = None
