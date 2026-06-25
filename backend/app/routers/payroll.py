from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import PayrollRun, PayrollEntry, Employee, Country
from app.schemas import PayrollRunResponse, PayrollRunDetail, PayrollEntryResponse

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.get("/runs", response_model=List[PayrollRunResponse])
def list_payroll_runs(db: Session = Depends(get_db)):
    runs = db.query(PayrollRun).order_by(PayrollRun.year.desc(), PayrollRun.month.desc()).all()
    return runs


@router.get("/runs/{run_id}", response_model=PayrollRunDetail)
def get_payroll_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(PayrollRun).filter(PayrollRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    
    entries = db.query(PayrollEntry, Employee).join(Employee).filter(PayrollEntry.payroll_run_id == run_id).all()
    entry_responses = []
    for entry, emp in entries:
        entry_responses.append(PayrollEntryResponse(
            id=entry.id,
            employee_id=entry.employee_id,
            employee_name=f"{emp.first_name} {emp.last_name}",
            gross_salary_usd=entry.gross_salary_usd,
            employer_ss_amount=entry.employer_ss_amount,
            employee_ss_amount=entry.employee_ss_amount,
            income_tax_amount=entry.income_tax_amount,
            other_deductions=entry.other_deductions,
            net_salary_usd=entry.net_salary_usd
        ))

    return PayrollRunDetail(
        id=run.id,
        name=run.name,
        month=run.month,
        year=run.year,
        status=run.status,
        total_employees=run.total_employees,
        total_gross_usd=run.total_gross_usd,
        total_deductions_usd=run.total_deductions_usd,
        total_net_usd=run.total_net_usd,
        created_at=run.created_at,
        entries=entry_responses
    )
