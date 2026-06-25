from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import Country, Employee, PayrollRun, PayrollEntry
from app.schemas import (
    DashboardResponse, DashboardKPIs, CountryPayrollBreakdown,
    MonthlyTrend, DepartmentBreakdown, TaxBreakdown
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    # KPIs
    total_employees = db.query(Employee).filter(Employee.status == "active").count()
    total_countries = db.query(Country).count()
    
    latest_run = db.query(PayrollRun).order_by(PayrollRun.year.desc(), PayrollRun.month.desc()).first()
    total_monthly_payroll = latest_run.total_gross_usd if latest_run else 0
    avg_employee_cost = total_monthly_payroll / total_employees if total_employees > 0 else 0
    
    compliant_countries = db.query(Country).filter(Country.compliance_status == "compliant").count()
    compliance_rate = (compliant_countries / total_countries * 100) if total_countries > 0 else 0
    
    # YoY growth (compare latest two runs)
    runs = db.query(PayrollRun).order_by(PayrollRun.year.desc(), PayrollRun.month.desc()).limit(2).all()
    yoy_growth = 0
    if len(runs) >= 2:
        prev = runs[1].total_gross_usd
        curr = runs[0].total_gross_usd
        yoy_growth = round(((curr - prev) / prev) * 100, 1) if prev > 0 else 0

    kpis = DashboardKPIs(
        total_employees=total_employees,
        total_countries=total_countries,
        total_monthly_payroll_usd=round(total_monthly_payroll, 2),
        avg_employee_cost_usd=round(avg_employee_cost, 2),
        compliance_rate=round(compliance_rate, 1),
        yoy_growth=yoy_growth
    )

    # Country breakdowns
    country_breakdowns = []
    countries = db.query(Country).all()
    for c in countries:
        emp_count = db.query(Employee).filter(Employee.country_id == c.id, Employee.status == "active").count()
        if emp_count == 0:
            continue
        
        totals = db.query(
            func.sum(PayrollEntry.gross_salary_usd),
            func.sum(PayrollEntry.employer_ss_amount),
            func.sum(PayrollEntry.net_salary_usd)
        ).join(Employee).filter(Employee.country_id == c.id).first()
        
        gross = totals[0] or 0
        emp_ss = totals[1] or 0
        net = totals[2] or 0
        avg_sal = gross / emp_count if emp_count > 0 else 0
        tax_burden = ((gross - net) / gross * 100) if gross > 0 else 0

        country_breakdowns.append(CountryPayrollBreakdown(
            country_name=c.name,
            country_code=c.code,
            currency=c.currency,
            employee_count=emp_count,
            total_gross_usd=round(gross, 2),
            total_employer_ss_usd=round(emp_ss, 2),
            total_net_usd=round(net, 2),
            avg_salary_usd=round(avg_sal, 2),
            tax_burden_pct=round(tax_burden, 1)
        ))

    # Monthly trends
    monthly_trends = []
    all_runs = db.query(PayrollRun).order_by(PayrollRun.year, PayrollRun.month).all()
    for run in all_runs:
        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_trends.append(MonthlyTrend(
            month=f"{month_names[run.month]} {run.year}",
            total_payroll_usd=run.total_gross_usd,
            total_employees=run.total_employees
        ))

    # Department breakdowns
    dept_data = db.query(
        Employee.department,
        func.count(Employee.id),
        func.avg(Employee.salary_usd),
        func.sum(Employee.salary_usd)
    ).filter(Employee.status == "active").group_by(Employee.department).all()

    department_breakdowns = []
    for dept, count, avg_sal, total in dept_data:
        department_breakdowns.append(DepartmentBreakdown(
            department=dept,
            employee_count=count,
            avg_salary_usd=round(avg_sal or 0, 2),
            total_payroll_usd=round(total or 0, 2)
        ))

    # Tax breakdowns
    tax_breakdowns = []
    for c in countries:
        tax_data = db.query(
            func.sum(PayrollEntry.income_tax_amount),
            func.sum(PayrollEntry.employee_ss_amount),
            func.sum(PayrollEntry.employer_ss_amount)
        ).join(Employee).filter(Employee.country_id == c.id).first()
        
        income_tax = tax_data[0] or 0
        emp_ss = tax_data[1] or 0
        empr_ss = tax_data[2] or 0
        total_tax = income_tax + emp_ss + empr_ss
        
        if total_tax > 0:
            tax_breakdowns.append(TaxBreakdown(
                country_name=c.name,
                income_tax_usd=round(income_tax, 2),
                employee_ss_usd=round(emp_ss, 2),
                employer_ss_usd=round(empr_ss, 2),
                total_tax_usd=round(total_tax, 2)
            ))

    return DashboardResponse(
        kpis=kpis,
        country_breakdowns=country_breakdowns,
        monthly_trends=monthly_trends,
        department_breakdowns=department_breakdowns,
        tax_breakdowns=tax_breakdowns
    )
