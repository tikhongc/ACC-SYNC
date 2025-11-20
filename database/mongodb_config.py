 # -*- coding: utf-8 -*-
"""
MongoDB Configuration and Connection Management Module
"""
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConfig:
    """MongoDB Configuration Class"""
    
    def __init__(self):
        # MongoDB connection configuration
        self.username = "chiutikhong"
        self.password = "abc261031"
        self.cluster_name = "cluster0.itxwgjo.mongodb.net"
        self.app_name = "Cluster0"
        
        # Build connection URI
        self.uri = f"mongodb+srv://{self.username}:{self.password}@{self.cluster_name}/?appName={self.app_name}"
        
        # Database name
        self.database_name = "acc_sync_db"
        
        # Client instance
        self.client = None
        self.database = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            # Create client connection
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB!")
            
            # Get database instance
            self.database = self.client[self.database_name]
            
            return True
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False
        except ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB server selection timeout: {e}")
            return False
        except Exception as e:
            logger.error(f"MongoDB connection unknown error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection disconnected")
    
    def get_database(self):
        """Get database instance"""
        if not self.database:
            if not self.connect():
                raise Exception("Unable to connect to MongoDB database")
        return self.database
    
    def get_collection(self, collection_name):
        """Get specified collection"""
        database = self.get_database()
        return database[collection_name]
    
    def test_connection(self):
        """Test database connection"""
        try:
            if self.connect():
                # Test basic operations
                test_collection = self.get_collection("test_connection")
                
                # Insert test document
                test_doc = {"test": "connection", "timestamp": "2024-11-03"}
                result = test_collection.insert_one(test_doc)
                logger.info(f"Test document inserted successfully, ID: {result.inserted_id}")
                
                # Query test document
                found_doc = test_collection.find_one({"_id": result.inserted_id})
                if found_doc:
                    logger.info(f"Test document queried successfully: {found_doc}")
                
                # Delete test document
                test_collection.delete_one({"_id": result.inserted_id})
                logger.info("Test document deleted successfully")
                
                logger.info("MongoDB connection test completed, all operations normal!")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
        finally:
            self.disconnect()

# Global database configuration instance
db_config = MongoDBConfig()

def get_db():
    """Convenience function to get database instance"""
    return db_config.get_database()

def get_collection(collection_name):
    """Convenience function to get collection"""
    return db_config.get_collection(collection_name)
