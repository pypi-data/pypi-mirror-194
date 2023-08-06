import argparse
import configparser
import datetime
from .core import link_files

def parse():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add --link command
    parser.add_argument('--link', action='store_true', help='Link model files')

    # Parse arguments
    args = parser.parse_args()
    return args

def parse_config():
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    # Extract values from configuration.ini
    paths = config['link_section']['path_to_mod_files'].split(',')
    old_names = config['link_section']['old_name_exp'].split(',')
    new_names = config['link_section']['new_name_exp'].split(',')
    date_in = datetime.datetime.strptime(config['link_section']['date_in'], '%Y%m%d').date()
    date_fin = datetime.datetime.strptime(config['link_section']['date_fin'], '%Y%m%d').date()
    time_res = config['link_section']['time_res_model'].split(',')
    out_paths = config['link_section']['path_to_out_model_folder'].split(',')
    return paths, old_names, new_names, date_in, date_fin, time_res, out_paths

if __name__ == '__main__':
    args = parse()

    if args.link:
        paths, old_names, new_names, date_in, date_fin, time_res, out_paths = parse_config()
        link_files(paths, old_names, new_names, date_in, date_fin, time_res, out_paths)
