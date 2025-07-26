ULTRA_PLUS_BOT - Advanced AI Trading System
==========================================

This is a complete, production-ready AI-powered cryptocurrency trading bot system with Persian language support and advanced machine learning capabilities.

## QUICK START

1. **Install Dependencies**
   pip install -r requirements_minimal.txt

2. **Set Environment Variables**
   Copy the following environment variables to your system:
   
   REQUIRED:
   - ULTRA_Plus_Bot=your_telegram_bot_token
   - OPENAI_API_KEY=your_openai_api_key
   - DATABASE_URL=your_database_url (PostgreSQL)
   
   OPTIONAL:
   - NEWSAPI_KEY=your_news_api_key
   - BINANCE_API_KEY=your_binance_api_key
   - BINANCE_SECRET_KEY=your_binance_secret_key

3. **Choose Deployment Method**

   **Option A: Replit Deployment (Recommended)**
   - Upload this project to Replit
   - Set environment variables in Replit Secrets
   - Click "Run" to start the system
   - Access Streamlit dashboard at port 5000

   **Option B: Cloud Run Deployment**
   - Use: python minimal_cloud_run.py
   - Optimized for <300MB image size
   - Single port (8080) configuration
   - Auto-scaling ready

   **Option C: Local Development**
   - Use: python main.py
   - Full feature development environment
   - Access monitoring dashboard at port 8080

## SYSTEM ARCHITECTURE

### Core Components:
- **ULTRA_PLUS_BOT.py**: Main bot with GPT-4 integration
- **minimal_cloud_run.py**: Optimized cloud deployment
- **app.py**: Streamlit web dashboard
- **ai_engine.py**: AI trading intelligence
- **market_data.py**: Multi-source data collection
- **trading_engine.py**: Core trading functionality

### Key Features:
- ✅ AI-powered trading decisions (GPT-4)
- ✅ Persian language support
- ✅ Multi-exchange integration
- ✅ Real-time monitoring dashboard
- ✅ Machine learning predictions
- ✅ Automated portfolio management
- ✅ Cost tracking and analysis
- ✅ Cloud-ready deployment

## WORKFLOW OPTIONS

The system provides multiple workflows for different use cases:

1. **Active Bot**: Single instance Telegram bot
2. **Autonomous System**: Background AI trading
3. **Cloud Run Optimized Bot**: Production deployment
4. **Monitoring Dashboard**: System health monitoring
5. **Streamlit App**: Web-based trading dashboard
6. **Telegram Notification Service**: Real-time alerts

## DEPLOYMENT READY

This system is fully optimized for cloud deployment:
- ✅ Image size: <300MB (reduced from 8GB+)
- ✅ Single port configuration (8080)
- ✅ Auto-scaling compatible
- ✅ Health check endpoints
- ✅ Comprehensive error handling

## CONFIGURATION FILES

- **requirements_minimal.txt**: Essential dependencies only
- **Dockerfile.cloudrun**: Optimized container image
- **.dockerignore**: Excludes unnecessary files
- **Procfile**: Cloud deployment configuration
- **replit.toml**: Single port configuration

## PERSIAN LANGUAGE SUPPORT

The system includes full Persian language support:
- Persian number formatting
- Shamsi calendar integration
- Persian trading terminology
- Culturally appropriate messaging

## SECURITY FEATURES

- ✅ Secure environment variable handling
- ✅ API key management
- ✅ Database encryption support
- ✅ Rate limiting protection
- ✅ Error logging and monitoring

## TROUBLESHOOTING

**Common Issues:**
1. "Module not found" errors: Run `pip install -r requirements_minimal.txt`
2. Database connection issues: Check DATABASE_URL environment variable
3. Telegram bot errors: Verify ULTRA_Plus_Bot token in environment
4. Port conflicts: Use different ports for different services

**Logs Location:**
- Application logs: Check console output
- Error logs: Stored in application data directory
- Database logs: Check PostgreSQL logs

## NEXT STEPS

1. Configure your API keys and secrets
2. Choose your deployment method
3. Start the system using one of the provided entry points
4. Monitor system health through the dashboard
5. Customize trading strategies as needed

## SUPPORT

This system is designed to be fully self-contained and portable. All necessary files and dependencies are included for immediate deployment on any platform.

For technical issues:
- Check the logs for detailed error messages
- Verify all environment variables are set correctly
- Ensure proper network connectivity for API calls

Deployment Date: July 17, 2025
System Version: 1.0.0
Architecture: Cloud-optimized, Multi-platform