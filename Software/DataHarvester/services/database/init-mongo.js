// Software/DataHarvester/services/database/init-mongo.js

db = db.getSiblingDB('dataharvester');

// Create projects collection with schema validation
db.createCollection('projects');

// Create indexes for projects collection
db.projects.createIndex({ "name": 1 }, { unique: true });
db.projects.createIndex({ "created_at": 1 });

// Create helper function for creating project collections
db.system.js.save({
    _id: "createProjectCollections",
    value: function(projectName) {
        const stages = ['raw', 'cleaned', 'processed'];
        stages.forEach(stage => {
            const collectionName = `${projectName}_${stage}`;
            
            db.createCollection(collectionName);
            
            // Create common indexes
            db[collectionName].createIndex({ "created_at": 1 });
            db[collectionName].createIndex({ "updated_at": 1 });
            
            // Stage-specific indexes and validations
            switch(stage) {
                case 'raw':
                    db[collectionName].createIndex({ "source_id": 1 }, { unique: true });
                    db[collectionName].createIndex({ "cleaned": 1 });
                    break;
                    
                case 'cleaned':
                    db[collectionName].createIndex({ "raw_id": 1 });
                    db[collectionName].createIndex({ "processed": 1 });
                    break;
                    
                case 'processed':
                    db[collectionName].createIndex({ "cleaned_id": 1 });
                    break;
            }
        });
    }
});

// Set up TTL index for old documents if needed
// db.raw_transcripts.createIndex({ "created_at": 1 }, { expireAfterSeconds: 7776000 }); // 90 days 