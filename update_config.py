import configparser


def update_config_version():
    latest_config = {'information': '',
                     'number': 0,
                     'model': 'unzip',
                     'nested_folders': 'True',
                     'nested_zip': False,
                     'delete_zip': True,
                     'check_zip': True,
                     'multithreading': '',
                     'skip_suffix': '',
                     'unzip_to_folder': ''
                     }

    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')

    for key in latest_config:
        if key not in config['DEFAULT']:
            config.set('DEFAULT', key, latest_config[key])

    config.write(open('config.ini', 'w', encoding='utf-8'))
