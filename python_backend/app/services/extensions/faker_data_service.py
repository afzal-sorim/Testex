import random
import time
import uuid
from typing import Dict, Any

class FakerDataService:
    """
    Non-invasive synthetic test data generator helper.
    Generates realistic, unique data values (emails, names, phone numbers, timestamps)
    to prevent database unique constraint collisions during test execution.
    """

    def generate_random_user(self) -> Dict[str, str]:
        """Generate a random user profile data dict."""
        uid = str(uuid.uuid4())[:8]
        timestamp = int(time.time())
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis"]
        
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        
        return {
            "first_name": fname,
            "last_name": lname,
            "username": f"user_{uid}",
            "email": f"{fname.lower()}.{lname.lower()}_{timestamp}@testdomain.com",
            "phone": f"608555{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} Main St",
            "city": "Madison",
            "zip_code": f"537{random.randint(10, 99)}"
        }

    def generate_random_task(self) -> Dict[str, str]:
        """Generate random task/todo data dict."""
        uid = str(uuid.uuid4())[:6]
        actions = ["Review PR", "Update Docs", "Run Regression", "Deploy Staging", "Audit Logs"]
        action = random.choice(actions)
        
        return {
            "title": f"{action} #{uid}",
            "description": f"Automated test item created at timestamp {int(time.time())}"
        }

faker_data_service = FakerDataService()
