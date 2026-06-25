from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.models import Employee, Country, PayrollEntry
from app.schemas import EmployeeResponse, EmployeeCreate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    country_id: Optional[int] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Employee, Country).join(Country, Employee.country_id == Country.id)
    
    if country_id:
        query = query.filter(Employee.country_id == country_id)
    if department:
        query = query.filter(Employee.department == department)
    if status:
        query = query.filter(Employee.status == status)
    if role:
        query = query.filter(Employee.role == role)

    results = query.all()
    response = []
    for emp, country in results:
        response.append(EmployeeResponse(
            id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            email=emp.email,
            country_id=emp.country_id,
            role=emp.role,
            department=emp.department,
            salary_local=emp.salary_local,
            salary_usd=emp.salary_usd,
            employment_type=emp.employment_type,
            hire_date=emp.hire_date,
            status=emp.status,
            tax_class=emp.tax_class,
            country_name=country.name,
            country_code=country.code,
            currency=country.currency
        ))
    return response


@router.get("/filters")
def get_filter_options(db: Session = Depends(get_db)):
    departments = [d[0] for d in db.query(Employee.department).distinct().all()]
    roles = [r[0] for r in db.query(Employee.role).distinct().all()]
    countries = db.query(Country.id, Country.name).all()
    return {
        "departments": departments,
        "roles": roles,
        "countries": [{"id": c[0], "name": c[1]} for c in countries]
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    result = db.query(Employee, Country).join(Country).filter(Employee.id == employee_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp, country = result
    return EmployeeResponse(
        id=emp.id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        email=emp.email,
        country_id=emp.country_id,
        role=emp.role,
        department=emp.department,
        salary_local=emp.salary_local,
        salary_usd=emp.salary_usd,
        employment_type=emp.employment_type,
        hire_date=emp.hire_date,
        status=emp.status,
        tax_class=emp.tax_class,
        country_name=country.name,
        country_code=country.code,
        currency=country.currency
    )
