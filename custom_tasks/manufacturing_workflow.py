# File: apps/custom_tasks/custom_tasks/manufacturing_workflow.py

import frappe

def execute():
    """Main function to create manufacturing workflows"""
    setup_workflow_actions()
    create_manufacturing_workflows()
    
def create_manufacturing_workflows():
    """Create workflows for Work Order and Job Card"""
    
    # Work Order Workflow States
    work_order_states = [
        {
            'state': 'Draft',
            'doc_status': 0,
            'allow_edit': 'Production Planner'
        },
        {
            'state': 'Pending Material',
            'doc_status': 1,
            'allow_edit': 'Store Manager'
        },
        {
            'state': 'Material Ready',
            'doc_status': 1,
            'allow_edit': 'Store Manager'
        },
        {
            'state': 'In Production',
            'doc_status': 1,
            'allow_edit': 'Production Supervisor'
        },
        {
            'state': 'Quality Check',
            'doc_status': 1,
            'allow_edit': 'Quality Manager'
        },
        {
            'state': 'Completed',
            'doc_status': 1,
            'allow_edit': 'Production Manager'
        }
    ]

    # Work Order Transitions
    work_order_transitions = [
        {
            'state': 'Draft',
            'action': 'Submit',
            'next_state': 'Pending Material',
            'allowed': 'Production Planner',
            'allow_self_approval': 1
        },
        {
            'state': 'Pending Material',
            'action': 'Material Verified',
            'next_state': 'Material Ready',
            'allowed': 'Store Manager',
            'allow_self_approval': 1
        },
        {
            'state': 'Material Ready',
            'action': 'Start Production',
            'next_state': 'In Production',
            'allowed': 'Production Supervisor',
            'allow_self_approval': 1
        },
        {
            'state': 'In Production',
            'action': 'Complete Production',
            'next_state': 'Quality Check',
            'allowed': 'Production Supervisor',
            'allow_self_approval': 1
        },
        {
            'state': 'Quality Check',
            'action': 'Quality Approved',
            'next_state': 'Completed',
            'allowed': 'Quality Manager',
            'allow_self_approval': 1
        }
    ]

    create_workflow('Work Order Process', 'Work Order', work_order_states, work_order_transitions)

    # Job Card States
    job_card_states = [
        {
            'state': 'Draft',
            'doc_status': 0,
            'allow_edit': 'Production Supervisor'
        },
        {
            'state': 'Material Requested',
            'doc_status': 1,
            'allow_edit': 'Store Manager'
        },
        {
            'state': 'In Progress',
            'doc_status': 1,
            'allow_edit': 'Production Operator'
        },
        {
            'state': 'Completed',
            'doc_status': 1,
            'allow_edit': 'Production Supervisor'
        }
    ]

    # Job Card Transitions
    job_card_transitions = [
        {
            'state': 'Draft',
            'action': 'Request Material',
            'next_state': 'Material Requested',
            'allowed': 'Production Supervisor',
            'allow_self_approval': 1
        },
        {
            'state': 'Material Requested',
            'action': 'Start Operation',
            'next_state': 'In Progress',
            'allowed': 'Production Operator',
            'allow_self_approval': 1
        },
        {
            'state': 'In Progress',
            'action': 'Complete',
            'next_state': 'Completed',
            'allowed': 'Production Supervisor',
            'allow_self_approval': 1
        }
    ]

    create_workflow('Job Card Process', 'Job Card', job_card_states, job_card_transitions)

def create_workflow(workflow_name, doc_type, states, transitions):
    """Create a new workflow with specified states and transitions"""
    try:
        # Delete existing workflow if it exists
        if frappe.db.exists('Workflow', workflow_name):
            frappe.delete_doc('Workflow', workflow_name, force=True)
            frappe.db.commit()

        # Create workflow states first
        states_list = []
        for state in states:
            state_doc = frappe.new_doc('Workflow State')
            state_doc.workflow_state_name = state['state']
            state_doc.style = ''
            if not frappe.db.exists('Workflow State', state['state']):
                state_doc.insert(ignore_permissions=True)
            states_list.append(state_doc.name)

        # Create workflow actions
        actions_list = []
        for transition in transitions:
            action_doc = frappe.new_doc('Workflow Action Master')
            action_doc.workflow_action_name = transition['action']
            if not frappe.db.exists('Workflow Action Master', transition['action']):
                action_doc.insert(ignore_permissions=True)
            actions_list.append(action_doc.name)

        # Create new workflow
        workflow = frappe.new_doc('Workflow')
        workflow.workflow_name = workflow_name
        workflow.document_type = doc_type
        workflow.is_active = 1
        workflow.send_email_alert = 1

        # Add states to workflow
        for state in states:
            workflow.append('states', {
                'state': state['state'],
                'doc_status': state['doc_status'],
                'allow_edit': state['allow_edit']
            })

        # Add transitions to workflow
        for transition in transitions:
            workflow.append('transitions', {
                'state': transition['state'],
                'action': transition['action'],
                'next_state': transition['next_state'],
                'allowed': transition['allowed'],
                'allow_self_approval': transition['allow_self_approval']
            })

        workflow.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Successfully created workflow: {workflow_name}")
        
    except Exception as e:
        print(f"Error creating workflow {workflow_name}: {str(e)}")
        frappe.db.rollback()

def setup_workflow_actions():
    """Setup workflow actions"""
    try:
        actions = [
            "Submit", "Material Verified", "Start Production",
            "Complete Production", "Quality Approved", "Request Material",
            "Start Operation", "Complete"
        ]
        
        for action in actions:
            if not frappe.db.exists('Workflow Action Master', action):
                wam = frappe.new_doc('Workflow Action Master')
                wam.workflow_action_name = action
                wam.insert(ignore_permissions=True)
                
        frappe.db.commit()
        print("Successfully created workflow actions")
        
    except Exception as e:
        print(f"Error setting up workflow actions: {str(e)}")
        frappe.db.rollback()