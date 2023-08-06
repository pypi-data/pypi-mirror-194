"""
This module handles the flow of tool for test measurement features.
Classes:
--------
    FastToolMeasurement
"""
import pandas as pd
from typing import Tuple
from datetime import datetime
from DSCode.library.ds.feature.test_measurement_cal.test_measurement_master import TestMeasurement
class FastToolMeasurement:
    def __init__(self, fast_tool_plan, config, region, test_id):
        """
        Constructs all the necessary attributes for the tool flow.

        Parameters
        ----------
            config : configuration present in config_data either for a region or overall
            region: key present in config
            test_id: current test test_id

        Initializes:
            fast_tool_plan: fast tool planning object
            config: config of the region
            metadata: metadata part of the config
            self._tarvarmapping: weekly sales column mapping
            self._storemstrmapping: store column mapping
            test_id: current test test_id
            test_msrmt_features: object of test measurement features
        """
        self._fast_tool_plan = fast_tool_plan
        self._config = config[region] if region in config else config
        self._metadata = self._config["metadata"]['test_measurement']
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]
        self._test_id = test_id
        self._test_msrmt_features = TestMeasurement(config=self._config, region=region)

    def validate_test_id_records(self)->Tuple[pd.DataFrame, pd.DataFrame,
                                             pd.DataFrame, pd.DataFrame, str, bool]:
        """
        About
        -----

        This function checks the following tables and return the records of the current test.
        If no record is found for the test in any of the table it will return error.
        Tables are checked:
        1) Test measurement table
        2) Test control master table
        3) test store map table
        4) test master table

        Return
        ------

        1) DataFrame of Test Master table,
        2) DataFrame of Test measurement table,
        3) DataFrame of test store map table,
        4) DataFrame of Test control stores master table,
        5) Message
        6) Boolean value True(success)/False(Failure)
        """
        test_measurement_table = self._fast_tool_plan._store_object\
            .read_test_measurement_table_by_test_ids(test_id=self._test_id)
        test_measurement_table = test_measurement_table[test_measurement_table['test_id_id'] == self._test_id]
        if test_measurement_table.shape[0] is 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "No records found in test measurement table for this test_id", False
        test_control_table = self._fast_tool_plan._store_object\
                                .read_control_store_by_test_ids(self._test_id)
        test_control_table = test_control_table[test_control_table['test_id_id'] == self._test_id]
        if test_control_table.shape[0] is 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "No records found in control store master table for this test_id", False

        test_map_table = self._fast_tool_plan._store_object\
                            .read_test_map_table_by_test_ids(self._test_id)
        test_map_table = test_map_table[test_map_table['test_id_id'] == self._test_id]
        if test_map_table.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "No record found in test store map table for this test_id", False
        test_master_table = self._fast_tool_plan._store_object\
                            .read_test_master_table_by_test_ids(self._test_id)
        test_master_table = test_master_table[test_master_table['test_id'] == self._test_id]
        if test_master_table.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "No record found in test master table for this test_id", False
        return test_master_table, test_measurement_table, test_map_table, test_control_table, "Validated successfully!", True

    def get_pre_post_sales(self, target_variable,test_master_table,test_map_table,test_control_table,
                applicability_criteria,stores_list, weeks_before=None, weeks_after=None)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        test_control_table = test_control_table.merge(test_map_table.rename(columns={'teststore_id':'Test_store_'+self._tarvarmapping['partner_id']}),
                                                                            on = ['test_id_id', 'Test_store_'+self._tarvarmapping['partner_id']])
        if (self._config["feature_parameter"]["test_variable_dates"] is 0) & ('pre_start' not in test_control_table.columns):
            test_control_table = test_master_table[['test_id', 'pre_start', 'pre_end', 'testwin_start','testwin_end']]\
                                                                            .merge(test_control_table,
                                                                                left_on='test_id',
                                                                                right_on='test_id_id')
        return self._fast_tool_plan\
                    ._sales_object\
                    .get_pre_post_sales_test_measurement(target_variable = target_variable,
                        test_control_stores_with_time_period = test_control_table,
                        applicability_criteria = applicability_criteria,
                        stores_list =stores_list[:],
                        weeks_req=[],
                        weeks_before = weeks_before,
                        weeks_after = weeks_after)

    def get_pre_post_annual_target_sales(self, target_variable,test_master_table,test_map_table,test_control_table,
                applicability_criteria,population_stores)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        stores = list(test_control_table["Test_store_" + self._tarvarmapping["partner_id"]].unique())
        stores.extend(list(test_control_table[self._storemstrmapping["partner_id"]].unique()))

        test_control_table = test_control_table.merge(test_map_table.rename(columns={'teststore_id':'Test_store_'+self._tarvarmapping['partner_id']}),
                                                                                                on = ['test_id_id', 'Test_store_'+self._tarvarmapping['partner_id']])
        if (self._config["feature_parameter"]["test_variable_dates"] is 0) & ('pre_start' not in test_control_table.columns):
            test_control_table = test_master_table[['test_id', 'pre_start', 'pre_end', 'testwin_start','testwin_end']]\
                                                                            .merge(test_control_table,
                                                                                left_on='test_id',
                                                                                right_on='test_id_id')

        rsv_time_start = test_master_table['timeframestart'].astype(str).values[0]
        rsv_time_end = test_master_table['timeframend'].astype(str).values[0]

        rsv_window_weeknumbers = self._fast_tool_plan._sales_object.find_weeks(datetime.strptime(rsv_time_start, '%Y-%m-%d').date(),
                                            datetime.strptime(rsv_time_end, '%Y-%m-%d').date())
        rsv_window_weeknumbers = list(map(int, rsv_window_weeknumbers))

        req_pre_sales, req_post_sales, weekly_sales,\
             stores_date_info, message, success_flag = self._fast_tool_plan\
                                                        ._sales_object\
                                                        .get_pre_post_sales_test_measurement(target_variable,
                                                            test_control_stores_with_time_period = test_control_table,
                                                            applicability_criteria = applicability_criteria,
                                                            stores_list =population_stores[:],
                                                            weeks_req=rsv_window_weeknumbers[:])
        if success_flag is False:
            return req_pre_sales, req_post_sales, pd.DataFrame(), pd.DataFrame(), list(), message, False
        rsvwindow_filter = (
                            (weekly_sales[self._tarvarmapping["week"]].isin(rsv_window_weeknumbers))\
                            &(weekly_sales[self._tarvarmapping["partner_id"]].isin(population_stores)))

        rsvwindow_target_data = weekly_sales[rsvwindow_filter][[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"],
                                                                      self._tarvarmapping["week"], target_variable]]
        rsvwindow_target_data = rsvwindow_target_data.drop_duplicates()

        return req_pre_sales, req_post_sales, rsvwindow_target_data, weekly_sales, stores_date_info, "sales computed successfully!!", True

    def _handle_outlier(self, test_control_stores_actual, test_control_stores_filtered, stores_list_tobe_included):
        computation_level = "Teststore "+self._config["feature_parameter"]['outlier_column']

        if len(stores_list_tobe_included) == 0:  # Base Case when user has not confirmed Outliers.
            test_control_stores_actual.sort_values(by= computation_level, inplace=True)
            test_control_stores_actual['Z-score'] = test_control_stores_actual[[computation_level,"Test vs Control change(in %)"]].\
                        groupby(computation_level).transform(lambda x : abs((x - x.mean())/x.std()))


            test_control_stores_actual = test_control_stores_actual[(test_control_stores_actual["Z-score"]<3)]
        else:
            test_control_stores_actual = test_control_stores_actual[(test_control_stores_actual["Test_store_"+self._tarvarmapping["partner_id"]].isin(stores_list_tobe_included))]

        if len(stores_list_tobe_included) == 0:  # Base Case when user has not confirmed Outliers.
            # Computing Outliers Teststores by CustomerChain(UK Only) based on Lift (Z-score)
            test_control_stores_filtered.sort_values(by= computation_level, inplace=True)
            test_control_stores_filtered['Z-score'] = test_control_stores_filtered[[computation_level,"Test vs Control change(in %)"]].\
                    groupby(computation_level).transform(lambda x : abs((x - x.mean())/x.std()))
            test_control_stores_filtered = test_control_stores_filtered[test_control_stores_filtered["Z-score"]<3]
        else:
            test_control_stores_filtered = test_control_stores_filtered[test_control_stores_filtered[
                "Test_store_"+self._tarvarmapping["partner_id"]].isin(stores_list_tobe_included)]
        return test_control_stores_actual, test_control_stores_filtered

    def get_test_vs_control_linegraph(self, teststores, target_variable,test_type,applicability_criteria,
            weeks_after = None, weeks_before = None,control_stores_sales_method='Approach1',
            business_categories=None)->Tuple[dict, str, bool]:

        if weeks_after is None:
            weeks_after = 0
        if weeks_before is None:
            weeks_before = 0
        if (len(teststores) != 0) & (target_variable is not None):
            test_master_table, _, test_map_table, test_control_table, message, success_flag = self.validate_test_id_records()
            if success_flag is False:
                return dict(), message, success_flag
            one_to_one = self._test_msrmt_features.detect_one_to_one_mapping(test_control_table)
            test_control_stores = test_control_table[test_control_table[
                        "Test_store_"+self._storemstrmapping["partner_id"]].isin(teststores)].reset_index(drop=True)

            if test_control_stores.shape[0] == 0:
                return dict(), "Please check the test stores list passed! no common test stores found from the database table", False

            test_control_stores = test_control_stores[test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]]\
                                                    .isin(test_map_table["teststore_id"].values.tolist())].reset_index(drop=True)
            if test_control_stores.shape[0] == 0:
                return dict(), "There is data inconsistency issue, test stores in control store map is not same as in test map table", False

            stores = list(test_control_table["Test_store_" + self._tarvarmapping["partner_id"]].unique())
            stores.extend(list(test_control_table[self._storemstrmapping["partner_id"]].unique()))
            req_pre_sales, req_post_sales, _,\
             _, message, success_flag = self.get_pre_post_sales(target_variable=target_variable,
                                                                            test_master_table=test_master_table,
                                                                            test_map_table=test_map_table,
                                                                            test_control_table=test_control_table,
                                                                            applicability_criteria=applicability_criteria,
                                                                            stores_list=stores,
                                                                            weeks_before = weeks_before,
                                                                            weeks_after = weeks_after)
            if success_flag is False:
                return dict(), message, success_flag
            if req_pre_sales.shape[0] == 0:
                return dict(), "Prewindow sales of the test control pair is not found", False

            if req_post_sales.shape[0] == 0:
                return dict(), "Postwindow sales of the test control pair is not found", False

            timeseries_dict =self._test_msrmt_features.get_test_vs_control_linegraph_util( req_pre_sales_information_df = req_pre_sales,
                                    req_post_sales_information_df = req_post_sales,
                                    control_stores_sales_method = control_stores_sales_method,
                                    one_to_one = one_to_one, test_control_stores=test_control_stores)
            return timeseries_dict, "Graph values calculated successfully", True
        else:
            return dict(), "Please check input parameters, either test stores list is not passed or target variable is None", False

    def _get_break_even_lift(self, population_store_weekly_sales, target_variable, test_master_table):
        if ("rawconvfactors" in self._config["metadata"]["test_configuration"]) and (len(self._config["metadata"]["test_configuration"]['rawconvfactors']) > 0):
            banner_label = self._tarvarmapping["banner"]
            partner_label = self._tarvarmapping["partner_id"]
            count_df = population_store_weekly_sales\
                        .groupby(banner_label)[partner_label]\
                        .count()\
                        .reset_index()\
                        .rename(columns={partner_label: "Count"})
            count_df["prop"] = count_df["Count"]/count_df["Count"].sum()
            count_df["stores_proportioned"] = count_df["prop"] * population_store_weekly_sales[self._tarvarmapping['partner_id']]\
                                                                        .nunique()
            count_df["stores_proportioned"] = count_df["stores_proportioned"].round(2)

            bannerwisestoresdict = dict(zip(count_df[banner_label],
                                            count_df["stores_proportioned"]))

            rawconvfactors = self._metadata["rawconvfactors"]
            numerator = sum([bannerwisestoresdict[k]*v for k,
                            v in rawconvfactors.items() if k in bannerwisestoresdict.keys()])
            denominator = sum(list(bannerwisestoresdict.values()))
            conversionfactor = numerator / denominator
            cost = cost/conversionfactor
            break_even_lift = (cost/population_store_weekly_sales[target_variable].sum())*100
        else:
            break_even_lift = float(test_master_table['break_even_lift'].values[0])
            conversionfactor = 1
        return conversionfactor, break_even_lift

    def _get_cost(self, test_master_table, population_store_weekly_sales=None, target_variable=None):
        return float(test_master_table['cost'].values[0])

    def _generate_KPI_values(self, target_variable_analysis_dict_actual, rsvwindow_target_data, target_variable,
        test_master_table, conversionfactor, cost)->dict:

        return self._test_msrmt_features._generate_KPI_values(
                        target_variable_analysis_dict_actual=target_variable_analysis_dict_actual,
                        rsvwindow_target_data=rsvwindow_target_data,
                        target_variable=target_variable,
                        test_master_table=test_master_table,
                        conversionfactor=conversionfactor,
                        cost = cost)

    def get_target_variable_analysis_results(self, teststores, target_variable, test_type, applicability_criteria,control_stores_sales_method='Approach1',
         outlier_column=None, business_categories=None, uploaded_file_df=None) -> Tuple[float, str, pd.DataFrame, pd.DataFrame, dict, dict, str, bool]:

        '''
        get_target_variable_analysis_results
        '''
        target_variable_analysis_dict_filtered = {}
        target_variable_analysis_dict_actual = {}

        test_master_table, test_measurement_table, test_map_table, test_control_table, message, success_flag = self.validate_test_id_records()
        if success_flag is False:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), message, success_flag
        requiredcols = self._metadata["testmeasurement_columns"]
        teststores_columns_rename_dict = {val: "Teststore "+val for val in requiredcols if val not in [
            self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]]}
        controlstores_columns_rename_dict = {val: "Controlstore "+val for val in requiredcols if val not in [
            self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]]}

        if ('outlier_detection' not in self._config['feature_parameter']) \
                    or (self._config['feature_parameter']['outlier_detection'] is 0):
            stores_list_tobe_included = []
        else:
            if (outlier_column is None) or (outlier_column == ""):
                return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(),\
                        dict(), "For outlier feature to work please pass the outlier column", False
            stores_list_tobe_included = test_map_table[test_map_table[outlier_column].astype(int)==0]\
                                                        ['teststore_id'].tolist()

        one_to_one = self._test_msrmt_features\
                                .detect_one_to_one_mapping(test_control_pairs=test_control_table)
        target_variable_actual = test_master_table['target_var'].values[0]

        stores_master_df = self._fast_tool_plan\
                                ._store_object\
                                .filter_population(applicability_criteria = applicability_criteria,
                                                    uploaded_file_df = uploaded_file_df)


        req_pre_sales_information_df, req_post_sales_information_df, rsvwindow_target_data,\
             _, _, message, success_flag = self.get_pre_post_annual_target_sales(
                                                    target_variable = target_variable,
                                                    test_master_table = test_master_table,
                                                    test_map_table = test_map_table,
                                                    test_control_table = test_control_table,
                                                    applicability_criteria = applicability_criteria,
                                                    population_stores = list(stores_master_df[self._storemstrmapping['partner_id']].unique()))
        if success_flag is False:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), message, success_flag

        if req_pre_sales_information_df.shape[0] == 0:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), \
                                    dict(), "Pre period sales for test control pair not found", False

        if req_post_sales_information_df.shape[0] == 0:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), \
                                    dict(), "Post period sales for test control pair not found", False

        test_control_stores = test_control_table.copy()
        test_control_stores = test_control_stores[test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]]\
                                                                        .isin(test_map_table["teststore_id"].values.tolist())]
        if len(test_control_stores) == 0:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), "Test stores in test store map and control store master doesnt match", False

        transformed_pre_sales = req_pre_sales_information_df\
            .groupby(['Test_store_'+self._storemstrmapping["partner_id"], 'Test_store_'+self._storemstrmapping["banner"],
                        self._storemstrmapping["partner_id"], self._storemstrmapping["banner"], 'Pre_period_weeks'])\
            .aggregate({"Test group - Pre Period Average":'sum', "Control group - Pre Period Average":'sum'})\
            .reset_index()
        transformed_pre_sales["Test group - Pre Period Average"] = round(transformed_pre_sales["Test group - Pre Period Average"]\
                                                                            /transformed_pre_sales['Pre_period_weeks'], 2)
        transformed_pre_sales["Control group - Pre Period Average"] = round(transformed_pre_sales["Control group - Pre Period Average"]\
                                                                            /transformed_pre_sales['Pre_period_weeks'], 2)

        transformed_post_sales = req_post_sales_information_df\
            .groupby(['Test_store_'+self._storemstrmapping["partner_id"], 'Test_store_'+self._tarvarmapping["banner"],
                        self._tarvarmapping["partner_id"], self._tarvarmapping["banner"], 'Post_period_weeks'])\
            .aggregate({"Test group - Post Period Average":'sum', "Control group - Post Period Average":'sum'})\
            .reset_index()
        transformed_post_sales["Test group - Post Period Average"] = round(transformed_post_sales["Test group - Post Period Average"]\
                                                                            /transformed_post_sales['Post_period_weeks'], 2)
        transformed_post_sales["Control group - Post Period Average"] = round(transformed_post_sales["Control group - Post Period Average"]\
                                                                            /transformed_post_sales['Post_period_weeks'], 2)

        test_control_stores_actual = test_control_stores.copy(deep=True)
        if len(teststores) > 0:
            test_control_stores_filtered = test_control_stores[test_control_stores[
                "Test_store_"+self._storemstrmapping["partner_id"]].isin(teststores)]
        else:
            test_control_stores_filtered = test_control_stores.copy(deep=True)
        # Storelevel lift results

        test_control_stores_actual = self._test_msrmt_features.get_storelevel_liftresults(
                                                                    one_to_one = one_to_one,
                                                                    test_control_stores = test_control_stores_actual,
                                                                    prewindow_target_data_grouped = transformed_pre_sales,
                                                                    postwindow_target_data_grouped = transformed_post_sales,
                                                                    target_variable = target_variable_actual,
                                                                    control_stores_sales_method = control_stores_sales_method,
                                                                    test_type=test_type)
        test_control_stores_filtered = self._test_msrmt_features.get_storelevel_liftresults(
                                                                    one_to_one = one_to_one,
                                                                    test_control_stores = test_control_stores_filtered,
                                                                    prewindow_target_data_grouped = transformed_pre_sales,
                                                                    postwindow_target_data_grouped = transformed_post_sales,
                                                                    target_variable = target_variable,
                                                                    control_stores_sales_method = control_stores_sales_method,
                                                                    test_type=test_type)

        "Handling NaNs in the data in actual store info"
        numeric_columns = test_control_stores_actual.select_dtypes(include=['number']).columns
        "fill 0 to all NaN in actual store info"
        test_control_stores_actual[numeric_columns] = test_control_stores_actual[numeric_columns].fillna(0)
        object_columns = list(set(test_control_stores_actual.columns) - set(numeric_columns))
        'fill "" to all NaN object columns in actual store info'
        test_control_stores_actual[object_columns] = test_control_stores_actual[object_columns].fillna("NOT-AVAILABLE")
        "Handling NaNs in the data in filtered store info"
        numeric_columns = test_control_stores_filtered.select_dtypes(include=['number']).columns
        "fill 0 to all NaN in filtered store info"
        test_control_stores_filtered[numeric_columns] = test_control_stores_filtered[numeric_columns].fillna(0)
        object_columns = list(set(test_control_stores_filtered.columns) - set(numeric_columns))
        'fill "" to all NaN object columns in filtered store info'
        test_control_stores_filtered[object_columns] = test_control_stores_filtered[object_columns].fillna("NOT-AVAILABLE")

        test_control_stores_actual = self._test_msrmt_features.prepare_test_measurement_columns(
                                                                    test_control_stores=test_control_stores_actual,
                                                                    stores_master_df=stores_master_df,
                                                                    test_type=test_type,
                                                                    requiredcols=requiredcols,
                                                                    teststores_columns_rename_dict=teststores_columns_rename_dict,
                                                                    controlstores_columns_rename_dict=controlstores_columns_rename_dict,
                                                                    one_to_one = one_to_one)

        test_control_stores_filtered = self._test_msrmt_features.prepare_test_measurement_columns(
                                                                    test_control_stores=test_control_stores_filtered,
                                                                    stores_master_df=stores_master_df,
                                                                    test_type=test_type,
                                                                    requiredcols=requiredcols,
                                                                    teststores_columns_rename_dict=teststores_columns_rename_dict,
                                                                    controlstores_columns_rename_dict=controlstores_columns_rename_dict,
                                                                    one_to_one = one_to_one)


        if ('outlier_detection' in self._config['feature_parameter'])and (self._config['feature_parameter']['outlier_detection'] is 1):
            test_control_stores_actual, test_control_stores_filtered = self._handle_outlier(
                                                                test_control_stores_actual = test_control_stores_actual,
                                                                test_control_stores_filtered = test_control_stores_filtered,
                                                                stores_list_tobe_included = stores_list_tobe_included)

        test_control_stores_req = test_control_stores_actual.copy(deep=True)
        test_control_stores_filtered_req = test_control_stores_filtered.copy(deep=True)

        control_pre_mean_actual = round(test_control_stores_req["Control group - Pre Period Average"].mean(), 2)
        control_post_mean_actual = round(test_control_stores_req["Control group - Post Period Average"].mean(), 2)
        control_change_percentage_actual = round(test_control_stores_req["Control group - Pre vs Post change(in %)"].mean(), 2)
        test_pre_mean_actual = round(test_control_stores_req["Test group - Pre Period Average"].mean(), 2)
        test_post_mean_actual = round(test_control_stores_req["Test group - Post Period Average"].mean(), 2)
        test_change_percentage_actual = round(test_control_stores_req["Test group - Pre vs Post change(in %)"].mean(), 2)
        test_vs_control_change_actual = round(test_control_stores_req["Test vs Control change(in %)"].mean(), 2)
        control_pre_mean_filtered = round(test_control_stores_filtered_req["Control group - Pre Period Average"].mean(), 2)
        control_post_mean_filtered = round(test_control_stores_filtered_req["Control group - Post Period Average"].mean(), 2)
        control_change_percentage_filtered = round(test_control_stores_filtered_req["Control group - Pre vs Post change(in %)"].mean(), 2)
        test_pre_mean_filtered = round(test_control_stores_filtered_req["Test group - Pre Period Average"].mean(), 2)
        test_post_mean_filtered = round(test_control_stores_filtered_req["Test group - Post Period Average"].mean(), 2)
        test_change_percentage_filtered = round(test_control_stores_filtered_req["Test group - Pre vs Post change(in %)"].mean(), 2)


        mean_changepercent = test_control_stores_req["Test vs Control change(in %)"].mean()
        conversionfactor, break_even_lift = self._get_break_even_lift(population_store_weekly_sales = rsvwindow_target_data,
                                                                     target_variable = target_variable,
                                                                     test_master_table = test_master_table)
        # Pvalue calculation
        probability, decision, pVal, message, success_flag = self._test_msrmt_features\
                                        .calculate_probability_decision(one_to_one = one_to_one,
                                            test_control_stores = test_control_stores_req,
                                            break_even_lift = break_even_lift,
                                            mean_changepercent= mean_changepercent)

        if success_flag is False:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), message, success_flag
        # Putting the calculated values in the dictionary
        target_variable_analysis_dict_actual["control_pre_mean"] = control_pre_mean_actual
        target_variable_analysis_dict_actual["control_post_mean"] = control_post_mean_actual
        target_variable_analysis_dict_actual["control_change_percentage"] = control_change_percentage_actual
        target_variable_analysis_dict_actual["test_pre_mean"] = test_pre_mean_actual
        target_variable_analysis_dict_actual["test_post_mean"] = test_post_mean_actual
        target_variable_analysis_dict_actual["test_change_percentage"] = test_change_percentage_actual
        target_variable_analysis_dict_actual["test_vs_control_change"] = test_vs_control_change_actual
        target_variable_analysis_dict_actual["PValue"] = round(pVal, 2)

        # Putting the calculated values in the dictionary
        target_variable_analysis_dict_filtered["control_pre_mean"] = control_pre_mean_filtered
        target_variable_analysis_dict_filtered["control_post_mean"] = control_post_mean_filtered
        target_variable_analysis_dict_filtered["control_change_percentage"] = control_change_percentage_filtered
        target_variable_analysis_dict_filtered["test_pre_mean"] = test_pre_mean_filtered
        target_variable_analysis_dict_filtered["test_post_mean"] = test_post_mean_filtered
        target_variable_analysis_dict_filtered["test_change_percentage"] = test_change_percentage_filtered
        target_variable_analysis_dict_filtered["test_vs_control"] = sorted(
            test_control_stores_filtered["Test vs Control change(in %)"].values.tolist(), reverse=True)

        # Dollar sales and lift
        cost = self._get_cost(test_master_table=test_master_table,
                                population_store_weekly_sales=rsvwindow_target_data,
                                target_variable=target_variable)

        target_variable_actual = self._generate_KPI_values(
                        target_variable_analysis_dict_actual=target_variable_analysis_dict_actual,
                        rsvwindow_target_data=rsvwindow_target_data,
                        target_variable=target_variable,
                        test_master_table=test_master_table,
                        conversionfactor=conversionfactor,
                        cost=cost)


        test_control_stores_filtered_req["Test vs (Control-Average)"] = round(test_control_stores_filtered_req[
            "Test group - Pre vs Post change(in %)"] - control_change_percentage_filtered, 2)

        #target_variable_analysis_dict_filtered["Test_store_Partner_ID_backup"] = test_control_stores_filtered.sort_values(by="Test vs Control change(in %)",ascending=False)[config_cols["Test_store_Partner_ID_backup"]].values.tolist()
        target_variable_analysis_dict_filtered["Test vs (Control-Average)"] = test_control_stores_filtered_req.sort_values(
            by="Test vs Control change(in %)", ascending=False)["Test vs (Control-Average)"].values.tolist()
        return probability, decision, test_control_stores_actual, test_control_stores_filtered, target_variable_analysis_dict_actual, target_variable_analysis_dict_filtered, "Calculated successfully", True

    # def get_lift_analysis_results_US(test_id=None, teststores=None, target_variable=None, business_categories=None, control_stores_sales_method='Approach1',
    #                              test_type=None, cbu_lvl1_categories=None, cbu_lvl2_categories=None, pack_lvl_categories=None, seasonal_packaging=None, store_type=None, category=None, config=None, brands=None, stores_list_tobe_included = None):

        # '''
        #     get_lift_analysis_results_US
        # '''
        # if stores_list_tobe_included is None:
        #     stores_list_tobe_included = []

        # try:
        #     if test_id is not None:
        #         Allmeasurementstores =MeasurementTbl.objects.filter(is_active=True, is_deleted=False, test_id=test_id).values()
        #         test_measurement_table = pd.DataFrame(Allmeasurementstores)
        #         Allcontrolstores = ControlStoreMstr.objects.filter(test_id=test_id, checked_flag=1, is_active=True, is_deleted=False).values()
        #         test_control_mapping_stores = pd.DataFrame(Allcontrolstores)
        #         Alltestmap = TestStoreMap.objects.filter(is_active=True, is_deleted=False, test_id_id=int(test_id)).values()
        #         teststore_map_df = pd.DataFrame(Alltestmap)
        #         results_measurement = TestMstr.objects.filter(test_id=test_id).values()
        #         test_master_table = pd.DataFrame(results_measurement)

        #         tarvarmapping = config["weekly_target_variable"]
        #         storemstrmapping = config["store_mstr_columns"]
        #         metadata = config["metadata"]["test_measurement"]
        #         category = str(test_master_table["businessType"].values[0])
        #         store_type = str(test_master_table["channel"].values[0])
        #         # Download Required columns
        #         requiredcols = metadata["testmeasurement_columns"]
        #         teststores_columns_rename_dict = {val: "Teststore "+val for val in requiredcols if val not in [
        #             storemstrmapping["partner_id"], storemstrmapping["banner"]]}
        #         controlstores_columns_rename_dict = {val: "Controlstore "+val for val in requiredcols if val not in [
        #             storemstrmapping["partner_id"], storemstrmapping["banner"]]}
        #         # Getting the parameters from the Test Measurement Table based on Testid
        #         test_measurement_table = test_measurement_table[test_measurement_table["test_id_id"] == test_id].reset_index()
        #         test_control_mapping_stores = test_control_mapping_stores[test_control_mapping_stores['test_id_id'] == test_id]
        #         teststore_map_df = teststore_map_df[teststore_map_df['test_id_id'] == test_id]
        #         test_master_table = test_master_table[test_master_table['test_id'] == test_id]
        #         stores_list_tobe_included = teststore_map_df[teststore_map_df['outlier_user_suggestion'].astype(int)==0]['teststore_id'].tolist()
        #         if len(test_measurement_table) > 0:
        #             stores_master_df = filter_population(banners=[test_master_table['channel'].values[0]],
        #                                                     store_segments=convert_string_list(test_master_table['banners'].values[0]),
        #                                                     segments=convert_string_list(test_master_table['store_segment'].values[0]),
        #                                                     territories=convert_string_list(test_master_table['territory_name'].values[0]),
        #                                                     regions=convert_string_list(test_master_table['region'].values[0]),
        #                                                     test_type=None,
        #                                                     test_id=test_id,
        #                                                     regionName=None,
        #                                                     team=test_master_table['team'].values[0], config=config)
        #             stores = list(test_control_mapping_stores[test_control_mapping_stores['test_id_id']
        #                         == test_id]["Test_store_" + tarvarmapping["partner_id"]].unique())
        #             stores.extend(list(
        #             test_control_mapping_stores[test_control_mapping_stores['test_id_id'] == test_id][storemstrmapping["partner_id"]].unique()))
        #             req_pre_sales_information_df, req_post_sales_information_df,store_date_info = get_weekly_targetvariables_data_variable_dates(
        #                 test_id=test_id,
        #                 target_variable=target_variable,
        #                 business_categories=business_categories,
        #                 cbu_lvl1_categories=cbu_lvl1_categories,
        #                 cbu_lvl2_categories=cbu_lvl2_categories,
        #                 pack_lvl_categories=pack_lvl_categories,
        #                 seasonal_categories=seasonal_packaging,
        #                 channel=store_type,
        #                 category=category,
        #                 brands=brands,
        #                 stores=stores, config=config)
        #             if (req_pre_sales_information_df.shape[0]>0)&(req_post_sales_information_df.shape[0]>0):
        #                 test_control_stores = test_control_mapping_stores[test_control_mapping_stores["test_id_id"] == test_id]
        #                 test_control_stores = test_control_stores[test_control_stores["Test_store_"+tarvarmapping["partner_id"]].isin(teststore_map_df["teststore_id"].values.tolist())]

        #                 test_control_stores = test_control_stores[test_control_stores["Test_store_"+tarvarmapping["partner_id"]].isin(teststore_map_df["teststore_id"].values.tolist())]
        #                 if len(teststores) > 0:
        #                     test_control_stores = test_control_stores[test_control_stores["Test_store_"+storemstrmapping["partner_id"]].isin(teststores)]
        #                 transformed_pre_sales = req_pre_sales_information_df.groupby(['Test_store_'+tarvarmapping['partner_id'], 'Test_store_'+tarvarmapping['banner'],tarvarmapping['partner_id'], tarvarmapping['banner'], 'Pre_period_weeks']).aggregate({"Test group - Pre Period Average":'sum', "Control group - Pre Period Average":'sum'}).reset_index()
        #                 transformed_pre_sales["Test group - Pre Period Average"] = round(transformed_pre_sales["Test group - Pre Period Average"]/transformed_pre_sales['Pre_period_weeks'], 2)
        #                 transformed_pre_sales["Control group - Pre Period Average"] = round(transformed_pre_sales["Control group - Pre Period Average"]/transformed_pre_sales['Pre_period_weeks'], 2)

        #                 transformed_post_sales = req_post_sales_information_df.groupby(['Test_store_'+tarvarmapping['partner_id'], 'Test_store_'+tarvarmapping['banner'],tarvarmapping['partner_id'], tarvarmapping['banner'], 'Post_period_weeks']).aggregate({"Test group - Post Period Average":'sum', "Control group - Post Period Average":'sum'}).reset_index()
        #                 transformed_post_sales["Test group - Post Period Average"] = round(transformed_post_sales["Test group - Post Period Average"]/transformed_post_sales['Post_period_weeks'], 2)
        #                 transformed_post_sales["Control group - Post Period Average"] = round(transformed_post_sales["Control group - Post Period Average"]/transformed_post_sales['Post_period_weeks'], 2)
        #                 one_to_one = detect_test_control_mapping(test_control_mapping_stores, storemstrmapping)
        #                 test_control_stores = get_storelevel_liftresults_US(test_control_stores=test_control_stores,
        #                                                                     target_variable=target_variable,
        #                                                                     control_stores_sales_method=control_stores_sales_method,
        #                                                                     prewindow_target_data_grouped=transformed_pre_sales,
        #                                                                     postwindow_target_data_grouped=transformed_post_sales,
        #                                                                     test_type=test_type,
        #                                                                     config=config,
        #                                                                     one_to_one = one_to_one)

        #                 test_control_stores = prepare_test_measurement_columns_US(test_control_stores=test_control_stores,
        #                                                                             stores_master_df=stores_master_df,
        #                                                                             test_type=test_type,
        #                                                                             requiredcols=requiredcols,
        #                                                                             storemstrmapping=storemstrmapping,
        #                                                                             teststores_columns_rename_dict=teststores_columns_rename_dict,
        #                                                                             controlstores_columns_rename_dict=controlstores_columns_rename_dict, one_to_one=one_to_one)
        #                 # Compute Outliers Teststores by CustomerChain(UK Only) based on Lift (Z-score)
        #                 computation_level = "Teststore "+storemstrmapping['segment']
        #                 test_control_stores.sort_values(by= computation_level, inplace=True)
        #                 test_control_stores['Z-score'] = test_control_stores[[computation_level,"Test vs Control change(in %)"]].\
        #                             groupby(computation_level).transform(lambda x : abs((x - x.mean())/x.std()))
        #                 test_control_stores['Outlier'] = test_control_stores['Z-score'].map(lambda x: 0 if x<3  else 1)

        #                 # If store is outlier according to the statistical test but user accepts it as non-outlier
        #                 test_control_stores.loc[((test_control_stores['Outlier']==1) &
        #                     (test_control_stores["Test_store_"+tarvarmapping["partner_id"]].isin(stores_list_tobe_included))),"Outlier"] = 0

        #                 # If store is non-outlier according to the statistical test but user already flag it as outlier
        #                 # This mean Base case i.e selection of Outlier by user already done atleast once.
        #                 if len(stores_list_tobe_included) != 0:
        #                     test_control_stores.loc[((test_control_stores['Outlier']==0) &
        #                         (~test_control_stores["Test_store_"+tarvarmapping["partner_id"]].isin(stores_list_tobe_included))),"Outlier"] = 1
        #                 test_control_stores.fillna(0, inplace=True)
        #                 test_control_stores.reset_index(drop=True, inplace=True)
        #                 lift_analysis_results = test_control_stores.copy(deep=True)
        #                 lift_analysis_results = lift_analysis_results.merge(teststore_map_df[['teststore_id', 'pre_start', 'pre_end', 'testwin_start', 'testwin_end']].rename(columns={'teststore_id':'Test_store_'+tarvarmapping["partner_id"]}))
        #                 return lift_analysis_results
        #             else:
        #                 return "Couldn't find sales of the stores in the timeframe"
        #         else:
        #             return "Couldn't find the Test details for the test id"
        #     else:
        #         return "Please pass appropriate parameters"
        # except:
        #     traceback.print_exc()
