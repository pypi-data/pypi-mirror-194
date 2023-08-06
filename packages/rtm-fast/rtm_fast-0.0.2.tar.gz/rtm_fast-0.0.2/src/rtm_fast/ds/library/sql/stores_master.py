
from datetime import datetime
from typing import Tuple, final

import pandas as pd

from .utility.sql_utility import SqlUtility


class Stores(SqlUtility):

    def __init__(self, config,  test_id):
        super().__init__(config)
        self._test_id = test_id
        self._metadata = self._config["metadata"]
        self._storemstrmapping = self._config["store_mstr_columns"]

    def set_test_id(self, test_id):
        """Sets the current test_id"""
        self._test_id = test_id

    def get_filtered_stores(self, applicability_criteria)->pd.DataFrame:
        """
            About function
            --------------
            This function needs to be overriden, developer needs to write the query to get store information from the storemaster table
            based on the filter selected in the applicability criteria

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store) selection made in the tool

            Return values
            -------
            store attributes dataframe
        """
        pass

    def get_uploaded_stores_info(self, stores_list, applicability_criteria)->pd.DataFrame:
        """
            About function
            --------------
            This function needs to be overriden, developer needs to write the query to get store information from the storemaster table
            based on the list of the store identifier (config[store_mstr_columns][partner_id]) value present in stores_list

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store) selection made in the tool

            Return values
            -------
            store attributes dataframe
        """
        pass

    def filter_population_uploaded_stores(self, uploaded_file_df=None) -> list:
        """
            About function
            --------------
            Once the uploaded population stores are stored in the database table 'config['tables']['upload_stores']' (storing of uploaded stores will be done by UI team)
            now these stores will be considered as the population stores everytime (store filters in the applicability criteria will be considered)

            Note: config['tables']['upload_stores'] this table will be maintaining store identifier refer config[store_mstr_columns][partner_id]
            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store) selection made in the tool

            uploaded_file_df: optional dataframe for DS person to work on upload functionality; it will have same attributes like config['tables']['upload_stores']
            Return values
            -------
            list of store identifiers
        """
        if (self._test_id is None) or ("upload_stores" not in self._config['tables']):
            storelist = []
        else:
            if uploaded_file_df is None:
                storelistquery = """SELECT store_id as {column_name} FROM {db}
                                    WHERE test_id_id = {testid}"""
                storelistqueryDf = self.execute_sql_query(query=storelistquery, data={"column_name": self._config["store_mstr_columns"]['partner_id'],
                                                                                        "db": self._config['tables']['upload_stores'],
                                                                                        "testid": self._test_id})
            else:
                storelistqueryDf = uploaded_file_df
                storelistqueryDf = storelistqueryDf[storelistqueryDf['test_id_id'] == self._test_id]

            storelist = [] if storelistqueryDf.shape[0] == 0 else list(storelistqueryDf[self._config["store_mstr_columns"]['partner_id']].unique())
        return storelist

    def filter_population(self, applicability_criteria, storelist=[],  uploaded_file_df = None)->pd.DataFrame:
        """
            About function
            --------------
            All the tool features depends on the population of stores, this function fetches the store records that meet either of the following:
            1) Store that were uploaded by user
            2) if stores were not uploaded then this function will use the store filter selected in applicability criteria to get stores

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store) selection made in the tool

            storelist: optional parameter in case the developer needs to fetch the attributes of known store identifier
            uploaded_file_df: optional dataframe for DS person to work on upload functionality; it will have same attributes like config['tables']['upload_stores']
            Return values
            -------
            dataframe of store attributes
        """
        if not storelist:
            storelist = self.filter_population_uploaded_stores(uploaded_file_df=uploaded_file_df)
        if not storelist:
            stores_master_df = self.get_filtered_stores( applicability_criteria=applicability_criteria)
        else:
            storelist.append(-1)
            stores_master_df = self.get_uploaded_stores_info(
                                                                stores_list = storelist,
                                                                applicability_criteria=applicability_criteria)
        return stores_master_df

    def read_test_master_table_by_test_ids(self, test_id) -> pd.DataFrame:
        """
            About function
            --------------
            This function reads all the details regarding the test from test master table refer config[tables][test_mstr]

            Parameters
            ----------
            test_id: could be a list of test ids or a single test id

            -------
            dataframe of test master filtered for specified test_id/s
        """
        if isinstance(test_id, list) ==False:
            test_id = [test_id]
        test_id.append(-1)
        return self.execute_sql_query(query="SELECT * FROM {test_master_table} WHERE is_active=1 and is_deleted = 0 AND test_id IN {test_ids}", data={'test_master_table': self._config['tables']['test_mstr'], "test_ids":tuple(test_id)})

    def read_test_measurement_table_by_test_ids(self, test_id):
        """
            About function
            --------------
            This function reads all the details from the test measturement table refer config[tables][test_mstr]

            Parameters
            ----------
            test_id: could be a list of test ids or a single test id

            -------
            dataframe of test measurement filtered for specified test_id/s
        """
        if isinstance(test_id, list) ==False:
            test_id = [test_id]
        test_id.append(-1)
        temp = self.execute_sql_query(query="SELECT * FROM {test_measurement_table} WHERE is_active=1 and is_deleted = 0 AND test_id IN {test_ids}", data={'test_measurement_table': self._config['tables']['measurement'], "test_ids":tuple(test_id)})
        if temp.shape[0] == 0:
            temp = pd.DataFrame(columns=['test_id_id'])
        return temp

    def read_test_master_table_active_tests(self, date):
        """
            About function
            --------------
            This function returns all tests records that have postwindow end date greater than input date. Table refer config[tables][test_mstr]

            Parameters
            ----------
            date: string value of format 'yyyy-mm-dd'

            -------
            dataframe of test measurement
        """
        temp = self.execute_sql_query(query="SELECT * FROM {test_master_table} WHERE is_active=1 and is_deleted = 0 AND testwin_end> '{date}'", data={'test_master_table': self._config['tables']['test_mstr'], "date":date})
        if temp.shape[0] == 0:
            temp = pd.DataFrame(columns=['test_id'])
        return temp

    def read_test_map_table_by_test_ids(self, test_id)->pd.DataFrame:
        """
            About function
            --------------
            This function reads all the details from the test store map table refer config[tables][test_store_map];
            This table stores the list of stores uploaded for the test

            Parameters
            ----------
            test_id: could be a list of test ids or a single test id

            -------
            dataframe of test store map filtered for specified test_id/s
        """
        if isinstance(test_id, list) ==False:
            test_id = [test_id]
        test_id.append(-1)
        temp = self.execute_sql_query(query="SELECT * FROM {test_map_table} WHERE is_active=1 and is_deleted = 0 AND test_id_id IN {test_id_ids}", data={"test_map_table": self._config['tables']['test_store_map'], "test_id_ids":tuple(test_id)})
        if temp.shape[0] == 0:
            temp = pd.DataFrame(columns=['created_on','modified_on','is_active','deleted_at','is_deleted','storemap_id','teststore_id','created_by_id','test_id_id','updated_by_id'])
        return temp

    def read_test_map_table_active_test_variable_dates(self, date) -> pd.DataFrame:
        """
            About function
            --------------
            This function reads all the details from the test store map table where postwindow end is greater than the date;
            Table name refer config[tables][test_store_map];
            This table stores the list of stores uploaded for the test

            Parameters
            ----------
            test_id: could be a list of test ids or a single test id

            -------
            dataframe of test store map filtered for specified test_id/s
        """
        temp = self.execute_sql_query(query="SELECT * FROM {test_map_table} WHERE is_active=1 and is_deleted = 0 AND testwin_end > '{date}'", data={"test_map_table": self._config['tables']['test_store_map'], "date":date})
        if temp.shape[0] == 0:
            temp = pd.DataFrame(columns=['created_on','modified_on','is_active','deleted_at','is_deleted','storemap_id','teststore_id','created_by_id','test_id_id','updated_by_id'])
        return temp

    def read_control_store_by_test_ids(self, test_id)->Tuple[str, bool]:
        """
            About function
            --------------
            This function reads all the details from the control store master table where test id is in the list/value passed;
            Table name refer config[tables][control_store_mstr];
            This table stores the list of stores uploaded for the test

            Parameters
            ----------
            test_id: could be a list of test ids or a single test id

            -------
            dataframe of test store map filtered for specified test_id/s
        """
        if isinstance(test_id, list) ==False:
            test_id = [test_id]
        test_id.append(-1)
        temp = self.execute_sql_query(query="SELECT * FROM {control_store_master} WHERE is_active = 1 and is_deleted = 0 AND test_id_id IN {test_id_ids}", data={"control_store_master": self._config['tables']['control_store_mstr'], "test_id_ids":tuple(test_id)})
        if temp.shape[0] == 0:
            temp = pd.DataFrame(columns=['is_active','is_deleted','constore_id','created_by_id','test_id_id','updated_by_id'])
        return temp

    @final
    def filter_active_test_control_stores(self, stores_master_df=None,   remove_type=None, max_week_data_available=None):
        """
            About function
            --------------
            This function removes the test or control stores from the stores_master_df passed

            Parameters
            ----------
            stores_master_df: population stores or dataframe of the stores
            remove_type: default is value set in config; based on that it either removes the active test stores or both active test and control stores,
            max_week_data_available: string 'yyyy-mm-dd' maximum date for which data is available in the database

            Return value
            -------
             message, success_flag
        """
        # Need to make Change here as per interaction with Database (starting here)
        storemstrmapping = self._config["store_mstr_columns"]
        if self._config["feature_parameter"]["test_variable_dates"] == 1:
            test_map_df = self.read_test_map_table_active_test_variable_dates(max_week_data_available)
            active_test = list(test_map_df['test_id_id'].unique())
            temp_test = list(self.read_test_master_table_by_test_ids(active_test)['test_id'].unique())
            active_test = set(temp_test).intersection(set(active_test))
        else:

            print("Fetching active test from test master table")
            active_test = list(self.read_test_master_table_active_tests(max_week_data_available)['test_id'].unique())
            active_test = list(set(active_test) - set([self._test_id]))
            if len(active_test)>0:
                test_map_df = self.read_test_map_table_by_test_ids(active_test)
            else:
                return stores_master_df

        active_test = list(set(active_test) - set([self._test_id]))
        if len(active_test) != 0:
            filtered_stores_df = stores_master_df[~stores_master_df[self._storemstrmapping['partner_id']].isin(
                test_map_df[test_map_df['test_id_id'].isin(active_test)]['teststore_id'].unique())]
            test_control_pair_df = self.read_control_store_by_test_ids(active_test)
            if test_control_pair_df.shape[0] > 0 and remove_type == 'both':
                """get the control stores info from the active tests details"""
                active_control_stores = test_control_pair_df[test_control_pair_df["test_id_id"].isin(
                    active_test)]
                """Filter the control stores"""
                if active_control_stores.shape[0] != 0:
                    filtered_stores_df = filtered_stores_df[~filtered_stores_df[storemstrmapping["partner_id"]].isin(
                        active_control_stores[storemstrmapping['partner_id']].values.tolist())]

            stores_master_df = filtered_stores_df
        return stores_master_df


    @final
    def validate_uploaded_stores_format(self, reference_file, uploaded_file, columns) -> Tuple[str, bool]:
        """
            About function
            --------------
            This function validates the uploaded store file with the columns passed


            Parameters
            ----------
            uploaded_file: the actual file user has uploaded
            uploaded_file: template file
            columns: by default it is extracted from the config file
            -------
             message, success_flag
        """

        if reference_file.shape[1] == 0:
            return "Reference file doesnt have any columns!!", False
        if uploaded_file.shape[1] == 0:
            return "Uploaded file doesnt have any columns!!", False

        if uploaded_file.shape[0] == 0:
            return "Uploaded file is empty!!", False

        check_number_columns = uploaded_file.shape[1] == reference_file.shape[1]
        if check_number_columns is False:
            return "Please refer template. Number of columns in uploaded file does not match with template", False

        check_column_names = sorted(
            uploaded_file.columns) == sorted(reference_file.columns)
        if check_column_names is False:
            return "Please refer template. Name of columns in uploaded file does not match with template", False

        actual_file_column_format = dict(
            uploaded_file.loc[:, sorted(uploaded_file.columns)].dtypes)
        reference_file_column_format = dict(sorted(columns))

        if actual_file_column_format != reference_file_column_format:
            return "Please ensure that uploaded matches the following datatypes: {}".format(reference_file_column_format), False
        check_format = actual_file_column_format == reference_file_column_format
        if check_number_columns & check_column_names & check_format:
            return "Uploaded file follows the template!!", True
        return "Uploaded file doesn't follow the template!!", False


    def validate_uploaded_presence_store_master(self, uploaded_stores, store_identifier, applicability_criteria)->Tuple[pd.DataFrame, str, bool]:
        """
            About function
            --------------
            This function validates the uploaded store from the store master table

            Parameters
            ----------
            uploaded_stores: the actual file user has uploaded
            store_identifier:
            applicability_criteria:
            -------
            dataframe of valid stores, message, success_flag
        """

        uploaded_stores_list = list(uploaded_stores[store_identifier].unique())
        total_stores = len(uploaded_stores_list)
        temp_uploaded_stores_list = uploaded_stores_list[:]
        temp_uploaded_stores_list.append(-1)
        uploaded_stores_mapped = self.get_uploaded_stores_info(stores_list = temp_uploaded_stores_list, applicability_criteria=applicability_criteria)
        if uploaded_stores_mapped.shape[0] == 0:
            return uploaded_stores_mapped, "All uploaded stores are not present in Store Master!!", False
        stores_not_mapped = set(uploaded_stores_list) - set(uploaded_stores_mapped[self._config["store_mstr_columns"]["partner_id"]].unique())
        stores_mapped = uploaded_stores_mapped.shape[0]
        percentage_mapped = round((uploaded_stores_mapped.shape[0])*100/total_stores, 2)
        message = "Out of {total_stores}, {store_mapped} got mapped which is around {percentage_mapped}".format(total_stores=total_stores, store_mapped=stores_mapped, percentage_mapped=percentage_mapped)

        return uploaded_stores_mapped, message, True

    @final
    def validate_uploaded_stores_active_stores(self, stores_df, max_date_data_available, active_stores_filter_type="both") -> Tuple[pd.DataFrame, pd.DataFrame, str, bool]:
        """
            About function
            --------------
            This function validates the uploaded store information and calculate the number of stores that are active in other test

            Parameters
            ----------
            stores_df: dataframe of the stores information that have been uploaded (must have config[store_mstr_columns][partner_id])
            max_date_data_available: string value of the maximum date data maintained in the sales table. Format 'yyyy-mm-dd'
            active_stores_filter_type: variable to keep a check on if we want to remove both test and control stores or test store only
                                    default value is 'both';
            -------
            dataframe of filtered stores, message, success_flag
        """


        filtered_stores = self.filter_active_test_control_stores(
            stores_master_df=stores_df,
            remove_type=active_stores_filter_type,
            max_week_data_available=max_date_data_available)
        if filtered_stores.shape[0] == 0:
            return filtered_stores, "All uploaded stores are participating in other tests", False
        total_stores = stores_df[self._config["store_mstr_columns"]["partner_id"]].nunique()
        active_stores = total_stores-filtered_stores[self._config["store_mstr_columns"]["partner_id"]].nunique()
        percent_active  = round(active_stores*100/total_stores, 2)
        message = "Out of {total_stores} valid stores, {active_stores} are active which is around {percentage} % cannot be used as test/control stores".format(total_stores=total_stores, active_stores=active_stores, percentage=percent_active)
        return filtered_stores, message, True
