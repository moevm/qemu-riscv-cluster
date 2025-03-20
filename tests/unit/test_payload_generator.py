import os
import pytest
import sys

from src.utils.payload_generator import PayloadGenerator

@pytest.mark.unit
def test_generate_binary_file(tmpdir):
    file_path = os.path.join(tmpdir, "test_binary.bin")
    
    generator = PayloadGenerator(size=1024, file_type="binary")
    generated_path = generator.generate(path=file_path)

    assert os.path.exists(generated_path)
    assert os.path.getsize(generated_path) == 1024

@pytest.mark.unit
def test_generate_text_file(tmpdir):
    file_path = os.path.join(tmpdir, "test_text.txt")
    
    generator = PayloadGenerator(size=1024, file_type="text")
    generated_path = generator.generate(path=file_path)

    assert os.path.exists(generated_path)
    assert os.path.getsize(generated_path) == 1024

@pytest.mark.unit
def test_generate_file_with_range(tmpdir):
    file_path = os.path.join(tmpdir, "test_range.bin")
    
    generator = PayloadGenerator(min_size=1024, max_size=2048, file_type="binary")
    generated_path = generator.generate(path=file_path)

    assert os.path.exists(generated_path)
    assert 1024 <= os.path.getsize(generated_path) <= 2048

@pytest.mark.unit
def test_generate_file_mb(tmpdir):
    file_path = os.path.join(tmpdir, "test_mb.txt")
    
    generator = PayloadGenerator(size=5, file_type="text", unit="MB")
    generated_path = generator.generate(path=file_path)

    assert os.path.exists(generated_path)
    assert os.path.getsize(generated_path) == 5 * 1024 * 1024

@pytest.mark.unit
def test_generate_file_with_invalid_type():
    with pytest.raises(ValueError, match="Invalid unit of measurement"):
        PayloadGenerator(size=1024, file_type="binary", unit="GB")

@pytest.mark.unit
def test_generate_file_with_negative_size():
    with pytest.raises(ValueError, match="size cannot be negative"):
        PayloadGenerator(size=-1024, file_type="binary")

@pytest.mark.unit
def test_generate_file_with_invalid_range():
    with pytest.raises(ValueError, match="min_size should be <= max_size"):
        PayloadGenerator(min_size=1024, max_size=512, file_type="binary")