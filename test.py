#/usr/bin/python
import sys

from optparse import make_option, OptionParser
def print_help(self, prog_name, subcommand):
    parser = self.create_parser(prog_name, subcommand)
    parser.print_help()



def parse_cmdline(prog_name):
    """Parses the relevant cmdline arguments
    """
    option_list = (
        make_option('-v', '--verbosity', action='store', dest='verbosityddddddd', default='1',
            type='choice', choices=['0', '1', '2', '3'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output'),
        make_option('--settings',
            help='The Python path to a settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.'),
        make_option('--pythonpath',
            help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".'),
        make_option('--traceback', action='store_true',
            help='Raise on exception'),
    )
 
    return OptionParser(prog=prog_name,
                            usage='',
                            version='1.0.1',
                            option_list=option_list)

if __name__ == "__main__":

    options, args = parse_cmdline(sys.argv[0]).parse_args(sys.argv[1:])

    print options
    print args

 
