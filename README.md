# Murray-Darling Basin Authority Stand Condition Tool input file converter

This Python Script is used to convert input raster files to the format required for the MDBA Stand Condition Tool 
The script automates the process set out in "Manually creating new input files for the MDBA Stand Condition Tool.docx"

The Script will convert 32 or 64 bit floating point 6 band rasters (Median epoch images from Landsat 5/7/8 R,G,B,Nir,Swir1,Swir2) into 16 bit BIL format files with an ENVI format header (see MD Veg Monitor Users Guide.pdf)

Inputs are a list of of 32 or 64 bit floating point 6 band raster images 
Outputs are bil format rasters with ENVI header files
The script is designed to be run from an ESRI Python Script tool interface (included in this package as SCT.tbx\stand_condition_raster_conversion_tool) or via python ide

SCT background:
The 2017 Stand Condition Tool (SCT), originally called the Murray-Darling Vegetation Monitor (MDVM) and later the Stand Condition Assessment Tool (SCA Tool/SCaT), is a piece of software which maps conditions of native tree stands across the MDB. The SCT requires Landsat summary images as input, and it outputs predictions of field variables, these are stand condition, plant area index (PAI), live basal area (LBA) and crown extent (CE). These predictions can be compared with relevant field data to determine the model fit using the in-built validation option. Additionally, field data can be used to post-process the model to better to fit the observed conditions and thus produce more representative maps (Murray-Darling Vegetation Monitor User’s Guide 2017
This script tool is used to process Landsat imagery to the correct specification for use by the SCT

Tool authored and maintained by Stephen Sunderland and Gabrielle Hunt, Murray-Darling Basin Authority 23/05/19

Requires ESRI ArcMap 10.x Arcpy and as installed python 2.7 x64
Questions to gis@mdba.gov.au
