from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String(3), nullable=False, unique=True)
    currency = Column(String, nullable=False)
    currency_symbol = Column(String, nullable=False)
    exchange_rate_to_usd = Column(Float, nullable=False)
    employer_ss_rate = Column(Float, nullable=False)
    employee_ss_rate = Column(Float, nullable=False)
    avg_income_tax_rate = Column(Float, nullable=False)
    payroll_frequency = Column(String, nullable=False)
    compliance_status = Column(String, nullable=False, default="compliant")
    mandatory_benefits = Column(JSON, default=list)
    notes = Column(Text, nullable=True)

    employees = relationship("Employee", back_populates="country")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    salary_local = Column(Float, nullable=False)
    salary_usd = Column(Float, nullable=False)
    employment_type = Column(String, nullable=False, default="full_time")
    hire_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="active")
    tax_class = Column(String, nullable=True)

    country = relationship("Country", back_populates="employees")
    payroll_entries = relationship("PayrollEntry", back_populates="employee")


class PayrollRun(Base):
    __tablename__ = "payroll_runs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="completed")
    total_employees = Column(Integer, nullable=False)
    total_gross_usd = Column(Float, nullable=False)
    total_deductions_usd = Column(Float, nullable=False)
    total_net_usd = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    entries = relationship("PayrollEntry", back_populates="payroll_run")


class PayrollEntry(Base):
    __tablename__ = "payroll_entries"

    id = Column(Integer, primary_key=True, index=True)
    payroll_run_id = Column(Integer, ForeignKey("payroll_runs.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    gross_salary_local = Column(Float, nullable=False)
    gross_salary_usd = Column(Float, nullable=False)
    employer_ss_amount = Column(Float, nullable=False)
    employee_ss_amount = Column(Float, nullable=False)
    income_tax_amount = Column(Float, nullable=False)
    other_deductions = Column(Float, default=0.0)
    net_salary_local = Column(Float, nullable=False)
    net_salary_usd = Column(Float, nullable=False)

    payroll_run = relationship("PayrollRun", back_populates="entries")
    employee = relationship("Employee", back_populates="payroll_entries")
