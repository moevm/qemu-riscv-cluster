import os
import pytest

import sys
from src.utils.payload_generator import PayloadGenerator

@pytest.mark.unit
def test_generate_binary_file(tmpdir):
    generator = PayloadGenerator(size=1024, file_type="binary")
    file_path = generator.generate(output_dir=tmpdir, filename="test_binary.bin")

    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) == 1024

@pytest.mark.unit
def test_generate_text_file(tmpdir):
    generator = PayloadGenerator(size=1024, file_type="text")
    file_path = generator.generate(output_dir=tmpdir, filename="test_text.txt")

    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) == 1024

@pytest.mark.unit
def test_generate_file_with_range(tmpdir):
    generator = PayloadGenerator(min_size=1024, max_size=2048, file_type="binary")
    file_path = generator.generate(output_dir=tmpdir, filename="test_range.bin")

    assert os.path.exists(file_path)
    assert 1024 <= os.path.getsize(file_path) <= 2048

@pytest.mark.unit
def test_generate_file_mb(tmpdir):
    generator = PayloadGenerator(size=5, file_type="text", unit="MB")
    file_path = generator.generate(output_dir=tmpdir, filename="test_range.bin")

    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) == 5242880

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