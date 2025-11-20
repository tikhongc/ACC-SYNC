# -*- coding: utf-8 -*-
"""
MongoDB Connection Test Script
"""
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.mongodb_config import MongoDBConfig

def main():
    """Main test function"""
    print("=== MongoDB Connection Test ===")
    
    # Create database configuration instance
    db_config = MongoDBConfig()
    
    # Display connection information
    print(f"Connection URI: {db_config.uri}")
    print(f"Database name: {db_config.database_name}")
    print()
    
    # Execute connection test
    print("Starting connection test...")
    success = db_config.test_connection()
    
    if success:
        print("\n[SUCCESS] MongoDB connection test successful!")
        print("Database is ready for use.")
    else:
        print("\n[FAILED] MongoDB connection test failed!")
        print("Please check network connection and database configuration.")
    
    return success

if __name__ == "__main__":
    main()