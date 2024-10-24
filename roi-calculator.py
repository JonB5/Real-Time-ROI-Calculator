import numpy_financial as npf
from datetime import datetime, timedelta

class ROICalculator:
    def __init__(self):
        self.purchase_price = 0
        self.down_payment = 0
        self.closing_costs = 0
        self.property_taxes = 0
        self.insurance = 0
        
        # Additional parameters needed for calculations
        self.monthly_rent = 0
        self.monthly_expenses = 0
        self.loan_term_years = 30
        self.interest_rate = 0.04  # 4% default interest rate
        self.appreciation_rate = 0.03  # 3% default appreciation rate
        
    def get_manual_inputs(self):
        """Get inputs manually from user"""
        self.purchase_price = float(input("Enter purchase price: $"))
        self.down_payment = float(input("Enter down payment: $"))
        self.closing_costs = float(input("Enter closing costs: $"))
        self.property_taxes = float(input("Enter annual property taxes: $"))
        self.insurance = float(input("Enter annual insurance: $"))
        self.monthly_rent = float(input("Enter expected monthly rent: $"))
        self.monthly_expenses = float(input("Enter expected monthly expenses (maintenance, vacancy, etc.): $"))
        
    def calculate_mortgage_payment(self):
        """Calculate monthly mortgage payment"""
        loan_amount = self.purchase_price - self.down_payment
        monthly_rate = self.interest_rate / 12
        num_payments = self.loan_term_years * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
            
        return npf.pmt(monthly_rate, num_payments, -loan_amount)
        
    def calculate_net_profit(self, years=1):
        """Calculate net profit over specified number of years"""
        monthly_mortgage = self.calculate_mortgage_payment()
        monthly_cash_flow = (
            self.monthly_rent - 
            monthly_mortgage - 
            (self.property_taxes / 12) - 
            (self.insurance / 12) - 
            self.monthly_expenses
        )
        
        # Calculate appreciation
        future_value = self.purchase_price * (1 + self.appreciation_rate)**years
        equity_gained = future_value - self.purchase_price
        
        # Calculate principal paid down
        total_mortgage_paid = monthly_mortgage * 12 * years
        initial_loan = self.purchase_price - self.down_payment
        remaining_loan = initial_loan * (1 + self.interest_rate)**years - total_mortgage_paid
        principal_paid = initial_loan - remaining_loan
        
        return (monthly_cash_flow * 12 * years) + equity_gained + principal_paid
        
    def calculate_roi(self, years=1):
        """Calculate annualized ROI"""
        total_investment = self.down_payment + self.closing_costs
        net_profit = self.calculate_net_profit(years)
        
        total_roi = (net_profit / total_investment) * 100
        annualized_roi = ((1 + total_roi/100)**(1/years) - 1) * 100
        
        return annualized_roi
        
    def calculate_cash_on_cash(self):
        """Calculate cash-on-cash return"""
        total_investment = self.down_payment + self.closing_costs
        annual_cash_flow = (
            (self.monthly_rent - self.calculate_mortgage_payment() - 
             (self.property_taxes / 12) - (self.insurance / 12) - 
             self.monthly_expenses) * 12
        )
        
        return (annual_cash_flow / total_investment) * 100
        
    def calculate_breakeven(self):
        """Calculate break-even point in years"""
        total_investment = self.down_payment + self.closing_costs
        annual_cash_flow = (
            (self.monthly_rent - self.calculate_mortgage_payment() - 
             (self.property_taxes / 12) - (self.insurance / 12) - 
             self.monthly_expenses) * 12
        )
        
        if annual_cash_flow <= 0:
            return float('inf')
            
        return total_investment / annual_cash_flow
        
    def calculate_irr(self, years=10):
        """Calculate internal rate of return"""
        cash_flows = [-1 * (self.down_payment + self.closing_costs)]  # Initial investment
        
        monthly_mortgage = self.calculate_mortgage_payment()
        monthly_cash_flow = (
            self.monthly_rent - 
            monthly_mortgage - 
            (self.property_taxes / 12) - 
            (self.insurance / 12) - 
            self.monthly_expenses
        )
        
        # Add annual cash flows
        for year in range(years):
            cash_flows.append(monthly_cash_flow * 12)
            
        # Add final year with property sale
        final_value = self.purchase_price * (1 + self.appreciation_rate)**years
        cash_flows[-1] += final_value
        
        # Calculate IRR
        try:
            irr = npf.irr(cash_flows)
            return float(irr) * 100 if irr is not None else None
        except:
            return None
            
    def generate_report(self):
        """Generate comprehensive investment report"""
        net_profit_1yr = self.calculate_net_profit(1)
        net_profit_5yr = self.calculate_net_profit(5)
        roi_1yr = self.calculate_roi(1)
        roi_5yr = self.calculate_roi(5)
        coc = self.calculate_cash_on_cash()
        breakeven = self.calculate_breakeven()
        irr = self.calculate_irr()
        
        irr_text = f"{irr:.2f}%" if irr is not None else "Not calculable"
        
        report = f"""
Real Estate Investment Analysis Report
====================================

Investment Details:
-----------------
Purchase Price: ${self.purchase_price:,.2f}
Down Payment: ${self.down_payment:,.2f}
Closing Costs: ${self.closing_costs:,.2f}
Property Taxes: ${self.property_taxes:,.2f}/year
Insurance: ${self.insurance:,.2f}/year

Monthly Cash Flow Analysis:
-------------------------
Monthly Rent: ${self.monthly_rent:,.2f}
Monthly Mortgage: ${self.calculate_mortgage_payment():,.2f}
Monthly Expenses: ${self.monthly_expenses:,.2f}
Net Monthly Cash Flow: ${(self.monthly_rent - self.calculate_mortgage_payment() - (self.property_taxes/12) - (self.insurance/12) - self.monthly_expenses):,.2f}

Performance Metrics:
------------------
Net Profit (1 year): ${net_profit_1yr:,.2f}
Net Profit (5 years): ${net_profit_5yr:,.2f}
Annualized ROI (1 year): {roi_1yr:.2f}%
Annualized ROI (5 years): {roi_5yr:.2f}%
Cash-on-Cash Return: {coc:.2f}%
Break-even Point: {breakeven:.1f} years
Internal Rate of Return (10 years): {irr_text}
"""
        return report

def main():
    calculator = ROICalculator()
    calculator.get_manual_inputs()
    print(calculator.generate_report())

if __name__ == "__main__":
    main()
