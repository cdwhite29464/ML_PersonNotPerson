# Organization : Jefferson County Open Space
# Creator : Chris White
# Date Created : 5/1/2022
# Editor :
# Script Name : NR_ML_PersonNoPerson
# File Location : "M:\GIS_TEAM\3_Resources\3_4_Tools_and_Software\Scripts\Python\Jpg_Exif_Data_Extract\NR_ML_PersonNoPerson.py"
# Short Description of Script : This script uses a machine learning model generated using the application Lobe a.i. designed to 
# identify if a photo has a person in it or not. The Lobe a.i. uses TensorFlow and simplifies the process of creating a machine 
# learning model.

from lobe import ImageModel
import shutil
from PIL import Image
import os
from os import listdir

model = ImageModel.load(r"BLANK\Models\PersonNoPersonV4\PersonNoPersonV4 TensorFlow")

imageFolderLocation = r"BLANK"
rootFolder = r"BLANK"
fList = imageFolderLocation.split("\\")
photoPrefix = fList[len(fList)-2]

# Source path
templateFolder = r"BLANK\TemplateFolder\ML_Processed_XXXXX"

# Destination path
destName = f"ML_Processed___{photoPrefix}"
dest_dir = os.path.join(rootFolder, destName)

# Copy the content of
# source to destination
shutil.copytree(templateFolder, dest_dir)


#Output Folder Names and Locations
personFolderName = "PythonPerson"
personFolder = os.path.join(dest_dir,personFolderName)
noPersonFolderName = "PythonNoPerson"
noPersonFolder = os.path.join(dest_dir,noPersonFolderName)
processedFolderName = "Processed"
processedFolder = os.path.join(dest_dir,noPersonFolderName)


os.chdir(imageFolderLocation)
for count,f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    newName = f"{photoPrefix}_{f_name}{f_ext}"
    os.rename(f,newName)


onlyfiles = [f for f in listdir(imageFolderLocation) if os.path.isfile(os.path.join(imageFolderLocation, f))]

for file in onlyfiles:
    print(file)
    f_name, f_ext = os.path.splitext(file)
    if f_ext in [".xls", ".xlsx", ".csv"]:
        None
    else:
        fileLocation = os.path.join(imageFolderLocation,file)
        img = Image.open(fileLocation)
        result = model.predict(img)

        # Print top prediction
        print(f"\tTop Perdiction: {result.prediction}")

        # Print all classes
        print(f"\tResults of Confidence")
        for label, confidence in result.labels:
            print(f"\t\t{label}: {confidence*100}%")

        if result.prediction == "Person":
            print("\t\t\tMove to Person Folder\n")
            shutil.copy(fileLocation, personFolder)
        elif result.prediction == "No Person":
            print("\t\t\tMove to Non-Person Folder\n")
            shutil.copy(fileLocation, noPersonFolder)



#Rename ML Processed Photos
os.chdir(personFolder)
for count,f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    if f_ext == ".JPG":
        newName = f"{f_name}_P{f_ext}"
        os.rename(f,newName)

os.chdir(noPersonFolder)
for count,f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    if f_ext == ".JPG":
        newName = f"{f_name}_N{f_ext}"
        os.rename(f,newName)


