# ERP Systems (Enterprise Resource Planning)

## Overview

Enterprise Resource Planning (ERP) systems integrate core business processes into unified systems that streamline operations across finance, HR, manufacturing, supply chain, and customer relationship management. This skill encompasses ERP implementation methodology, module configuration, data migration, process optimization, and ongoing system management. ERP systems serve as the operational backbone of organizations, providing single sources of truth and enabling data-driven decision making across enterprise functions.

## Core Capabilities

Financial management modules handle general ledger, accounts payable/receivable, fixed assets, and financial reporting with multi-currency and multi-entity support. Supply chain management covers procurement, inventory, order management, and logistics with demand forecasting and optimization. Human resources modules manage employee data, payroll, benefits, talent acquisition, and performance management. Manufacturing execution supports production planning, shop floor control, quality management, and maintenance scheduling.

CRM integration unifies customer data across sales, marketing, and service functions. Business intelligence and reporting provide dashboards, ad-hoc queries, and automated reporting across all modules. Workflow and approval automation streamline business processes with configurable rules and notifications. API and integration capabilities connect ERP systems with external applications, data warehouses, and third-party services.

## Usage Examples

```python
from erp_skill import ERPManager, FinanceModule, SupplyChainModule, HRModule, ReportGenerator

# Initialize ERP system
erp = ERPManager(
    system="SAP S/4HANA",  # or "Oracle ERP Cloud", "Microsoft Dynamics 365"
    instance="production",
    client_id="100"
)

# Configure organizational structure
org_structure = erp.setup_organization(
    company_code={
        "code": "US01",
        "name": "US Operations",
        "currency": "USD",
        "country": "US"
    },
    business_areas=[
        {"code": "US-NE", "name": "Northeast", "company_code": "US01"},
        {"code": "US-SE", "name": "Southeast", "company_code": "US01"},
        {"code": "US-WE", "name": "West", "company_code": "US01"}
    ],
    profit_centers=[
        {"code": "PC-001", "name": "Sales Division", "business_area": "US-NE"},
        {"code": "PC-002", "name": "Manufacturing", "business_area": "US-WE"}
    ],
    cost_centers=[
        {"code": "CC-100", "name": "IT Department", "budget": 500000, "profit_center": "PC-001"},
        {"code": "CC-200", "name": "Operations", "budget": 1000000, "profit_center": "PC-002"}
    ]
)

# Configure finance module
finance = FinanceModule(
    erp_instance=erp,
    fiscal_year_start="01-01"
)

# Set up chart of accounts
chart_of_accounts = finance.setup_chart_of_accounts(
    structure="US-GAAP",
    account_types=[
        {"type": "Asset", "range": "1000-1999"},
        {"type": "Liability", "range": "2000-2999"},
        {"type": "Equity", "range": "3000-3999"},
        {"type": "Revenue", "range": "4000-4999"},
        {"type": "Expense", "range": "5000-8999"}
    ],
    segments=["Company Code", "Business Area", "Profit Center", "Cost Center"]
)

# Create journal entry
journal_entry = finance.create_journal_entry(
    document_type="SA",  # Standard Journal Entry
    posting_date="2024-01-15",
    currency="USD",
    line_items=[
        {"account": "101000", "debit": 50000, "text": "Cash received from customer A"},
        {"account": "121000", "credit": 50000, "text": "Accounts receivable"}
    ],
    company_code="US01"
)
print(f"Journal Entry Created: {journal_entry.document_number}")
print(f"Status: {journal_entry.status}")

# Configure accounts payable
ap = finance.setup_accounts_payable(
    vendor_groups=[
        {"code": "VG-001", "name": "Domestic Suppliers"},
        {"code": "VG-002", "name": "International Suppliers"}
    ],
    payment_terms=[
        {"code": "NET30", "name": "Net 30", "days": 30},
        {"code": "NET60", "name": "Net 60", "days": 60},
        {"code": "2P10", "name": "2% 10 Net 30", "days": 30, "discount_days": 10, "discount_percent": 2}
    ]
)

# Create purchase order
po = finance.create_purchase_order(
    vendor="V-10001",
    company_code="US01",
    purchasing_organization="PO-001",
    purchasing_group="PG-001",
    items=[
        {"material": "MAT-001", "quantity": 100, "unit_price": 50, "delivery_date": "2024-02-01"},
        {"material": "MAT-002", "quantity": 50, "unit_price": 100, "delivery_date": "2024-02-01"}
    ],
    conditions=[
        {"type": "PBXX", "description": "Base Price"},
        {"type": "MWST", "description": "Sales Tax", "rate": 8.25}
    ]
)
print(f"Purchase Order Created: {po.number}")
print(f"Total Value: {po.currency} {po.total_value}")

# Configure supply chain module
supply_chain = SupplyChainModule(
    erp_instance=erp
)

# Set up material management
material_master = supply_chain.create_material_master(
    material_number="MAT-NEW-001",
    material_type="FERT",  # Finished Product
    material_description="Widget Pro X1",
    base_unit="EA",
    material_group="Electronics",
    plants=[
        {"plant": "US01", "storage_location": "WH1", "mrp_controller": "MRP01"}
    ],
    purchasing_info=[
        {"plant": "US01", "vendor": "V-10001", "standard_price": 45}
    ],
    sales_info=[
        {"sales_organization": "US01", "distribution_channel": "01", "standard_price": 79.99}
    ]
)

# Create sales order
sales_order = supply_chain.create_sales_order(
    customer="C-20001",
    sales_organization="US01",
    distribution_channel="01",
    division="01",
    items=[
        {"material": "MAT-NEW-001", "quantity": 10, "requested_date": "2024-02-15"},
        {"material": "MAT-NEW-002", "quantity": 5, "requested_date": "2024-02-15"}
    ],
    pricing=[
        {"type": "PR00", "description": "Base Price"},
        {"type": "MWST", "description": "Tax", "rate": 8.25}
    ]
)
print(f"Sales Order Created: {sales_order.number}")

# Configure HR module
hr = HRModule(
    erp_instance=erp
)

# Create employee record
employee = hr.create_employee(
    personnel_number="EMP-5001",
    first_name="John",
    last_name="Smith",
    birth_date="1985-03-15",
    hire_date="2024-01-02",
    organizational_unit="IT-DEPT",
    job_title="Software Engineer",
    pay_type="Monthly",
    salary=8500,
    employment_type="Full-Time"
)

# Configure time recording
time_record = hr.record_time(
    employee="EMP-5001",
    work_date="2024-01-15",
    hours_worked=8,
    absence_type=None,
    overtime_hours=2
)

# Generate financial reports
report_gen = ReportGenerator(
    erp_instance=erp
)

# Generate balance sheet
balance_sheet = report_gen.generate_financial_statement(
    report_type="BALANCE_SHEET",
    company_code="US01",
    fiscal_year="2024",
    period="01",
    format="PDF"
)
print(f"Balance Sheet Generated: {balance_sheet.file_path}")

# Generate P&L statement
income_statement = report_gen.generate_financial_statement(
    report_type="INCOME_STATEMENT",
    company_code="US01",
    fiscal_year="2024",
    period="01",
    compare_to_previous=True,
    format="EXCEL"
)

# Generate aged receivables report
ar_aging = report_gen.generate_aging_report(
    report_type="ACCOUNTS_RECEIVABLE",
    as_of_date="2024-01-15",
    aging_buckets=[30, 60, 90, 120],
    company_code="US01"
)
print("Aged Receivables Summary:")
for bucket, amount in ar_aging.buckets.items():
    print(f"  {bucket}: ${amount:,.2f}")
print(f"Total Outstanding: ${ar_aging.total:,.2f}")

# Export data for data warehouse
data_export = erp.export_data(
    tables=[
        {"table": "BKPF", "fields": ["BUKRS", "BELNR", "GJAHR", "BLART", "BLDAT"], "filters": [{"field": "GJAHR", "operator": "=", "value": "2024"}]},
        {"table": "BSEG", "fields": ["BUKRS", "BELNR", "BUZEI", "SAKNR", "DMBTR"], "filters": [{"field": "GJAHR", "operator": "=", "value": "2024"}]},
        {"table": "MARA", "fields": ["MATNR", "MTART", "MBRSH", "MATKL"], "filters": []},
        {"table": "MSEG", "fields": ["MATNR", "WERKS", "LGORT", "MENGE", "MEINS"], "filters": [{"field": "GJAHR", "operator": "=", "value": "2024"}]}
    ],
    format="PARQUET",
    target_path="/datawarehouse/staging/erp/"
)
print(f"Data Export Complete: {data_export.tables_exported} tables exported")
```

## Best Practices

Begin ERP implementations with thorough process discovery and requirements gathering, documenting current state workflows and defining future state processes before configuration. Adopt a phased implementation approach, going live with core modules first and adding complexity incrementally. Invest heavily in data quality and cleansing before migration, as poor data undermines system value.

Design organizational structures and chart of accounts to support both operational needs and financial reporting requirements. Implement robust change management and training programs to drive user adoption. Establish clear governance with defined roles for business process owners, technical administrators, and auditors. Plan for ongoing optimization and enhancements, treating ERP implementations as continuous improvement programs rather than one-time projects.

## Related Skills

- Business Intelligence (reporting and analytics)
- Data Warehousing (enterprise data management)
- Project Management (implementation methodology)
- Database Management (ERP database optimization)

## Use Cases

Manufacturing companies use ERP to coordinate production planning, inventory management, and order fulfillment. Retail organizations integrate POS, inventory, and financial data for unified merchandise planning. Service companies manage projects, resources, and billing through ERP professional services modules. Healthcare organizations leverage ERP for supply chain, financial management, and compliance reporting.
