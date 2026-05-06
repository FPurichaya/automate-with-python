import requests
import smtplib
import os
import paramiko
import linode_api4
import schedule
import time
from linode_api4 import LinodeClient, Instance, ApiError

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
HOSTNAME = os.environ.get('HOSTNAME')
USERNAME = os.environ.get('USERNAME')
KEY_FILENAME = os.environ.get('KEY_FILENAME')

def restart_server_and_container():
    # restart linode server
    print('Rebooting the server...')
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 97194100)
    nginx_server.reboot()
    # restart application
    while True:
        nginx_server = client.load(linode_api4.Instance, 97194100)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break

def send_notification(message):
    print('Sending email to fix the bug...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_container():
        print('Restarting the application...')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_FILENAME, timeout=10)
        stdin, stdout, stderr = ssh.exec_command('docker start 6022e309ca9c')
        print(stdout.readlines())
        ssh.close()

def monitor_application():
    try:
        response = requests.get('http://172.104.160.62:8080/')
        if response.status_code == 200:
            print('Application is running successfully.')
        else:
            print('Application is not running.')
            message = f"Subject: SITE DOWN \n Application returns {response.status_code}. Fix the bug to save the world!"
            send_notification(message)
            restart_container()
    except Exception as ex:
            print(f"Connection Error: {ex}")
            message = f"Subject: SITE DOWN \n Application isn't accessible. Fix the bug to save the world!"
            send_notification(message)
            restart_container()

schedule.every(5).seconds.do(monitor_application)
while True:
    schedule.run_pending()