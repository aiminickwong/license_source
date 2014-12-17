#! /usr/bin/python
import sys
# also available at http://www.gnu.org/copyleft/gpl.html.
from optparse import make_option, OptionParser

from licenseimport.license_util.license_run import run,bs

def parse_cmdline(prog_name):
    """Parses the relevant cmdline arguments
    """
    option_list = (
        make_option('-n', '--name', action='store', dest='orgname', default=None,
            
            help='Please enter your orgnazation name '),
        make_option('-l','--license',dest='license',
            help='Please enter your license associated with the orgnazation'),
    )
 
    return OptionParser(prog=prog_name,
                            usage='',
                            version='1.0.1',
                            option_list=option_list)

if __name__ == "__main__":

    options, args = parse_cmdline(sys.argv[0]).parse_args(sys.argv[1:])

    print options
    print args

 

    #args=sys.argv
    #name=args[1]
    #license=args[2]
    #import pdb
   # pdb.set_trace()
    print dir(options)
    run(options.orgname,options.license)

