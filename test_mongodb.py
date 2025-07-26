#!/usr/bin/env python3
"""
Test MongoDB Connection for ULTRA_PLUS_BOT
"""

import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def test_mongodb():
    """Test MongoDB connection and basic operations"""
    try:
        # Get MongoDB URI from environment
        MONGODB_URI = os.environ.get('MONGODB_URI')
        if not MONGODB_URI:
            print("❌ MONGODB_URI not found in environment")
            return False
            
        print("🔗 Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URI)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get database and collection
        database = client.get_database("ultra_plus_trading_bot")
        users_collection = database.get_collection("users")
        
        # Test document insertion
        test_user = {
            'user_id': 999999999,
            'username': 'MongoDB Test User',
            'balance': 10000,
            'trades': 0,
            'total_profit': 0,
            'bot_intelligence': 50,
            'join_date': datetime.now(),
            'test_document': True
        }
        
        print("📝 Inserting test document...")
        result = await users_collection.insert_one(test_user)
        print(f"✅ Document inserted with ID: {result.inserted_id}")
        
        # Test document retrieval
        print("🔍 Retrieving test document...")
        retrieved = await users_collection.find_one({'user_id': 999999999})
        if retrieved:
            print(f"✅ Document retrieved: {retrieved['username']}")
        
        # Test document update
        print("🔄 Updating test document...")
        await users_collection.update_one(
            {'user_id': 999999999},
            {'$set': {'balance': 15000, 'last_test': datetime.now()}}
        )
        
        # Verify update
        updated = await users_collection.find_one({'user_id': 999999999})
        if updated and updated['balance'] == 15000:
            print("✅ Document update successful!")
        
        # Clean up test document
        print("🧹 Cleaning up test document...")
        await users_collection.delete_one({'user_id': 999999999})
        print("✅ Test document deleted")
        
        # Check collections
        print("📊 Available collections:")
        collections = await database.list_collection_names()
        for collection in collections:
            count = await database[collection].count_documents({})
            print(f"   • {collection}: {count} documents")
        
        print("\n🎉 MongoDB integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    result = asyncio.run(test_mongodb())
    exit(0 if result else 1)