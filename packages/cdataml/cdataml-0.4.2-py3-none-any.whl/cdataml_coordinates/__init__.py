import sys, os, subprocess, getopt
import pandas as pd
import cv2 as cv
import numpy as np
from importlib_resources import files

def loadkey():
    data_path = files('data').joinpath('lesion_score_key.tif')
    key = cv.imread(cv.samples.findFile(str(data_path)))
    return(key)

def saveandquit(input_loc, output_loc, dataframe):
    # Function to save to output location and close the tool
    exitprogram = True
    print("Saving and Quitting ...")
    os.rename(input_loc, "backup_" + os.path.basename(input_loc)) # Keep a backup of the previous version incase of user error
    dataframe.to_csv(output_loc, index=False)
    cv.destroyAllWindows() # Close the windows
    sys.exit()

def makeselectionsquare(coords):
    # Function to make coordinates selected in OpenCV tool square by increasing shorter length to match longer.
    hlen = coords[3] - coords[1] # Horizontal length
    vlen = coords[2] - coords[0] # Vertical length
    diff = abs(hlen-vlen) # Difference
    # Add half the difference between them to the greater of the shorter axis
    # Subtract half the difference between them to the lesser of the shorter axis
    if hlen == max(hlen, vlen): # If wider than tall
        coords[2] = coords[2] + (diff / 2)
        coords[0] = coords[0] - (diff / 2)
    else: # If taller than wide
        coords[3] = coords[3] + (diff / 2)
        coords[1] = coords[1] - (diff / 2)
    return coords

def skipspots(row, colname, varcurrent, dataframe):
    # Function to skip an image or leaf
    tempoffsets = [] # If next image is part of the same replicate, the offsets should be continuous between the two images
    skip = 0

    while True:
        if(row+skip == len(dataframe)): # If the end of cdata is reached, save and quit
            print("End of Dataframe!")
            saveandquit()
            break
        else:
            testid = int(dataframe.loc[row+skip, colname]) # Find value of variable in potential next row
            if testid == varcurrent: # Compare it with the current variable value
                tempoffsets.append(dataframe.loc[row+skip, "Offset"]) # If no change, store offset to be shunted along later
                # Fill the coordinates and scores with "Skip" and offset values with 0, since they must be integers.
                dataframe.loc[row+skip, "y1"] = "Skip"
                dataframe.loc[row+skip, "y2"] = "Skip"
                dataframe.loc[row+skip, "x1"] = "Skip"
                dataframe.loc[row+skip, "x2"] = "Skip"
                dataframe.loc[row+skip, "Score"] = "Skip"
                dataframe.loc[row+skip, "Offset"] = 0
                skip = skip + 1
            else: # If the potential next variable value is different to the current one, break
                if colname == "Img-ID": # If the chosen skip was image, then the offset values may need to be shunted along.
                    if dataframe.loc[row, "Offset"] != dataframe["Offset"].max(): # If the current offset isn't the maximum value, there are still leaves left in this replicate
                        dataframe.iloc[row:row+skip, dataframe.columns.get_loc("Offset")] = 0 # Replace previous offset values with 0s
                        dataframe.iloc[row+skip:row+(2*skip), dataframe.columns.get_loc("Offset")] = tempoffsets # Update the next offset values to continue from point of skip
                        dataframe.iloc[row+(2*skip):row+(3*skip), dataframe.columns.get_loc("Offset")] = 0 # Update any offsets attributed to the image after the maximum to 0
                # Return row index following skips
                print("Skipped " + str(skip) + " rows")
                row = row + skip
                print("Updated Row: ", str(row), "/", str(len(dataframe)))
                return(row)

