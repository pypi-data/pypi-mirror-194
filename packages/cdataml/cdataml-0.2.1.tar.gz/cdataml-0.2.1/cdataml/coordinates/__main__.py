from . import *
if __name__ == "__main__":
    import getopt, sys

    # Default arguments
    input_loc, output_loc, image_loc, scoring = None, None, None, False

    # Options
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:s")
    for opt, arg in opts:
        if opt in "-h":
            print('''
            python3 coordinates.py <OPTIONS>

            Options:
            -i <Input cdata filepath>
            -o <Output cdata filepath>
            -f <Imagefilepath data filepath>
            -s Scoring default = False, use this to set to True

            ''')
            sys.exit()
        elif opt in "-i": # Input cdata file
            input_loc = os.path.abspath(arg)
        elif opt in "-o": # Output cdata file
            output_loc = os.path.abspath(arg)
        elif opt in "-f":
            image_loc = os.path.abspath(arg)
        elif opt in "-s": # Scoring
            scoring = True

    recorddata(input_loc, output_loc, image_loc, scoring)
