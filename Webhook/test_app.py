import unittest
from unittest.mock import patch, MagicMock
import json
from app import app

class TestWebhookApp(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.Client')
    def test_trigger_call_success(self, mock_client):
        """Test successful call triggering"""
        # Mock Twilio client
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        # Mock call creation
        mock_call = MagicMock()
        mock_call.sid = 'test_call_sid_123'
        mock_client_instance.calls.create.return_value = mock_call
        
        # Test GET request
        response = self.app.get('/trigger-call')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('Call initiated with SIDs', response.get_data(as_text=True))
        
        # Verify Twilio client was called
        mock_client.assert_called_once()
        mock_client_instance.calls.create.assert_called()

    @patch('app.Client')
    def test_trigger_call_post(self, mock_client):
        """Test POST request to trigger call"""
        # Mock Twilio client
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        # Mock call creation
        mock_call = MagicMock()
        mock_call.sid = 'test_call_sid_456'
        mock_client_instance.calls.create.return_value = mock_call
        
        # Test POST request
        response = self.app.post('/trigger-call')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('Call initiated with SIDs', response.get_data(as_text=True))

    @patch('app.Client')
    def test_multiple_calls(self, mock_client):
        """Test multiple call creation"""
        # Mock Twilio client
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        # Mock multiple calls
        mock_calls = [MagicMock(), MagicMock()]
        mock_calls[0].sid = 'call_sid_1'
        mock_calls[1].sid = 'call_sid_2'
        mock_client_instance.calls.create.side_effect = mock_calls
        
        # Test request
        response = self.app.get('/trigger-call')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('call_sid_1', response_text)
        self.assertIn('call_sid_2', response_text)
        
        # Verify multiple calls were made
        self.assertEqual(mock_client_instance.calls.create.call_count, 2)

    @patch('app.Client')
    def test_call_failure(self, mock_client):
        """Test handling of call failures"""
        # Mock Twilio client to raise exception
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.calls.create.side_effect = Exception("Twilio error")
        
        # Test request - should handle exception gracefully
        response = self.app.get('/trigger-call')
        
        # The app doesn't have explicit error handling, so this test
        # documents current behavior
        self.assertEqual(response.status_code, 500)

    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404"""
        response = self.app.get('/invalid-endpoint')
        self.assertEqual(response.status_code, 404)

    def test_health_check(self):
        """Test basic health check endpoint"""
        # This would require adding a health check endpoint to app.py
        response = self.app.get('/health')
        # Currently returns 404 since endpoint doesn't exist
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)