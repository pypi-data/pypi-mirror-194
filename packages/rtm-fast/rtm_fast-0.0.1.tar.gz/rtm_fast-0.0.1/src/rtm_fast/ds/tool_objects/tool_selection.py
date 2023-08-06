"""About module: App team interacts with this module to get an object of FAST tool flow.
The App team developer needs to pass region name (same as key present in config_data_registry.py)
"""
import sys
import traceback
from DSCode.ds_code_registry import *
from DSCode.config_data_registry import config

def get_tool_object(region, test_id):
    """
            About function
            --------------
            This function returns the appropriate FAST tool flow object for a market
            In markets config there must be a key "Constructors" and this key will have
            a dictionary. In that dictionary there will be one key of "Tool".

            Example
            -------
            US:{"Constructors": {
            "Sales": "FAST_US_Sales",
            "Stores": "FAST_US_Stores",
            "Tool": "Fast_US_Tool"},
            ....
            }

            Parameters
            ----------
            region: region or market name by which DS developer has registered code to library,
            test_id: test_id of the current test

            Return values
            -------
            tool flow object
        """
    config_copy = config[region].copy() if region in config else config.copy()
    if 'Tool' in config_copy['Constructors']:
        tool_object = getattr(sys.modules[__name__],
                            config_copy["Constructors"]['Tool'])(config=config_copy,
                                                                region=region,
                                                                test_id=test_id)
        return tool_object
    raise Exception("An Error has occured while creating stores object: {}"\
            .format(traceback.format_exc()))

def get_tool_msrmt_object(region, test_id):
    """
            About function
            --------------
            This function returns the appropriate FAST tool flow object for a market
            In markets config there must be a key "Constructors" and this key will have
            a dictionary. In that dictionary there will be one key of "Tool".

            Example
            -------
            US:{"Constructors": {
            "Sales": "FAST_US_Sales",
            "Stores": "FAST_US_Stores",
            "Tool": "Fast_US_Tool"},
            ....
            }

            Parameters
            ----------
            region: region or market name by which DS developer has registered code to library,
            test_id: test_id of the current test

            Return values
            -------
            tool flow object
        """
    config_copy = config[region].copy() if region in config else config.copy()
    if 'Tool' in config_copy['Constructors']:
        tool_object = getattr(sys.modules[__name__],
                            config_copy["Constructors"]['ToolMeasurement'])( fast_tool_plan = get_tool_object(region, test_id),
                                                                            config=config_copy,
                                                                            region=region,
                                                                            test_id=test_id)
        return tool_object
    raise Exception("An Error has occured while creating stores object: {}"\
            .format(traceback.format_exc()))
