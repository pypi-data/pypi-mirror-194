"""
    About module: Handles all the features that are related to test measurement phase
    Classes:
        TestMeasurement
"""
import numpy as np
from scipy import stats
from typing import Tuple
class TestMeasurement:
    """
    A class to represent features of TestMeasurement.
    ...

    Attributes
    ----------
    config : configuration present in config_data either for a region or overall
    _tarvarmapping: sales table columns mapping
    _storemstrmapping: store table columns mapping

    Methods
    -------
    detect_one_to_one_mapping(): to check if there is 1:1 or 1:many mapping between test and control stores

    get_breakeven_lift(): estimates the breakeven lift% value
    get_cost(): estimates the cost of implementing RTM activity if breakeven lift is known
    """
    def __init__(self, config, region) -> None:
        """
        Constructs all the necessary attributes for the test measurement object.

        Parameters
        ----------
             config : configuration present in config_data either for a region or overall
            _tarvarmapping: sales table columns mapping
            _storemstrmapping: store table columns mapping
        """
        self._config = config[region] if region in config else config
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]
        self._metadata = self._config['metadata']['test_measurement']


    def detect_one_to_one_mapping(self, test_control_pairs) -> bool:
        """
            About function
            --------------
            This function determines if there is 1:1 or 1:many mapping between test and control pairs

            Parameters
            ----------
            test_control_pairs: test control pairs from control store master table;
                                columns Test

            Return values
            -------
            boolean True/False
        """
        control_store_count = test_control_pairs\
                            .groupby('Test_store_'+self._storemstrmapping["partner_id"])\
                            .aggregate({self._storemstrmapping["partner_id"]:'nunique'})\
                            .reset_index()
        if control_store_count[control_store_count[self._storemstrmapping["partner_id"]]>1].shape[0]>0:
            return False
        return True

    def get_test_vs_control_linegraph_util(self, req_pre_sales_information_df, req_post_sales_information_df,control_stores_sales_method, one_to_one, test_control_stores) -> dict:
        timeseries_dict = {}



        controlstores_weekly_target_presales = test_control_stores.merge(req_pre_sales_information_df,
                                                                on=['Test_store_'+self._storemstrmapping["partner_id"],
                                                                    'Test_store_'+self._storemstrmapping["banner"],
                                                                    self._storemstrmapping["partner_id"],
                                                                    self._storemstrmapping["banner"]],
                                                                )
        controlstores_weekly_target_presales.rename(
            columns={
                        'Week': "Preperiod Weeks",
                        'Control group - Pre Period Average': "Pre period target"
                    },
                    inplace=True)

        controlstores_weekly_target_postsales = test_control_stores.merge(req_post_sales_information_df,
                                                                on=['Test_store_'+self._storemstrmapping["partner_id"],
                                                                    'Test_store_'+self._storemstrmapping["banner"],
                                                                    self._storemstrmapping["partner_id"],
                                                                    self._storemstrmapping["banner"]])
        controlstores_weekly_target_postsales.rename(
            columns={
                        'Week': "Postperiod Weeks",
                        'Control group - Post Period Average': "Post period target"
                    },
                    inplace=True)

        teststores_weekly_target_presales = test_control_stores.merge(req_pre_sales_information_df,
                                                            on=["Test_store_"+self._storemstrmapping["partner_id"],
                                                            "Test_store_"+self._storemstrmapping["banner"]])

        teststores_weekly_target_presales.drop([self._tarvarmapping["partner_id"]+"_y",
                                                    self._tarvarmapping["banner"]+"_y"],
                                                axis=1,
                                                inplace=True)
        teststores_weekly_target_presales.rename(columns=
                                                {
                                                    'Test group - Pre Period Average': "Pre period target",
                                                    self._storemstrmapping["partner_id"]+"_x": self._storemstrmapping["partner_id"],
                                                    self._storemstrmapping["banner"]+"_x": self._storemstrmapping["banner"],
                                                    'Week': "Preperiod Weeks"
                                                },
                                                    inplace=True)

        teststores_weekly_target_postsales = test_control_stores.merge(req_post_sales_information_df,
                                                            on=["Test_store_"+self._storemstrmapping["partner_id"],
                                                            "Test_store_"+self._storemstrmapping["banner"]])
        teststores_weekly_target_postsales.rename(columns=
                                                {
                                                    'Test group - Post Period Average': "Post period target",
                                                    'Week': "Postperiod Weeks",
                                                    self._storemstrmapping["partner_id"]+"_x": self._storemstrmapping["partner_id"],
                                                    self._storemstrmapping["banner"]+"_x": self._storemstrmapping["banner"]}, inplace=True)
        teststores_weekly_target_postsales.drop([self._tarvarmapping["partner_id"]+"_y", self._tarvarmapping["banner"]+"_y"], axis=1, inplace=True)



        controlstores_weekly_target_postsales["Postperiod Weeks"] = controlstores_weekly_target_postsales["Postperiod Weeks"].apply(
            lambda x: str(x)[:4]+" Week "+str('%02d' % int(str(x)[-2:])))
        teststores_weekly_target_postsales["Postperiod Weeks"] = teststores_weekly_target_postsales["Postperiod Weeks"].apply(
            lambda x: str(x)[:4]+" Week "+str('%02d' % int(str(x)[-2:])))

        controlstores_weekly_target_presales["Preperiod Weeks"] = controlstores_weekly_target_presales["Preperiod Weeks"].apply(
            lambda x: str(x)[:4]+" Week "+str('%02d' % int(str(x)[-2:])))
        teststores_weekly_target_presales["Preperiod Weeks"] = teststores_weekly_target_presales["Preperiod Weeks"].apply(
            lambda x: str(x)[:4]+" Week "+str('%02d' % int(str(x)[-2:])))
        if control_stores_sales_method == 'Approach1' and one_to_one==False:#
            controlstores_weekly_target_presales = controlstores_weekly_target_presales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],
                                                                                "Test_store_"+self._storemstrmapping["banner"],
                                                                                "Preperiod Weeks",
                                                                                'Pre_period_weeks']).aggregate({'Pre period target':'mean'}).reset_index()

            controlstores_weekly_target_postsales = controlstores_weekly_target_postsales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],
                                                                                "Test_store_"+self._storemstrmapping["banner"],
                                                                                "Postperiod Weeks",
                                                                                'Post_period_weeks']).aggregate({'Post period target':'mean'}).reset_index()


        if  control_stores_sales_method == 'Approach2' and one_to_one==False :
            controlstores_weekly_target_presales["Overall Similarity Score"] = controlstores_weekly_target_presales['Similarity Score']/controlstores_weekly_target_presales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"],"Preperiod Weeks"])['Similarity Score'].transform('sum')
            controlstores_weekly_target_presales['Pre period target'] = controlstores_weekly_target_presales['Pre period target']*controlstores_weekly_target_presales["Overall Similarity Score"]
            controlstores_weekly_target_presales = controlstores_weekly_target_presales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],
                                                                                "Test_store_"+self._storemstrmapping["banner"],
                                                                                "Preperiod Weeks"])['Pre period target'].sum().reset_index()
            controlstores_weekly_target_postsales["Overall Similarity Score"] = controlstores_weekly_target_postsales['Similarity Score']/controlstores_weekly_target_postsales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"],"Postperiod Weeks"])['Similarity Score'].transform('sum')
            controlstores_weekly_target_postsales['Post period target'] = controlstores_weekly_target_postsales['Post period target']*controlstores_weekly_target_postsales["Overall Similarity Score"]
            controlstores_weekly_target_postsales = controlstores_weekly_target_postsales.groupby(["Test_store_"+self._storemstrmapping["partner_id"],
                                                                                "Test_store_"+self._storemstrmapping["banner"],
                                                                                "Postperiod Weeks"])['Post period target'].sum().reset_index()

        control_post_weekly_timeseries = controlstores_weekly_target_postsales.groupby(
            "Postperiod Weeks")["Post period target"].mean().reset_index()
        test_post_weekly_timeseries = teststores_weekly_target_postsales.groupby(
            "Postperiod Weeks")["Post period target"].mean().reset_index()
        control_pre_weekly_timeseries = controlstores_weekly_target_presales.groupby(
            "Preperiod Weeks")["Pre period target"].mean().reset_index()
        test_pre_weekly_timeseries = teststores_weekly_target_presales.groupby(
            "Preperiod Weeks")["Pre period target"].mean().reset_index()

        test_pre_weekly_timeseries['Pre period target'] = test_pre_weekly_timeseries['Pre period target'].round(2)
        control_pre_weekly_timeseries['Pre period target'] = control_pre_weekly_timeseries['Pre period target'].round(2)
        test_post_weekly_timeseries['Post period target'] = test_post_weekly_timeseries['Post period target'].round(2)
        control_post_weekly_timeseries['Post period target'] = control_post_weekly_timeseries['Post period target'].round(2)

        timeseries_dict["Test Preperiod"] = [test_pre_weekly_timeseries['Preperiod Weeks'].values.tolist(
        ), test_pre_weekly_timeseries['Pre period target'].values.tolist()]
        timeseries_dict["Control Preperiod"] = [control_pre_weekly_timeseries['Preperiod Weeks'].values.tolist(
        ), control_pre_weekly_timeseries['Pre period target'].values.tolist()]
        timeseries_dict["Test Postperiod"] = [test_post_weekly_timeseries['Postperiod Weeks'].values.tolist(
        ), test_post_weekly_timeseries['Post period target'].values.tolist()]
        timeseries_dict["Control Postperiod"] = [control_post_weekly_timeseries['Postperiod Weeks'].values.tolist(
        ), control_post_weekly_timeseries['Post period target'].values.tolist()]

        # print("Time taken in seconds: ",
        #       datetime.datetime.now()-start_time)

        return timeseries_dict

    def get_storelevel_liftresults(self, one_to_one, test_control_stores,
                                  prewindow_target_data_grouped,
                                  postwindow_target_data_grouped,
                                  target_variable, control_stores_sales_method, test_type=None):
        """
        get_storelevel_liftresults_US
        """
        print("In get_storelevel_liftresults_US")
        test_control_stores = test_control_stores.merge(prewindow_target_data_grouped,
                                                            on=["Test_store_"+self._storemstrmapping["partner_id"], "Test_store_"+self._storemstrmapping["banner"],
                                                                self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]],
                                                            how="left")
        test_control_stores = test_control_stores.merge(postwindow_target_data_grouped,
                                                            on=["Test_store_"+self._storemstrmapping["partner_id"], "Test_store_"+self._storemstrmapping["banner"],
                                                                self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]],
                                                            how="left")

        if control_stores_sales_method == 'Approach1' and one_to_one==False:
            control_stores_rsv_calculation = test_control_stores.groupby(["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]]).agg({"Control group - Pre Period Average":'mean',
            "Control group - Post Period Average":'mean',self._storemstrmapping["partner_id"]:'nunique'}).reset_index().rename(columns={self._storemstrmapping["partner_id"]:"Control Store Count"})
            test_control_stores.drop(columns=[self._storemstrmapping["partner_id"],self._storemstrmapping["banner"],"Control group - Pre Period Average","Control group - Post Period Average"],inplace=True)
            test_control_stores.drop_duplicates(subset=["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]],inplace=True)
            test_control_stores = test_control_stores.merge(control_stores_rsv_calculation,on=["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]])

        if control_stores_sales_method == 'Approach2' and one_to_one==False:
            test_control_stores["RSV Proportion based on Similarity"] = test_control_stores['Similarity Score']/test_control_stores.groupby(["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]])['Similarity Score'].transform('sum')
            test_control_stores["Control group - Pre Period Average"] = test_control_stores["Control group - Pre Period Average"]*test_control_stores["POS Proportion based on Similarity"]
            test_control_stores["Control group - Post Period Average"] = test_control_stores["Control group - Post Period Average"]*test_control_stores["POS Proportion based on Similarity"]
            control_stores_rsv_calculation = test_control_stores.groupby(["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]]).agg({"Control group - Pre Period Average":'sum',
            "Control group - Post Period Average":'sum',self._storemstrmapping["partner_id"]:'nunique'}).reset_index().rename(columns={self._storemstrmapping["partner_id"]:"Control Store Count"})
            test_control_stores.drop(columns=[self._storemstrmapping["partner_id"],self._storemstrmapping["banner"],
                                            "Control group - Pre Period Average","Control group - Post Period Average",
                                            "POS Proportion based on Similarity",'Similarity Score'],inplace=True)
            test_control_stores.drop_duplicates(subset=["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]],inplace=True)
            test_control_stores = test_control_stores.merge(control_stores_rsv_calculation,on=["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]])

        test_control_stores["Variable"] = target_variable
        test_control_stores["Test group - Pre vs Post change"] = test_control_stores["Test group - Post Period Average"] - \
            test_control_stores["Test group - Pre Period Average"]
        test_control_stores["Control group - Pre vs Post change"] = test_control_stores["Control group - Post Period Average"] - \
            test_control_stores["Control group - Pre Period Average"]
        test_control_stores["Test group - Pre vs Post change(in %)"] = ((test_control_stores["Test group - Post Period Average"] -
                                                                        test_control_stores["Test group - Pre Period Average"])/test_control_stores["Test group - Pre Period Average"])*100
        test_control_stores["Control group - Pre vs Post change(in %)"] = ((test_control_stores["Control group - Post Period Average"] -
                                                                            test_control_stores["Control group - Pre Period Average"])/test_control_stores["Control group - Pre Period Average"])*100

        test_control_stores["Test group - Post Period Estimated"] = test_control_stores["Test group - Pre Period Average"]*(
            test_control_stores["Control group - Pre vs Post change(in %)"]/100)
        test_control_stores["Test group - Post Period Estimated"] = test_control_stores[[
            "Test group - Pre Period Average", "Test group - Post Period Estimated"]].sum(axis=1)
        test_control_stores["Test group - Post Period Estimated"] = test_control_stores["Test group - Post Period Estimated"].round(
            2)
        test_control_stores["Incremental RSV"] = test_control_stores["Test group - Post Period Average"] - \
            test_control_stores["Test group - Post Period Estimated"]

        #test_control_stores["Test vs Control change(in %)"] = test_control_stores["Test group - Pre vs Post change(in %)"] - test_control_stores["Control group - Pre vs Post change(in %)"]
        test_control_stores["Test vs Control change(in %)"] = ((test_control_stores["Test group - Post Period Average"] -
                                                                test_control_stores["Test group - Post Period Estimated"])/test_control_stores["Test group - Post Period Estimated"])*100

        test_control_stores["Test group - Pre vs Post change"] = test_control_stores["Test group - Pre vs Post change"].round(
            2)
        test_control_stores["Control group - Pre vs Post change"] = test_control_stores["Control group - Pre vs Post change"].round(
            2)
        test_control_stores["Test group - Pre vs Post change(in %)"] = test_control_stores["Test group - Pre vs Post change(in %)"].round(
            2)
        test_control_stores["Control group - Pre vs Post change(in %)"] = test_control_stores[
            "Control group - Pre vs Post change(in %)"].round(2)
        test_control_stores["Test vs Control change(in %)"] = test_control_stores["Test vs Control change(in %)"].round(
            2)
        #test_control_stores["Test group - Estimated vs Post change(in %)"] = test_control_stores["Test group - Estimated vs Post change(in %)"].round(2)
        ####Handling NaNs in the data
        numeric_columns = test_control_stores.select_dtypes(include=['number']).columns
        # fill 0 to all NaN
        test_control_stores[numeric_columns] = test_control_stores[numeric_columns].fillna(0)
        test_control_stores[numeric_columns] = test_control_stores[numeric_columns].replace([np.inf, -np.inf], 0)

        object_columns = list(set(test_control_stores.columns) - set(numeric_columns))
        # fill "" to all NaN object columns
        test_control_stores[object_columns] = test_control_stores[object_columns].fillna("NOT-AVAILABLE")

        return test_control_stores

    def prepare_test_measurement_columns(self, one_to_one, test_control_stores=None, stores_master_df=None, requiredcols=None,
                                        teststores_columns_rename_dict=None, controlstores_columns_rename_dict=None,
                                        test_type=None):
        """
        prepare_test_measurement_columns_US
        """
        if one_to_one==False:
                test_control_stores = test_control_stores.merge(stores_master_df[requiredcols],
                                    left_on=["Test_store_"+self._storemstrmapping["partner_id"],"Test_store_"+self._storemstrmapping["banner"]],
                                    right_on=[self._storemstrmapping["partner_id"],self._storemstrmapping["banner"]],
                                    how="left")

                test_control_stores.drop([self._storemstrmapping["partner_id"],self._storemstrmapping["banner"]],axis=1,inplace=True)
                test_control_stores.rename(columns=teststores_columns_rename_dict,inplace=True)
                return test_control_stores
        else:
            test_control_stores = test_control_stores.merge(stores_master_df[requiredcols],
                                                            left_on=["Test_store_"+self._storemstrmapping["partner_id"], "Test_store_"+self._storemstrmapping["banner"]],
                                                            right_on=[self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]],
                                                            how="left")
            test_control_stores.drop([self._storemstrmapping["partner_id"]+"_y",
                                    self._storemstrmapping["banner"]+"_y"], axis=1, inplace=True)
            test_control_stores.rename(columns={self._storemstrmapping["partner_id"]+"_x": self._storemstrmapping["partner_id"],
                                                self._storemstrmapping["banner"]+"_x": self._storemstrmapping["banner"]}, inplace=True)
            test_control_stores.rename(columns=teststores_columns_rename_dict, inplace=True)

            test_control_stores = test_control_stores.merge(stores_master_df[requiredcols],
                                                            left_on=[self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]],
                                                            right_on=[self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]],
                                                            how="left")
            test_control_stores.rename(columns=controlstores_columns_rename_dict, inplace=True)

            return test_control_stores


    def calculate_probability_decision(self, one_to_one, test_control_stores, break_even_lift, mean_changepercent)->Tuple[float, str, float, str, bool]:
        if one_to_one == True:
            columns_req = ["Test_store_"+self._storemstrmapping["partner_id"], "Test group - Pre vs Post change(in %)",
                    "Control group - Pre vs Post change(in %)", "Test_store_" + self._storemstrmapping["partner_id"], self._storemstrmapping["partner_id"],
                    "Test group - Pre vs Post change", "Control group - Pre vs Post change"]
            if len(set(columns_req).intersection(set(test_control_stores.columns)))<len(set(columns_req)):
                return 0, "", 0, "Either of the columns are missing required in probability calculations; {}".format(columns_req), False
            stdev_changepercent_1 = test_control_stores.groupby("Test_store_"+self._storemstrmapping["partner_id"]).aggregate(
                {"Test group - Pre vs Post change(in %)": 'mean'})["Test group - Pre vs Post change(in %)"].std()
            stdev_changepercent_2 = test_control_stores.groupby(self._storemstrmapping["partner_id"]).aggregate(
                {"Control group - Pre vs Post change(in %)": 'mean'})["Control group - Pre vs Post change(in %)"].std()
            noofdatapoints1 = test_control_stores["Test_store_" + self._storemstrmapping["partner_id"]].nunique()
            noofdatapoints2 = test_control_stores[self._storemstrmapping["partner_id"]].nunique()
        else:
            columns_req = ["Test group - Pre vs Post change(in %)", "Control group - Pre vs Post change(in %)",
                    "Test group - Pre vs Post change", "Control group - Pre vs Post change"]
            if len(set(columns_req).intersection(set(test_control_stores.columns)))<len(set(columns_req)):
                return 0, "", 0, "Either of the columns are missing required in probability calculations; {}".format(columns_req), False

            stdev_changepercent_1 = test_control_stores["Test group - Pre vs Post change(in %)"].std()
            stdev_changepercent_2 = test_control_stores["Control group - Pre vs Post change(in %)"].std()
            noofdatapoints1 = test_control_stores.shape[0]
            noofdatapoints2 = test_control_stores.shape[0]
        pooled_stdev_numerator = ((noofdatapoints1-1)*np.power(stdev_changepercent_1, 2)+(
            noofdatapoints2-1)*np.power(stdev_changepercent_2, 2))
        pooled_stdev_denominator = (noofdatapoints1+noofdatapoints2-2)
        pooled_stdev = np.sqrt(pooled_stdev_numerator/pooled_stdev_denominator)

        stderr = pooled_stdev * \
            np.sqrt(1/noofdatapoints1+1/noofdatapoints2)

        probability = round(1 - stats.norm.cdf(float(break_even_lift), mean_changepercent, stderr), 2)
        if (probability >= self._metadata["probability_thresholds"][1]) & (probability <= self._metadata["probability_thresholds"][2]):
            decision = "Implement the change"
        elif (probability >= self._metadata["probability_thresholds"][0]) & (probability < self._metadata["probability_thresholds"][1]):
            decision = "Can Implement the change with caution"
        else:
            decision = "Do not implement the change"

        tStat, pVal = stats.ttest_ind(test_control_stores["Test group - Pre vs Post change"].values,
                                        test_control_stores["Control group - Pre vs Post change"].values, nan_policy='omit')


        return probability, decision, pVal, "Probability calculated successfully!!", True

    def _generate_KPI_values(self, rsvwindow_target_data, target_variable, test_master_table,
        target_variable_analysis_dict_actual, conversionfactor, cost) -> dict:
        total_sales = rsvwindow_target_data[target_variable].sum()
        number_stores = rsvwindow_target_data[self._tarvarmapping['partner_id']].nunique()
        inc_rsv_lift = (target_variable_analysis_dict_actual["test_vs_control_change"]/100)*total_sales
        inc_mac_lift = inc_rsv_lift*conversionfactor
        earnings = inc_mac_lift - (cost)
        costoutput = cost
        rsv_weeks = rsvwindow_target_data[self._tarvarmapping['week']].nunique()
        target_variable_analysis_dict_actual['rsv_week_numbers'] = list(rsvwindow_target_data[self._tarvarmapping['week']].unique())
        target_variable_analysis_dict_actual["overall_sales"] = total_sales
        target_variable_analysis_dict_actual["sales_week"] = round(total_sales/rsv_weeks, 2)
        target_variable_analysis_dict_actual["number_stores"] = number_stores
        target_variable_analysis_dict_actual["inc_rsv_lift"] = round(inc_rsv_lift, 2)
        target_variable_analysis_dict_actual["inc_mac_lift"] = round(inc_mac_lift, 2)
        target_variable_analysis_dict_actual["earnings"] = round(earnings, 2)
        target_variable_analysis_dict_actual["cost"] = round(costoutput, 2)
        target_variable_analysis_dict_actual["inc_rsv_lift_per_store"] = round(inc_rsv_lift/number_stores, 2)
        target_variable_analysis_dict_actual["inc_rsv_lift_per_store_per_week"] = round(target_variable_analysis_dict_actual["inc_rsv_lift_per_store"]\
                                                                                            /rsv_weeks, 2)
        target_variable_analysis_dict_actual["earnings_per_store"] = round(earnings/number_stores, 2)
        target_variable_analysis_dict_actual["earnings_per_store_per_week"] = round(target_variable_analysis_dict_actual["earnings_per_store"]\
                                                                                /rsv_weeks, 2)
        target_variable_analysis_dict_actual["cost_per_store"] = round(costoutput/number_stores, 2)
        target_variable_analysis_dict_actual["cost_per_store_per_week"] = round(target_variable_analysis_dict_actual["cost_per_store"]\
                                                                                /rsv_weeks, 2)
        target_variable_analysis_dict_actual['earnings_per_week'] = round(inc_rsv_lift/rsv_weeks, 2)
        return target_variable_analysis_dict_actual
