#!/usr/bin/env python3
"""
Test database connection script for My Vocabulary Vault Backend
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def test_database_connection():
    """Test the database connection"""
    print("🔍 Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            
            # Test if our database exists
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"🗄️  Connected to database: {db_name}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"📋 Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("📋 No tables found (run migrations first)")
                
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_redis_connection():
    """Test Redis connection if available"""
    try:
        import redis
        print("\n🔍 Testing Redis connection...")
        print(f"Redis URL: {settings.REDIS_URL}")
        
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        print("✅ Redis connection successful!")
        return True
        
    except ImportError:
        print("\n⚠️  Redis not installed (pip install redis)")
        return False
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 My Vocabulary Vault - Database Connection Test")
    print("=" * 50)
    
    # Test database
    db_success = test_database_connection()
    
    # Test Redis
    redis_success = test_redis_connection()
    
    print("\n" + "=" * 50)
    if db_success:
        print("✅ Database connection test passed!")
    else:
        print("❌ Database connection test failed!")
        
    if redis_success:
        print("✅ Redis connection test passed!")
    else:
        print("⚠️  Redis connection test failed (optional)")
    
    print("\n📋 Next steps:")
    if not db_success:
        print("1. Check if PostgreSQL is running")
        print("2. Verify database credentials in .env file")
        print("3. If using Docker: ./scripts/docker-commands.sh start")
    else:
        print("1. Run migrations: alembic upgrade head")
        print("2. Start the server: python run.py")
    
    return 0 if db_success else 1

if __name__ == "__main__":
    sys.exit(main())
