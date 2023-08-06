from src import _internal




def parse():
    import configparser
    import os

    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Get the directory containing the current file
    current_dir = os.path.dirname(current_file_path)

    # Traverse up the directory hierarchy until we find a directory containing a file named 'requirements.txt'
    while not os.path.exists(os.path.join(current_dir, 'requirements.txt')):
        current_dir = os.path.dirname(current_dir)

    # The root directory of the project is the parent directory of the directory containing 'requirements.txt'
    root_dir = os.path.dirname(current_dir)
    config = configparser.ConfigParser()
    config.read(f'{root_dir}/config.ini')

    endpoint = config.get('Data', 'endpoint')
    uuid = config.get('Data', 'uuid')
    launch_name = config.get('Data', 'launch_name')
    project = config.get('Data', 'project')

    _internal.Data.endpoint = endpoint
    _internal.Data.uuid = uuid
    _internal.Data.launch_name = launch_name 
    _internal.Data.project = project
    _internal.Data.update_url()