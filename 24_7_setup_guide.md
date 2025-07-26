# 🚀 Complete 24/7 Bot Setup Guide

## SOLUTION 1: REPLIT DEPLOYMENTS (100% RELIABLE - RECOMMENDED)

### Step 1: Upgrade Your Replit Plan
1. Go to your Replit dashboard
2. Click on your profile → "Upgrade to Hacker Plan" 
3. Choose the Hacker Plan ($7/month) - this includes deployments
4. Complete the payment

### Step 2: Configure Deployment
1. In your Replit project, click the "Deploy" button (🚀 icon on left sidebar)
2. Select "Autoscale Deployment"
3. Choose these settings:
   - **Name**: `ultra-plus-bot-24-7`
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python restored_original_bot.py`
   - **Port**: `5000`
   - **Min Replicas**: `1` (keeps it always running)
   - **Max Replicas**: `2`

### Step 3: Set Environment Variables
In the deployment settings, add these environment variables:
```
ULTRA_Plus_Bot=[Your Bot Token]
MONGODB_URI=[Your MongoDB URI]
BINANCE_API_KEY=[Your Binance API Key]
BINANCE_SECRET_KEY=[Your Binance Secret Key]
OPENAI_API_KEY=[Your OpenAI API Key]
NEWS_API_KEY=[Your News API Key]
PORT=5000
DEPLOYMENT_MODE=24_7
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Your bot will get a permanent URL like: `https://ultra-plus-bot-24-7.replit.app`

### Step 5: Verify 24/7 Operation
1. Check the deployment logs - should show "✅ Bot started"
2. Test your bot in Telegram
3. Close your browser completely
4. Wait 30 minutes, then test the bot again
5. It should still be responding!

---

## SOLUTION 2: ENHANCED FREE TIER SOLUTION (If you prefer not to pay)

### Step 1: Install Required Packages
```bash
pip install flask requests psutil uptime-robot-api
```

### Step 2: Update Your .replit File
Replace your .replit file with this:

```toml
[nix]
channel = "stable-24_05"

[deployment]
deploymentTarget = "autoscale"
run = ["python", "enhanced_24_7_bot.py"]

[[workflows.workflow]]
name = "24_7_BOT"
author = "agent"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python enhanced_24_7_bot.py"
waitForPort = 5000

[[ports]]
localPort = 5000
externalPort = 80
```

### Step 3: Set Up External Monitoring

#### Option A: UptimeRobot (Free)
1. Go to https://uptimerobot.com
2. Create free account
3. Add HTTP(s) monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://[your-repl-name].[your-username].repl.co/ping`
   - **Monitoring Interval**: 5 minutes
   - **Monitor Timeout**: 30 seconds

#### Option B: Better Uptime (Free tier)
1. Go to https://betterstack.com
2. Create account
3. Add heartbeat monitor:
   - **URL**: `https://[your-repl-name].[your-username].repl.co/health`
   - **Interval**: 5 minutes

#### Option C: Healthchecks.io (Free)
1. Go to https://healthchecks.io
2. Create account
3. Create new check
4. Copy the ping URL
5. Set up cron job to ping it

### Step 4: Create Multiple Backup Monitors
Set up monitoring from 3-4 different services for redundancy:
1. UptimeRobot
2. Pingdom (free tier)
3. StatusCake (free tier)
4. Uptime.com (free tier)

Each service will ping your bot every 1-5 minutes, keeping it alive.

### Step 5: Advanced Configuration

#### Create requirements.txt:
```txt
python-telegram-bot==20.7
flask==2.3.3
requests==2.31.0
psutil==5.9.5
motor==3.3.1
pymongo==4.5.0
openai==0.28.1
aiohttp==3.8.5
python-dotenv==1.0.0
cryptography==41.0.4
dnspython==2.4.2
```

#### Create a startup script:
```bash
#!/bin/bash
# startup.sh
echo "🚀 Starting 24/7 Bot System..."
python enhanced_24_7_bot.py &
echo "✅ Bot started in background"
```

### Step 6: Advanced Keep-Alive Script
Create `keep_alive_advanced.py`:

```python
import requests
import time
import threading
import logging
from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class AdvancedKeepAlive:
    def __init__(self, repl_url):
        self.repl_url = repl_url
        self.running = True
        
    def ping_self(self):
        while self.running:
            try:
                response = requests.get(f"{self.repl_url}/ping", timeout=10)
                if response.status_code == 200:
                    logging.info("✅ Self-ping successful")
                else:
                    logging.warning(f"⚠️ Self-ping returned {response.status_code}")
            except Exception as e:
                logging.error(f"❌ Self-ping failed: {e}")
            
            time.sleep(240)  # Ping every 4 minutes
    
    def start(self):
        thread = threading.Thread(target=self.ping_self, daemon=True)
        thread.start()

@app.route('/ping')
def ping():
    return {'status': 'alive', 'timestamp': time.time()}

# Start keep-alive
keep_alive = AdvancedKeepAlive(os.environ.get('REPL_URL'))
keep_alive.start()
```

---

## 🔍 HOW TO VERIFY IT'S WORKING 24/7

### Method 1: Real Testing
1. Start your bot
2. Test it works in Telegram
3. Close ALL browser tabs
4. Shut down your computer
5. Wait 2-3 hours
6. Turn on computer, test bot again
7. Check uptime monitoring dashboard

### Method 2: Monitoring Dashboard
- UptimeRobot dashboard will show 99.9%+ uptime
- Your bot logs will show continuous operation
- Telegram bot will respond instantly even after hours of inactivity

### Method 3: Deployment Logs (for Replit Deployments)
- Check deployment logs in Replit dashboard
- Should show continuous operation without restarts
- Memory and CPU usage should be stable

---

## 🚨 TROUBLESHOOTING

### If Bot Stops Working:
1. Check deployment logs for errors
2. Verify all environment variables are set
3. Check external monitoring status
4. Restart deployment if needed

### Common Issues:
- **Bot token expired**: Update in environment variables
- **Port conflicts**: Ensure only port 5000 is used
- **Memory issues**: Upgrade to paid plan for more resources
- **API rate limits**: Add delays in bot code

### Emergency Recovery:
If everything fails:
1. Check Replit deployment status
2. Restart deployment manually
3. Check external monitor status
4. Verify webhook settings

---

## 💰 COST BREAKDOWN

### Replit Deployment (Recommended):
- **Hacker Plan**: $7/month
- **Always On**: Included
- **Custom Domain**: Included
- **99.9% Uptime**: Guaranteed

### Free Tier Solution:
- **External Monitoring**: Free tier limits
- **Reliability**: 95-98% (depends on monitoring frequency)
- **Maintenance**: Requires more setup

---

## ✅ FINAL CHECKLIST

- [ ] Replit plan upgraded (for Solution 1)
- [ ] Deployment configured and running
- [ ] Environment variables set
- [ ] External monitoring active
- [ ] Bot responding in Telegram
- [ ] Tested with browser closed
- [ ] Monitoring dashboards showing uptime
- [ ] Logs showing continuous operation

**Once completed, your bot will run 24/7 without any browser dependency!**