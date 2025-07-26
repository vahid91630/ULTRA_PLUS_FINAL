#!/usr/bin/env python3
"""
System Status Checker - تست جامع وضعیت سیستم
"""

import asyncio
import subprocess
import sys
import os
from datetime import datetime

def check_python_syntax():
    """Check Python syntax of main files"""
    try:
        result = subprocess.run([sys.executable, '-m', 'py_compile', 'restored_original_bot.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python syntax: OK")
            return True
        else:
            print(f"❌ Python syntax error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Syntax check failed: {e}")
        return False

def check_imports():
    """Check if all imports work"""
    try:
        import restored_original_bot
        print("✅ Main bot imports: OK")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_file_structure():
    """Check essential files exist"""
    essential_files = [
        'restored_original_bot.py',
        'fully_autonomous_trading_engine.py', 
        'real_exchange_tester.py',
        'data_reset_system.py'
    ]
    
    missing = []
    for file in essential_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    else:
        print("✅ File structure: OK")
        return True

async def main():
    """Run comprehensive system check"""
    print("🔍 ULTRA_PLUS_BOT System Status Check")
    print("=" * 50)
    print(f"📅 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all checks
    checks = [
        check_file_structure(),
        check_python_syntax(), 
        check_imports()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print()
    print("📊 SUMMARY:")
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL SYSTEMS OPERATIONAL")
        return True
    else:
        print("⚠️ Some issues found")
        return False

if __name__ == "__main__":
    asyncio.run(main())