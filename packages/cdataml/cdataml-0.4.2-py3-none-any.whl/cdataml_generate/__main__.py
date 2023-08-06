from . import *
if __name__ == "__main__":
    import getopt, sys

    # Default arguments
    input_loc, output_loc, leaves_per_img, spots_per_leaf = None, None, 8, 8

    # Options
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:s:")
    for opt, arg, in opts:
        if opt in "-h": # help
            print('''
            python3 generate.py

            Options:
            -i <Input cdata filepath>
            -o <Output cdata filepath>
            -l <Max number of leaves per image>
            -s <Standard number of spots per leaf>

            ''')
            sys.exit()
        elif opt == "-i": # input filepath (location containing images)
            input_loc = arg
        elif opt in "-o": # output location
            output_loc = arg
        elif opt in "-l": # maximum number of leaves per image
            leaves_per_img = arg
        elif opt in "-s": # spots per leaf
            spots_per_leaf = arg

    imagedoc(input_loc, output_loc)
    treatdoc(output_loc, spots_per_leaf)
    cdata(input_loc, output_loc, leaves_per_img, spots_per_leaf)
