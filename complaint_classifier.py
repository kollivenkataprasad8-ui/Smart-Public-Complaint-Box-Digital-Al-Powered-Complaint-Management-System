"""
AI Complaint Classifier Module
Uses machine learning to categorize complaints into predefined categories
"""

import re
import pickle
import os
from typing import Tuple, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


class ComplaintClassifier:
    """AI-powered complaint categorization system"""
    
    def __init__(self, model_path: str = None):
        """Initialize the classifier"""
        self.model_path = model_path
        self.pipeline = None
        self.categories = [
            'Water Supply',
            'Road Maintenance',
            'Electricity',
            'Sanitation',
            'Other'
        ]
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text data"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def create_training_data(self) -> Tuple[List[str], List[str]]:
        """Generate synthetic training data for the classifier"""
        
        # Water Supply complaints
        water_complaints = [
            "No water supply in our area for the past 3 days",
            "Water pressure is very low in the morning",
            "Dirty water coming from taps, needs urgent attention",
            "Water pipe burst on main street causing flooding",
            "Irregular water supply timing in our locality",
            "Water quality is poor, smells bad",
            "No water connection for new house",
            "Water meter not working properly",
            "Leaking water pipeline near the park",
            "Water supply stopped suddenly without notice",
            "Contaminated water supply causing health issues",
            "Need new water connection for building",
            "Water tank overflow causing wastage",
            "Underground water pipe leakage",
            "Insufficient water pressure in upper floors"
        ]
        
        # Road Maintenance complaints
        road_complaints = [
            "Large pothole on main road causing accidents",
            "Street lights not working for 2 weeks",
            "Road completely damaged after rain",
            "Need speed breakers near school zone",
            "Broken footpath dangerous for pedestrians",
            "Road construction incomplete for months",
            "No street lighting in our colony",
            "Damaged road surface near market area",
            "Potholes everywhere on highway stretch",
            "Road marking faded and needs repainting",
            "Manholes without covers on the road",
            "Uneven road surface causing vehicle damage",
            "Need zebra crossing near bus stop",
            "Road widening work pending for long time",
            "Broken tiles on footpath causing injuries"
        ]
        
        # Electricity complaints
        electricity_complaints = [
            "Frequent power cuts in our area",
            "Voltage fluctuation damaging appliances",
            "Electricity pole damaged and dangerous",
            "No power supply for 8 hours daily",
            "Electric wires hanging low and risky",
            "Meter reading incorrect and bill too high",
            "Transformer making loud noise",
            "Power outage during night time",
            "Electricity connection not provided",
            "Street light pole fallen on road",
            "Exposed electrical wires near residential area",
            "Transformer oil leaking",
            "Power supply interruption every day",
            "Faulty meter needs replacement",
            "High voltage current causing appliance damage"
        ]
        
        # Sanitation complaints
        sanitation_complaints = [
            "Garbage not collected for 5 days",
            "Overflowing drainage in our street",
            "Foul smell from open drain",
            "Waste bins not provided in area",
            "Sewage water on road for weeks",
            "Garbage dump near residential area",
            "Blocked drainage causing flooding",
            "No proper waste disposal system",
            "Stray dogs spreading garbage",
            "Public toilet in poor condition",
            "Drainage overflow during rain",
            "Garbage collection vehicle not coming regularly",
            "Open defecation due to lack of toilets",
            "Mosquito breeding in stagnant water",
            "Littering problem in public park"
        ]
        
        # Other complaints
        other_complaints = [
            "Illegal construction in neighborhood",
            "Noise pollution from nearby factory",
            "Stray animals causing nuisance",
            "Encroachment on public land",
            "Tree branches blocking view",
            "Need CCTV cameras for security",
            "Park maintenance required",
            "Building permission not granted",
            "Land dispute with neighbor",
            "Air pollution from industries",
            "Illegal parking blocking entrance",
            "Need public transport facility",
            "School building in poor condition",
            "Hospital staff behavior complaint",
            "Government office not functioning properly"
        ]
        
        # Combine all complaints with labels
        complaints = (
            water_complaints + road_complaints + electricity_complaints +
            sanitation_complaints + other_complaints
        )
        
        labels = (
            ['Water Supply'] * len(water_complaints) +
            ['Road Maintenance'] * len(road_complaints) +
            ['Electricity'] * len(electricity_complaints) +
            ['Sanitation'] * len(sanitation_complaints) +
            ['Other'] * len(other_complaints)
        )
        
        return complaints, labels
    
    def train(self, save_model: bool = True):
        """Train the complaint classification model"""
        print("Generating training data...")
        complaints, labels = self.create_training_data()
        
        # Preprocess all complaints
        complaints = [self.preprocess_text(c) for c in complaints]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            complaints, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        print("Training the model...")
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate on test set
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save confusion matrix data for visualization
        cm = confusion_matrix(y_test, y_pred, labels=self.categories)
        
        # Save model
        if save_model and self.model_path:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.pipeline, f)
            print(f"\nModel saved to {self.model_path}")
        
        return accuracy, cm, y_test, y_pred
    
    def load_model(self):
        """Load a pre-trained model"""
        if self.model_path and os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.pipeline = pickle.load(f)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError("Model file not found. Please train the model first.")
    
    def predict(self, complaint_text: str) -> Tuple[str, float]:
        """Predict category for a new complaint"""
        if self.pipeline is None:
            raise ValueError("Model not trained or loaded")
        
        # Preprocess the text
        processed_text = self.preprocess_text(complaint_text)
        
        # Predict category
        category = self.pipeline.predict([processed_text])[0]
        
        # Get prediction probability
        probabilities = self.pipeline.predict_proba([processed_text])[0]
        confidence = max(probabilities)
        
        return category, confidence
    
    def predict_priority(self, complaint_text: str, category: str) -> str:
        """Determine priority based on keywords and category"""
        text_lower = complaint_text.lower()
        
        # High priority keywords
        high_priority_keywords = [
            'urgent', 'emergency', 'dangerous', 'accident', 'health', 
            'death', 'fire', 'flood', 'burst', 'leaking', 'exposed',
            'fallen', 'broken', 'damaged', 'contaminated', 'overflow'
        ]
        
        # Medium priority keywords
        medium_priority_keywords = [
            'irregular', 'frequent', 'poor', 'need', 'required',
            'not working', 'problem', 'issue'
        ]
        
        # Check for high priority
        for keyword in high_priority_keywords:
            if keyword in text_lower:
                return 'High'
        
        # Check for medium priority
        for keyword in medium_priority_keywords:
            if keyword in text_lower:
                return 'Medium'
        
        # Default to low priority
        return 'Low'


if __name__ == "__main__":
    # Train and save the model
    model_path = "/home/ubuntu/complaint_system/models/classifier_model.pkl"
    classifier = ComplaintClassifier(model_path=model_path)
    accuracy, cm, y_test, y_pred = classifier.train(save_model=True)
    
    # Test predictions
    print("\n" + "="*50)
    print("Testing Predictions:")
    print("="*50)
    
    test_complaints = [
        "Water supply has stopped in our area",
        "There is a big pothole on the main road",
        "Power cut for 6 hours daily",
        "Garbage not collected for a week"
    ]
    
    for complaint in test_complaints:
        category, confidence = classifier.predict(complaint)
        priority = classifier.predict_priority(complaint, category)
        print(f"\nComplaint: {complaint}")
        print(f"Category: {category} (Confidence: {confidence:.2f})")
        print(f"Priority: {priority}")

