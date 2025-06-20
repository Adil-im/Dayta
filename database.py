import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        # Initialize the DB with required tables.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(""" CREATE TABLE IF NOT 
                EXISTS records(
                    sr.no INTEGER PRIMARY KEY AUTOINCREMENT,     
                    visit_date DATE NOT NULL,
                    company_name TEXT NOT NULL
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
                ) """)
            conn.commit()

    
    
