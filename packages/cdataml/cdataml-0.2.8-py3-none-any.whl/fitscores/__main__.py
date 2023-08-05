from . import *
if __name__ == "__main__":
    import getopt, sys

    # Default arguments
    input_loc, output_loc, rawfile = None, None, None

    # Options
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:r:")
    for opt, arg in opts:
        if opt in "-h":
            print('''
            python3 fitscores.py <OPTIONS>

            Options:
            -i <Input cdata filepath>
            -o <Output cdata filepath>
            -r <Raw score data filepath>

            ''')
            sys.exit()
        elif opt in "-i": # Unscored cdata file
            input_loc = os.path.abspath(arg)
        elif opt in "-o": # Output file for scored cdata file
            output_loc = os.path.abspath(arg)
        elif opt in "-r": # Data file including scores
            rawfile = os.path.abspath(arg)

    fitscores(input_loc, output_loc, rawfile)
