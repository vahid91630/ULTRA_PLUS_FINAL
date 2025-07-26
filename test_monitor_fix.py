#!/usr/bin/env python3
"""
تست مانیتور پس از رفع مشکل
"""
import requests
import json

def test_monitor():
    print("🧪 Testing Monitor after fix...")
    
    try:
        health_response = requests.get("http://localhost:5000/health", timeout=3)
        health_data = health_response.json()
        
        print(f"📡 Health Status: {health_data.get('status', 'unknown')}")
        print(f"🟢 Ready: {health_data.get('ready', False)}")
        print(f"⏱️ Uptime: {health_data.get('uptime', 0)} seconds")
        
        readiness_response = requests.get("http://localhost:5000/readiness", timeout=3)
        readiness_data = readiness_response.json()
        
        print(f"🤖 Bot Status: {readiness_data.get('bot_status', 'unknown')}")
        print(f"✅ Readiness: {readiness_data.get('ready', False)}")
        
        if health_data.get('ready') and readiness_data.get('ready'):
            print("\n🎉 مانیتور کاملاً درست شد! (Monitor completely fixed!)")
            return True
        else:
            print("\n⚠️ مانیتور هنوز مشکل دارد (Monitor still has issues)")
            return False
            
    except Exception as e:
        print(f"❌ Error testing monitor: {e}")
        return False

if __name__ == "__main__":
    test_monitor()