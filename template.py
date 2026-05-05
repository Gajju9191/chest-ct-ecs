import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "cnnClassifier"

# List of files and folders to create
list_of_files = [
    # Source code structure
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    
    # Configuration files
    "config/config.yaml",
    "params.yaml",
    
    # Application files
    "requirements.txt",
    "setup.py",
    "app.py",
    "Dockerfile",
    
    # Infrastructure as Code
    "terraform/main.tf",
    "terraform/variables.tf",
    "terraform/outputs.tf",
    
    # CI/CD Pipeline
    "jenkins/Jenkinsfile",
    
    # Web templates
    "templates/index.html",
    
    # Research
    "research/trials.ipynb",
]

# Create directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    # Create directory if it has a path
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")
    
    # Create empty file if it doesn't exist
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filename}")

# Create data directories
data_directories = [
    "data/raw",
    "data/processed", 
    "data/test",
    "models",
    "logs",
    "uploads",
    "scripts",
    "notebooks"
]

for dir_path in data_directories:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    logging.info(f"Creating directory: {dir_path}/")

# Create .gitkeep files to preserve empty directories
gitkeep_files = [
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/test/.gitkeep",
    "models/.gitkeep",
    "logs/.gitkeep",
    "uploads/.gitkeep"
]

for gitkeep in gitkeep_files:
    Path(gitkeep).touch(exist_ok=True)
    logging.info(f"Creating: {gitkeep}")

logging.info("\n" + "="*60)
logging.info("Project structure created successfully!")
logging.info("="*60)