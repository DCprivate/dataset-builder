# Software/DataHarvester/services/mongo_service/init_mongo.py

from typing import List
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.errors import CollectionInvalid

def init_database(client: MongoClient) -> Database:
    """Initialize the dataharvester database"""
    return client.dataharvester

def create_projects_collection(db: Database) -> None:
    """
    Create and configure the projects collection.
    This collection stores metadata about different data harvesting projects.
    """
    try:
        db.create_collection("projects")
    except CollectionInvalid:
        # Collection already exists
        pass

    # Create indexes for projects collection
    db.projects.create_index([("name", ASCENDING)], unique=True)
    db.projects.create_index([("created_at", ASCENDING)])

def create_project_collections(db: Database, project_name: str) -> None:
    """
    Create collections for a specific project with appropriate indexes.
    Each project gets three collections for different processing stages:
    - raw: Initial ingested data
    - cleaned: Data after cleaning/preprocessing
    - processed: Final processed data
    
    Args:
        db: MongoDB database instance
        project_name: Name of the project to create collections for
    """
    # Define processing stages
    stages: List[str] = ['raw', 'cleaned', 'processed']
    
    for stage in stages:
        collection_name = f"{project_name}_{stage}"
        
        try:
            db.create_collection(collection_name)
        except CollectionInvalid:
            # Collection already exists
            pass
            
        collection = db[collection_name]
        
        # Create common indexes for all stages
        collection.create_index([("created_at", ASCENDING)])
        collection.create_index([("updated_at", ASCENDING)])
        
        # Create stage-specific indexes
        if stage == 'raw':
            # Raw data indexes
            collection.create_index([("source_id", ASCENDING)], unique=True)
            collection.create_index([("cleaned", ASCENDING)])
            
        elif stage == 'cleaned':
            # Cleaned data indexes
            collection.create_index([("raw_id", ASCENDING)])
            collection.create_index([("processed", ASCENDING)])
            
        elif stage == 'processed':
            # Processed data indexes
            collection.create_index([("cleaned_id", ASCENDING)])

def init_mongo(mongo_uri: str = "mongodb://localhost:27017/") -> None:
    """
    Initialize MongoDB with required collections and indexes.
    
    Args:
        mongo_uri: MongoDB connection URI
    """
    client = MongoClient(mongo_uri)
    db = init_database(client)
    
    # Set up base collections
    create_projects_collection(db)
    
    # Optional: Set up TTL index for data retention
    # db.raw_transcripts.create_index([("created_at", ASCENDING)], 
    #                                expireAfterSeconds=7776000)  # 90 days

    try:
        client.close()
    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")

if __name__ == "__main__":
    init_mongo() 