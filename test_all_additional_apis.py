#!/usr/bin/env python3
"""
آزمایش تمام API های اضافی
"""

import os
import requests
import time
from datetime import datetime

def test_alpha_vantage():
    """آزمایش Alpha Vantage API"""
    try:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            return {"status": "MISSING", "error": "کلید موجود نیست"}
        
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'Global Quote' in data:
                quote = data['Global Quote']
                price = quote.get('05. price', 'N/A')
                return {
                    "status": "CONNECTED",
                    "api_key_length": len(api_key),
                    "sample_price": f"IBM: ${price}",
                    "symbol_tested": "IBM"
                }
            elif 'Error Message' in data:
                return {
                    "status": "ERROR",
                    "error": data['Error Message'],
                    "api_key_exists": True
                }
            else:
                return {
                    "status": "QUOTA_EXCEEDED",
                    "error": "احتمال تمام شدن quota روزانه",
                    "api_key_exists": True
                }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}",
                "api_key_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def test_polygon_api():
    """آزمایش Polygon.io API"""
    try:
        api_key = os.getenv('POLYGON_API_KEY')
        if not api_key:
            return {"status": "MISSING", "error": "کلید موجود نیست"}
        
        url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apikey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK' and data.get('results'):
                result = data['results'][0]
                price = result.get('c', 'N/A')
                return {
                    "status": "CONNECTED",
                    "api_key_length": len(api_key),
                    "sample_price": f"AAPL: ${price}",
                    "data_count": len(data['results'])
                }
            else:
                return {
                    "status": "ERROR",
                    "error": data.get('error', 'Unknown error'),
                    "api_key_exists": True
                }
        elif response.status_code == 401:
            return {
                "status": "UNAUTHORIZED",
                "error": "کلید API نامعتبر یا منقضی",
                "api_key_exists": True
            }
        elif response.status_code == 429:
            return {
                "status": "RATE_LIMITED",
                "error": "محدودیت نرخ درخواست",
                "api_key_exists": True
            }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}",
                "api_key_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def test_news_api():
    """آزمایش News API"""
    try:
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            return {"status": "MISSING", "error": "کلید موجود نیست"}
        
        url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&pageSize=5&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                return {
                    "status": "CONNECTED",
                    "api_key_length": len(api_key),
                    "articles_count": len(articles),
                    "sample_headline": articles[0]['title'][:50] + "..." if articles else "No articles"
                }
            else:
                return {
                    "status": "ERROR",
                    "error": data.get('message', 'Unknown error'),
                    "api_key_exists": True
                }
        elif response.status_code == 401:
            return {
                "status": "UNAUTHORIZED",
                "error": "کلید API نامعتبر",
                "api_key_exists": True
            }
        elif response.status_code == 429:
            return {
                "status": "QUOTA_EXCEEDED",
                "error": "محدودیت درخواست روزانه",
                "api_key_exists": True
            }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}",
                "api_key_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def test_twitter_api():
    """آزمایش Twitter API"""
    try:
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        if not bearer_token:
            return {"status": "MISSING", "error": "Bearer token موجود نیست"}
        
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "TradingBot/1.0"
        }
        
        url = "https://api.twitter.com/2/tweets/search/recent?query=bitcoin&max_results=10"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                tweets = data['data']
                return {
                    "status": "CONNECTED",
                    "token_length": len(bearer_token),
                    "tweets_count": len(tweets),
                    "sample_tweet": tweets[0]['text'][:50] + "..." if tweets else "No tweets"
                }
            else:
                return {
                    "status": "NO_DATA",
                    "error": "بدون داده",
                    "token_exists": True
                }
        elif response.status_code == 401:
            return {
                "status": "UNAUTHORIZED",
                "error": "Bearer token نامعتبر",
                "token_exists": True
            }
        elif response.status_code == 429:
            return {
                "status": "RATE_LIMITED",
                "error": "محدودیت نرخ",
                "token_exists": True
            }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}: {response.text[:100]}",
                "token_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "token_exists": bool(bearer_token)
        }

