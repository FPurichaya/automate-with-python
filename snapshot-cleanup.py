import boto3
import schedule
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name="ap-southeast-1")

def cleanup_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            }
        ]
    )

    for volume in volumes['Volumes']:
        snapshots = ec2_client.describe_snapshots(
            OwnerIds=['self'],
            Filters=[
                {
                    'Name': 'volume-id',
                    'Values': [volume['VolumeId']]
                }
            ]
        )

    sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    for snap in sorted_by_date[2:]:
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print(response)

schedule.every(20).seconds.do(cleanup_volume_snapshots)

while True:
    schedule.run_pending()
