import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        # Initialize the DB with required tables.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS visits(
                    sr_no INTEGER PRIMARY KEY AUTOINCREMENT,     
                    visit_date DATE NOT NULL,
                    company_name TEXT NOT NULL,
                    customer_address TEXT,
                    location TEXT,
                    name_of_customer TEXT,
                    designation TEXT,
                    customer_contact_no INTEGER,
                    customer_mail_id TEXT,
                    tpe_or_non_tpe TEXT CHECK(tpe_or_non_tpe IN ('TPE', 'NON-TPE')),
                    existing_machine_turning TEXT,
                    turning_make TEXT,
                    existing_machines_milling TEXT,
                    milling_make TEXT,
                    tpe_machines_nos INTEGER DEFAULT 0,
                    non_tpe_machines INTEGER DEFAULT 0,
                    sector TEXT,
                    opportunity_for_new TEXT CHECK(opportunity_for_new IN ('YES', 'NO')),
                    business_plan_current_fy TEXT,
                    remarks TEXT,
                    load_status TEXT CHECK(load_status IN ('YES', 'NO')),
                    discussed_tpe_model TEXT,
                    regional_manager_remarks TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) 
            """)
            conn.commit()

    def add_visit(self,visit_data: Dict[str, Any]) -> int:
         """Add a new visit record to the database."""
         with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visits (
                    visit_date, company_name, customer_address, location, name_of_customer,
                    designation, customer_contact_no, customer_mail_id, tpe_or_non_tpe,
                    existing_machine_turning, turning_make, existing_machines_milling, milling_make,
                    tpe_machines_nos, non_tpe_machines, sector, opportunity_for_new,
                    business_plan_current_fy, remarks, load_status, discussed_tpe_model,
                    regional_manager_remarks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                visit_data.get('visit_date'),
                visit_data.get('company_name'),
                visit_data.get('customer_address'),
                visit_data.get('location'),
                visit_data.get('name_of_customer'),
                visit_data.get('designation'),
                visit_data.get('customer_contact_no'),
                visit_data.get('customer_mail_id'),
                visit_data.get('tpe_or_non_tpe'),
                visit_data.get('existing_machine_turning'),
                visit_data.get('turning_make'),
                visit_data.get('existing_machines_milling'),
                visit_data.get('milling_make'),
                visit_data.get('tpe_machines_nos', 0),
                visit_data.get('non_tpe_machines', 0),
                visit_data.get('sector'),
                visit_data.get('opportunity_for_new'),
                visit_data.get('business_plan_current_fy'),
                visit_data.get('remarks'),
                visit_data.get('load_status'),
                visit_data.get('discussed_tpe_model'),
                visit_data.get('regional_manager_remarks')
            ))
            conn.commit()
            return cursor.lastrowid

    def update_visit(self, sr_no: int, visit_data: Dict[str, Any]) -> bool:
            """Update an existing visit record."""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query based on provided data
                update_fields = []
                values = []
                
                field_mapping = {
                    'visit_date': 'visit_date',
                    'company_name': 'company_name',
                    'customer_address': 'customer_address',
                    'location': 'location',
                    'name_of_customer': 'name_of_customer',
                    'designation': 'designation',
                    'customer_contact_no': 'customer_contact_no',
                    'customer_mail_id': 'customer_mail_id',
                    'tpe_or_non_tpe': 'tpe_or_non_tpe',
                    'existing_machine_turning': 'existing_machine_turning',
                    'turning_make': 'turning_make',
                    'existing_machines_milling': 'existing_machines_milling',
                    'milling_make': 'milling_make',
                    'tpe_machines_nos': 'tpe_machines_nos',
                    'non_tpe_machines': 'non_tpe_machines',
                    'sector': 'sector',
                    'opportunity_for_new': 'opportunity_for_new',
                    'business_plan_current_fy': 'business_plan_current_fy',
                    'remarks': 'remarks',
                    'load_status': 'load_status',
                    'discussed_tpe_model': 'discussed_tpe_model',
                    'regional_manager_remarks': 'regional_manager_remarks'
                }
                
                for key, value in visit_data.items():
                    if key in field_mapping and value is not None:
                        update_fields.append(f"{field_mapping[key]} = ?")
                        values.append(value)
                
                if not update_fields:
                    return False
                
                # Add updated_at timestamp
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                values.append(sr_no)
                
                query = f"UPDATE visits SET {', '.join(update_fields)} WHERE sr_no = ?"
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
                

    def get_visit_by_id(self, sr_no: int) -> Optional[Dict[str, Any]]:
        """Get a specific visit by serial number. """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM visits WHERE sr.no = ? ", (sr_no))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_visits(self) -> List[Dict[str, Any]]:
        """Retrieve all visit records from the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM visits ORDER BY visit_date DESC, sr_no DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_visits_by_month(self,year:int,month:int) -> List[Dict[str, Any]]:
        "Retrieve visits for a specific month and year"        
        with sqlite3.connect(self.db_path) as conn: 
            conn.row_factory =  sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM visits 
            WHERE strftime('%Y', visit_date) = ? AND strftime(''%m', visit_date) = ?
            ORDER BY visit_date DESC, sr_no DESC       
           """, (str(year), f"{month:02d}"))
            return[dict(row) for row in cursor.fetchall()]

           








    
   
