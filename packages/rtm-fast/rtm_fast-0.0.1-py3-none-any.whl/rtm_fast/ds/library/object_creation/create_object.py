"""
    About module: Handles the creation of appropriate Sales and Store object for a market
"""
import sys
import traceback
from DSCode.common_utilities_registry import *

def get_sales_object(config, test_id):
    """
            About function
            --------------
            This function returns the appropriate sales object for a market
            In markets config there must be a key "Constructors" and this key will have
            a dictionary. In that dictionary there will be one key of "Sales".

            Note: dont set value of "Sales" key as Sales master class,
            developer needs to inherit Sales master class in common utility
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
            config: config set for the market,
            test_id: test_id of the current test

            Return values
            -------
            sales object
        """
    if 'Sales' in config['Constructors']:
        sales_object = getattr(sys.modules[__name__],
                            config["Constructors"]['Sales'])(config=config,
                                                            test_id=test_id)

        return sales_object
    raise Exception("An Error has occured while creating sales object: {}"\
                                        .format(traceback.format_exc()))

def get_store_object(config, test_id):
    """
            About function
            --------------
            This function returns the appropriate store object for a market
            In markets config there must be a key "Constructors" and this key will have
            a dictionary. In that dictionary there will be one key of "Store".

            Note: dont set value of "Store" key as Store master class,
            developer needs to inherit Store master class in common utility
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
            config: config set for the market,
            test_id: test_id of the current test

            Return values
            -------
            Store object
        """
    if 'Stores' in config['Constructors']:
        stores_object = getattr(sys.modules[__name__],
                                config["Constructors"]['Stores'])(config=config,
                                                                    test_id=test_id)
        return stores_object
    raise Exception("An Error has occured while creating stores object: {}"\
                                                .format(traceback.format_exc()))
