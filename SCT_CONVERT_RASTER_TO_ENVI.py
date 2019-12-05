# Script to convert 32 or 64 bit floating point 6 band rasters into 16 bit bil files with an ENVI format header
# as required for input into the MDBA Stand Condition Tool
# Inputs are a set of 32 or 64 bit floating point 6 band raster images (Landsat 5/7/8 RGBNir,Swir1,Swir2)
# Outputs are bil format rasters with ENVI header files

# Created by MDBA, S Sunderland, G Hunt, 23/05/19

# Requires ESRI ArcMap 10.x Arcpy and python 2.7


import arcpy
import collections
import sys
import traceback
import os

###############################################################################################################
# function to get module inputs, either from manual (ide or command line) input or from an ESRI python script
#  tool interface
# If its run from an ESRI tool Parameters are passed using  sysargvs
# called form "__main___" code block
# code poition at top for ease of manual editing


def get_script_inputs(sysargvs):
    # function to get the input varables form an esri tool window
    inputfilelist = ""
    outputfolder = ""
    try:
        if len(sysargvs) > 1:  # getting inputs from an ESRI tool window
            printmsg("Inputs from ESRI tool:", sysargvs)
            input_gp_objects_filelist = arcpy.GetParameter(0)  # parameters are a list of ESRI raster objects (rasters)
            # require string paths, so convert all gp objs to strings
            inputfilelist = [str(gp_obj) for gp_obj in input_gp_objects_filelist]
            # get output folder as a string
            outputfolder = arcpy.GetParameterAsText(1)
        else:
            # manually set inputs and outputs
            inputfilelist = [r'C:\\STAND_CONDITION_TOOL_PROJECT\\testdata\\MDB_P75_3_0000009472-0000009472.tif;'
                             r'C:\\STAND_CONDITION_TOOL_PROJECT\\testdata\\MDB_P75_3_0000009472-0000009473.tif']

            outputfolder = r'C:\\GSS\\STAND_CONDITION_TOOL_PROJECT\\testdata\\output'

    except Exception as err:
        printmsg("Get_Inputs_from ESRI_Tool_Window error", str(err.args[0]), str(traceback.format_exc()))

    return inputfilelist, outputfolder


#################################################################################################################
# Module to read a standard ERRI format bil header and output the values in ENVI header format as required by the
# Stand Condition Tool
#

