from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import Country, Employee, PayrollEntry
from app.schemas import CountryResponse, CountryDetail

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/", response_model=List[CountryResponse])
def list_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    result = []
    for c in countries:
        emp_count = db.query(Employee).filter(Employee.country_id == c.id, Employee.status == "active").count()
        total_payroll = db.query(func.sum(PayrollEntry.gross_salary_usd)).join(Employee).filter(Employee.country_id == c.id).scalar() or 0
        result.append(CountryResponse(
            id=c.id,
            name=c.name,
            code=c.code,
            currency=c.currency,
            currency_symbol=c.currency_symbol,
            exchange_rate_to_usd=c.exchange_rate_to_usd,
            employer_ss_rate=c.employer_ss_rate,
            employee_ss_rate=c.employee_ss_rate,
            avg_income_tax_rate=c.avg_income_tax_rate,
            payroll_frequency=c.payroll_frequency,
            compliance_status=c.compliance_status,
            mandatory_benefits=c.mandatory_benefits,
            notes=c.notes,
            employee_count=emp_count,
            total_payroll_usd=round(total_payroll, 2)
        ))
    return result


@router.get("/{country_id}", response_model=CountryDetail)
def get_country(country_id: int, db: Session = Depends(get_db)):
    c = db.query(Country).filter(Country.id == country_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Country not found")
    
    emp_count = db.query(Employee).filter(Employee.country_id == c.id, Employee.status == "active").count()
    total_payroll = db.query(func.sum(PayrollEntry.gross_salary_usd)).join(Employee).filter(Employee.country_id == c.id).scalar() or 0
    
    employees = db.query(Employee).filter(Employee.country_id == c.id).all()
    emp_responses = []
    for e in employees:
        emp_responses.append({
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name,
            "email": e.email,
            "country_id": e.country_id,
            "role": e.role,
            "department": e.department,
            "salary_local": e.salary_local,
            "salary_usd": e.salary_usd,
            "employment_type": e.employment_type,
            "hire_date": e.hire_date,
            "status": e.status,
            "tax_class": e.tax_class,
            "country_name": c.name,
            "country_code": c.code,
            "currency": c.currency
        })

    return CountryDetail(
        id=c.id,
        name=c.name,
        code=c.code,
        currency=c.currency,
        currency_symbol=c.currency_symbol,
        exchange_rate_to_usd=c.exchange_rate_to_usd,
        employer_ss_rate=c.employer_ss_rate,
        employee_ss_rate=c.employee_ss_rate,
        avg_income_tax_rate=c.avg_income_tax_rate,
        payroll_frequency=c.payroll_frequency,
        compliance_status=c.compliance_status,
        mandatory_benefits=c.mandatory_benefits,
        notes=c.notes,
        employee_count=emp_count,
        total_payroll_usd=round(total_payroll, 2),
        employees=emp_responses
    )
