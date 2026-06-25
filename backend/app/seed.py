from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import Country, Employee, PayrollRun, PayrollEntry
from datetime import date
import random


def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing
    db.query(PayrollEntry).delete()
    db.query(PayrollRun).delete()
    db.query(Employee).delete()
    db.query(Country).delete()
    db.commit()

    countries_data = [
        {
            "name": "United States",
            "code": "US",
            "currency": "USD",
            "currency_symbol": "$",
            "exchange_rate_to_usd": 1.0,
            "employer_ss_rate": 0.0765,
            "employee_ss_rate": 0.0765,
            "avg_income_tax_rate": 0.22,
            "payroll_frequency": "bi-weekly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Social Security", "Medicare", "Unemployment Insurance", "Workers Compensation"],
            "notes": "FICA: 6.2% SS + 1.45% Medicare each. Federal and state income tax withheld."
        },
        {
            "name": "United Kingdom",
            "code": "GB",
            "currency": "GBP",
            "currency_symbol": "£",
            "exchange_rate_to_usd": 1.27,
            "employer_ss_rate": 0.138,
            "employee_ss_rate": 0.08,
            "avg_income_tax_rate": 0.20,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["National Insurance", "Workplace Pension (auto-enrolment)", "Statutory Sick Pay", "Statutory Maternity Pay"],
            "notes": "NIC Class 1 primary 8%, secondary 13.8%. Income tax 20% basic rate. Pension auto-enrolment 3% employer min."
        },
        {
            "name": "Germany",
            "code": "DE",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.2065,
            "employee_ss_rate": 0.2065,
            "avg_income_tax_rate": 0.25,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Health Insurance", "Pension Insurance", "Unemployment Insurance", "Long-term Care Insurance"],
            "notes": "Four-pillar social insurance. Split 50/50 employer/employee. Church tax may apply. Tax class system (I-VI)."
        },
        {
            "name": "France",
            "code": "FR",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.45,
            "employee_ss_rate": 0.22,
            "avg_income_tax_rate": 0.20,
            "payroll_frequency": "monthly",
            "compliance_status": "attention",
            "mandatory_benefits": ["Social Security", "Health Insurance", "Pension", "Accident Insurance", "Family Allowances"],
            "notes": "High employer contribution rate at 45%. Income tax withheld at source (PAS). 13th month common."
        },
        {
            "name": "Portugal",
            "code": "PT",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.2375,
            "employee_ss_rate": 0.11,
            "avg_income_tax_rate": 0.18,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Social Security", "Health Subsystem", "Meal Allowance (€7-10/day)", "13th & 14th Month Salary"],
            "notes": "NHR regime for expats offers reduced tax rates. 13th and 14th month salaries mandatory."
        },
        {
            "name": "Spain",
            "code": "ES",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.3057,
            "employee_ss_rate": 0.0635,
            "avg_income_tax_rate": 0.19,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Social Security", "Unemployment Insurance", "Professional Training Fund", "14 Monthly Payments"],
            "notes": "14 monthly payments (extra in July and December). IRPF withholding varies 2-47% progressive."
        },
        {
            "name": "Netherlands",
            "code": "NL",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.2765,
            "employee_ss_rate": 0.2765,
            "avg_income_tax_rate": 0.24,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Welfare Act (WIA/WAO)", "Unemployment Insurance", "Health Insurance (Zvw)", "Holiday Pay (8%)"],
            "notes": "8% holiday pay mandatory. 30% ruling for skilled migrants. Box system for income tax."
        },
        {
            "name": "Ireland",
            "code": "IE",
            "currency": "EUR",
            "currency_symbol": "€",
            "exchange_rate_to_usd": 1.08,
            "employer_ss_rate": 0.1115,
            "employee_ss_rate": 0.04,
            "avg_income_tax_rate": 0.20,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["PRSI", "Pension Auto-enrolment (from 2025)", "Statutory Sick Pay", "Annual Leave (4 weeks min)"],
            "notes": "Low employer PRSI at 11.15%. USC applies to employees. Tax credits system."
        },
        {
            "name": "Canada",
            "code": "CA",
            "currency": "CAD",
            "currency_symbol": "C$",
            "exchange_rate_to_usd": 0.74,
            "employer_ss_rate": 0.0825,
            "employee_ss_rate": 0.0715,
            "avg_income_tax_rate": 0.20,
            "payroll_frequency": "bi-weekly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["CPP/QPP", "Employment Insurance", "Workers Compensation", "Provincial Health Tax"],
            "notes": "CPP2 second tier fully phased in for 2026. EI employer pays 1.4x employee rate. Provincial variations."
        },
        {
            "name": "Brazil",
            "code": "BR",
            "currency": "BRL",
            "currency_symbol": "R$",
            "exchange_rate_to_usd": 0.18,
            "employer_ss_rate": 0.20,
            "employee_ss_rate": 0.11,
            "avg_income_tax_rate": 0.15,
            "payroll_frequency": "monthly",
            "compliance_status": "attention",
            "mandatory_benefits": ["INSS", "FGTS (8%)", "13th Salary", "Vacation Bonus (1/3)", "Meal/Food Voucher"],
            "notes": "FGTS 8% deposited to worker account. 13th salary paid in two installments. Vacation bonus is 1/3 of monthly salary."
        },
        {
            "name": "India",
            "code": "IN",
            "currency": "INR",
            "currency_symbol": "₹",
            "exchange_rate_to_usd": 0.012,
            "employer_ss_rate": 0.12,
            "employee_ss_rate": 0.12,
            "avg_income_tax_rate": 0.15,
            "payroll_frequency": "monthly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["EPF (12%)", "ESI (if applicable)", "Gratuity", "Professional Tax"],
            "notes": "EPF 12% from both employer and employee (up to wage ceiling). ESI for employees earning under ₹21,000/month."
        },
        {
            "name": "Australia",
            "code": "AU",
            "currency": "AUD",
            "currency_symbol": "A$",
            "exchange_rate_to_usd": 0.66,
            "employer_ss_rate": 0.115,
            "employee_ss_rate": 0.02,
            "avg_income_tax_rate": 0.235,
            "payroll_frequency": "bi-weekly",
            "compliance_status": "compliant",
            "mandatory_benefits": ["Superannuation (11.5%)", "PAYG Withholding", "Workers Compensation", "Leave Entitlements"],
            "notes": "Superannuation guarantee 11.5% (rising to 12% by 2025). PAYG withholding for income tax. 4 weeks annual leave."
        },
    ]

    countries = []
    for c in countries_data:
        country = Country(**c)
        db.add(country)
        countries.append(country)
    db.commit()

    # Refresh to get IDs
    for c in countries:
        db.refresh(c)

    # Generate employees
    roles = ["Software Engineer", "Product Manager", "UX Designer", "Data Analyst", "DevOps Engineer", "QA Engineer", "Engineering Manager", "Sales Representative", "Customer Success", "HR Specialist"]
    departments = ["Engineering", "Product", "Design", "Data", "Operations", "Sales", "Customer Success", "People"]
    first_names = ["James", "Maria", "Chen", "Sofia", "Liam", "Emma", "Noah", "Olivia", "Aiden", "Isabella",
                   "Lucas", "Mia", "Mason", "Charlotte", "Ethan", "Amelia", "Logan", "Harper", "Oliver", "Evelyn",
                   "Elijah", "Abigail", "Jackson", "Emily", "Ava", "Alexander", "Sophia", "Daniel", "Elizabeth",
                   "William", "Camila", "Michael", "Luna", "Benjamin", "Penelope", "Henry", "Layla", "Sebastian",
                   "Chloe", "Jack", "Victoria", "Owen", "Riley", "Samuel", "Zoey", "Matthew", "Nora", "Joseph",
                   "Grace", "Leo", "Hannah", "Mateo", "Lily", "David", "Ellie", "John", "Scarlett", "Wyatt"]
    last_names = ["Smith", "Garcia", "Wang", "Silva", "Johnson", "Muller", "Brown", "Rodriguez", "Jones", "Patel",
                  "Davis", "Santos", "Wilson", "O'Brien", "Martinez", "Lopez", "Anderson", "Suzuki", "Taylor",
                  "Kim", "Thomas", "Tanaka", "Jackson", "Kowalski", "White", "Chen", "Harris", "Rossi", "Martin",
                  "Fernandez", "Thompson", "Sato", "Robinson", "Lima", "Clark", "Moreau", "Lewis", "Jansen",
                  "Lee", "Novak", "Walker", "Murphy", "Hall", "Dubois", "Allen", "Reyes", "Young", "Ivanov",
                  "Hernandez", "Koch", "King", "Meyer", "Wright", "Smit", "Green", "Singh", "Baker", "Costa"]

    employees_data = []
    # 5 employees per country
    for country in countries:
        for i in range(5):
            role = random.choice(roles)
            dept = random.choice(departments)
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            base_salary_usd = get_realistic_salary(country.code, role)
            salary_local = base_salary_usd / country.exchange_rate_to_usd
            hire_date = date(2022, random.randint(1, 12), random.randint(1, 28))

            emp = Employee(
                first_name=fname,
                last_name=lname,
                email=f"{fname.lower()}.{lname.lower()}@{country.code.lower()}payroll.example.com",
                country_id=country.id,
                role=role,
                department=dept,
                salary_local=round(salary_local, 2),
                salary_usd=round(base_salary_usd, 2),
                employment_type="full_time",
                hire_date=hire_date,
                status="active",
                tax_class=random.choice(["I", "II", "III", None]) if country.code == "DE" else None
            )
            db.add(emp)
            employees_data.append(emp)

    db.commit()
    for e in employees_data:
        db.refresh(e)

    # Generate payroll runs for Q4 2024
    months = [(10, "October"), (11, "November"), (12, "December")]
    payroll_runs = []

    for month_num, month_name in months:
        pr = PayrollRun(
            name=f"{month_name} 2024 Payroll",
            month=month_num,
            year=2024,
            status="completed",
            total_employees=len(employees_data),
            total_gross_usd=0,
            total_deductions_usd=0,
            total_net_usd=0
        )
        db.add(pr)
        db.commit()
        db.refresh(pr)

        total_gross = 0
        total_deductions = 0
        total_net = 0

        for emp in employees_data:
            country = next(c for c in countries if c.id == emp.country_id)
            gross_usd = emp.salary_usd

            # Calculate deductions
            employer_ss = gross_usd * country.employer_ss_rate
            employee_ss = gross_usd * country.employee_ss_rate
            income_tax = gross_usd * country.avg_income_tax_rate
            other = gross_usd * random.uniform(0.01, 0.04)  # Misc deductions

            total_ded = employee_ss + income_tax + other
            net_usd = gross_usd - total_ded
            gross_local = gross_usd / country.exchange_rate_to_usd
            net_local = net_usd / country.exchange_rate_to_usd

            entry = PayrollEntry(
                payroll_run_id=pr.id,
                employee_id=emp.id,
                gross_salary_local=round(gross_local, 2),
                gross_salary_usd=round(gross_usd, 2),
                employer_ss_amount=round(employer_ss, 2),
                employee_ss_amount=round(employee_ss, 2),
                income_tax_amount=round(income_tax, 2),
                other_deductions=round(other, 2),
                net_salary_local=round(net_local, 2),
                net_salary_usd=round(net_usd, 2)
            )
            db.add(entry)
            total_gross += gross_usd
            total_deductions += total_ded
            total_net += net_usd

        pr.total_gross_usd = round(total_gross, 2)
        pr.total_deductions_usd = round(total_deductions, 2)
        pr.total_net_usd = round(total_net, 2)
        db.commit()
        payroll_runs.append(pr)

    db.close()
    print(f"Seeded {len(countries)} countries, {len(employees_data)} employees, {len(payroll_runs)} payroll runs")


def get_realistic_salary(country_code: str, role: str) -> float:
    """Return realistic annual salary in USD based on country and role."""
    base_multipliers = {
        "Engineering Manager": 1.5,
        "Product Manager": 1.3,
        "Software Engineer": 1.2,
        "DevOps Engineer": 1.15,
        "Data Analyst": 1.05,
        "UX Designer": 1.1,
        "QA Engineer": 0.95,
        "Sales Representative": 0.9,
        "Customer Success": 0.85,
        "HR Specialist": 0.8,
    }
    multi = base_multipliers.get(role, 1.0)

    country_bases = {
        "US": 110000, "GB": 85000, "DE": 78000, "FR": 72000,
        "PT": 48000, "ES": 65000, "NL": 75000, "IE": 70000,
        "CA": 88000, "BR": 35000, "IN": 25000, "AU": 82000,
    }
    base = country_bases.get(country_code, 60000)
    variance = random.uniform(0.85, 1.25)
    return round(base * multi * variance / 12, 2)  # Monthly


if __name__ == "__main__":
    seed_data()
