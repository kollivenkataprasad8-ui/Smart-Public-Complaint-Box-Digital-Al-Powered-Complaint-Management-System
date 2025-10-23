"""
Test module for Smart Public Complaint Box
Tests all major functionalities of the system
"""

import sys
sys.path.append('/home/ubuntu/complaint_system')

from backend.complaint_service import ComplaintService
from models.complaint_classifier import ComplaintClassifier
import time


def test_classifier():
    """Test the AI classifier with various complaints"""
    print("\n" + "="*70)
    print("TEST 1: AI CLASSIFIER FUNCTIONALITY")
    print("="*70)
    
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    classifier = ComplaintClassifier(model_path)
    classifier.load_model()
    
    test_cases = [
        "Water supply is irregular and comes only for 2 hours",
        "The road near my house has multiple dangerous potholes",
        "Power cuts happening every day for 4-5 hours",
        "Garbage is not being collected and creating health hazard",
        "Street lights are not working in our colony",
        "Contaminated water supply causing diseases",
        "Sewage overflow on the main road",
        "Electricity meter showing wrong readings",
        "Need urgent repair of broken water pipeline",
        "Road construction work incomplete for months"
    ]
    
    results = []
    for i, complaint in enumerate(test_cases, 1):
        category, confidence = classifier.predict(complaint)
        priority = classifier.predict_priority(complaint, category)
        
        print(f"\n{i}. Complaint: {complaint}")
        print(f"   Category: {category}")
        print(f"   Priority: {priority}")
        print(f"   Confidence: {confidence:.2%}")
        
        results.append({
            'complaint': complaint,
            'category': category,
            'priority': priority,
            'confidence': confidence
        })
    
    return results


def test_complaint_workflow():
    """Test the complete complaint workflow"""
    print("\n" + "="*70)
    print("TEST 2: COMPLETE COMPLAINT WORKFLOW")
    print("="*70)
    
    db_path = "/home/ubuntu/complaint_system/data/complaint_system.db"
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    
    service = ComplaintService(db_path, model_path)
    
    # Test 1: User Registration
    print("\n--- User Registration ---")
    user_id = service.register_user(
        "Test User", 
        f"testuser_{int(time.time())}@example.com", 
        "testpass123"
    )
    print(f"✓ User registered with ID: {user_id}")
    
    # Test 2: Complaint Submission
    print("\n--- Complaint Submission ---")
    result = service.submit_complaint(
        user_id,
        "Urgent: Water Pipeline Burst",
        "Major water pipeline burst near the market causing flooding and water wastage",
        "Market Street, Sector 15"
    )
    complaint_id = result['complaint_id']
    print(f"✓ Complaint submitted with ID: {complaint_id}")
    print(f"  Category: {result['category']}")
    print(f"  Priority: {result['priority']}")
    print(f"  Status: {result['status']}")
    
    # Test 3: Retrieve Complaint Details
    print("\n--- Retrieve Complaint Details ---")
    details = service.get_complaint_details(complaint_id)
    if details:
        print(f"✓ Complaint retrieved successfully")
        print(f"  Title: {details['title']}")
        print(f"  Category: {details['category']}")
        print(f"  Priority: {details['priority']}")
        print(f"  Status: {details['status']}")
    
    # Test 4: Update Complaint Status
    print("\n--- Update Complaint Status ---")
    service.update_complaint_status(complaint_id, "In Progress")
    updated_details = service.get_complaint_details(complaint_id)
    print(f"✓ Status updated to: {updated_details['status']}")
    
    # Test 5: Get User Complaints
    print("\n--- Get User Complaints ---")
    user_complaints = service.get_user_complaints(user_id)
    print(f"✓ Found {len(user_complaints)} complaint(s) for user")
    
    return {
        'user_id': user_id,
        'complaint_id': complaint_id,
        'result': result
    }


def test_statistics():
    """Test statistics generation"""
    print("\n" + "="*70)
    print("TEST 3: SYSTEM STATISTICS")
    print("="*70)
    
    db_path = "/home/ubuntu/complaint_system/data/complaint_system.db"
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    
    service = ComplaintService(db_path, model_path)
    stats = service.get_statistics()
    
    print(f"\n✓ Total Complaints: {stats['total_complaints']}")
    
    print("\n--- Complaints by Status ---")
    for item in stats['by_status']:
        print(f"  {item['status']}: {item['count']}")
    
    print("\n--- Complaints by Category ---")
    for item in stats['by_category']:
        print(f"  {item['category']}: {item['count']}")
    
    print("\n--- Complaints by Priority ---")
    for item in stats['by_priority']:
        print(f"  {item['priority']}: {item['count']}")
    
    return stats


def test_performance():
    """Test system performance metrics"""
    print("\n" + "="*70)
    print("TEST 4: PERFORMANCE METRICS")
    print("="*70)
    
    db_path = "/home/ubuntu/complaint_system/data/complaint_system.db"
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    
    service = ComplaintService(db_path, model_path)
    
    # Test response time for complaint submission
    print("\n--- Testing Response Time ---")
    start_time = time.time()
    
    for i in range(10):
        service.submit_complaint(
            1,
            f"Test Complaint {i}",
            "This is a test complaint for performance measurement",
            "Test Location"
        )
    
    end_time = time.time()
    avg_time = (end_time - start_time) / 10
    
    print(f"✓ Average time per complaint submission: {avg_time*1000:.2f} ms")
    print(f"✓ Throughput: {10/(end_time - start_time):.2f} complaints/second")
    
    return {
        'avg_response_time': avg_time,
        'throughput': 10/(end_time - start_time)
    }


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SMART PUBLIC COMPLAINT BOX - SYSTEM TESTING")
    print("="*70)
    
    # Run all tests
    classifier_results = test_classifier()
    workflow_results = test_complaint_workflow()
    stats_results = test_statistics()
    performance_results = test_performance()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70)

