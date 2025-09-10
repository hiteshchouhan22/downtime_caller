# Downtime Caller - Python Webhook Service

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](Webhook/requirements.txt)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](Webhook/requirements.txt)
[![Twilio](https://img.shields.io/badge/twilio-7.4.0-red.svg)](Webhook/requirements.txt)

## 🎯 Project Overview

A simple Python Flask webhook service that integrates with **Uptime Kuma** monitoring system to send **automated phone call alerts** via Twilio API when services go down.

### Key Features

- **📞 Automated Phone Calls**: Triggers voice calls during downtime events
- **🔗 Webhook Integration**: Easy integration with Uptime Kuma notifications
- **⚙️ Environment Configuration**: Secure credential management
- **📊 Status Monitoring**: Built-in health checks and status endpoints
- **🌐 Web Interface**: Beautiful HTML instruction page
- **🛠️ Error Handling**: Comprehensive error handling and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Twilio account with phone number
- Uptime Kuma (optional, for integration)

### Installation & Setup

1. **Navigate to the webhook directory:**
```bash
cd ./downtime_caller/Webhook
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

**Windows:**
```bash
set TWILIO_ACCOUNT_SID=your_twilio_account_sid
set TWILIO_AUTH_TOKEN=your_twilio_auth_token
set TWILIO_PHONE_NUMBER=+1234567890
set PHONE_NUMBERS=+1234567890,+0987654321
```

**Linux/Mac:**
```bash
export TWILIO_ACCOUNT_SID=your_twilio_account_sid
export TWILIO_AUTH_TOKEN=your_twilio_auth_token
export TWILIO_PHONE_NUMBER=+1234567890
export PHONE_NUMBERS=+1234567890,+0987654321
```

4. **Start the webhook service:**
```bash
python app.py
```

5. **Access the service:**
- **Web Interface**: http://localhost:5000/
- **Health Check**: http://localhost:5000/health
- **Trigger Calls**: http://localhost:5000/trigger-call

## 📋 Environment Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number (from) | `+1234567890` |
| `PHONE_NUMBERS` | Comma-separated numbers to call | `+1234567890,+0987654321` |

### Where to Find Twilio Credentials:
1. Sign up at [Twilio.com](https://www.twilio.com)
2. Go to **Console** → **Account Info**
3. Find your **Account SID** and **Auth Token**
4. Purchase a phone number in **Phone Numbers** section

## 🔌 API Endpoints

### `GET /`
**Description**: Interactive instruction page with complete setup guide
```bash
curl http://localhost:5000/
```

### `GET /health`
**Description**: Health check endpoint
```bash
curl http://localhost:5000/health
```
**Response:**
```json
{
    "status": "healthy",
    "service": "Downtime Caller Webhook",
    "version": "1.0.0"
}
```

### `POST /trigger-call`
**Description**: Trigger phone calls for downtime alerts
```bash
curl -X POST http://localhost:5000/trigger-call
```
**Response:**
```json
{
    "success": true,
    "calls_initiated": 2,
    "call_sids": ["CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"],
    "message": "Successfully initiated 2 call(s)"
}
```

## 🔗 Uptime Kuma Integration

### Step-by-Step Setup:

1. **Start your webhook service** (see Quick Start above)

2. **Access Uptime Kuma Dashboard**
   - Default: http://localhost:3001

3. **Add Webhook Notification**
   - Go to **Settings** → **Notifications**
   - Click **Add New Notification**
   - Select **Webhook** type
   - **Webhook URL**: `http://localhost:5000/trigger-call`
   - Click **Save**

4. **Assign to Monitors**
   - Edit your monitors
   - In **Notifications** section, select your webhook
   - Save the monitor

5. **Test the Integration**
   - Use the **Test** button in notifications
   - Or manually trigger: `curl -X POST http://localhost:5000/trigger-call`

## 🧪 Testing

### Manual Testing
```bash
# Test webhook endpoint
curl -X POST http://localhost:5000/trigger-call

# Check service health
curl http://localhost:5000/health

# View instruction page
curl http://localhost:5000/
```

### Expected Behavior
- **With proper configuration**: Phone calls will be initiated to all configured numbers
- **Without configuration**: Clear error messages with setup instructions
- **Partial configuration**: Detailed error reporting for missing variables

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Twilio credentials not configured"
**Solution**: Set `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` environment variables

#### 📞 "Phone numbers not configured"
**Solution**: Set `PHONE_NUMBERS` environment variable with valid phone numbers

#### 🚫 "Twilio authentication failed"
**Solution**: Verify your Account SID and Auth Token are correct

#### 📱 "Invalid phone number format"
**Solution**: Use E.164 format: `+[country_code][phone_number]`

### Debugging Tips
- Check console output for detailed error messages
- Visit http://localhost:5000/ for complete setup guide
- Ensure Twilio account has sufficient balance
- Verify phone numbers are in correct format

## 📁 File Structure

```
Webhook/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface template
└── test_app.py        # Unit tests
```

## 💰 Cost Considerations

- **Twilio Pricing**: Calls typically cost $0.01-0.02 per minute
- **Free Trial**: Twilio provides free credits for testing
- **Usage**: Each downtime event triggers one call per configured number

## 🛠️ Development

### Running Tests
```bash
python -m pytest test_app.py -v
```

### Code Structure
- **Flask Routes**: `/`, `/health`, `/trigger-call`
- **Environment Validation**: Checks for required variables on startup
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Structured logging with timestamps

## 📝 Example Usage

```python
# Basic usage - set environment variables first
cd Webhook
python app.py

# The service will show startup information:
# ✅ All environment variables configured!
# 🚀 Service will run on http://0.0.0.0:5000
```

## 📄 License

This project is licensed under the MIT License.

---

**Quick Commands:**
```bash
# Install and run
cd f:\downtime_caller\Webhook
pip install -r requirements.txt
python app.py

# Test the service
curl -X POST http://localhost:5000/trigger-call
```
