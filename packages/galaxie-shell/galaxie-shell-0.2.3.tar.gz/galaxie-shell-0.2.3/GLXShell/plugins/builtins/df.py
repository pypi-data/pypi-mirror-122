# http://pwet.fr/man/linux/commandes/posix/touch/
# https://www.maizure.org/projects/decoded-gnu-coreutils/df.html
# https://pubs.opengroup.org/onlinepubs/9699919799/utilities/df.html

import math
import os
from argparse import RawDescriptionHelpFormatter

import cmd2
from tabulate import tabulate

from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

df_parser = cmd2.Cmd2ArgumentParser(
    description="The df utility shall write the amount of available space and file slots for file systems on which "
                "the invoking user has appropriate read access. File systems shall be specified by the file operands; "
                "when none are specified, information shall be written for all file systems. The format of the "
                "default output from df is unspecified, but all space figures are reported in 512-byte units, "
                "unless the -k option is specified. This output shall contain at least the file system names, "
                "amount of available space on each of these file systems, and, if no options other than -t are "
                "specified, the number of free file slots, or inodes, available; when -t is specified, the output "
                "shall contain the total allocated space as well.",
    add_help=False,
    formatter_class=RawDescriptionHelpFormatter
)
#      --help               display this help and exit
#      --version            output version information and exit
df_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)
df_parser.add_argument('--help',
                       action='store_true',
                       help="display this help and exit"
                       )
df_parser.add_argument(
    "-h",
    dest="human_readable",
    action="store_true",
    default=False,
    help="print sizes in powers of 1024 (e.g., 1023M)",
)
df_parser.add_argument(
    "-k",
    dest="kilo",
    action='store_const', const=1024,
    help="use 1024-byte units, instead of the default 512-byte units, when writing space figures.",
)
df_parser.add_argument(
    "-P",
    dest="portability",
    action="store_true",
    default=True,
    help="produce a POSIX output",
)
df_parser.add_argument(
    "-t",
    dest="total",
    action="store_true",
    help="include total allocated-space figures in the output. ",
)
df_parser.add_argument(
    "file",
    completer=cmd2.Cmd.path_complete,
    nargs="?",
    const=0,
    help="A pathname of a file within the hierarchy of the desired file system. If a file other than a FIFO, "
         "a regular file, a directory, or a special file representing the device containing the file system (for "
         "example, /dev/dsk/0s1) is specified, the results are unspecified. If the file operand names a "
         "file other than a special file containing a file system, df shall write the amount of free space in the "
         "file system containing the specified file operand. Otherwise, df shall write the amount of free space in "
         "that file system. ",
)


