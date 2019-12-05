# Automated test module for the Stand Condition Tool Raster Coverter project script
# runs automated test on all major functions
# Input requirement, test data folder \\SCT\testdata

# Required imports

from SCT_CONVERT_RASTER_TO_ENVI import *


# function to confirm correct aquisition of input varables in ESRI tool or IDE mode
def test_get_inputvariables():
    test_env_list = [sys.argv[0],
                     [r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\MDB_P75_3_0000009472-0000009472.tif;'
                     r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\MDB_P75_3_0000009472-0000009473.tif'],
                     r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\output']

    current_sys_env = sys.argv #backup existing system variables
    sys.argv = test_env_list # apply test variables
    (input_raster_variable,input_outputfolder_variable)= get_script_inputs(test_env_list) # run the input function
    sys.argv = current_sys_env # restore system vars
    # test that function has returned values correctly
    assert (input_raster_variable == test_env_list[1]) and (input_outputfolder_variable == test_env_list[2])

# test function for creation of an ESRI Bil raster
def test_create_envi_header_template():
    output_raster = r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\output\MDB_P75_3_0000009472-0000009472.bil'
    create_envi_header_template(output_raster)
    newhdr = r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\output\MDB_P75_3_0000009472-0000009472.hdr'
    assert(os.path.isfile(newhdr)) # check file exists

# test function for creation of an ESRI Bil raster, after createion tests that new raster can be read and that
# it has required number of bands, is the correct type and pixel type
def test_convert_rasterinput_to_esri_bil():
    try:
        input_raster = r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\MDB_P75_3_0000009472-0000009472.tif'
        output_raster = r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\output\MDB_P75_3_0000009472-0000009472.bil'
        # run convert raster function
        convert_rasterinput_to_esri_bil(input_raster, output_raster)
        output_raster_bands = read_raster_bands(output_raster) # get new raster bands
        pixel_format = arcpy.Describe(output_raster_bands[0]).pixelType # get new raster pixel type
        raster_format = arcpy.Describe(output_raster).format # get new raster format
        assert arcpy.Exists(output_raster) and (len(output_raster_bands) == 6) and (raster_format == 'BIL')\
               and (pixel_format == 'S16')
    except Exception as err:
        printerrormsg("convert raster function error", str(err.args), str(traceback.format_exc()))
        raise(AssertionError)


def test_get_dataset_projection_factory_code():
    output_raster = r'\\prod.local\storage\GSS\STAND_CONDITION_TOOL_PROJECT\TOOLS\TESTDATA\\output\MDB_P75_3_0000009472-0000009472.bil'
    stand_condition_tool_data_spatial_reference_code = 4326
    assert(get_dataset_projection_factory_code(output_raster) == stand_condition_tool_data_spatial_reference_code)

if __name__ == "__main__":
    test_get_inputvariables()
    test_convert_rasterinput_to_esri_bil()
    test_get_dataset_projection_factory_code()
    test_create_envi_header_template()
    printmsg("Everything passed")
