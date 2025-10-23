"""
Database module for Smart Public Complaint Box
Handles database initialization, schema creation, and connection management
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import os


class Database:
    """Database manager for the complaint management system"""
    
    def __init__(self, db_path: str = "complaint_system.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def initialize_schema(self):
        """Create all required tables"""
        self.connect()
        
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'citizen',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Categories table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)
        
        # Departments table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                email TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        """)
        
        # Complaints table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT,
                category_id INTEGER,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Submitted',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        """)
        
        # Assignments table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_id INTEGER NOT NULL,
                department_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id),
                FOREIGN KEY (department_id) REFERENCES departments(department_id)
            )
        """)
        
        # Attachments table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attachments (
                attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id)
            )
        """)
        
        self.conn.commit()
        print("Database schema initialized successfully")
        
    def seed_data(self):
        """Insert initial data for categories and departments"""
        self.connect()
        
        # Insert categories
        categories = [
            ('Water Supply', 'Issues related to water supply, quality, and availability'),
            ('Road Maintenance', 'Potholes, damaged roads, and street lighting'),
            ('Electricity', 'Power cuts, voltage fluctuations, and electrical hazards'),
            ('Sanitation', 'Garbage collection, drainage, and cleanliness'),
            ('Other', 'Miscellaneous issues not covered in other categories')
        ]
        
        for cat in categories:
            try:
                self.cursor.execute(
                    "INSERT INTO categories (name, description) VALUES (?, ?)", 
                    cat
                )
            except sqlite3.IntegrityError:
                pass  # Category already exists
        
        # Insert departments
        departments = [
            ('Water Department', 1, 'water@example.com'),
            ('Public Works Department', 2, 'pwd@example.com'),
            ('Electricity Board', 3, 'electricity@example.com'),
            ('Sanitation Department', 4, 'sanitation@example.com'),
            ('General Administration', 5, 'admin@example.com')
        ]
        
        for dept in departments:
            try:
                self.cursor.execute(
                    "INSERT INTO departments (name, category_id, email) VALUES (?, ?, ?)",
                    dept
                )
            except sqlite3.IntegrityError:
                pass  # Department already exists
        
        self.conn.commit()
        print("Seed data inserted successfully")
        
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        self.connect()
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return last row id"""
        self.connect()
        self.cursor.execute(query, params)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        self.close()
        return last_id


if __name__ == "__main__":
    # Initialize database
    db = Database("/home/ubuntu/complaint_system/data/complaint_system.db")
    db.initialize_schema()
    db.seed_data()
    db.close()