class GLXDf(cmd2.CommandSet):
    def __init__(self):
        super().__init__()
        # Internal Variables

    @staticmethod
    def df_print_help():
        df_parser.print_help()

    @staticmethod
    def df_print_version():
        cmd2.Cmd().poutput(
            "df ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    def df(self, file=None, block_size=None, total=None, human_readable=None):
        """Exit this application"""
        # Return True to stop the command loop
        if block_size is None:
            block_size = 512

        devices_list = []
        if file:
            if not os.path.exists(file):
                cmd2.Cmd().perror(f"df: {file}: No such file or directory")
                cmd2.cmd2.last_result = 1
                return True

            if not os.access(file, os.R_OK) or not os.access(self.df_find_mount_point(file),
                                                             os.R_OK):  # pragma: no cover
                cmd2.Cmd().perror(f"df: {file}: Permission denied")
                cmd2.cmd2.last_result = 1
                return True

            for line in self.df_get_devices():
                if self.df_find_mount_point(file) == line[1]:
                    devices_list.append(self.df_get_device_information(
                        file_system_name=line[0],
                        file_system_root=line[1],
                        block_size=block_size,
                    ))

        else:
            for line in self.df_get_devices():
                devices_list.append(self.df_get_device_information(
                    file_system_name=line[0],
                    file_system_root=line[1],
                    block_size=block_size,
                ))

        if devices_list:
            if total:
                total_space_free, total_space_used, total_total_space = self.df_get_totals(
                    devices_list
                )

                devices_list.append(
                    ["total",
                     total_total_space,
                     total_space_used,
                     total_space_free,
                     "%d%%" % int(math.ceil(100 * (float(total_total_space - total_space_free) / total_total_space))),
                     "-"]
                )

            block_size_text, tabular_data = self.df_get_info_to_print(
                block_size,
                devices_list,
                human_readable
            )

            self.df_print_final(block_size_text, tabular_data)

            cmd2.cmd2.last_result = 0
        else:
            cmd2.cmd2.last_result = 1
        return True

    def df_get_info_to_print(self, block_size, devices_list, human_readable):
        block_size_text = f"{block_size}-blocks"
        if human_readable:
            tabular_data = []
            block_size_text = "Size"
            for line in devices_list:
                if str(line[1]) != '-' and str(line[2]) != '-' and str(line[3]) != '-':
                    tabular_data.append([line[0],
                                         self.sizeof(int(line[1]) * block_size),
                                         self.sizeof(int(line[2]) * block_size),
                                         self.sizeof(int(line[3]) * block_size),
                                         line[4],
                                         line[5]]
                                        )
                else:
                    tabular_data.append(line)
        else:
            tabular_data = devices_list

        return block_size_text, tabular_data

    @staticmethod
    def df_get_totals(devices_list):
        total_total_space = 0
        total_space_used = 0
        total_space_free = 0
        for device in devices_list:
            try:
                total_total_space += int(device[1])
            except ValueError:
                pass
            try:
                total_space_used += int(device[2])
            except ValueError:
                pass
            try:
                total_space_free += int(device[3])
            except ValueError:
                pass
        return total_space_free, total_space_used, total_total_space

    @staticmethod
    def df_print_final(block_size_text, tabular_data):
        cmd2.Cmd().poutput(
            tabulate(
                tabular_data=tabular_data,
                headers=["Filesystem",
                         block_size_text,
                         "Used",
                         "Available",
                         "Capacity",
                         "Mounted on"],
                tablefmt="plain",
                colalign=("left", "right", "right", "right", "right", "left")
            )
        )

    @cmd2.with_argparser(df_parser)
    @cmd2.with_category("Builtins")
    def do_df(self, args):

        if args.version:  # pragma: no cover
            self.df_print_version()
            cmd2.cmd2.last_result = 0
            return

        if args.help:  # pragma: no cover
            self.df_print_help()
            cmd2.cmd2.last_result = 0
            return

        self.df(
            file=args.file,
            block_size=args.kilo,
            total=args.total,
            human_readable=args.human_readable,
        )  # pragma: no cover

    @staticmethod
    def df_find_mount_point(path):
        if not os.path.islink(path):
            path = os.path.abspath(path)
        elif os.path.islink(path) and os.path.lexists(os.readlink(path)):  # pragma: no cover
            path = os.path.realpath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
            if os.path.islink(path) and os.path.lexists(os.readlink(path)):  # pragma: no cover
                path = os.path.realpath(path)
        return path

    @staticmethod
    def df_get_device_information(
            file_system_name=None,
            file_system_root=None,
            block_size=None):
        try:
            statvfs = os.statvfs(file_system_root)
            space_free = statvfs.f_bavail * statvfs.f_frsize / block_size
            total_space = statvfs.f_blocks * statvfs.f_frsize / block_size
            space_used = total_space - space_free
            if total_space == 0:
                percentage_used = '-'
            else:
                percentage_used = "%d%%" % int(math.ceil(100 * (float(total_space - space_free) / total_space)))

            return ["%s" % file_system_name,
                    "%d" % total_space,
                    "%d" % space_used,
                    "%d" % space_free,
                    "%s" % percentage_used,
                    "%s" % file_system_root,
                    ]
        except PermissionError:  # pragma: no cover
            return ["%s" % file_system_name,
                    "%s" % '-',
                    "%s" % '-',
                    "%s" % '-',
                    "%s" % '-',
                    "%s" % file_system_root,
                    ]

    def df_get_devices(self, file=None):
        if file is None and os.path.exists('/etc/mtab'):
            file = '/etc/mtab'
        if file is None and os.path.exists('/proc/mounts'):  # pragma: no cover
            file = '/proc/mounts'
        if file is None:  # pragma: no cover
            raise SystemError("Impossible to locate /etc/mtab or /proc/mounts file")

        file_entries = []
        for line in self.get_file_content(file=file).splitlines():
            if len(line.split()) < 4:  # pragma: no cover
                continue
            file_entries.append(line.split())
        return file_entries

    @staticmethod
    def get_file_content(file=None):
        if not os.path.exists(file):
            raise FileExistsError(f"{file} do not exist")
        if not os.access(file, os.R_OK):  # pragma: no cover
            raise PermissionError(f"{file} can't be read")

        with open(file) as datafile:
            return datafile.read().strip()

    @staticmethod
    def sizeof(value=None):
        """
        Convert a num to a human readable thing it use metric prefix.

        :param value: a ``value`` to translate for a future display
        :type value: int or float
        :return: str
        :raise TypeError: when ``value`` argument is not a int or float
        """
        #     Metric prefixes in everyday use:
        #
        #     yotta	Y	1000000000000000000000000	10 power 24
        #     zetta	Z	1000000000000000000000	10 power 21
        #     exa	E	1000000000000000000	10 power 18
        #     peta	P	1000000000000000	10 power 15
        #     tera	T	1000000000000	10 power 12
        #     giga	G	1000000000	10 power 9
        #     mega	M	1000000	10 power 6
        #     kilo	k	1000	10 power 3
        #     (none)	(none)	1	10 power 0

        # Exit a soon of possible
        if type(value) != int and type(value) != float and type(value) != int:
            raise TypeError("'value' must be a int or float type")

        suffix = ["", "k", "M", "G", "T", "P", "E", "Z", "Y"]
        i = 0 if value < 1 else int(math.log(value, 1024)) + 1
        v = value / math.pow(1024, i)
        v, i = (v, i) if v > 0.5 else (v * 1024, (i - 1 if i else 0))

        return str(str(int(round(v, 0))) + suffix[i])
