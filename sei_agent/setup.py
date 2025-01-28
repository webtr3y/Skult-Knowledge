from pathlib import Path
import os

def setup_project():
    # Define base directory
    base_dir = Path("sei_agent")
    
    # Create directory structure
    directories = [
        "app/api",
        "app/config",
        "app/middleware",
        "app/utils",
        "app/services/protocol_trackers",
        "app/models",
        "tests/test_api",
        "logs"
    ]
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py files
        init_file = dir_path / "__init__.py"
        init_file.touch(exist_ok=True)

if __name__ == "__main__":
    setup_project() 