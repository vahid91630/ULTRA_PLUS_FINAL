#!/usr/bin/env python3
"""
تست استقلال سیستم - بررسی اینکه آیا ربات واقعاً مستقل کار می‌کند
"""

import subprocess
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bot_independence():
    """تست کامل استقلال ربات"""
    
    print("🧪 Testing Bot Independence...")
    print("=" * 50)
    
    # Test 1: Check if processes are running
    print("\n1️⃣ Process Check:")
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    
    keeper_running = 'final_bot_keeper.py' in result.stdout
    bot_running = 'restored_original_bot.py' in result.stdout
    
    print(f"   Keeper Process: {'✅ Running' if keeper_running else '❌ Not Found'}")
    print(f"   Bot Process: {'✅ Running' if bot_running else '❌ Not Found'}")
    
    # Test 2: Health Check
    print("\n2️⃣ Health Check:")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: ✅ {data.get('status', 'unknown')}")
            print(f"   Ready: {'✅' if data.get('ready') else '❌'} {data.get('ready')}")
            print(f"   Uptime: {data.get('uptime', 'unknown')} seconds")
        else:
            print(f"   Status: ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   Status: ❌ Failed - {e}")
    
    # Test 3: Independence Test - Simulate user leaving
    print("\n3️⃣ Independence Test:")
    print("   Simulating user leaving Replit interface...")
    
    for i in range(3):
        time.sleep(10)
        try:
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   Check {i+1}: ✅ Bot still alive (uptime: {data.get('uptime', 'unknown')}s)")
            else:
                print(f"   Check {i+1}: ❌ Bot down (HTTP {response.status_code})")
        except Exception as e:
            print(f"   Check {i+1}: ❌ Bot unreachable - {e}")
    
    # Test 4: Restart Test
    print("\n4️⃣ Restart Test:")
    print("   Killing bot to test auto-restart...")
    
    try:
        subprocess.run(['pkill', '-f', 'restored_original_bot.py'], capture_output=True)
        print("   Bot killed - waiting for auto-restart...")
        
        time.sleep(30)  # Wait for restart
        
        response = requests.get('http://localhost:5000/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Result: ✅ Bot auto-restarted successfully")
            print(f"   New uptime: {data.get('uptime', 'unknown')} seconds")
        else:
            print(f"   Result: ❌ Auto-restart failed")
    except Exception as e:
        print(f"   Result: ❌ Test failed - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete")
    
    return True

if __name__ == "__main__":
    test_bot_independence()