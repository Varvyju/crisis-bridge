import sys
import os
import pytest
from PIL import Image

# Add root directory to python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import AegisCore

def test_parse_ai_response_valid_json():
    """Testing JSON is successfully extracted without markdown tags."""
    raw_response = '''```json
    {
        "CrisisType": "Medical",
        "SeverityLevel": "High",
        "Location": "Central Station"
    }
    ```'''
    result = AegisCore.parse_ai_response(raw_response)
    assert result["CrisisType"] == "Medical"
    assert result["SeverityLevel"] == "High"
    assert result["Location"] == "Central Station"

def test_parse_ai_response_raw_dict():
    """Testing raw dict string without markdown parses successfully."""
    raw_response = '''{
        "CrisisType": "Fire",
        "SeverityLevel": "Critical",
        "Location": "Building A"
    }'''
    result = AegisCore.parse_ai_response(raw_response)
    assert result["CrisisType"] == "Fire"
    assert result["SeverityLevel"] == "Critical"

def test_optimize_image_rescaling(tmp_path):
    """Testing that an image is properly downscaled for performance."""
    # Create a dummy large image
    image = Image.new('RGB', (2000, 2000), color = 'red')
    
    # Process it
    optimized_img = AegisCore.optimize_image(image, max_size=(500, 500))
    
    # Assert size was constrained
    assert optimized_img.size[0] <= 500
    assert optimized_img.size[1] <= 500

def test_parse_ai_response_invalid_json(mocker):
    """Testing error handling when the LLM returns completely invalid JSON."""
    raw_response = "I couldn't parse this crisis."
    
    # We expect a json decode error
    # We expect a json decode error
    import json
    with pytest.raises(json.JSONDecodeError):
        AegisCore.parse_ai_response(raw_response)

def test_upload_evidence_auth_failure(mocker):
    """Testing that failure in GCS storage returns None without crashing the app."""
    # Mock cloud_auth to True to enter the function
    mocker.patch('app.cloud_auth', True)
    # Mock the Client to throw an explicit error simulating missing ADC credentials
    mocker.patch('app.cloud_storage.Client', side_effect=Exception("Missing standard Google credentials"))
    
    img = Image.new('RGB', (100, 100), color='blue')
    result = AegisCore.upload_evidence(img)
    
    assert result is None

def test_translate_protocol_exception_fallback(mocker):
    """Testing that if Google Translate times out, it gracefully returns the original text."""
    mocker.patch('app.cloud_auth', True)
    # Mock translation throw
    mocker.patch('app.translate.Client', side_effect=Exception("Timeout Connection Refused"))
    
    original_text = "Step 1: Extinguish Fire."
    result = AegisCore.translate_protocol(original_text, target_lang="es")
    
    # Needs to fallback to exact original text
    assert result == "Step 1: Extinguish Fire."
    
def test_translate_protocol_success(mocker):
    """Testing successful translation path via mocks."""
    mocker.patch('app.cloud_auth', True)
    
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.translate.return_value = {'translatedText': 'Paso 1: Extinguir Fuego'}
    
    mocker.patch('app.translate.Client', return_value=mock_client_instance)
    
    result = AegisCore.translate_protocol("Step 1: Extinguish Fire.", target_lang="es")
    
    assert result == 'Paso 1: Extinguir Fuego'
