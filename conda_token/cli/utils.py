
import os
from .. import repo_config


def condarc_path_args(parser):
    """Add condarc path arguments."""
    config_file_location_group = parser.add_argument_group(
        'Config File Location Selection',
        "Without one of these flags, the user config file at '%s' is used." % repo_config.escaped_user_rc_path
    )
    location = config_file_location_group.add_mutually_exclusive_group()
    location.add_argument(
        "--system",
        action="store_true",
        help="Write to the system .condarc file at '%s'." % repo_config.escaped_sys_rc_path,
    )
    location.add_argument(
        "--env",
        action="store_true",
        help="Write to the active conda environment .condarc file (%s). "
             "If no environment is active, write to the user config file (%s)."
             "" % (
                 os.getenv('CONDA_PREFIX', "<no active environment>").replace("%", "%%"),
                 repo_config.escaped_user_rc_path,
             ),
    )
    location.add_argument(
        "--file",
        action="store",
        help="Write to the given file."
    )