def test_mongodb_connection():
    """آزمایش MongoDB"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            return {"status": "MISSING", "error": "MongoDB URI موجود نیست"}
        
        # بررسی فرمت URI
        if mongodb_uri.startswith('mongodb://') or mongodb_uri.startswith('mongodb+srv://'):
            return {
                "status": "URI_VALID",
                "uri_length": len(mongodb_uri),
                "type": "MongoDB Atlas" if "mongodb+srv" in mongodb_uri else "MongoDB Standard",
                "note": "URI معتبر - اتصال واقعی نیاز به pymongo دارد"
            }
        else:
            return {
                "status": "INVALID_FORMAT",
                "error": "فرمت URI نامعتبر",
                "uri_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

def test_openai_detailed():
    """آزمایش دقیق OpenAI"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {"status": "MISSING", "error": "کلید موجود نیست"}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # تست quota
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "status": "CONNECTED",
                "api_key_length": len(api_key),
                "model_tested": "gpt-3.5-turbo",
                "quota_status": "OK"
            }
        elif response.status_code == 429:
            error_data = response.json().get('error', {})
            return {
                "status": "QUOTA_EXCEEDED",
                "error": error_data.get('message', 'Quota exceeded'),
                "quota_type": error_data.get('type', 'unknown'),
                "api_key_exists": True
            }
        elif response.status_code == 401:
            return {
                "status": "UNAUTHORIZED",
                "error": "کلید نامعتبر",
                "api_key_exists": True
            }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}: {response.text[:100]}",
                "api_key_exists": True
            }
            
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def check_session_secret():
    """بررسی Session Secret"""
    try:
        session_secret = os.getenv('SESSION_SECRET')
        if not session_secret:
            return {"status": "MISSING", "error": "Session secret موجود نیست"}
        
        # بررسی قوت secret
        length = len(session_secret)
        
        if length >= 32:
            strength = "قوی"
        elif length >= 16:
            strength = "متوسط"
        else:
            strength = "ضعیف"
        
        return {
            "status": "EXISTS",
            "length": length,
            "strength": strength,
            "note": "برای احراز هویت session استفاده می‌شود"
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

def main():
    """تست همه API های اضافی"""
    print("🔍 آزمایش کامل API های اضافی")
    print("=" * 60)
    
    tests = {
        "Alpha Vantage": test_alpha_vantage,
        "Polygon.io": test_polygon_api,
        "News API": test_news_api,
        "Twitter API": test_twitter_api,
        "MongoDB": test_mongodb_connection,
        "OpenAI (دقیق)": test_openai_detailed,
        "Session Secret": check_session_secret
    }
    
    results = {}
    connected_count = 0
    total_count = len(tests)
    
    for service_name, test_func in tests.items():
        print(f"\n🔄 آزمایش {service_name}...")
        
        start_time = time.time()
        result = test_func()
        end_time = time.time()
        
        result['test_duration'] = round(end_time - start_time, 2)
        results[service_name] = result
        
        status = result['status']
        
        if status in ["CONNECTED", "URI_VALID", "EXISTS"]:
            print(f"✅ {service_name}: متصل/موجود")
            connected_count += 1
            
            # اطلاعات اضافی
            if 'sample_price' in result:
                print(f"   💰 نمونه قیمت: {result['sample_price']}")
            if 'articles_count' in result:
                print(f"   📰 مقالات: {result['articles_count']} مقاله")
            if 'tweets_count' in result:
                print(f"   🐦 توییت‌ها: {result['tweets_count']} توییت")
            if 'strength' in result:
                print(f"   🔒 قدرت: {result['strength']}")
                
        elif status in ["QUOTA_EXCEEDED", "RATE_LIMITED"]:
            print(f"⚠️ {service_name}: محدودیت quota/rate")
            print(f"   ℹ️ کلید معتبر اما محدود")
            
        elif status == "MISSING":
            print(f"❌ {service_name}: کلید موجود نیست")
            
        else:
            print(f"❌ {service_name}: خطا")
            print(f"   🔍 جزئیات: {result.get('error', 'نامشخص')[:60]}")
        
        print(f"   ⏱️ زمان: {result['test_duration']} ثانیه")
    
    # خلاصه نهایی
    print(f"\n📊 خلاصه نتایج:")
    print("=" * 40)
    
    working_apis = []
    limited_apis = []
    missing_apis = []
    error_apis = []
    
    for service, result in results.items():
        status = result['status']
        if status in ["CONNECTED", "URI_VALID", "EXISTS"]:
            working_apis.append(f"✅ {service}")
        elif status in ["QUOTA_EXCEEDED", "RATE_LIMITED"]:
            limited_apis.append(f"⚠️ {service}")
        elif status == "MISSING":
            missing_apis.append(f"❌ {service}")
        else:
            error_apis.append(f"❌ {service}")
    
    print("فعال:")
    for api in working_apis:
        print(f"  {api}")
    
    if limited_apis:
        print("\nمحدود:")
        for api in limited_apis:
            print(f"  {api}")
    
    if missing_apis:
        print("\nمفقود:")
        for api in missing_apis:
            print(f"  {api}")
    
    if error_apis:
        print("\nخطا:")
        for api in error_apis:
            print(f"  {api}")
    
    print(f"\n🎯 نتیجه کلی: {len(working_apis) + len(limited_apis)}/{total_count} API در دسترس")
    
    # تحلیل کیفیت
    if len(working_apis) >= 4:
        print("✅ کیفیت عالی - اکثر API ها فعال")
    elif len(working_apis) >= 2:
        print("⚠️ کیفیت خوب - برخی API ها فعال")
    else:
        print("❌ کیفیت ضعیف - API های کمی فعال")
    
    return results

if __name__ == "__main__":
    main()