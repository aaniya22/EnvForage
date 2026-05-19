import pytest
from pydantic import ValidationError
from backend.schemas.seed import GenerationRequest

def test_valid_payload_parsing():
    data = {
        "target_os": "linux",
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    request = GenerationRequest(**data)
    assert request.target_os == "linux"
    assert request.framework == "pytorch"
    assert request.cuda_version == "12.1"

def test_invalid_target_os_raises_error():
    data = {
        "target_os": "invalid_os_name",
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        GenerationRequest(**data)

def test_invalid_data_types_raises_error():
    data = {
        "target_os": 12345,
        "framework": "pytorch",
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        GenerationRequest(**data)

def test_missing_required_fields_raises_error():
    data = {
        "cuda_version": "12.1"
    }
    with pytest.raises(ValidationError):
        GenerationRequest(**data)

def test_empty_payload_raises_error():
    with pytest.raises(ValidationError):
        GenerationRequest(**{})
        