def create_envi_header_template(input_bil_raster):
    # Converting from ESRI bil header format:
    #
    # BYTEORDER      I
    # LAYOUT         BIL
    # NROWS          3394
    # NCOLS          3127
    # NBANDS         6
    # NBITS          16
    # BANDROWBYTES   6254
    # TOTALROWBYTES  37524
    # PIXELTYPE      UNSIGNEDINT
    # ULXMAP         54968.8796999978
    # ULYMAP         5897638.26270001
    # XDIM           29.9999999999998
    # YDIM           29.9999999999997
    # NODATA         -1.797693e+308

    # ENVI hdr format:
    #     ENVI
    # description = {\\***.BIL}
    # samples = 9472
    # lines = 9472
    # bands   = 6
    # header offset = 0
    # file type = ENVI Standard
    # data type = 2
    # interleave = bil
    # byte order = 0
    # map info = {{Geographic Lat/Lon, 1, 1,140.552610225786,-27.5527221526361,0.000269494585235856,
    # 0.000269494585235856,WGS-84}}
    # coordinate system string = {GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],
    # PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]}
    # band names = {
    # Band 1,
    # Band 2,
    # Band 3,
    # Band 4,
    # Band 5,
    # Band 6}

    # Constant strings used for the output ENVI header for spatial coordinate system EPSG 4326
    mapinfostringlist = ['{Geographic Lat/Lon, 1, 1,', '143', '-34', '0.00025', '0.00025', 'WGS-84}']
    coordinatesystemstring = 'coordinate system string = {GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",' \
                             'SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],' \
                             'UNIT["Degree",0.017453292519943295]]}'

    # ENVI header key list
    envi_hdr_dict_keys = [('ENVI', 'ENVI'),
                          ('description', ''),
                          ('samples', ''),
                          ('lines', ''),
                          ('bands', 'bands   = 6'),
                          ('header offset', 'header offset = 0'),
                          ('file type', 'file type = ENVI Standard'),
                          ('data type', 'data type = 2'),
                          ('interleave', 'interleave = bil'),
                          ('byte order', "byte order = 0"),
                          ('map info', ''),
                          ('coordinate system string', coordinatesystemstring),
                          ('band names', 'band names = {'),
                          ('Band 1', 'Band 1,'),
                          ('Band 2', 'Band 2,'),
                          ('Band 3', 'Band 3,'),
                          ('Band 4', 'Band 4,'),
                          ('Band 5', 'Band 5,'),
                          ('Band 6', 'Band 6}')]

    envi_hdr_dict = collections.OrderedDict(envi_hdr_dict_keys)

    for akey in envi_hdr_dict.keys():
        printmsg(akey, envi_hdr_dict[akey])

    try:
        # derive esri header file path from bil filename
        bil_fn_parts = os.path.split(input_bil_raster)
        bil_base_fn = os.path.splitext(bil_fn_parts[1])[0]
        newesrihdrpath = os.path.join(bil_fn_parts[0], bil_base_fn + ".hdr")

        printmsg("processing esri header file", newesrihdrpath)
        if os.path.exists(
                newesrihdrpath):  # if header file exists open for reading as text file and populate a
            # dictionary with the key values

            newesrihdrdict = collections.OrderedDict()  # new empty dictionary for ESRI value
            with open(newesrihdrpath) as ESRIHeaderfile:
                for textline in ESRIHeaderfile:
                    linelist = textline.split(" ")  # split current line by spaces, first element is the key(ie ULXMAP)
                    valuelist = []
                    for valstring in linelist:  # remove all the empty values form the input string
                        if not valstring == "":
                            valuelist.append(valstring)

                    # vallist will have the key and value as elements 0 and 1"
                    # printmsg(valuelist)
                    try:
                        newesrihdrdict.update([(valuelist[0], valuelist[
                            1].rstrip())])  # add the key value and the data value with \n stripped
                    except Exception as err:
                        printerrormsg("read ESRI header file error", str(err.args[0]),
                                      str(traceback.format_exc()))  # error with keys

            ESRIHeaderfile.close()  # close the header file
            # display ESRI values from header

            printmsg("ESRI values dictionary:")
            for keys in newesrihdrdict.keys():
                printmsg(keys, newesrihdrdict[keys])

            envi_hdr_dict['samples'] = "samples = " + str(newesrihdrdict['NCOLS'])
            envi_hdr_dict['lines'] = "lines = " + str(newesrihdrdict['NROWS'])

            # assign esri header values to build  mapinfostring part of header
            mapinfostringlist[1] = str(newesrihdrdict['ULXMAP'])
            mapinfostringlist[2] = str(newesrihdrdict['ULYMAP'])
            mapinfostringlist[3] = str(newesrihdrdict['XDIM'])
            mapinfostringlist[4] = str(newesrihdrdict['YDIM'])

            mapinfostr = "map info = {" + mapinfostringlist[0] + mapinfostringlist[1] + "," + mapinfostringlist[2] + \
                         "," + mapinfostringlist[3] + "," + mapinfostringlist[4] + "," + mapinfostringlist[5] + "}"

            envi_hdr_dict['map info'] = mapinfostr
            envi_hdr_dict['description'] = 'description = {' + str(input_bil_raster) + "}"
            printmsg("Writing new ENVI format header file")
            # write out the new header
            try:

                try:
                    #  rename the old esri header
                    renamednewesrihdrpath = newesrihdrpath + "old"
                    os.rename(newesrihdrpath, renamednewesrihdrpath)
                except Exception as err:
                    printerrormsg("rename old ENVI header file error", str(err.args[0]),
                                  str(traceback.format_exc()))
                if not os.path.exists(newesrihdrpath):  # old header file renamed succesfully
                    newenvihdrpath = newesrihdrpath  # write out new header with original name
                    with open(newenvihdrpath, 'w') as newhdrfile:
                        for akey in envi_hdr_dict.keys():
                            newhdrfile.write(envi_hdr_dict[akey] + '\n')
                    newhdrfile.close()
                else:
                    printerrormsg("Unable to delete old header file", newesrihdrpath)
            except Exception as err:
                printerrormsg("write ENVI header file error", str(err.args[0]),
                              str(traceback.format_exc()))  # error with keys
            printmsg("New ENVI Header file succesfully created for ", input_bil_raster)
            return True  # on success return true

    except Exception as err:
        printerrormsg("get header function error in ", str(err.args[0]), str(traceback.format_exc()))

    return False  # on any other state return false

