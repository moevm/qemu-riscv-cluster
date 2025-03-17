import os
import random
import uuid
from typing import Optional, Literal

class PayloadGenerator:
    """
    This class is a payload generator.
    """
    def __init__(
        self,
        size: Optional[int] = None,
        min_size: int = 0,
        max_size: Optional[int] = None,
        file_type: Literal["binary", "text"] = "binary",
        text_charset: str = "abcdefghijklmnopqrstuvwxyz",
        unit: Literal["B", "KB", "MB"] = "B"
    ):
        if unit not in ("B", "KB", "MB"):
            raise ValueError("Invalid unit of measurement. Allowed: 'B', 'KB', 'MB'")
        
        multipliers = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 ** 2
        }
        multiplier = multipliers[unit]

        if size is not None:
            if min_size != 0 or max_size is not None:
                raise ValueError("size cannot be combined with min_size/max_size")
            if size < 0:
                raise ValueError("size cannot be negative")
            self.file_size = size * multiplier
        else:
            if max_size is None:
                raise ValueError("Specify the max_size when using the range")
            if min_size < 0 or max_size < 0:
                raise ValueError("The dimensions cannot be negative")
            if min_size > max_size:
                raise ValueError("min_size should be <= max_size")
            self.file_size = random.randint(min_size, max_size) * multiplier

        self.file_type = file_type
        self.text_charset = text_charset

    def generate(self, output_dir: Optional[str] = None, filename: Optional[str] = None) -> str:
        """
        Generates a file 

        Arguments:

        `output_dir: Optional[str]` - the directory where the file will be located

        `filename: Optional[str]` - file name

        Output data:

        `str` - the string that represents the absolute path
        """
        if filename is None:
            ext = "bin" if self.file_type == "binary" else "txt"
            filename = f"{uuid.uuid4().hex}.{ext}"
        
        filepath = os.path.join(output_dir, filename) if output_dir else filename
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if output_dir else None

        if self.file_type == "binary":
            self._generate_binary(filepath)
        else:
            self._generate_text(filepath)

        return os.path.abspath(filepath)

    def _generate_binary(self, path: str):
        """binary data generation"""
        with open(path, 'wb') as f:
            remaining = self.file_size
            while remaining > 0:
                chunk_size = min(remaining, 4 * 1024 * 1024)
                chunk = os.urandom(chunk_size)
                f.write(chunk)
                remaining -= chunk_size

    def _generate_text(self, path: str):
        """text data generation"""
        charset = self.text_charset
        buffer_size = 128 * 1024
        
        with open(path, 'w', encoding='utf-8') as f:
            remaining = self.file_size
            buffer = []
            current_buffer_size = 0
            while remaining > 0:
                approx_bytes_per_char = 2
                chars_to_generate = max(remaining // approx_bytes_per_char, 1)
                chunk = ''.join(random.choices(charset, k=chars_to_generate))
                encoded = chunk.encode('utf-8')

                if len(encoded) > remaining:
                    encoded = encoded[:remaining]
                    chunk = encoded.decode('utf-8', errors='ignore')
                
                buffer.append(chunk)
                current_buffer_size += len(encoded)
                remaining -= len(encoded)
                
                if current_buffer_size >= buffer_size:
                    f.write(''.join(buffer))
                    buffer = []
                    current_buffer_size = 0

            if buffer:
                f.write(''.join(buffer))

    def get_charset(self):
        return self.text_charset