# Murray-Darling Basin Authority Stand Condition Tool

The 2017 Stand Condition Tool (SCT), originally called the Murray-Darling Vegetation Monitor (MDVM) and later the Stand Condition Assessment Tool (SCA Tool/SCaT), is a piece of software which maps conditions of native tree stands across the MDB. The SCT requires Landsat summary images as input, and it outputs predictions of field variables, these are stand condition, plant area index (PAI), live basal area (LBA) and crown extent (CE). These predictions can be compared with relevant field data to determine the model fit using the in-built validation option. Additionally, field data can be used to post-process the model to better to fit the observed conditions and thus produce more representative maps (Murray-Darling Vegetation Monitor User’s Guide 2017).

Some datasets will be needed for running these codes:
* Boundary of the Murray-Darling Basin        - https://code.earthengine.google.com/?asset=users/Projects/MDB_single
* Collection of floodplain shapefiles         - https://code.earthengine.google.com/?asset=users/Projects/mfp
* BWS Regions                                 - https://code.earthengine.google.com/?asset=users/Projects/BWSRegions
* ANAE Wetlands (converted to raster)         - https://code.earthengine.google.com/?asset=users/Projects/Hunt/MFP/Wetlands_desc2
* Interim NSW Wetlands (from ANAE as raster)  - https://code.earthengine.google.com/?asset=users/Projects/Hunt/MFP/Interim_NSW1
* Species mask                                - https://code.earthengine.google.com/?asset=users/Projects/SCT_supplementary_files/MDBVTmap1
* Collection of output condition rasters      - https://code.earthengine.google.com/?asset=users/Projects/Condition_8bit

For more information on the datasets see https://www.mdba.gov.au/sites/default/files/pubs/bp-eval-2020-tree-stand-condition-assessment-tool.pdf

## Create SCT inputs

To operate this code you will need a Google Earth Engine login subject to their Terms and Condtions (https://earthengine.google.com/terms/). Copy and paste the code into the Code Editor (https://code.earthengine.google.com/). 

This code uses Landsat satellite imagery stored on Google Earth Engine and exports the resulting image percentiles to Google Cloud. It is designed to use the entire Murray-Darling Basin shapefile. 

## Murray-Darling Basin Authority Stand Condition Tool input file converter

This script tool is used to process Landsat imagery to the correct specification for use by the SCT. Requires ESRI ArcMap 10.x Arcpy and as installed python 2.7 x64

This Python Script is used to convert input raster files to the format required for the MDBA Stand Condition Tool 
The script automates the process set out in "Manually creating new input files for the MDBA Stand Condition Tool.docx"

The Script will convert 32 or 64 bit floating point 6 band rasters (Median epoch images from Landsat 5/7/8 R,G,B,Nir,Swir1,Swir2) into 16 bit BIL format files with an ENVI format header (see MD Veg Monitor Users Guide.pdf)

Inputs are a list of of 32 or 64 bit floating point 6 band raster images 
Outputs are bil format rasters with ENVI header files
The script is designed to be run from an ESRI Python Script tool interface (included in this package as SCT.tbx\stand_condition_raster_conversion_tool) or via python ide

## Calculate area of binned condition

To operate this code you will need a Google Earth Engine login subject to their Terms and Condtions (https://earthengine.google.com/terms/). Copy and paste the code into the Code Editor (https://code.earthengine.google.com/). 

This code takes in the output condition raster from the Stand Condition Tool and calculates the area of the binned condition. The SCT tool outputs condition between 0 and 10, however the pre-calculated condition rasters (https://code.earthengine.google.com/?asset=users/Projects/Condition_8bit) are scaled between 0 and 100. 

### Questions
Codes authored and maintained by Stephen Sunderland, Murray-Darling Basin Authority 23/05/19
Questions to gis@mdba.gov.au
