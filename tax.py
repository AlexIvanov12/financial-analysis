import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'sqlite:///finance.db'  # Приклад для SQLite
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    annual_income = Column(Float)
    federal_tax = Column(Float)
    provincial_tax = Column(Float)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def calculate_taxes(name, annual_income, province):
    federal_tax_rate = 0.15
    federal_tax = annual_income * federal_tax_rate
    #provincial tax
    provincial_tax_rate = 0.10 if province == 'Ontario' else 0.08
    provincial_tax = annual_income * provincial_tax_rate
    #save information in basedata
    employee = Employee(name = name, annual_income = annual_income, federal_tax = federal_tax, provincial_tax = provincial_tax)
    session.add(employee)
    session.commit()
    return federal_tax, provincial_tax

# Приклад використання
name = "John Doe"
annual_income = 50000  # Припустимо дохід 50,000
province = "Ontario"
federal_tax, provincial_tax = calculate_taxes(name, annual_income, province)
print(f"Federal Tax: ${federal_tax}, Provincial Tax: ${provincial_tax}")
