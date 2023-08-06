import os, glob
import pandas as pd
from natsort import natsorted

def imagedoc(input_loc, output_loc):
    # 1) CSV document for containing image filepaths
    # Filepaths of all TIFF images in input location
    dir_path = os.path.join(input_loc, '**/*.tif')

    filenames = []
    for file in glob.glob(dir_path, recursive=True):
        filenames.append(file)
        filenames = natsorted(filenames)

    # Index values
    file_IDs = [FID for FID in range(1, len(filenames)+1)]

    # Combine and output to output location
    imagecsv = pd.DataFrame({'Img-ID': file_IDs, 'Path': filenames})
    imagecsv.to_csv(os.path.join(output_loc, 'images.csv'), index=False)
    print("images.csv created")

def treatdoc(output_loc, spots_per_leaf):
    # 2) CSV document to containing treatment pattern

    # Index values
    treatcsv = pd.DataFrame({'Treat-ID': [TID for TID in range(1, int(spots_per_leaf)+1)]})
    # Empty columns to be filled by user
    treatcsv['TreatmentName'] = None
    treatcsv['Effector'] = None
    treatcsv['NLR1'] = None
    treatcsv['NLR2'] = None
    # Output to output location
    treatcsv.to_csv(os.path.join(output_loc, 'treatments.csv'), index=False)
    print("treatments.csv created")

def cdata(input_loc, output_loc, leaves_per_img, spots_per_leaf):
    # 3) CSV document for CDA location, score, and coordinate data
    dir_path = os.path.join(input_loc, '**/*.tif')
    filenames = []
    for file in glob.glob(dir_path, recursive=True):
        filenames.append(file)

    # Initialise arrays to contain column data
    USIs, Img_IDs, Plant_IDs, Plant_Per_Img_IDs, Leaf_IDs, Offsets, Spot_IDs = [], [], [], [], [], [], []
    Img_ID, Plant_ID, Plant_Per_Img_ID, Leaf_ID, Offset, Spot_ID = 1, 1, 1, 1, 1, 1

    df_length = int(spots_per_leaf) * int(leaves_per_img) * len(filenames)

    for i in range(1, df_length+1):
        # USI (Unique Spot Identifier)
        USIs.append('S' + str(i))

        # Img_ID
        Img_IDs.append(Img_ID)
        if i % (df_length / len(filenames)) == 0:
            Img_ID = Img_ID + 1

        # Plant_ID
        Plant_IDs.append(Plant_ID)
        if i % (2 * int(spots_per_leaf)) == 0:
            Plant_ID = Plant_ID + 1

        # Plant_Per_Image
        Plant_Per_Img_IDs.append(Plant_Per_Img_ID)
        if i % (2 * int(spots_per_leaf)) == 0:
            if Plant_Per_Img_ID == int(leaves_per_img) / 2:
                Plant_Per_Img_ID = 1
            else:
                Plant_Per_Img_ID = Plant_Per_Img_ID + 1

        # Leaf_ID
        Leaf_IDs.append(Leaf_ID)
        if i % int(spots_per_leaf) == 0:
            if Leaf_ID == 1:
                Leaf_ID = 2
            elif Leaf_ID == 2:
                Leaf_ID = 1

        # Offset
        Offsets.append(Offset)
        if i % (int(spots_per_leaf)*2) == 0:
            if Offset == int(spots_per_leaf):
                Offset = 1
            else:
                Offset = Offset + 1

        # Spot_ID
        Spot_IDs.append(Spot_ID)
        if (i+1) % int(spots_per_leaf) == 0:
            Spot_ID = int(spots_per_leaf)
        else:
            Spot_ID = (i+1) % int(spots_per_leaf)

    cdatacsv = pd.DataFrame({'Unique_Spot_ID': USIs, 'Img-ID': Img_IDs, 'Plant-ID': Plant_IDs, 'Plant-Per-Img-ID': Plant_Per_Img_IDs, 'Leaf-ID': Leaf_IDs, 'Spot-ID': Spot_IDs, 'Offset': Offsets})
    cdatacsv['Treat-ID'] = cdatacsv['Spot-ID']
    cdatacsv["Replicate"] = None
    cdatacsv['Score'] = None
    cdatacsv['y1'] = None
    cdatacsv['y2'] = None
    cdatacsv['x1'] = None
    cdatacsv['x2'] = None

    cdatacsv.to_csv(os.path.join(output_loc, 'cdata.csv'), index=False)
    print("cdata.csv created")
