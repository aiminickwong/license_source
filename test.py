import sys

from optparse import OptionParser
def parse_cmdline():
    """Parses the relevant cmdline arguments
    """
    parser = OptionParser()
    parser.add_option("--name",
                      dest="defaults",
                      help="Your Orgnazation Name")
    parser.add_option("--license",
                      action='store_true',
                      dest="dry",
                      default=False,
                      help="license NO.")
    return parser


if __name__ == "__main__":

    options, args = parse_cmdline().parse_args(sys.argv[1:])

    print options
    print args

 
