# Software/DataHarvester/src/monitoring/health.py

import nltk
from typing import Tuple, List, Dict
import pymongo
from infrastructure.logging.logger import get_logger
from infrastructure.config.config_manager import ConfigManager

logger = get_logger()

class HealthChecker:
    """System health monitoring."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.db_config = self.config.get_config('database')
        
    @staticmethod
    def check_nltk_data() -> Tuple[bool, List[str]]:
        """Check if all required NLTK data is available."""
        required_data = [
            'punkt',
            'stopwords',
            'words'
        ]
        missing_data = []
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}' if data == 'punkt' 
                             else f'corpora/{data}')
            except LookupError:
                missing_data.append(data)
        
        return len(missing_data) == 0, missing_data

    @staticmethod
    def check_mongodb(mongo_uri: str) -> bool:
        """Check MongoDB connection."""
        try:
            client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            logger.info("MongoDB health check: OK")
            return True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {str(e)}")
            return False
            
    def check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            import shutil
            _, _, free = shutil.disk_usage("/app")
            free_gb = free // (2**30)
            if free_gb < 1:  # Less than 1GB free
                logger.warning(f"Low disk space: {free_gb}GB free")
                return False
            logger.info(f"Disk space check: OK ({free_gb}GB free)")
            return True
        except Exception as e:
            logger.error(f"Disk space check failed: {str(e)}")
            return False
    
    def check_all(self) -> Dict[str, bool]:
        """Run all health checks."""
        results = {
            'mongodb': self.check_mongodb(self.db_config.get('mongodb', {}).get('uri', 'mongodb://mongo:27017/')),
            'disk_space': self.check_disk_space()
        }
        
        all_passed = all(results.values())
        status = "HEALTHY" if all_passed else "UNHEALTHY"
        logger.info(f"Health check complete. Status: {status}")
        
        return results

    @staticmethod
    def perform_checks(mongo_uri: str) -> bool:
        """Perform all health checks."""
        logger.info("Starting system health checks...")

        # Check NLTK data
        nltk_ok, missing_data = HealthChecker.check_nltk_data()
        if not nltk_ok:
            logger.error(f"Missing NLTK data: {', '.join(missing_data)}")
            return False
        logger.info("NLTK data check passed")

        # Check MongoDB connection
        if not HealthChecker.check_mongodb(mongo_uri):
            logger.error("MongoDB connection check failed")
            return False
        logger.info("MongoDB connection check passed")

        logger.info("All health checks passed")
        return True 