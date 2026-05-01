import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='ap-southeast-1')
ec2 = boto3.resource('ec2', region_name='ap-southeast-1')

def check_instance_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    for status in statuses['InstanceStatuses']:
        int_status = status['InstanceStatus']['Status']
        sys_status = status['InstanceStatuses']['Status']
        state = status['InstanceStatuses']['State']
        print(f"Instance {status['InstanceId']} is {state} with instance status {int_status} and system status {sys_status}")
    print("#######################################\n")
schedule.every(5).minutes.do(check_instance_status)

while True:
    schedule.run_pending()
