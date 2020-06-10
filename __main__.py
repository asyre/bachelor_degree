import sys
import os

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

if sys.argv[0].endswith("__main__.py"):
    import os.path

    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    # (it's just a hint anyway)
    # (if you have spaces in your executable you get what you deserve!)
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m diploma"
    del os

from executor.main import main
from executor.scheduler import create_scheduler_from_string

__pyroutertest = True


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


import argparse

parser = argparse.ArgumentParser(description='PyRouterTest runner')
parser.add_argument('dist', action="store", help="dist")
parser.add_argument('-ip', action="store", help="...", type=str, dest="include_path")
parser.add_argument('-in', action="store", help="...", type=str, dest="include_name")
parser.add_argument('-sp', action="store", help="...", type=str, dest="skip_path")
parser.add_argument('-sn', action="store", help="...", type=str, dest="skip_name")
parser.add_argument('-a', action="store", help="...", type=str, dest="allure")
parser.add_argument('-r', action="store", help="...", type=str, dest="report")
parser.add_argument('--silent', action="store", help="...", nargs='?', const=True, type=str2bool, dest="silent",
                    default=False)
parser.add_argument('--scheduler', action="store", help="...", type=str, dest="scheduler", default="priority")

args = parser.parse_args()
print(args)
# TODO добавить обработку ошибок
args.scheduler = create_scheduler_from_string(args.scheduler)

main(scheduler=args.scheduler,
     report_dir=args.report,
     allure_dir=args.allure,
     log_enabled=not args.silent,
     path_include_reg=args.include_path,
     name_include_reg=args.include_name,
     path_exclude_reg=args.skip_path,
     name_exclude_reg=args.skip_name
     )
