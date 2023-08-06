"""
    About module: Handles all the features that are related to
    Sales/volume fetch from the datasource
    Classes:
        Sales
"""

from datetime import datetime, timedelta
from typing import Tuple
import pandas as pd
from DSCode.library.ds_common_functions import str_to_date
from .utility.sql_utility import SqlUtility

class Sales (SqlUtility):
    """
    A class to represent features of Sales.
    ...

    Attributes
    ----------

    Methods
    -------
    """
    def __init__(self, config, test_id=None):
        """
        Constructs all the necessary attributes for the rsv estimate object.

        Parameters
        ----------
            config : configuration present in config_data either for a region or overall
            test_id: the id given to current test
        """
        super().__init__(config)
        self._test_id = test_id
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._metadata = self._config["metadata"]["test_configuration"]

    def get_sales_weeks(self, applicability_criteria) -> int:
        """
            About function
            --------------
            This function returns the sales weeks set from config of the region
            This checks applicability criteria first if there is "sales_weeks" key in it

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store)
            selection made in the tool

            example
            -------
            if want to calculate yearly lift then sales_week = 104 (52*2 number of weeks);
             sales_lifts_sales_weeks = 52 (number of weeks in a year)


            Return values
            -------
            integer value of weeks to be considered in sales calculation
        """

        if 'sales_weeks' in applicability_criteria:
            return applicability_criteria['sales_weeks']
        return self._metadata["sales_weeks"]

    def get_lift_sales_weeks(self, applicability_criteria) -> int:
        """
            About function
            --------------
            This function returns the number of weeks to be considered for lift calculation
            This checks applicability criteria first if there is "sales_lifts_sales_weeks" key in it

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store)
                selection made in the tool

            example
            -------
            if want to calculate yearly lift then sales_week = 104 (52*2 number of weeks);
            sales_lifts_sales_weeks = 52 (number of weeks in a year)

            Return values
            -------
            integer value of weeks to be considered for lift calculation
        """
        if 'sales_lifts_sales_weeks' in applicability_criteria:
            return applicability_criteria['sales_lifts_sales_weeks']
        return self._metadata['sales_lifts_sales_weeks']

    def get_summary_sales_weeks(self, applicability_criteria):

        """
            About function
            --------------
            It returns the number of weeks for which sales need to be calculated
            to calculate the summary.

            It checks both applicability criteria and config.
            First priority is given to applicability criteria

            Parameters
            ----------
            applicability_criteria: key-value pairs of the filters (product and store)
                selection made in the tool


            Return values
            -------
            integer value of weeks to be considered for summary calculations
        """
        if 'summary_sales_weeks' in applicability_criteria:
            return applicability_criteria['summary_sales_weeks']
        return self._config['metadata']['test_planning']\
                                            ['summary_sales_weeks']


    def get_cbu_sales(self, stores, applicability_criteria, weeks) -> pd.DataFrame:
        """
            About function
            --------------
            This function interacts with weekly sales table and calculates the
            sales and volume of selected products(total sales of products)
            at store in the given weeks

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                selection made in the tool
            week: list of week values in which sales needs to be calculated

            Return values
            -------
            dataframe with weekly sales of the stores
        """
        print("{} {} {} {}".format(self._test_id,stores, applicability_criteria, weeks))
        return pd.DataFrame()

    def get_overall_sales(self, stores, weeks, applicability_criteria=None) -> pd.DataFrame:
        """
            About function
            --------------
            This function interacts with weekly sales table and calculates the overall
            sales and volume (doesnt consider product attributes) at store in the given weeks

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                selection made in the tool
            week: list of week values in which sales needs to be calculated

            Return values
            -------
            dataframe with weekly sales of the stores
        """
        print("{} {} {} {} ".format(self._test_id,stores, applicability_criteria, weeks))
        return pd.DataFrame()

    def get_max_week_config_master(self, applicability_criteria=None) -> str:
        """
            About function
            --------------
            This function interacts with config master table in the database and returns
            max date maintained in the config table

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                    selection made in the tool

            Return values
            -------
            max date maintained in the table
        """
        print(len(applicability_criteria.keys()))
        config_master = self.execute_sql_query(query="SELECT * FROM {table_name}",
                                            data={
                                               "table_name": self._config['tables']['config_mstr']
                                               })
        return config_master[config_master['key_name'] == 'max_date']['week'].values[0]

    def get_valid_weekly_target_data(self, stores, applicability_criteria,\
         target_variable, test_master_df,test_type,\
             sales_week, consideryearweeks=None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:

        """
            About function
            --------------
            get valid weekly target data calculates the selected product sales and overall sales;
            merge them and validate for continuity check.
            Set 'is_product_present' in config to 0 in case region doesnt have product attributes.
            And set 'data_continuity_check' in config to 0 in case dont want to have
            sales continuity checks

            Parameters
            ----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                        selection made in the tool
            target_variable: Sales column name or volume column name
            prewindow_start: starting date of the prewindow
            prewindow_end: end date of the prewindow
            postwindow_start: starting date of the postwindow
            postwindow_end: end date of the postwindow
            test_type: to handle any test_type conditions
            business_categories: optional parameter
            consideryearweeks: optional parameter to skip the week calculation done in the function

            Return values
            -------
            product and overall sales value merged at store and week level, message and success flag
        """
        if target_variable is not None:
            #Following condition is there in case there are regions that wants validate sales on
            #  different time period
            if consideryearweeks is None:
                consideryearweeks = []
            if not consideryearweeks:
                yearweeks = self.find_last104_weeks_from_baseline_end(
                        str_to_date(test_master_df['pre_end'].values[0])
                        )
                yearweeks.sort(reverse=True)
                consideryearweeks = yearweeks[:sales_week]
                consideryearweeks.sort(reverse=False)
            stores.append(-1)
            print(test_type)
            #"""Execute the overall sales query"""
            weekly_overal_level_sales = self.get_overall_sales(
                                        stores=stores,
                                        applicability_criteria=applicability_criteria,
                                        weeks=consideryearweeks)
            #"""if region supports product attributes"""
            if weekly_overal_level_sales.shape[0] == 0:
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), consideryearweeks, "Overall sales for stores not found", False
            store_identifier = self._tarvarmapping['partner_id']
            weekly_cbu_level_sales = pd.DataFrame()
            if self._config["feature_parameter"]["is_product_present"] == 1:
                #"""Execute the CBU sales query """
                weekly_cbu_level_sales = self.get_cbu_sales(
                                            stores=stores,
                                            applicability_criteria=applicability_criteria,
                                            weeks=consideryearweeks
                                            )
                if weekly_cbu_level_sales.shape[0] == 0:
                    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), consideryearweeks,"CBU sales for stores not found", False
                rsv_lbl = self._tarvarmapping["rsv"]
                vol_lbl = self._tarvarmapping['volume']
                #"""Renaming the CBU query target variables to required columnes"""
                weekly_cbu_level_sales.rename(columns={rsv_lbl: "CBU_Category_"+rsv_lbl,
                                                        vol_lbl: 'CBU_Category_'+vol_lbl},
                                                         inplace=True)
                #"""Join the CBU query results and Overall query results"""
                weekly_merged_level_sales = weekly_overal_level_sales\
                                    .merge(weekly_cbu_level_sales,
                                            on=[store_identifier,
                                                self._tarvarmapping["banner"],
                                                self._tarvarmapping['week']])
                #"""Remove stores with 0 sales value"""
                if target_variable == rsv_lbl:
                    eliminatestores1 = weekly_merged_level_sales[weekly_merged_level_sales[
                        "CBU_Category_"+target_variable] == 0][store_identifier].unique()
                else:
                    eliminatestores1 = weekly_merged_level_sales[weekly_merged_level_sales[
                        "CBU_Category_"+target_variable] == 0][store_identifier].unique()
                weekly_merged_level_sales = weekly_merged_level_sales[~(
                    weekly_merged_level_sales[store_identifier]\
                            .isin(eliminatestores1))]
            else:
                weekly_merged_level_sales = weekly_overal_level_sales

            #"""Data Continuity check"""
            if self._config['feature_parameter']['data_continuity_check'] == 1:
                weekcountsdf = weekly_merged_level_sales\
                    .groupby(store_identifier)[self._tarvarmapping["week"]]\
                    .nunique()\
                    .reset_index()\
                    .rename(columns={self._tarvarmapping["week"]: "Week_Count"})
                eliminatestores2 = weekcountsdf[weekcountsdf["Week_Count"]
                                                < sales_week][store_identifier].unique()
                if len(eliminatestores2) > 0:
                    #"""Eliminate stores that may not have continuous data"""
                    weekly_merged_level_sales = weekly_merged_level_sales[~(
                        weekly_merged_level_sales[store_identifier].isin(eliminatestores2))]
                if weekly_merged_level_sales.shape[0] == 0:
                    return weekly_merged_level_sales, weekly_overal_level_sales,\
                     weekly_cbu_level_sales, consideryearweeks,\
                         "No store match with continuity criteria! Modify parameter selected", \
                            False
            if weekly_merged_level_sales.shape[0] == 0:
                return weekly_merged_level_sales, weekly_overal_level_sales,\
                     weekly_cbu_level_sales, consideryearweeks,\
                        "No common week-store pair found in overall and cbu sales",\
                             False
            print("Unique weeks",
                  weekly_merged_level_sales[self._tarvarmapping['week']].nunique())
        return weekly_merged_level_sales, weekly_overal_level_sales, weekly_cbu_level_sales,consideryearweeks, \
                "Valid Sales calculated Successfully!!", True

    def get_sales_calculate_rsv(self, stores, target_variable, \
            applicability_criteria, consideryearweeks) -> Tuple[pd.DataFrame, list]:
        '''
            get sales calculate rsv calls the cbu sales/overall sales and
            calculate the total sales in the selected time period and population stores.
            Set 'is_product_present' in config to 0 in case region doesnt have product attributes.

            Parameters:
            -----------
            stores: list of store identifier values for which sales need to be calculated
            applicability_criteria: key-value pairs of the filters (product and store)
                    selection made in the tool
            consideryearweeks: to calculate sales in that period

            Returns:
            --------
            product and overall sales value merged at store
            week level,
            message,
            success flag
        '''
        if target_variable is not None:
            applicability_criteria['week_value'] = tuple(consideryearweeks)

            stores.append(-1)
            start_time = datetime.now()
            if self._config["feature_parameter"]["is_product_present"] == 1:
                weekly_overal_level_sales = self.get_cbu_sales(
                            stores=stores,
                            applicability_criteria=applicability_criteria,
                            weeks=consideryearweeks)
            else:
                weekly_overal_level_sales = self.get_overall_sales(
                            stores=stores,
                            applicability_criteria=applicability_criteria,
                            weeks=consideryearweeks)
            print("Time taken (get_sales_calculate_rsv) sales: {} seconds".format(
                (datetime.now()-start_time).total_seconds()))

            return weekly_overal_level_sales, consideryearweeks

        return pd.DataFrame(), []

    def _lift_calculation_util(self, weekly_sales, first_half_weeks,
                        second_half_weeks, target_variable) -> Tuple[pd.DataFrame, str, bool]:
        """
            About function
            --------------
            utility function that calculates the lift(growth in cbu and overall sales) for stores

            Parameters
            ----------
            weekly_sales: dataframe that has weekly store sales
            first_half_weeks: list of week values present in first half of time frame
            second_half_weeks: list of week values present in second half of time frame
            target_variable: key-value pairs of the filters (product and store)
                selection made in the tool
            Return values
            -------
            dataframe with lift CBU and overall lift values, message and success flag
        """
        weekly_rsv_year1 = weekly_sales[weekly_sales[self._tarvarmapping["week"]]\
                                                        .isin(first_half_weeks)]
        weekly_rsv_year2 = weekly_sales[weekly_sales[self._tarvarmapping["week"]]\
                                                        .isin(second_half_weeks)]
        weekly_rsv_year1[self._tarvarmapping["year"]] = "Year1"
        weekly_rsv_year2[self._tarvarmapping["year"]] = "Year2"

        aggdict = {k: sum for k in [self._tarvarmapping["rsv"],
                                     self._tarvarmapping["volume"]]}
        groupbycolumns = [self._tarvarmapping["partner_id"],
                        self._tarvarmapping["banner"],
                        self._tarvarmapping["year"]]
        rsv_lbl =self._tarvarmapping["rsv"]
        vol_lbl = self._tarvarmapping["volume"]
        if self._config['feature_parameter']["is_product_present"] == 1:
            aggdict.update({k: sum for k in [
                           "CBU_Category_"+rsv_lbl,
                           "CBU_Category_"+vol_lbl]})

        annualrsvdatayear1 = weekly_rsv_year1\
                                .groupby(groupbycolumns)\
                                .agg(aggdict)\
                                .reset_index()
        annualrsvdatayear2 = weekly_rsv_year2\
                                .groupby(groupbycolumns)\
                                .agg(aggdict)\
                                .reset_index()

        annualrsvdatayear1[rsv_lbl] = annualrsvdatayear1[rsv_lbl]\
                                        .round(2)
        annualrsvdatayear2[rsv_lbl] = annualrsvdatayear2[rsv_lbl]\
                                        .round(2)

        annualrsvdatayear1[vol_lbl] = annualrsvdatayear1[vol_lbl]\
                                    .round(2)
        annualrsvdatayear2[vol_lbl] = annualrsvdatayear2[vol_lbl]\
                                    .round(2)

        annualrsvdatayear1colsdict = {rsv_lbl: rsv_lbl +' Year 1',
                                      vol_lbl: vol_lbl + ' Year 1'}
        annualrsvdatayear2colsdict = {rsv_lbl: rsv_lbl +' Year 2',
                                      vol_lbl: vol_lbl+' Year 2'}
        if self._config['feature_parameter']["is_product_present"] == 1:
            cbu_rsv_lbl = "CBU_Category_"+self._tarvarmapping["rsv"]
            cbu_vol_lbl = "CBU_Category_"+self._tarvarmapping["volume"]
            annualrsvdatayear1[cbu_rsv_lbl] = annualrsvdatayear1[cbu_rsv_lbl].round(2)
            annualrsvdatayear2[cbu_rsv_lbl] = annualrsvdatayear2[cbu_rsv_lbl].round(2)

            annualrsvdatayear1[cbu_vol_lbl] = annualrsvdatayear1[cbu_vol_lbl].round(2)
            annualrsvdatayear2[cbu_vol_lbl] = annualrsvdatayear2[cbu_vol_lbl].round(2)
            annualrsvdatayear1colsdict.update({cbu_rsv_lbl: cbu_rsv_lbl + ' Year 1',
                                               cbu_vol_lbl: cbu_vol_lbl + " Year 1"})
            annualrsvdatayear2colsdict.update({cbu_rsv_lbl: cbu_rsv_lbl+' Year 2',
                                               cbu_vol_lbl: cbu_vol_lbl+" Year 2"})

        annualrsvdatayear1.rename(
            columns=annualrsvdatayear1colsdict, inplace=True)
        annualrsvdatayear2.rename(
            columns=annualrsvdatayear2colsdict, inplace=True)

        mergecols = [self._tarvarmapping["partner_id"],
                    self._tarvarmapping["banner"]]

        annualrsvdatamerged = annualrsvdatayear1.merge(
                                                        annualrsvdatayear2,
                                                        on=mergecols)
        annualrsvdatamerged.drop(labels=[self._tarvarmapping["year"]+"_x",
                                         self._tarvarmapping["year"]+"_y"],
                                 axis=1,
                                 inplace=True)

        salesfilter = ((annualrsvdatamerged[target_variable+" Year 1"] > 0)
                       & (annualrsvdatamerged[target_variable+" Year 2"] > 0))
        annualrsvdatamerged = annualrsvdatamerged[salesfilter]
        trg_var_yr1_lbl =target_variable+" Year 1"
        trg_var_yr2_lbl =target_variable+" Year 2"
        trg_lift_lbl = target_variable+" Lift"
        annualrsvdatamerged[trg_lift_lbl] = (annualrsvdatamerged[trg_var_yr2_lbl] -
                                                annualrsvdatamerged[trg_var_yr1_lbl])\
                                                    /annualrsvdatamerged[trg_var_yr1_lbl]

        annualrsvdatamerged[target_variable +
                            " Lift"] = annualrsvdatamerged[target_variable+" Lift"].round(2)
        if self._config['feature_parameter']["is_product_present"] == 1:
            cbu_year2_sales_lbl = "CBU_Category_"+target_variable+" Year 2"
            cbu_year1_sales_lbl = "CBU_Category_"+target_variable+" Year 1"
            cbu_lift_lbl = "CBU_Category_"+target_variable+" Lift"
            annualrsvdatamerged[cbu_lift_lbl] = (annualrsvdatamerged[cbu_year2_sales_lbl] -
                                                    annualrsvdatamerged[cbu_year1_sales_lbl])\
                                                        /annualrsvdatamerged[cbu_year1_sales_lbl]

            annualrsvdatamerged[cbu_lift_lbl] = \
                        annualrsvdatamerged[cbu_lift_lbl].round(2)
        return annualrsvdatamerged, "Successfully calculated lift values", True

    def get_annual_rsv_lifts(self, target_variable, test_master_df, stores, \
        applicability_criteria, test_type)\
             -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        """
            About function
            --------------
            get annual rsv lifts calculate the lift of the stores passed
            calls the get_valid_weekly_target_data and divides the sales of stores into two
            time periods (division of weeks done based on the value of 'sales_lifts_sales_weeks')

            Parameters
            ----------
            target_variable: weekly sales column which is needs to be estimates (sales or volume),
            prewindow_start: date from which preperiod starts,
            prewindow_end: date on which preperiod ends,
            postwindow_start:date from which postperiod starts,
            postwindow_end: date on which postperiod ends,
            stores: list of stores for which lift is calculated,
            applicability_criteria: the product and stores attributes selected at tool in
                    dictionary format,
            test_type: type of test from the tool selection (Activity, RTM impact, others...),

            example
            -------

            if want to calculate yearly lift then sales_week = 104 (52*2 number of weeks);
             sales_lifts_sales_weeks = 52 (number of weeks in a year)

            Return values
            -------
            dataframe with lift CBU and overall lift values, list of weeks on which
                sales is calculated,message and success flag
        """

        # Getting the the target varaibles file
        sales_week = self.get_sales_weeks(applicability_criteria)
        sales_lifts_sales_weeks = self.get_lift_sales_weeks(applicability_criteria)

        weekly_ovrl_cbu_sales,weekly_overall_sales, weekly_cbu_sales, consideryearweeks,\
             message, success_flag = self.get_valid_weekly_target_data(
                                        stores=stores,
                                        applicability_criteria=applicability_criteria,
                                        target_variable=target_variable,
                                        test_master_df = test_master_df,
                                        test_type=test_type,
                                        sales_week=sales_week)

        weeks1 = consideryearweeks[:sales_lifts_sales_weeks]
        weeks2 = consideryearweeks[sales_lifts_sales_weeks:]


        if success_flag is False:
            return pd.DataFrame(), weekly_ovrl_cbu_sales, consideryearweeks, message, success_flag


        annualrsvdatamerged, _, success_flag = self\
                        ._lift_calculation_util(weekly_sales=weekly_ovrl_cbu_sales,
                                                first_half_weeks=weeks1,
                                                second_half_weeks=weeks2,
                                                target_variable=target_variable)
        return annualrsvdatamerged, weekly_ovrl_cbu_sales, weekly_overall_sales, weekly_cbu_sales, consideryearweeks,\
                 "Annual Lift calculated Successfully!", True

    def get_total_weekly_target_data(self, test_master_df, stores_list,sales_week, target_variable,
                                    applicability_criteria,test_type,
                                    consideryearweeks = None)\
                                         -> Tuple[pd.DataFrame, list, str, bool]:


        """
            About function
            --------------
            This function gets the overall sales in the "sales week" time
                period or weeks to be considered

            Parameters
            ----------
            prewindow_end: date on which preperiod ends,
            stores_list: list of stores for which lift is calculated,
            applicability_criteria: the product and stores attributes
                    selected at tool in dictionary format,
            test_type: type of test from the tool selection
                (Activity, RTM impact, others...),
            sales_week: optional parameter is the number of weeks for which the sales
                 to be calculated and validated,
            consideryearweeks: optional parameter a list of weeks, if want to skip the
                 calculation of weeks
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
        print(test_type, target_variable)
        if consideryearweeks is None:
            consideryearweeks = []
        if not consideryearweeks:
            yearweeks = self.find_last104_weeks_from_baseline_end(
            datetime.strptime(test_master_df['pre_end'].values[0], '%Y-%m-%d').date())
            yearweeks.sort(reverse=True)
            consideryearweeks = yearweeks[:sales_week]
            consideryearweeks.sort(reverse=False)
        stores_list.append(-1)

        weekly_overal_level_sales = self.get_overall_sales(
            stores=stores_list,
            applicability_criteria=applicability_criteria,
            weeks=consideryearweeks)
        if weekly_overal_level_sales.shape[0] == 0:
            return weekly_overal_level_sales, consideryearweeks, "No Sales found", False
        return weekly_overal_level_sales, consideryearweeks, "Sales calculated successfully!", True

    def get_weekly_targetvariables_data(self, target_variable, test_master_df,
                 stores, applicability_criteria) \
                    -> Tuple[pd.DataFrame, pd.DataFrame, list, list, str, bool]:
        """
            About function
            --------------
            This function fetches the sales in prewindow and postwindow selected
                and returns respective sales

            Parameters
            ----------
            stores: list of stores for which lift is calculated,
            applicability_criteria: the product and stores attributes
                    selected at tool in dictionary format,
            test_master_df: is a dataframe that have records of the current
                     test from test measurement table

            Return values
            -------
            overall sales values dataframe,
            list of weeks on which sales is calculated,
            message
            success flag
        """

        pre_window_weeknumbers = self.find_weeks(
                                    str_to_date(test_master_df["pre_start"].values[0]),
                                    str_to_date(test_master_df["pre_end"].values[0])
                                )
        pre_window_weeknumbers = list(map(int, pre_window_weeknumbers))

        post_window_weeknumbers = self.find_weeks(
                                str_to_date(test_master_df["testwin_start"].values[0]),
                                str_to_date(test_master_df["testwin_end"].values[0])
                                )
        post_window_weeknumbers = list(map(int, post_window_weeknumbers))

        weeks_req = post_window_weeknumbers[:]
        weeks_req.extend(pre_window_weeknumbers)

        if self._config['feature_parameter']["is_product_present"] == 1:
            weekly_target_data = self.get_cbu_sales(
                stores=stores[:],
                applicability_criteria=applicability_criteria,
                weeks=weeks_req)
        else:
            weekly_target_data = self.get_overall_sales(
                stores=stores[:],
                applicability_criteria=applicability_criteria,
                weeks=weeks_req)

        if target_variable not in weekly_target_data.columns.tolist():
            return pd.DataFrame(), pd.DataFrame(), [], []
        # Select for relevant CBU and weeks
        prewindow_filter = (
            (weekly_target_data[self._tarvarmapping["week"]].isin(pre_window_weeknumbers)))

        postwindow_filter = (
            (weekly_target_data[self._tarvarmapping["week"]].isin(post_window_weeknumbers)))

        prewindow_target_data = weekly_target_data[prewindow_filter][[
            self._tarvarmapping["partner_id"], self._tarvarmapping["banner"],
            self._tarvarmapping["week"], self._tarvarmapping['rsv'],
            self._tarvarmapping['volume']]]
        postwindow_target_data = weekly_target_data[postwindow_filter][[
            self._tarvarmapping["partner_id"], self._tarvarmapping["banner"],
            self._tarvarmapping["week"], self._tarvarmapping['rsv'],
            self._tarvarmapping['volume']]]

        return prewindow_target_data, postwindow_target_data, pre_window_weeknumbers, \
            post_window_weeknumbers,  "Sales Calculated successfully!!", True

    def get_pre_post_sales_test_measurement(self, target_variable, test_control_stores_with_time_period,
        applicability_criteria, stores_list, weeks_req=None, weeks_before=None, weeks_after = None)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:

        if weeks_req is None:
            weeks_req = []

        if weeks_before is None:
            weeks_before = 0
        if weeks_after is None:
            weeks_after = 0
        columns_req = ['pre_start', 'pre_end', 'testwin_start','testwin_end','Test_store_'+self._tarvarmapping['partner_id'], 'Test_store_'+self._tarvarmapping['banner'],
                                                                                self._tarvarmapping['partner_id'], self._tarvarmapping['banner']]
        if len(set(columns_req).intersection(set(test_control_stores_with_time_period.columns)))<len(columns_req):
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(), "Either of these columns not passed {}".format(columns_req), False

        stores_date_info = test_control_stores_with_time_period.to_dict(orient='records')

        for record in stores_date_info:
            pre_start = datetime.strptime(record['pre_start'], '%Y-%m-%d').date() \
                            -timedelta(weeks=weeks_before)
            pre_end = datetime.strptime(record['pre_end'], '%Y-%m-%d').date() \
                            -timedelta(weeks=weeks_before)
            testwin_start = datetime.strptime(record['testwin_start'], '%Y-%m-%d').date() \
                            +timedelta(weeks=weeks_after)
            testwin_end = datetime.strptime(record['testwin_end'], '%Y-%m-%d').date() \
                            +timedelta(weeks=weeks_after)

            pre_window_weeknumbers = self.find_weeks(pre_start,
                                                    pre_end)
            pre_window_weeknumbers = list(map(int, pre_window_weeknumbers))

            post_window_weeknumbers = self.find_weeks(testwin_start,
                                                    testwin_end)
            post_window_weeknumbers = list(map(int, post_window_weeknumbers))
            weeks_req.extend(pre_window_weeknumbers)
            weeks_req.extend(post_window_weeknumbers)
            record['pre_period_weeks_required'] = pre_window_weeknumbers
            record['post_period_weeks_required'] = post_window_weeknumbers

        weeks_req = list(set(weeks_req))
        stores_list = list(set(stores_list))
        if self._config["feature_parameter"]["is_product_present"] is 1:
            weekly_sales = self.get_cbu_sales(
                                            stores=stores_list[:],
                                            applicability_criteria=applicability_criteria,
                                            weeks=weeks_req[:])
        else:
            weekly_sales = self.get_overall_sales(
                                        stores=stores_list[:],
                                        applicability_criteria=applicability_criteria,
                                        weeks=weeks_req[:])
        if weekly_sales.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), list()
        req_pre_sales, req_post_sales = self._convert_sales_pre_post(weekly_sales = weekly_sales.drop(self._tarvarmapping['banner'], axis=1),
                                                                    stores_date_info_dict_list = stores_date_info,
                                                                    target_variable = target_variable,
                                                                    test_control_map_table = test_control_stores_with_time_period)
        req_post_sales = req_post_sales.merge(test_control_stores_with_time_period[['Test_store_'+self._tarvarmapping['partner_id'], 'Test_store_'+self._tarvarmapping['banner'],
                                                                                self._tarvarmapping['partner_id'], self._tarvarmapping['banner']]],
                                                                                on=['Test_store_'+self._tarvarmapping['partner_id'],self._tarvarmapping['partner_id']])
        req_pre_sales = req_pre_sales.merge(test_control_stores_with_time_period[['Test_store_'+self._tarvarmapping['partner_id'], 'Test_store_'+self._tarvarmapping['banner'],
                                                                                self._tarvarmapping['partner_id'], self._tarvarmapping['banner']]],
                                                                                on=['Test_store_'+self._tarvarmapping['partner_id'],self._tarvarmapping['partner_id']])

        return req_pre_sales, req_post_sales, weekly_sales, stores_date_info, "sales computed successfully!!", True

