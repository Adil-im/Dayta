import click
import os
from datetime import datetime, date
from .database import Database
import traceback

# Initialize Database
db = Database()

def validate_date(ctx ,param, value):
    ''' validate date format: DD-MM-YYYY'''     
    if value is None:
        return None
    try: 
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format")

def validate_tpe_choice(ctx, param, value):
    ''' validate TPE or NON-TPE choice'''
    if value is None:
        return None
    if value.upper() not in ['TPE', 'NON-TPE']:
        raise click.BadParameter("Must be either TPE or NON-TPE")
    return value.upper()

def validate_yes_no(ctz, param, value):
    ''' validate YES/NO choice'''
    if value is None:
        return None
    if value.upper() not in ["YES", "NO"]:
        raise click.BadParameter("Must be either YES or NO")
    return value.upper()

@click.group()
def cli() -> None:
    print("Sales Engineer's CLI tool - track business visits and customer data")
    pass
        
@cli.command()
@click.option('--visit-date','-d', callback=validate_date, help='Visit date(YYYY-MM-DD)', prompt="Visit date(YYYY-MM-DD)" )
@click.option('--company-name', '-c', help='Company name', prompt='Company name')
@click.option('--customer-address', '-a', help='Customer address')
@click.option('--location', '-l', help="Location")
@click.option('--customer-name', '-n', help='Name of customer')
@click.option('--designation', help='Customer designation')
@click.option('--contact-no', type=int, help='Company contact number')
@click.option('--email', help='Customer email ID')
@click.option('--tpe-status',callback=validate_tpe_choice, help='TPE or NON-TPE customer')
@click.option('--existing-turning', help='Existing machine [TURNING]')
@click.option('--turning-make', help='Turning machine make')
@click.option('--existing-milling', help='Existing machines [MILLING]')
@click.option('--milling-make', help='Milling machine make')
@click.option('--tpe-machines', type=int,default=0, help='TPE machines count')
@click.option('--non-tpe-machines', type=int,default=0 , help='Non-tpe machines count')
@click.option('--sector', help='Business sector')
@click.option('--opportunity', callback=validate_yes_no, help='Opportunity for new (YES/NO)')
@click.option('--business-plan', help='business plan - current FY')
@click.option('--remarks', help='General remarks')
@click.option('--load', callback=validate_yes_no, help='Load status [YES/NO]')
@click.option('--tpe-model', help='Discussed TPE model')
@click.option('--rm-remarks', help='Regional Manager remarks')
def add(visit_date, company_name, customer_address, location, customer_name, designation,
        contact_no, email, tpe_status, existing_turning, turning_make, existing_milling,
        milling_make, tpe_machines, non_tpe_machines, sector, opportunity, business_plan,
        remarks, load, tpe_model, rm_remarks):
    """Add a new visit record to the database."""
    try:
        visit_data = {
            'visit_date': visit_date,
            'company_name': company_name,
            'customer_address': customer_address,
            'location': location,
            'name_of_customer': customer_name,
            'designation': designation,
            'customer_contact_no': contact_no,
            'customer_mail_id': email,
            'tpe_or_non_tpe': tpe_status,
            'existing_machine_turning': existing_turning,
            'turning_make': turning_make,
            'existing_machines_milling': existing_milling,
            'milling_make': milling_make,
            'tpe_machines_nos': tpe_machines,
            'non_tpe_machines': non_tpe_machines,
            'sector': sector,
            'opportunity_for_new': opportunity,
            'business_plan_current_fy': business_plan,
            'remarks': remarks,
            'load_status': load,
            'discussed_tpe_model': tpe_model,
            'regional_manager_remarks': rm_remarks
        }
        
        sr_no = db.add_visit(visit_data)
        click.echo(f"✅ Visit record added successfully with Serial No: {sr_no}")
        
        # Show the added record summary
        click.echo(f"\nAdded visit record:")
        click.echo(f"Serial No: {sr_no}")
        click.echo(f"Visit Date: {visit_date}")
        click.echo(f"Company: {company_name}")
        
        if customer_name:
            click.echo(f"Customer: {customer_name}")
        if tpe_status:
            click.echo(f"Customer Type: {tpe_status}")
            
    except Exception as e:
        click.echo(f"❌ Error adding visit record: {e}", err=True)




if __name__ == '__main__':
    cli()