###################################################################################################################
# function to convert from input raster to ESRI bil format
# inputs are a file name to a valid raster file
# (6 band floating point tif, with spatial reference EPSG: 4326
# output is a 16 bit signed integer bil file


def convert_rasterinput_to_esri_bil(input_raster, output_raster):  # module to take input file and output to tif
    # Set arcpy overwrite environment variable
    arcpy.env.overwriteOutput = True
    try:
        printmsg("Saving", input_raster, " to ", output_raster)
        # generate statistics and pyramids for the raster
        # on export for easy inspection
        arcpy.env.rasterStatistics = 'STATISTICS 10 10'
        arcpy.env.pyramid = "PYRAMIDS -1 NEAREST DEFAULT NO_SKIP"
        arcpy.env.compression = "LZ77"
        # set the ouput pixel type to 16 bit signed as required by the SCT
        outputpixeltype = "16_BIT_SIGNED"
        # convert the raster
        arcpy.CopyRaster_management(in_raster=input_raster,
                                    out_rasterdataset=output_raster,
                                    config_keyword="",
                                    background_value="",
                                    nodata_value="",
                                    onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE",
                                    pixel_type=outputpixeltype,
                                    scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE",
                                    format="Esri BIL",
                                    transform="NONE")
        return True  # on success return true

    except Exception as err:
        printerrormsg("convert raster function error", str(err.args[0]), str(traceback.format_exc()))
    return False  # on error return false


###################################################################################################################
# Function to get the spatial reference code for the input dataset
# input is a raster dataset
# output will be the spatial reference epsg code or None if it canot be read
def get_dataset_projection_factory_code(inputdataset, spatial_reference_factory_code=None):  # get the spatial reference
    #  use arcpy describe function to get a describe object and from that its spatial reference code
    try:
        spatial_reference_factory_code = arcpy.Describe(inputdataset).spatialReference.factoryCode
    except Exception as err:
        printerrormsg("get dataset projection function error", str(err.args[0]), str(traceback.format_exc()))
    return spatial_reference_factory_code

#######################################################################################################################
# Function to read the bands for a raster and return the bands in a list
#
# inputs are a raster filename
# output is an list of the bands


def read_raster_bands(input_raster):
    bands = []  # on failure return empty list
    try:
        # open the describe object for the raster
        describe_object = arcpy.Describe(input_raster)
        for rb in describe_object.children:  # get cheldren objects (bands) for this raster and add to a list
            bands.append((os.path.join(input_raster, rb.name)))
    except Exception as err:
        printerrormsg("get raster bands function error", str(err.args[0]), str(traceback.format_exc()))
    return bands
# -----------------------------------------------------------------------------------------------------------------------
# Generic helper message output functions, so that output works in ESRI script or esri tool modes

# function to concatenate input strings for aoutput as a message
# inputs are single or multiple strings, sepearetd by ,


def checktext(*arg):
    argstr = ""
    argtxt = arg[0]
    if len(argtxt) > 1:
        for allargs in argtxt:
            argstr = argstr + " " + str(allargs)
    else:
        argstr = str(argtxt)
    return argstr


