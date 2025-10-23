"""
Complaint Management Service
Handles all complaint-related operations
"""

import sys
import os
sys.path.append('/home/ubuntu/complaint_system')

from backend.database import Database
from models.complaint_classifier import ComplaintClassifier
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class ComplaintService:
    """Service for managing complaints"""
    
    def __init__(self, db_path: str, model_path: str):
        """Initialize the complaint service"""
        self.db = Database(db_path)
        self.classifier = ComplaintClassifier(model_path)
        
        # Load or train the model
        if os.path.exists(model_path):
            self.classifier.load_model()
        else:
            print("Training new model...")
            self.classifier.train(save_model=True)
    
    def register_user(self, name: str, email: str, password: str, role: str = 'citizen') -> int:
        """Register a new user"""
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        query = """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """
        try:
            user_id = self.db.execute_update(query, (name, email, password_hash, role))
            print(f"User registered successfully with ID: {user_id}")
            return user_id
        except Exception as e:
            print(f"Error registering user: {e}")
            return -1
    
    def submit_complaint(self, user_id: int, title: str, description: str, 
                        location: str = None) -> Dict[str, Any]:
        """Submit a new complaint with AI categorization"""
        
        # Use AI to categorize the complaint
        category_name, confidence = self.classifier.predict(description)
        priority = self.classifier.predict_priority(description, category_name)
        
        # Get category ID
        category_query = "SELECT category_id FROM categories WHERE name = ?"
        categories = self.db.execute_query(category_query, (category_name,))
        
        if not categories:
            category_id = None
        else:
            category_id = categories[0]['category_id']
        
        # Insert complaint
        complaint_query = """
            INSERT INTO complaints 
            (user_id, title, description, location, category_id, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Submitted')
        """
        
        complaint_id = self.db.execute_update(
            complaint_query,
            (user_id, title, description, location, category_id, priority)
        )
        
        # Auto-assign to department
        if category_id:
            dept_query = "SELECT department_id FROM departments WHERE category_id = ?"
            departments = self.db.execute_query(dept_query, (category_id,))
            
            if departments:
                dept_id = departments[0]['department_id']
                assign_query = """
                    INSERT INTO assignments (complaint_id, department_id)
                    VALUES (?, ?)
                """
                self.db.execute_update(assign_query, (complaint_id, dept_id))
        
        return {
            'complaint_id': complaint_id,
            'category': category_name,
            'priority': priority,
            'confidence': confidence,
            'status': 'Submitted'
        }
    
    def get_complaint_details(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve details of a specific complaint"""
        query = """
            SELECT 
                c.complaint_id,
                c.title,
                c.description,
                c.location,
                cat.name as category,
                c.priority,
                c.status,
                c.created_at,
                c.updated_at,
                u.name as user_name,
                u.email as user_email
            FROM complaints c
            LEFT JOIN categories cat ON c.category_id = cat.category_id
            LEFT JOIN users u ON c.user_id = u.user_id
            WHERE c.complaint_id = ?
        """
        
        results = self.db.execute_query(query, (complaint_id,))
        return results[0] if results else None
    
    def get_user_complaints(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all complaints submitted by a user"""
        query = """
            SELECT 
                c.complaint_id,
                c.title,
                cat.name as category,
                c.priority,
                c.status,
                c.created_at
            FROM complaints c
            LEFT JOIN categories cat ON c.category_id = cat.category_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        """
        
        return self.db.execute_query(query, (user_id,))
    
    def update_complaint_status(self, complaint_id: int, new_status: str) -> bool:
        """Update the status of a complaint"""
        query = """
            UPDATE complaints 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE complaint_id = ?
        """
        
        try:
            self.db.execute_update(query, (new_status, complaint_id))
            print(f"Complaint {complaint_id} status updated to {new_status}")
            return True
        except Exception as e:
            print(f"Error updating complaint status: {e}")
            return False
    
    def get_complaints_by_department(self, department_id: int) -> List[Dict[str, Any]]:
        """Get all complaints assigned to a department"""
        query = """
            SELECT 
                c.complaint_id,
                c.title,
                c.description,
                c.location,
                cat.name as category,
                c.priority,
                c.status,
                c.created_at,
                u.name as user_name,
                u.email as user_email
            FROM complaints c
            LEFT JOIN categories cat ON c.category_id = cat.category_id
            LEFT JOIN users u ON c.user_id = u.user_id
            LEFT JOIN assignments a ON c.complaint_id = a.complaint_id
            WHERE a.department_id = ?
            ORDER BY 
                CASE c.priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                END,
                c.created_at DESC
        """
        
        return self.db.execute_query(query, (department_id,))
    
    def get_all_complaints(self) -> List[Dict[str, Any]]:
        """Get all complaints in the system"""
        query = """
            SELECT 
                c.complaint_id,
                c.title,
                cat.name as category,
                c.priority,
                c.status,
                c.created_at,
                u.name as user_name
            FROM complaints c
            LEFT JOIN categories cat ON c.category_id = cat.category_id
            LEFT JOIN users u ON c.user_id = u.user_id
            ORDER BY c.created_at DESC
        """
        
        return self.db.execute_query(query)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics for dashboard"""
        stats = {}
        
        # Total complaints
        total_query = "SELECT COUNT(*) as total FROM complaints"
        stats['total_complaints'] = self.db.execute_query(total_query)[0]['total']
        
        # Complaints by status
        status_query = """
            SELECT status, COUNT(*) as count 
            FROM complaints 
            GROUP BY status
        """
        stats['by_status'] = self.db.execute_query(status_query)
        
        # Complaints by category
        category_query = """
            SELECT cat.name as category, COUNT(*) as count
            FROM complaints c
            LEFT JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.name
        """
        stats['by_category'] = self.db.execute_query(category_query)
        
        # Complaints by priority
        priority_query = """
            SELECT priority, COUNT(*) as count
            FROM complaints
            GROUP BY priority
        """
        stats['by_priority'] = self.db.execute_query(priority_query)
        
        return stats


if __name__ == "__main__":
    # Initialize service
    db_path = "/home/ubuntu/complaint_system/data/complaint_system.db"
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    
    service = ComplaintService(db_path, model_path)
    
    # Register sample users
    print("\n" + "="*50)
    print("Registering Users")
    print("="*50)
    user1_id = service.register_user("John Doe", "john@example.com", "password123")
    user2_id = service.register_user("Jane Smith", "jane@example.com", "password456")
    
    # Submit sample complaints
    print("\n" + "="*50)
    print("Submitting Complaints")
    print("="*50)
    
    complaints_data = [
        (user1_id, "No water supply", "Water supply has been stopped for 3 days in our area", "Block A, Sector 12"),
        (user1_id, "Damaged road", "Large pothole on main road causing accidents", "Main Street"),
        (user2_id, "Power outage", "Frequent power cuts for 6 hours daily", "Colony B"),
        (user2_id, "Garbage issue", "Garbage not collected for one week, causing foul smell", "Park Avenue"),
    ]
    
    for user_id, title, desc, loc in complaints_data:
        result = service.submit_complaint(user_id, title, desc, loc)
        print(f"\nComplaint submitted: {title}")
        print(f"  ID: {result['complaint_id']}")
        print(f"  Category: {result['category']}")
        print(f"  Priority: {result['priority']}")
        print(f"  Confidence: {result['confidence']:.2f}")

