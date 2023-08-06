# http://pwet.fr/man/linux/commandes/posix/touch/
# https://www.maizure.org/projects/decoded-gnu-coreutils/touch.html
# https://pubs.opengroup.org/onlinepubs/9699919799/utilities/touch.html
import argparse

import cmd2

from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

touch_parser = argparse.ArgumentParser(
    description="The touch utility shall change the modification times, access times, or both of files. "
                "The modification time shall be equivalent to the value of the st_mtime member of the stat "
                " structure for a file, as described in the System Interfaces volume of IEEE Std 1003.1-2001; "
                "the access time shall be equivalent to the value of st_atime."
                ""
                "The time used can be specified by the -t time option-argument, the corresponding time fields "
                "of the file referenced by the -r ref_file option-argument, or the date_time operand, as specified "
                "in the following sections. If none of these are specified, touch shall use the current time "
                "(the value returned by the equivalent of the time() function defined in the System Interfaces "
                "volume of IEEE Std 1003.1-2001).")
#      --help               display this help and exit
#      --version            output version information and exit
touch_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)
touch_parser.add_argument(
    "-a",
    dest="access_time",
    help="Change the access time of file. Do not change the modification time unless -m is also specified.",
)
touch_parser.add_argument(
    "-c",
    help="Do not create a specified file if it does not exist. Do not write any diagnostic messages "
         "concerning this condition.",
)
touch_parser.add_argument(
    "-m",
    help="Change the modification time of file. Do not change the access time unless -a is also specified.",
)
touch_parser.add_argument(
    "-r",
    help="Use the corresponding time of the file named by the pathname ref_file instead of the current time.",
)
touch_parser.add_argument(
    "-t",

    help="Use the specified time instead of the current time. The option-argument shall be a decimal number of the form",
)

touch_parser.add_argument(
    "file",
    help="Use the specified time instead of the current time. The option-argument shall be a decimal number of the form"

)


class GLXTouch(cmd2.CommandSet):
    def __init__(self):
        super().__init__()
        # Internal Variables

    @property
    def result(self):
        return True

    @staticmethod
    def touch_print_version():
        cmd2.Cmd().poutput(
            "touch ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    def touch(self, file=None):
        raise NotImplementedError("Touch is not implemented yet ..., use !touch")

    @cmd2.with_argparser(touch_parser)
    @cmd2.with_category("Builtins")
    def do_touch(self, args):
        # print(args.NUMBER)
        if args.version:  # pragma: no cover
            self.touch_print_version()
            return

        if args.file:  # pragma: no cover
            self.touch(file=args.file)
        else:
            touch_parser.print_help()  # pragma: no cover
