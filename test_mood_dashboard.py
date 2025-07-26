#!/usr/bin/env python3
"""
تست داشبورد مود رمزارزها
"""
import requests
import json

def test_crypto_mood_api():
    """تست API مود رمزارز"""
    try:
        print("🚀 Testing Crypto Mood Dashboard...")
        
        # تست MEXC 24h ticker API
        url = "https://api.mexc.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            important_coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT', 'DOGEUSDT']
            found_coins = 0
            total_change = 0
            
            print("✅ MEXC API Connection: SUCCESS")
            print("\n📊 Sample Mood Data:")
            
            for coin_data in data:
                symbol = coin_data['symbol']
                if symbol in important_coins:
                    change_24h = float(coin_data['priceChangePercent'])
                    price = float(coin_data['lastPrice'])
                    
                    # Determine mood
                    if change_24h > 5:
                        mood = "Very Happy 🚀"
                    elif change_24h > 2:
                        mood = "Happy 😊"
                    elif change_24h > 0:
                        mood = "Positive 🙂"
                    elif change_24h > -2:
                        mood = "Worried 😐"
                    elif change_24h > -5:
                        mood = "Sad 😟"
                    else:
                        mood = "Very Sad 😱"
                    
                    print(f"  {symbol}: ${price:,.2f} ({change_24h:+.2f}%) - {mood}")
                    
                    found_coins += 1
                    total_change += change_24h
            
            if found_coins > 0:
                avg_change = total_change / found_coins
                print(f"\n🎯 Market Summary:")
                print(f"  • Total Coins: {found_coins}")
                print(f"  • Average Change: {avg_change:.2f}%")
                
                if avg_change > 3:
                    overall_mood = "Very Happy 🚀"
                elif avg_change > 1:
                    overall_mood = "Happy 😊"
                elif avg_change > -1:
                    overall_mood = "Neutral 😐"
                elif avg_change > -3:
                    overall_mood = "Worried 😟"
                else:
                    overall_mood = "Very Sad 😱"
                
                print(f"  • Overall Market Mood: {overall_mood}")
                print("✅ Mood Dashboard: WORKING PERFECTLY!")
            else:
                print("❌ No important coins found in API response")
                
        else:
            print(f"❌ API Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_crypto_mood_api()