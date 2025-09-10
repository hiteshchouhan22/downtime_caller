from flask import Flask, jsonify, request, render_template
from twilio.rest import Client
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with comprehensive HTML instruction page"""
    # Check environment variables status
    missing_vars = []
    if not os.getenv('TWILIO_ACCOUNT_SID'):
        missing_vars.append('TWILIO_ACCOUNT_SID')
    if not os.getenv('TWILIO_AUTH_TOKEN'):
        missing_vars.append('TWILIO_AUTH_TOKEN')
    if not os.getenv('TWILIO_PHONE_NUMBER'):
        missing_vars.append('TWILIO_PHONE_NUMBER')
    if not os.getenv('PHONE_NUMBERS'):
        missing_vars.append('PHONE_NUMBERS')
    
    if missing_vars:
        env_status = f'''
        <div class="warning">
            <span class="status-indicator status-warning"></span>
            <strong>⚠️ Missing Environment Variables:</strong><br>
            {', '.join(missing_vars)}<br>
            <strong>Action Required:</strong> Configure these variables before using the service
        </div>
        '''
    else:
        env_status = '''
        <div class="success">
            <span class="status-indicator status-running"></span>
            <strong>✅ All Environment Variables Configured!</strong><br>
            Service is ready to handle downtime alerts
        </div>
        '''
    
    return render_template('index.html', env_status=env_status)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Downtime Caller Webhook',
        'version': '1.0.0'
    }), 200

@app.route('/trigger-call', methods=['GET', 'POST'])
def trigger_call():
    try:
        # Get credentials from environment variables or use defaults
        account_sid = os.getenv('TWILIO_ACCOUNT_SID', '<acc-sid>')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN', '<acc-auth>')
        
        # Validate credentials
        if account_sid == '<acc-sid>' or auth_token == '<acc-auth>':
            logger.warning("Using default Twilio credentials - please set environment variables")
            return jsonify({
                'error': 'Twilio credentials not configured',
                'message': 'Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables',
                'help': 'Visit http://localhost:5000/ for complete setup instructions'
            }), 400
        
        client = Client(account_sid, auth_token)

        # List of numbers to call - can be configured via environment variable
        numbers_env = os.getenv('PHONE_NUMBERS', '')
        if numbers_env:
            numbers_to_call = [num.strip() for num in numbers_env.split(',')]
        else:
            numbers_to_call = ['<number>', '<number>']  # Default placeholder
        
        # Validate phone numbers
        if not numbers_to_call or numbers_to_call == ['<number>', '<number>']:
            return jsonify({
                'error': 'Phone numbers not configured',
                'message': 'Please set PHONE_NUMBERS environment variable with comma-separated phone numbers',
                'help': 'Visit http://localhost:5000/ for complete setup instructions'
            }), 400
        
        call_sids = []  # To store Call SIDs
        errors = []  # To store any errors

        for number in numbers_to_call:
            try:
                call = client.calls.create(
                                twiml='<Response><Say>Alert: Service monitoring detected downtime. Please check your systems immediately.</Say></Response>',
                                to=number,
                                from_=os.getenv('TWILIO_PHONE_NUMBER', '<twilio-number>')
                            )
                call_sids.append(call.sid)
                logger.info(f"Call initiated successfully to {number}: {call.sid}")
            except Exception as e:
                error_msg = f"Failed to call {number}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)

        # Prepare response
        response_data = {
            'success': len(call_sids) > 0,
            'calls_initiated': len(call_sids),
            'call_sids': call_sids,
            'errors': errors,
            'timestamp': logger.info.__defaults__[0] if hasattr(logger.info, '__defaults__') else 'N/A'
        }
        
        if call_sids:
            call_sids_str = ', '.join(call_sids)
            response_data['message'] = f"Successfully initiated {len(call_sids)} call(s) with SIDs: {call_sids_str}"
            status_code = 200
        else:
            response_data['message'] = "No calls were initiated successfully"
            response_data['help'] = "Visit http://localhost:5000/ for troubleshooting guide"
            status_code = 500
            
        return jsonify(response_data), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in trigger_call: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'help': 'Visit http://localhost:5000/ for troubleshooting guide'
        }), 500

if __name__ == '__main__':
    logger.info("Starting Downtime Caller Webhook Service...")
    logger.info("=====================================================")
    logger.info("Service will run on http://0.0.0.0:5000")
    logger.info("")
    logger.info("Available Endpoints:")
    logger.info("  GET  /           - Complete setup instructions")
    logger.info("  GET  /health     - Health check")
    logger.info("  POST /trigger-call - Trigger phone calls")
    logger.info("  GET  /trigger-call - Trigger phone calls")
    logger.info("")
    logger.info("Setup Instructions:")
    logger.info("  1. Visit http://localhost:5000/ for complete setup guide")
    logger.info("  2. Configure Twilio environment variables")
    logger.info("  3. Add webhook URL to Uptime Kuma notifications")
    logger.info("")
    
    # Check environment variables and provide helpful warnings
    missing_vars = []
    if not os.getenv('TWILIO_ACCOUNT_SID'):
        missing_vars.append('TWILIO_ACCOUNT_SID')
    if not os.getenv('TWILIO_AUTH_TOKEN'):
        missing_vars.append('TWILIO_AUTH_TOKEN')
    if not os.getenv('TWILIO_PHONE_NUMBER'):
        missing_vars.append('TWILIO_PHONE_NUMBER')
    if not os.getenv('PHONE_NUMBERS'):
        missing_vars.append('PHONE_NUMBERS')
    
    if missing_vars:
        logger.warning("⚠️  Missing Environment Variables:")
        for var in missing_vars:
            logger.warning(f"   - {var}")
        logger.warning("")
        logger.warning("🔧 To configure:")
        logger.warning("   Windows: set VARIABLE_NAME=value")
        logger.warning("   Linux/Mac: export VARIABLE_NAME=value")
        logger.warning("")
        logger.warning("📋 Visit http://localhost:5000/ for detailed setup instructions")
        logger.warning("")
    else:
        logger.info("✅ All environment variables configured!")
        logger.info("")
    
    logger.info("=====================================================")
    logger.info("Starting Flask application...")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error("Please check if port 5000 is available")
