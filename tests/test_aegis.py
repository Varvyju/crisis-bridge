import sys
import os
import pytest
from PIL import Image

# Add root directory to python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import parse_ai_response, optimize_image

def test_parse_ai_response_valid_json():
    """Testing JSON is successfully extracted without markdown tags."""
    raw_response = '''```json
    {
        "CrisisType": "Medical",
        "SeverityLevel": "High",
        "Location": "Central Station"
    }
    ```'''
    result = parse_ai_response(raw_response)
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
    result = parse_ai_response(raw_response)
    assert result["CrisisType"] == "Fire"
    assert result["SeverityLevel"] == "Critical"

def test_optimize_image_rescaling(tmp_path):
    """Testing that an image is properly downscaled for performance."""
    # Create a dummy large image
    image = Image.new('RGB', (2000, 2000), color = 'red')
    
    # Process it
    optimized_img = optimize_image(image, max_size=(500, 500))
    
    # Assert size was constrained
    assert optimized_img.size[0] <= 500
    assert optimized_img.size[1] <= 500

def test_parse_ai_response_invalid_json(mocker):
    """Testing error handling when the LLM returns completely invalid JSON."""
    raw_response = "I couldn't parse this crisis."
    
    # We expect a json decode error
    import json
    with pytest.raises(json.JSONDecodeError):
        parse_ai_response(raw_response)
