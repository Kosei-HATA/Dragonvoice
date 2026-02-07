import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Mock libraries NOT present in the env to avoid ImportErrors
sys.modules["TTS"] = MagicMock()
sys.modules["TTS.api"] = MagicMock()
sys.modules["pedalboard"] = MagicMock()
sys.modules["pedalboard.io"] = MagicMock()
sys.modules["scipy"] = MagicMock()
sys.modules["scipy.io"] = MagicMock()
sys.modules["scipy.io.wavfile"] = MagicMock()

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import app
from fastapi.testclient import TestClient
from app.main import app

class TestDragonAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
    @patch("app.services.tts_service.tts_service.generate_raw_audio")
    @patch("app.services.dsp_service.dsp_service.process_audio")
    def test_generate_dragon(self, mock_process, mock_generate):
        # Setup mocks
        mock_generate.return_value = ([0.1] * 100, 24000)
        mock_process.return_value = b"RIFF____WAVEfmt ____data____" # Dummy WAV header
        
        print("\nTesting /v1/generate_dragon endpoint...")
        response = self.client.post(
            "/v1/generate_dragon",
            json={"text": "Test Dragon", "language": "en"}
        )
        
        # Check status
        print(f"Status Code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        
        # Check content type
        print(f"Content-Type: {response.headers['content-type']}")
        self.assertEqual(response.headers["content-type"], "audio/wav")
        
        # Check body
        self.assertTrue(response.content.startswith(b"RIFF"))
        print("Response validation successful.")

    def test_empty_text(self):
        print("\nTesting empty text validation...")
        response = self.client.post(
            "/v1/generate_dragon",
            json={"text": "", "language": "en"}
        )
        self.assertEqual(response.status_code, 400)
        print("Empty text rejected correctly (400 Bad Request).")

if __name__ == '__main__':
    unittest.main()
