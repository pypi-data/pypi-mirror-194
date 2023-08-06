import argparse
from ._internal import start_launch
HOST = ''
LAUNCH_NAME = ''
UUID = ''
PROJECT = ''

def config():
    parser = argparse.ArgumentParser(description='Pytest Report Portal Wrapper')
    parser.add_argument('--host', '-H', default='localhost', help='host:ip or domain name (Example: localhost:8080)')
    parser.add_argument('--launch-name', '-l', default='new launch' ,help='New launch name ( default is "new launch" )')
    parser.add_argument('--bearer-uuid', '-u', required=True, help='Auth bearer UUID')
    parser.add_argument('--project-name', '-p', required=True, help='Report Portal project name')
    args = parser.parse_args()
    global HOST
    global LAUNCH_NAME
    global UUID
    global PROJECT
    HOST = args.host
    LAUNCH_NAME = args.launch_name
    UUID = args.bearer_id
    PROJECT = args.project_name


if __name__ == '__main__':
    config()
    start_launch()
    