def recorddata(input_loc, output_loc, image_loc, scoring):

    # Make sure all columns are loaded
    pd.set_option("display.max_colwidth", None)

    # Load cdata and imagedata
    cdata = pd.read_csv(input_loc)
    image_paths = pd.read_csv(image_loc)
    previmg = ""

    if scoring == True:
        key = loadkey() # Need to add Lesion Score Key to PyPI files.

        # Identify next row with no coordinates and retrieve related data
    for row in range(0, len(cdata["y1"])):
        if pd.isna(cdata.loc[row, "y1"]) == True:
            currentrow = row
            break

    # Loop through cdata, presenting the corresponding image and metadata in a window, in which the user can drag coordinates around individual CDAs and optionally score them.
    exitprogram = False
    while exitprogram == False:

        # Retrieve metadata
        usi = cdata.loc[currentrow, "Unique_Spot_ID"]
        imgid = int(cdata.loc[currentrow, "Img-ID"])
        plantperimgid = int(cdata.loc[currentrow, "Plant-Per-Img-ID"])
        leafid = int(cdata.loc[currentrow, "Leaf-ID"])
        spotid = int(cdata.loc[currentrow, "Spot-ID"])
        offset = int(cdata.loc[currentrow, "Offset"])

        # Check if current imgid is same as previous - if not, load current imgid
        imgpath = image_paths.loc[image_paths["Img-ID"] == imgid, "Path"].to_string(index = False)
        if imgpath != previmg:
            img = cv.imread(cv.samples.findFile(imgpath))

        if img is None:
            print("Could not read image: " + imgpath)

        # Add space to the top containing current row metadata needed to identify a CDA
        metadatabar = np.full((200, img.shape[1], 3), 255, dtype=np.uint8)
        imgwithmetadata = np.concatenate((metadatabar, img))
        metadatatext = "".join(str(e) for e in ["USI:", usi, ", PlantPerImgID:", plantperimgid, ", LeafID:", leafid, ", Offset:", offset, ", SpotID:", spotid])
        cv.putText(img = imgwithmetadata, text = metadatatext, org = (50, 160), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=8, color=(0, 0, 0),thickness=8)

        # Append score key to bottom if scoring option chosen
        if scoring == True:
            scorescale = key.shape[1] / imgwithmetadata.shape[1]
            keydimensions = (int(key.shape[1]/scorescale), int(key.shape[0]/scorescale))
            scaledkey = cv.resize(key, keydimensions)
            imgwithmetadata = np.concatenate((imgwithmetadata, scaledkey))

        # Scale image down (large images take very long to load)
        scaleval = 0.25
        dim = (int(imgwithmetadata.shape[1]*scaleval), int(imgwithmetadata.shape[0]*scaleval))
        scaledfinalimg = cv.resize(imgwithmetadata, dim)

        # Display image and bring to front
        cv.imshow("Cell Death Area Coordinate and Scoring Tool", scaledfinalimg)
        cv.setWindowProperty("Cell Death Area Coordinate and Scoring Tool", cv.WND_PROP_TOPMOST, 1)

        # Select bounding box
        print("Please select an area of interest by dragging a box, or press c to quit scoring")
        fromCenter = False
        boundingbox = cv.selectROI("Cell Death Area Coordinate and Scoring Tool", scaledfinalimg, fromCenter)

        # Message for next steps
        if scoring == True:
            print("Please press either ESC to exit or enter a score between 0 and 6.")
        else:
            print("Please press either ESC to exit or any other value to continue")

        exitkeyloop = False # To break from keypress while loop
        while exitkeyloop == False:
            keypress = cv.waitKey(0)
            if keypress == 27: # Escape
                print("ESC Pressed - exiting OpenCV selectROI()")
                saveandquit(input_loc, output_loc, cdata)

            elif keypress == ord('m'): # Missing leaf
                print("Skipping to next leaf")
                currentrow = skipspots(currentrow, "Leaf-ID", leafid, cdata)
                exitkeyloop = True

            elif keypress == ord('n'): # Next image
                print("Skipping to next image")
                currentrow = skipspots(currentrow, "Img-ID", imgid, cdata)
                exitkeyloop = True
            else:
                if scoring == True:
                    if keypress in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6')]: # if a score is pressed
                        print("Score given: " + str(chr(keypress)))
                        cdata.loc[currentrow, "New_Score"] = chr(keypress) # save the score (chr is reverse of ord)
                    else:
                        print("That did not work. Please press either ESC to exit or a score from 0 to 6.")
                        continue

                # Saving scaled coordinates
                y1 = int(boundingbox[1])
                y2 = int(boundingbox[1] + boundingbox[3])
                x1 = int(boundingbox[0])
                x2 = int(boundingbox[0] + boundingbox[2])

                # Remove from the number of pixels from the metadata bar and scale coordinates up by the downsizing of the image.
                y1 -= scaleval * 200 # 200 is height of metadata bar
                y2 -= scaleval * 200
                coords = [y1/scaleval, x1/scaleval, y2/scaleval, x2/scaleval]

                # Make selection square
                squarecoords = makeselectionsquare(coords)

                # Store in cdata
                cdata.loc[currentrow, "y1"] = squarecoords[0]
                cdata.loc[currentrow, "y2"] = squarecoords[2]
                cdata.loc[currentrow, "x1"] = squarecoords[1]
                cdata.loc[currentrow, "x2"] = squarecoords[3]

                # If end of dataframe reached, save and quit, else move to next row
                if currentrow == len(cdata)-1:
                    print("End of Dataframe!")
                    saveandquit(input_loc, output_loc, cdata)
                else:
                    currentrow += 1
                    print("Updated Row: ", str(currentrow), "/", str(len(cdata)))
                exitkeyloop = True
        previmg = imgpath
