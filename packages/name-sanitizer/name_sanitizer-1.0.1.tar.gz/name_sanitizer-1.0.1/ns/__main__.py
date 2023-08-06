import argparse, sys, os, subprocess
from ns.config import Config
from ns.sanitizer import Sanitizer

parser = argparse.ArgumentParser()
parser.add_argument('--a', help= 'Anonymize the file name with a random string', nargs='?', const=True, type=bool)
parser.add_argument('--r', help= 'Execute the sanitizer recursive', nargs='?', const=True, type=bool)
parser.add_argument('--only_dir', help='Execute the sanitizer only for directories.', nargs='?', const=True, type=bool)
parser.add_argument('--only_file', help='Execute the sanitizer only for files.', nargs='?', const=True, type=bool)
parser.add_argument('--extensions', help='Define extensions of files renamed. Extensions required be separated by commas', type=str)
args = parser.parse_args()
launch_path = os.getcwd()
config = Config(launch_path, args.a, args.r, args.only_dir, args.only_file, args.extensions)
sanitizer = Sanitizer(config)
sanitizer.start()