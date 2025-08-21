#!/usr/bin/env python3
"""
Cleanup Script: Remove unused modules and dependencies
This script removes AI, Gamification, Vocabulary, and Topics modules that are not yet implemented
"""

import os
import shutil
from pathlib import Path

def remove_directory(path: str):
    """Remove directory if it exists"""
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"✅ Removed: {path}")
    else:
        print(f"⚠️  Not found: {path}")

def main():
    """Main cleanup function"""
    print("🧹 Starting cleanup of unused modules...")
    
    # Define paths to remove
    modules_to_remove = [
        "app/modules/ai",
        "app/modules/gamification", 
        "app/modules/vocabulary",
        "app/modules/topics"
    ]
    
    # Remove directories
    for module_path in modules_to_remove:
        remove_directory(module_path)
    
    print("\n✅ Cleanup completed!")
    print("\n📋 Summary of removed modules:")
    print("   - AI Module (models only, no API)")
    print("   - Gamification Module (models only, no API)")
    print("   - Vocabulary Module (schemas only, no models/API)")
    print("   - Topics Module (schemas only, no models/API)")
    
    print("\n🎯 Remaining modules (Phase 1 complete):")
    print("   ✅ Auth Module (5 endpoints)")
    print("   ✅ Flashcards Module (12 endpoints)")
    print("   ✅ Learning Module (6 endpoints)")
    print("   ✅ Analytics Module (7 endpoints)")
    
    print("\n📊 Total endpoints: 30")
    print("📊 Total modules: 4/8")

if __name__ == "__main__":
    main()
