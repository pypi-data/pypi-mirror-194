import argparse
import _internal


def config():
    parser = argparse.ArgumentParser(description='Pytest Report Portal Wrapper')
    parser.add_argument('--host', '-H', default='localhost', help='host:ip or domain name (Example: localhost:8080)')
    parser.add_argument('--launch-name', '-l', default='new launch' ,help='New launch name ( default is "new launch" )')
    parser.add_argument('--bearer-uuid', '-u', required=True, help='Auth bearer UUID')
    parser.add_argument('--project-name', '-p', required=True, help='Report Portal project name')
    args = parser.parse_args()

    _internal.HOST = args.host
    _internal.LAUNCH_NAME = args.launch_name
    _internal.UUID = args.bearer_id
    _internal.PROJECT = args.project_name


if __name__ == '__main__':
    config()
    _internal.start_launch()
    
