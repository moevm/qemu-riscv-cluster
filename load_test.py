import time
import random
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import start_http_server, Counter, Histogram
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from client.client import FileClient
from utils.payload_generator import PayloadGenerator

load_dotenv(os.path.join(os.path.dirname(__file__), "env", ".grpc.env"))

REQUEST_COUNT = Counter('grpc_requests_total', 'Total gRPC requests')
REQUEST_LATENCY = Histogram('grpc_request_latency_seconds', 'gRPC request latency')
REQUEST_SIZE = Histogram('grpc_request_size_bytes', 'Size of uploaded files')
REQUEST_ERRORS = Counter('grpc_request_errors_total', 'Total gRPC request errors')

def parse_file_size(size_str: str) -> tuple[int, str]:
    """Parse file size string (e.g., '1MB')"""
    size_str = size_str.upper()
    if size_str.endswith('MB'):
        return int(size_str[:-2]), 'MB'
    elif size_str.endswith('KB'):
        return int(size_str[:-2]), 'KB'
    elif size_str.endswith('B'):
        return int(size_str[:-1]), 'B'
    else:
        return int(size_str), 'B'

class LoadTest:
    def __init__(self, num_users=10, duration=300, file_size="1MB", file_type="text"):
        self.num_users = num_users
        self.duration = duration
        self.file_size = file_size
        self.file_type = file_type
        self.results = []
        self.lock = threading.Lock()
        
        self.client = FileClient()
        
        size, unit = parse_file_size(file_size)
        
        self.generator = PayloadGenerator(
            size=size,
            file_type=self.file_type,
            unit=unit
        )

    def make_request(self):
        start_time = time.time()
        try:
            file_path = self.generator.generate()
            
            response = self.client.upload_and_validate(file_path, self.file_type)
            
            latency = time.time() - start_time
            REQUEST_COUNT.inc()
            REQUEST_LATENCY.observe(latency)
            REQUEST_SIZE.observe(response.size)
            
            with self.lock:
                self.results.append(latency)
                
            os.remove(file_path)
                
        except Exception as e:
            print(f"Error making request: {e}")
            REQUEST_ERRORS.inc()

    def user_loop(self):
        end_time = time.time() + self.duration
        while time.time() < end_time:
            self.make_request()
            time.sleep(1.0 / self.num_users)  # Rate limiting

    def run(self):
        print(f"Starting load test with {self.num_users} users for {self.duration} seconds")
        print(f"Test file size: {self.file_size}")
        print(f"Test file type: {self.file_type}")
        start_time = time.time()
        
        #start Prometheus metrics server
        start_http_server(8000)
        
        #start user threads
        with ThreadPoolExecutor(max_workers=self.num_users) as executor:
            futures = [executor.submit(self.user_loop) for _ in range(self.num_users)]
            for future in futures:
                future.result()
        
        if self.results:
            avg_latency = statistics.mean(self.results)
            p95_latency = statistics.quantiles(self.results, n=20)[18]  # 95th percentile
            p99_latency = statistics.quantiles(self.results, n=100)[98]  # 99th percentile
            
            print("\nTest Results:")
            print(f"Total Requests: {len(self.results)}")
            print(f"Average Latency: {avg_latency:.3f}s")
            print(f"95th Percentile: {p95_latency:.3f}s")
            print(f"99th Percentile: {p99_latency:.3f}s")
            print(f"Total Duration: {time.time() - start_time:.2f}s")

if __name__ == '__main__':
    num_users = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    file_size = sys.argv[3] if len(sys.argv) > 3 else "1MB"
    file_type = sys.argv[4] if len(sys.argv) > 4 else "text"
    
    test = LoadTest(num_users, duration, file_size, file_type)
    test.run() 