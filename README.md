# Task 1: Custom Stock Ledger Report

## Overview
Created a custom stock ledger report in ERPNext that tracks item inventory movements with detailed purchase information and provides Excel export functionality.

## Features Implemented

### 1. Report Columns
The report includes the following columns:
- Item Name & Code: Basic item identification
- Valuation Rate: Current item valuation
- Last Purchase Rate: Most recent purchase price
- Purchase Information:
  - Purchase Order (PO) reference
  - Purchase Receipt (PR) number
  - Purchase Invoice (PI) number
- Quantity Tracking:
  - Balance Quantity: Current stock level
  - In-Quantity: Stock additions
  - Out-Quantity: Stock deductions

### 2. Filters Implementation
Key filters include:
- Company (required): Filters by organization
- Date Range (required): From and To dates for transaction period
- Warehouse: Optional filter for specific warehouse
- Item: Optional filter for specific items

### 3. Excel Export Functionality
Implemented a custom Excel export button with the following features:
- Creates an Excel workbook with formatted columns
- Handles data conversion and formatting:
  - Currency formatting for rates
  - Number formatting for quantities
  - Proper alignment and borders
- Error handling for empty datasets
- Base64 encoding for secure file transfer

### 4. Report Integration
- Added report shortcut to Stock Workspace for easy access
## Technical Implementation

### Backend (Python)
Added all function for get columns and rows and also added function for download Excel 


### Frontend (JavaScript)
javascript
IN frontend added button which call the function of python download report

## Usage
1. Navigate to Stock module
2. Click on "Custom Stock Ledger" in the workspace
3. Set desired filters (Company and Date range are required)
4. Click "Download Excel Report" for Excel export

## Technical Notes
- Uses proper table aliases to avoid column ambiguity
- Implements server-side Excel generation for better performance
- Includes error handling for both server and client side
- Maintains consistent formatting in Excel output




# Task 2:  Manual Workflow Documentation
      ** Manual Workflow Documentation ** - https://docs.google.com/document/d/1XXJ20aSZibK4a6Trp8oQmoW3CWhTh_N5cZIqZpTdyS8/edit?tab=t.2qfm2k1r7j96

      
# Task 3: Production and Manufacturing Workflow
Features
**Workflows for Work Order**

Defines the stages of the Work Order lifecycle:
Draft: Editable by the Production Planner.
Pending Material: Verified by the Store Manager.
Material Ready: Materials prepared by the Store Manager.
In Production: Managed by the Production Supervisor.
Quality Check: Inspected by the Quality Manager.
Completed: Final state after production.
Includes transitions such as:
Submit: Moves the state from Draft to Pending Material.
Material Verified: Marks the materials as ready.
Start Production: Begins the production process.
Complete Production: Marks production as complete.
Quality Approved: Approves the quality check.
Workflows for Job Card

**Defines operational stages:**
Draft: Created by the Production Supervisor.
Material Requested: Materials requested by the operator.
In Progress: Work is ongoing.
Completed: Work is finished.
Includes transitions such as:
Request Material: Transitions to Material Requested.
Start Operation: Moves to In Progress.
Complete: Marks the job card as completed.
Workflow Actions

Predefined actions such as Submit, Material Verified, Start Production, and Complete Production.
Automatically set up in the Workflow Action Master Doctype.
How It Works
Setup Workflow Actions

Ensures all necessary workflow actions are created if not already present.
Create Workflows

Deletes any existing workflows with the same name to avoid duplication.
Creates and inserts workflows for Work Order and Job Card with defined states, transitions, and roles.
Customization

Easily extendable to add more workflows or modify existing ones as per business needs.
Usage
Add the Python script to your custom app, e.g., apps/custom_tasks/custom_tasks/manufacturing_workflow.py.
Run the script in the Frappe/ERPNext environment:
bash
Copy code
**bench execute custom_tasks.manufacturing_workflow.execute**

The workflows will be created and added to the Workflow List in ERPNext.
Example Workflow: Work Order
A Work Order is created by the Production Planner in the Draft state.
The Store Manager verifies materials, transitioning it to Material Ready.
The Production Supervisor starts production, moving the state to In Production.
Once production is complete, it moves to Quality Check, managed by the Quality Manager.
The Work Order is marked as Completed after a successful quality check.

# Task 4: Purchase Funnel

in this task i have used a custom api which give the purchase reletaed data of the suppier and using the script i create the charts but as previously i havent worked on this charts so it gave 
some errors 


      
