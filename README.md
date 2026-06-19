# Automate with Python
This repository contains Python automation projects focused on AWS cloud operations, infrastructure management, Kubernetes administration, and DevOps automation.

## Repository Branches
- feature/basic-ec2: Basic AWS VPC automation with Boto3
- feature/website-monitoring: Implements website health monitoring using Python.
- feature/restore-volume: Automates EBS volume restoration from snapshots.
- feature/auto-cleanup: Automates cleanup of unused cloud resources.
- feature/volume-backups: Automates EBS snapshot creation and backup management.
- feature/eks-with-python: Automates Amazon EKS and Kubernetes operations using Python.

## Prerequisites
### Python
Install Python 3:
```python
brew install python3
python3 --version
```
### Dependencies
Install Dependencies
```python
pip install boto3
```

### AWS Credentials
Configure AWS CLI:
```python
aws configure
```
Required information:
AWS Access Key ID
AWS Secret Access Key
Default Region
Output Format

Verify configuration:
```python
aws sts get-caller-identity
```

### Getting Started
Clone the repository:
```python
git clone https://github.com/FPurichaya/automate-with-python.git
cd automate-with-python
```

Switch to a branch:
```python
git checkout feature/basic-ec2
```

Run the automation script:
```python
python3 main.py
```
