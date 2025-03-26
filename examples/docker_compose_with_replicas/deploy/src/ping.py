import os
import time


def main():
    hostname = "deploy-central_node-1"
    time.sleep(10)
    response = os.system(f"ping -c 1 {hostname}")
    time.sleep(60)
    return response

if __name__ == "__main__":
    main()
