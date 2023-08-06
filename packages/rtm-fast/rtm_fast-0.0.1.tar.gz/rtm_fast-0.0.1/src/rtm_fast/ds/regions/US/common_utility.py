"""
    About module: All customizations done for US market wrt Sales and Store functions

    Classes:
        FastStoresUS
        FastSalesUS
"""
from typing import Tuple

import pandas as pd
from DSCode.library.sql.sales_master import Sales
from DSCode.library.sql.stores_master import Stores


class FastSalesUS(Sales):
    """
    A class to represent features of TargetEstimate.
    ...

    Attributes
    ----------
    config : configuration present in config_data either for a region or overall
    region: key present in config
    sales_object : Object of sales class
    store_object : Object of store class

    Methods
    -------
    data_extract(): to calculate required sales/volume and get the store details in population
    calculate_rsv(): calculate the RSV/POS/Sales/Volume value required
                     and estimate number of stores in population
    get_breakeven_lift(): estimates the breakeven lift% value
    get_cost(): estimates the cost of implementing RTM activity if breakeven lift is known
    """
    def __init__(self, config,  test_id) -> None:
        super().__init__(config=config, test_id=test_id)
        self._cbu_sales = pd.DataFrame()
        self._overall = pd.DataFrame()

    def get_cbu_sales(self, stores, applicability_criteria, weeks):
        """
            About function
            --------------
            This function interacts with weekly sales table and calculates the
            sales of selected products (total sales of products) at store in the given weeks

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store) selection
            made in the tool week: list of week values in which sales needs to be calculated

            Return values
            -------
            dataframe with weekly sales of the stores
        """
        if "businessType" not in applicability_criteria:
            raise Exception("businessType not passed to applicability criteria")
        applicability_criteria['consumption_value'].append("")
        applicability_criteria['seasonal_value'].append("")
        applicability_criteria['category_value'].append("")
        applicability_criteria['brands_value'].append("")
        applicability_criteria['pack_value'].append("")
        applicability_criteria['store_value'] = tuple(stores)
        applicability_criteria['week_value'] = tuple(weeks)
        applicability_criteria['category_value'] = tuple(applicability_criteria['category_value'])
        applicability_criteria['brands_value'] = tuple(applicability_criteria['brands_value'])
        applicability_criteria['pack_value'] = tuple(applicability_criteria['pack_value'])
        applicability_criteria['consumption_value'] = tuple(
                                                    applicability_criteria['consumption_value']
                                                    )
        applicability_criteria['seasonal_value'] = tuple(applicability_criteria['seasonal_value'])

        if applicability_criteria['businessType'] == "MW":
            query = """SELECT Week, StoreId,ROUND(SUM(POS),2) as POS,ROUND(SUM(Volume),2) as Volume,
                                 '{channel}' as StoreClassification
                            FROM {sales_table} as sales JOIN {product_table} as products ON products.UPC=sales.UPC
                                AND products.StoreClassification='{channel}'
                                AND Category IN {category_value}
                                AND brands IN {brands_value}
                                AND PackType IN {pack_value}
                                AND Consumption IN {consumption_value}
                                AND seasonalPackaging IN {seasonal_value}
                                AND IsMars = 1 AND Week IN {week_value}
                                AND StoreId IN {store_value}
                            GROUP BY Week, StoreId"""

        else:
            query = """SELECT Week, StoreId,ROUND(SUM(POS),2) as POS,ROUND(SUM(Volume),2) as Volume,
                                '{channel}' as StoreClassification
                            FROM {sales_table} as sales JOIN {product_table} as products ON products.UPC=sales.UPC
                                AND products.StoreClassification='{channel}'
                                AND Category IN {category_value}
                                AND brands IN {brands_value}
                                AND PackType IN {pack_value}
                                AND Consumption IN {consumption_value}
                                AND seasonalPackaging IN {seasonal_value}
                                AND Week IN {week_value}
                                AND StoreId IN {store_value}
                            GROUP BY Week, StoreId"""
        self._cbu_sales = self.execute_sql_query(query, applicability_criteria)
        return self._cbu_sales

    def get_overall_sales(self, stores, weeks, applicability_criteria=None):
        """
            About function
            --------------
            This function interacts with weekly sales table and calculates the overall sales
            (doesnt consider product attributes) at store in the given weeks

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store) selection
                        made in the tool
            week: list of week values in which sales needs to be calculated

            Return values
            -------
            dataframe with weekly sales of the stores
        """
        if "businessType" not in applicability_criteria:
            raise Exception("businessType not passed to applicability criteria")
        applicability_criteria['store_value'] = tuple(stores)
        applicability_criteria['week_value'] = tuple(weeks)
        if applicability_criteria['businessType'] == "MW":
            query = """SELECT Week, StoreId, ROUND(SUM(POS),2) as POS,
                                ROUND(SUM(Volume),2) as Volume,'{channel}' as StoreClassification
                        FROM {sales_table} as sales JOIN {product_table} as products ON products.UPC=sales.UPC
                            AND products.StoreClassification='{channel}'
                            AND IsMars = 1 AND Week IN {week_value}
                            AND StoreId IN {store_value}
                        GROUP BY Week, StoreId"""
        else:
            query = """SELECT Week, StoreId, ROUND(SUM(POS), 2) as POS,
                            ROUND(SUM(Volume), 2) as Volume, '{channel}' as StoreClassification
                        FROM {sales_table} as sales
                        WHERE Week IN {week_value}  AND StoreId IN {store_value}
                        GROUP BY Week, StoreId"""
        self._overall = self.execute_sql_query(query, applicability_criteria)
        return self._overall


    def get_total_weekly_target_data(self, test_master_df, stores_list, sales_week,target_variable,\
        applicability_criteria, test_type, consideryearweeks=None) \
                                -> Tuple[pd.DataFrame, list, str, bool]:
        """
            About function
            --------------
            This function gets the overall sales in the "sales week" time period or
            weeks to be considered

            Parameters
            ----------
            prewindow_end: date on which preperiod ends,
            stores_list: list of stores for which lift is calculated,
            applicability_criteria: the product and stores attributes selected at
                        tool in dictionary format,
            test_type: type of test from the tool selection (Activity, RTM impact, others...),
            sales_week: optional parameter is the number of weeks for
                    which the sales to be calculated and validated ,
            consideryearweeks: optional parameter a list of weeks, if want to skip
                    the calculation of weeks
            example
            -------

            if want to calculate yearly lift then sales_week = 104 (52*2 number of weeks);
            sales_lifts_sales_weeks = 52 (number of weeks in a year)

            Return values
            -------
            overall sales values dataframe,
            list of weeks on which sales is calculated,
            message
            success flag
        """
        sales_week=self._config['metadata']['test_configuration']\
                        ['sales_weeks']\
                        [applicability_criteria['channel']]
        weekly_target_variables_file, consideryearweeks,\
             message, success_flag = super().get_total_weekly_target_data(
                                    target_variable=target_variable,
                                    test_master_df = test_master_df,
                                    stores_list = stores_list,
                                    sales_week = sales_week,
                                    applicability_criteria = applicability_criteria,
                                    test_type = test_type,
                                    consideryearweeks = consideryearweeks)
        return weekly_target_variables_file, consideryearweeks, message, success_flag

    def get_max_week_config_master(self, applicability_criteria=None):
        """
            About function
            --------------
            This function interacts with config master table in the database and returns
             max date maintained in the table

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                    selection made in the tool

            Return values
            -------
            max date maintained in the table
        """
        config_master = self.execute_sql_query(query="SELECT * FROM {table_name}",
                                                data={"table_name": self._config['tables']\
                                                                    ['config_mstr'],
                                                    "channel":applicability_criteria["channel"]})
        print(config_master)
        print(config_master.columns)
        return config_master[config_master['key'] == 'max_date']['week'].values[0]