# function to output a standard message, using print or arcpy.AddMessage


def printmsg(*arg):
    try:
        message = checktext(arg)  # pass string(s) to checktext for formatting
        if len(sys.argv) > 1:  # running in esri tool so use arcpy messaging functions
            arcpy.AddMessage(str(message))
        else:  # in script mode so ues python print
            print(str(message))
    except Exception as err:
        print("print output function error" + str(err.args[0]) + str(traceback.format_exc()))
        arcpy.AddError("print output function error" + str(err.args[0]) + str(traceback.format_exc()))

# function to output an error  message, using print or arcpy.AddError


def printerrormsg(*arg):

    try:
        message = checktext(arg)  # pass string(s) to checktext for formatting
        if len(sys.argv) > 1:  # running in esri tool so use arcpy error messaging functions
            arcpy.AddError(str(message))
        else:
            print("Error:" + str(message))
    except Exception as err:
        print("print output function error" + str(err.args[0]) + str(traceback.format_exc()))
        arcpy.AddError("print output function error" + str(err.args[0]) + str(traceback.format_exc()))

# function to output a warning  message, using print or arcpy.AddError


def printwarningmsg(*arg):
    try:
        message = checktext(arg)
        if len(sys.argv) > 1:  # running in esri tool so use arcpy warning messaging functions
            arcpy.AddWarning(str(message))
        else:
            print("Warning:" + str(message))
    except Exception as err:
        print("print output function error" + str(err.args[0]) + str(traceback.format_exc()))
        arcpy.AddError("print output function error" + str(err.args[0]) + str(traceback.format_exc()))


######################################################################################################################
# Main section for module SCT Raster Tool
#
def run_main():

        # get the input files list and output folder, can be passed as part of an esri script tool or as a manually
        # set string
        (inputfilelist, output_raster_folder) = get_script_inputs(sys.argv)

        for input_raster in inputfilelist:  # process each file in the input list
            printmsg(type(input_raster), input_raster)

            # check number of bands is correct
            rasterbandslist = read_raster_bands(input_raster)
            printmsg("raster bands count", len(rasterbandslist))
            if len(rasterbandslist) != stand_condition_tool_raster_bands_count:
                printwarningmsg("input raster ", input_raster, " has ", len(rasterbandslist), "bands",
                                stand_condition_tool_raster_bands_count, "Landsat 7/8 bands required")
                continue
            # check that the projection of the input raster is correct for use by the sct tool
            factory_code = get_dataset_projection_factory_code(input_raster)
            printmsg("factory code", factory_code)
            if factory_code != stand_condition_tool_data_spatial_reference_code:
                printwarningmsg("input raster ", input_raster, " has spatial reference EPSG code", factory_code,
                                stand_condition_tool_data_spatial_reference_code, "projection required")
                continue
            # Build output bil file name and path
            output_raster = os.path.join(output_raster_folder, os.path.splitext(os.path.split(input_raster)[1])[0]
                                         + ".BIL")

            printmsg("Converting raster", input_raster, " into an SCT format bil file", output_raster)

            if not convert_rasterinput_to_esri_bil(input_raster,
                                                   output_raster):  # if error on convert then skip to next
                # raster
                printerrormsg("input raster ", input_raster, "could not be converted")
                continue
            if not create_envi_header_template(output_raster):
                printerrormsg("ENVI header for", output_raster, "could not be created")
                continue


# Global constants

stand_condition_tool_raster_bands_count = 6  # number of landsat 7 bands required for a SCT raster
# Red,Green,Blue,Nir, Swir1, Swire2
stand_condition_tool_data_spatial_reference_code = 4326

# Main program module
# program statements all run from run_main to avoid scope issues with globals
if __name__ == "__main__":

    # Set environment variables ##
    arcpy.env.overwriteOutput = True

    try:
        run_main()

    except Exception as main_err:
        printerrormsg("main function error in ", __file__, str(main_err.args[0]), str(traceback.format_exc()))
