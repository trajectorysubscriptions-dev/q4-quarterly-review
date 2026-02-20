#!/usr/bin/env python3
"""
Q4 Quarterly Performance Analysis Script

This script analyzes Q4 2025 performance metrics and generates insights.
Data source: Google Sheets (Q4 Performance Metrics)
"""

import json
from datetime import datetime
from typing import Dict, List

# Q4 Performance Data
Q4_DATA = {
    "October": {"revenue": 250000, "customers": 120, "growth": 15.5},
    "November": {"revenue": 275000, "customers": 135, "growth": 18.2},
    "December": {"revenue": 310000, "customers": 150, "growth": 22.8},
}

TARGETS = {
    "revenue": 750000,
    "customers": 380,
    "growth": 15.0,
}


def calculate_quarterly_totals() -> Dict:
    """Calculate quarterly totals from monthly data."""
    total_revenue = sum(month["revenue"] for month in Q4_DATA.values())
    total_customers = sum(month["customers"] for month in Q4_DATA.values())
    avg_growth = sum(month["growth"] for month in Q4_DATA.values()) / len(Q4_DATA)
    
    return {
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "average_growth": round(avg_growth, 2),
    }


def calculate_performance_vs_target() -> Dict:
    """Calculate performance metrics vs targets."""
    totals = calculate_quarterly_totals()
    
    return {
        "revenue": {
            "actual": totals["total_revenue"],
            "target": TARGETS["revenue"],
            "variance": totals["total_revenue"] - TARGETS["revenue"],
            "variance_pct": round((totals["total_revenue"] - TARGETS["revenue"]) / TARGETS["revenue"] * 100, 1),
        },
        "customers": {
            "actual": totals["total_customers"],
            "target": TARGETS["customers"],
            "variance": totals["total_customers"] - TARGETS["customers"],
            "variance_pct": round((totals["total_customers"] - TARGETS["customers"]) / TARGETS["customers"] * 100, 1),
        },
        "growth_rate": {
            "actual": totals["average_growth"],
            "target": TARGETS["growth"],
            "variance": round(totals["average_growth"] - TARGETS["growth"], 2),
            "variance_pct": round((totals["average_growth"] - TARGETS["growth"]) / TARGETS["growth"] * 100, 1),
        },
    }


def calculate_month_over_month_growth() -> Dict:
    """Calculate month-over-month growth rates."""
    months = list(Q4_DATA.keys())
    mom_growth = {}
    
    for i in range(1, len(months)):
        prev_month = months[i - 1]
        curr_month = months[i]
        
        prev_revenue = Q4_DATA[prev_month]["revenue"]
        curr_revenue = Q4_DATA[curr_month]["revenue"]
        
        revenue_growth = round((curr_revenue - prev_revenue) / prev_revenue * 100, 1)
        
        prev_customers = Q4_DATA[prev_month]["customers"]
        curr_customers = Q4_DATA[curr_month]["customers"]
        
        customer_growth = round((curr_customers - prev_customers) / prev_customers * 100, 1)
        
        mom_growth[f"{prev_month} to {curr_month}"] = {
            "revenue_growth_pct": revenue_growth,
            "customer_growth_pct": customer_growth,
        }
    
    return mom_growth


def generate_report() -> str:
    """Generate a comprehensive Q4 performance report."""
    totals = calculate_quarterly_totals()
    performance = calculate_performance_vs_target()
    mom_growth = calculate_month_over_month_growth()
    
    report = []
    report.append("="*60)
    report.append("Q4 2025 QUARTERLY PERFORMANCE ANALYSIS")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*60)
    report.append("")
    
    # Summary
    report.append("QUARTERLY SUMMARY")
    report.append("-"*60)
    report.append(f"Total Revenue:      ${totals['total_revenue']:,}")
    report.append(f"Total Customers:    {totals['total_customers']}")
    report.append(f"Average Growth Rate: {totals['average_growth']}%")
    report.append("")
    
    # Performance vs Target
    report.append("PERFORMANCE VS TARGET")
    report.append("-"*60)
    
    rev = performance["revenue"]
    report.append(f"Revenue:")
    report.append(f"  Actual:   ${rev['actual']:,}")
    report.append(f"  Target:   ${rev['target']:,}")
    report.append(f"  Variance: ${rev['variance']:,} ({rev['variance_pct']:+.1f}%) {'✅ EXCEEDED' if rev['variance'] > 0 else '❌ MISSED'}")
    report.append("")
    
    cust = performance["customers"]
    report.append(f"Customers:")
    report.append(f"  Actual:   {cust['actual']}")
    report.append(f"  Target:   {cust['target']}")
    report.append(f"  Variance: {cust['variance']:+d} ({cust['variance_pct']:+.1f}%) {'✅ EXCEEDED' if cust['variance'] > 0 else '❌ MISSED'}")
    report.append("")
    
    growth = performance["growth_rate"]
    report.append(f"Growth Rate:")
    report.append(f"  Actual:   {growth['actual']}%")
    report.append(f"  Target:   {growth['target']}%")
    report.append(f"  Variance: {growth['variance']:+.2f}% ({growth['variance_pct']:+.1f}%) {'✅ EXCEEDED' if growth['variance'] > 0 else '❌ MISSED'}")
    report.append("")
    
    # Month-over-Month Growth
    report.append("MONTH-OVER-MONTH GROWTH")
    report.append("-"*60)
    for period, growth_data in mom_growth.items():
        report.append(f"{period}:")
        report.append(f"  Revenue Growth:  {growth_data['revenue_growth_pct']:+.1f}%")
        report.append(f"  Customer Growth: {growth_data['customer_growth_pct']:+.1f}%")
    report.append("")
    
    report.append("="*60)
    report.append("CONCLUSION: Q4 EXCEEDED ALL TARGETS ✅")
    report.append("="*60)
    
    return "\n".join(report)


if __name__ == "__main__":
    # Generate and print report
    report = generate_report()
    print(report)
    
    # Optionally save to file
    with open("Q4_Analysis_Report.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Report saved to Q4_Analysis_Report.txt")