class FastStoresUS(Stores):
    """
    A class to represent features of TargetEstimate.
    ...

    Attributes
    ----------
    config : configuration present in config_data either for a region or overall
    region: key present in config
    sales_object : Object of sales class
    store_object : Object of store class

    Methods
    -------
    data_extract(): to calculate required sales/volume and get the store details in population
    calculate_rsv(): calculate the RSV/POS/Sales/Volume value required
                     and estimate number of stores in population
    get_breakeven_lift(): estimates the breakeven lift% value
    get_cost(): estimates the cost of implementing RTM activity if breakeven lift is known
    """
    def __init__(self, config, test_id) -> None:
        super().__init__(config=config, test_id=test_id)

    def get_filtered_stores(self, applicability_criteria):
        """
            About function
            --------------
            This function needs to be overriden, developer needs to write the query
            to get store information from the storemaster table
            based on the filter selected in the applicability criteria

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store)
            selection made in the tool

            Return values
            -------
            store attributes dataframe
        """
        if "team" not in applicability_criteria:
            raise Exception("team is not passed to applicability criteria")
        # """Returns the store information based on applicability criteria filters"""
        applicability_criteria['regions_value'].append("")
        applicability_criteria['territory_value'].append("")
        applicability_criteria['store_name_value'].append("")
        applicability_criteria['segments_value'].append("")
        applicability_criteria['store_name_value'] = \
                                                tuple(applicability_criteria['store_name_value'])
        applicability_criteria['segments_value'] = \
                                                tuple(applicability_criteria['segments_value'])
        applicability_criteria['regions_value'] = \
                                                tuple(applicability_criteria['regions_value'])
        applicability_criteria['territory_value'] = \
                                                tuple(applicability_criteria['territory_value'])
        if applicability_criteria['team'] == 'RTM':
            query_store_filter = """SELECT *
                                    FROM {store_table}
                                    WHERE StoreClassification = '{channel}'
                                        AND IsCovered = 1
                                        AND RegionName IN {regions_value}
                                        AND TerritoryName IN {territory_value}
                                        AND StoreName IN {store_name_value}
                                        AND MasterChain IN {segments_value}"""
        else:
            query_store_filter = """SELECT * FROM {store_table}
                                    WHERE StoreClassification = '{channel}'
                                        AND RegionName IN {regions_value}
                                        AND TerritoryName IN {territory_value}
                                        AND StoreName IN {store_name_value}
                                        AND MasterChain IN {segments_value}"""
        return self.execute_sql_query(query_store_filter, applicability_criteria)

    def get_uploaded_stores_info(self, stores_list, applicability_criteria):
        """
            About function
            --------------
            This function needs to be overriden, developer needs to write the query to get
            store information from the storemaster table
            based on the list of the store identifier (config[store_mstr_columns][partner_id])
            value present in stores_list

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store)
            selection made in the tool

            Return values
            -------
            store attributes dataframe
        """
        applicability_criteria['store_value'] = tuple(stores_list)
        query_uploaded_population = """SELECT *
                                        FROM {store_table}
                                        WHERE StoreId IN {store_value}
                                        AND StoreClassification = '{channel}'"""

        return self.execute_sql_query(query_uploaded_population, applicability_criteria)

    def check_details_uploaded_stores(self, stores_list, applicability_criteria):
        """
            This function based on the selection (StoreId, StoreNumber, TDLinxNo) will check
            uploaded values with appropriate columns
        """
        if stores_list is None:
            stores_list = []
        stores_list.append(-1)
        applicability_criteria['store_value'] = tuple(stores_list)

        query = "SELECT * FROM {store_table} WHERE {store_identifier_attribute} IN {store_value}"
        return self.execute_sql_query(query, stores=stores_list,data= applicability_criteria)

    def validate_uploaded_presence_store_master(self, uploaded_stores, \
                store_identifier, applicability_criteria)->Tuple[pd.DataFrame, str, bool]:
        if 'store_identifier_attribute' not in applicability_criteria:
            return pd.DataFrame(),\
                     "Please pass the Store identifier attribute to the function", False
        store_idn_att = applicability_criteria['store_identifier_attribute']
        if (applicability_criteria['store_identifier_attribute'] == 'StoreNumber') \
            & (('segments_value' not in applicability_criteria) \
                    or (len(applicability_criteria['segments_value']) == 0)):
            return pd.DataFrame(), "Please pass the MasterChain info to the upload function", False

        stores_list = list(uploaded_stores[store_identifier].unique())

        upld_str_dtls = self.check_details_uploaded_stores(stores_list=stores_list[:],
                                                                    applicability_criteria=applicability_criteria)
        str_iden_clmn = self._storemstrmapping['partner_id']
        banner_clmn = self._config["store_mstr_columns"]["banner"]
        covered_clmn = self._storemstrmapping["is_covered"]
        if upld_str_dtls.shape[0] == 0:
            return upld_str_dtls, "All uploaded stores are not present in Store Master!!", False
        stores_list = list(set(stores_list) - set([-1]))
        message = "Out of {uploaded_stores} uploaded stores, {stores_present} in store master"\
                                                    .format(uploaded_stores=len(stores_list),
                                                    stores_present=len(set(upld_str_dtls[store_idn_att].unique())- set([-1])))

        # """If different channel stores are uploaded"""
        if applicability_criteria["channel"] not in upld_str_dtls[banner_clmn].unique():
            diff_banner_str = upld_str_dtls[upld_str_dtls[banner_clmn]!=applicability_criteria["channel"]]
            return pd.DataFrame(), "Please remove!! Stores belonging to other channels {} \n"\
                        .format(diff_banner_str[store_idn_att].values.tolist()), False
        check_details = upld_str_dtls[upld_str_dtls[banner_clmn] == applicability_criteria["channel"]]
        message = "Out of {uploaded_stores} valid stores, {stores_present} in selected channel"\
                        .format(uploaded_stores = len(set(upld_str_dtls[store_idn_att].unique())- set([-1])),
                                stores_present=check_details[store_idn_att].nunique()) + '\n' +message

        upld_str_dtls = check_details

        # """Fetch details of the uploaded stores"""
        if (applicability_criteria["team"] == "RTM") & (0 in upld_str_dtls[covered_clmn].unique()):
            return pd.DataFrame(), "Please remove!! NON-RTM stores found. List of {} that belongs to NON-RTM: {}\n"\
                .format(store_idn_att,
                        upld_str_dtls[upld_str_dtls[covered_clmn]==0]\
                                [store_idn_att].unique()) + message, False
        if applicability_criteria["team"] == "RTM":
            check_details = upld_str_dtls[upld_str_dtls[covered_clmn] == 1]
            upld_str_dtls = check_details
        # """if store number are uploaded then no storenumber is mapped to multiple storeIds"""

        if store_identifier == 'StoreNumber':
            map_store_id = upld_str_dtls.groupby('StoreNumber').aggregate({str_iden_clmn:'nunique'}).reset_index()
            if map_store_id[map_store_id[str_iden_clmn]>1].shape[0]>0:
                return pd.DataFrame(), \
                    "Please remove!!Some Store Numbers({}) are mapped to multiple StoreIds\n"\
                                            .format(list(map_store_id[map_store_id[str_iden_clmn]>1]\
                                                ['StoreNumber'].unique())) + message, False

        return upld_str_dtls, message, True

