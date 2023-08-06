from typing import Tuple, final

import numpy as np
import pandas as pd
import statsmodels.api as sm
from DSCode.library.ds_common_functions import gower_matrix
from scipy import stats
from sklearn.preprocessing import StandardScaler


class CntrlStoreSelectionFeature:
    def __init__(self, config, region,sales_object, store_object,test_id) -> None:
        self._config = config[region] if region in config else config
        self._sales_object = sales_object #Ceab sales object
        self._store_object = store_object
        self._metadata = self._config["metadata"]
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]
        self._test_id = test_id
        self._control_pool = []

    def data_extract(self, applicability_criteria, target_variable, test_type, store_list, uploaded_file_df=None)->Tuple[pd.DataFrame, pd.DataFrame,list,pd.DataFrame, pd.DataFrame,str, bool]:

        test_master = self._store_object.read_test_master_table_by_test_ids(test_id=self._test_id)
        test_master = test_master[test_master['test_id'] == self._test_id]
        if test_master.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(),[],pd.DataFrame(),pd.DataFrame(),\
                     """No records found for the current test in Test Master table!!""", False

        stores_master_df = self._store_object.filter_population(applicability_criteria=applicability_criteria, storelist = store_list, uploaded_file_df = uploaded_file_df)
        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(),[], pd.DataFrame(), pd.DataFrame(),"No stores found in the population", False
        annualrsvlifts, valid_sales_stores, _, _, consideryearweeks,\
                 message, success_flag = self._sales_object.get_annual_rsv_lifts(
                                                                                target_variable=target_variable,
                                                                                test_master_df = test_master,
                                                                                stores = list(stores_master_df[self._storemstrmapping["partner_id"]].unique()),
                                                                                applicability_criteria=applicability_criteria,
                                                                                test_type=test_type,
                                                                                )
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(),[],pd.DataFrame(), pd.DataFrame(),message, False
        return annualrsvlifts, valid_sales_stores,consideryearweeks,test_master, stores_master_df, "Sales computed Successfully!", True
    @final
    def _get_feature_thresholds(self, teststores, controlstores, features)-> Tuple[dict]:

        """
        # This function corresponds to the test vs population summary module in the tool - No uk specific code in it
        # Note this function is currently not in use in the latest version of the FAST Tool
        """
        threshold_dict = {}
        metadata = self._config["metadata"]["test_planning"]

        for feature in features:

            std1 = teststores[feature].std()
            std2 = controlstores[feature].std()

            samples1 = teststores[feature].shape[0]
            samples2 = controlstores[feature].shape[0]

            numerator = np.power((std1*std1/samples1 + std2*std2/samples2), 2)
            denominator = (np.power((std1*std1/samples1), 2)/(samples1-1) +
                        np.power((std2*std2/samples2), 2)/(samples2-1))
            degfreedom = numerator/denominator
            pval = metadata["test_vs_control_pvalue"]

            criticalvalue = stats.t.ppf(1-pval/2, degfreedom)

            difference_in_means = criticalvalue * \
                np.sqrt((std1*std1/samples1 + std2*std2/samples2))

            threshold_dict[feature] = difference_in_means

        return threshold_dict

    @final
    def prepare_test_control_stores(self, dfA=None, dfB=None, teststoreid=None, gowerdistances=None, num_cntrl_rejected=None, calltype=None,
                                reqcontrolstores=None, corrbased=None, rejected_with_control_left=None):
        """
            prepare_test_control_stores
        """

        dfB["Gower_Distance"] = gowerdistances
        dfB = dfB.sort_values(by="Gower_Distance", ascending=True)
        dfB["Similarity_Measure"] = 1 - dfB["Gower_Distance"]

        if num_cntrl_rejected is None:
            if calltype == "old":
                dfB = dfB.head(1)
            if calltype == "new":
                if corrbased == 1:
                    top5_percent_stores = dfB[dfB['Similarity_Measure'] > (
                        dfB['Similarity_Measure'].max() - 0.05)]
                    if top5_percent_stores.shape[0] >= reqcontrolstores:
                        dfB = top5_percent_stores
                    else:
                        dfB = dfB.head(reqcontrolstores)
                else:
                    dfB = dfB.head(reqcontrolstores)
        else:
            dfB = dfB[~(dfB[self._storemstrmapping["partner_id"]].isin(
                rejected_with_control_left[teststoreid]))]
            if calltype == "old":
                dfB = dfB.head(1)
            if calltype == "new":
                reqcontrolstores = 1  # always for recompute scenario when corrbased=0
                if corrbased == 1:
                    top5_percent_stores = dfB[dfB['Similarity_Measure'] > (
                        dfB['Similarity_Measure'].max() - 0.05)].shape[0]
                    if top5_percent_stores > reqcontrolstores:
                        reqcontrolstores = top5_percent_stores
                dfB = dfB.head(reqcontrolstores)

        filteredteststoredf = dfA[dfA[self._storemstrmapping["partner_id"]]
                                == teststoreid]
        for col in self._metadata['test_planning']["teststores_columns"]:
            dfB["Test_store_" + col] = filteredteststoredf[col].values[0]
        return dfB

    @final
    def _prepare_test_control_stores_vecotrize(self, useA=None, useB=None, test_df=None, control_df=None, calltype=None,
                                          reqcontrolstores=None, corrbased=None):

        """
            _prepare_test_control_stores_vecotrize
        """
        gowermatrix = gower_matrix(useA, useB)
        test_df.rename(columns={
                    self._storemstrmapping["partner_id"]: 'Test_store_'+self._storemstrmapping["partner_id"]}, inplace=True)
        test_df['key'] = 1
        test_control = test_df.merge(control_df, on='key')
        test_control.drop(columns=['key'], inplace=True)
        test_control['Gower_Distance'] = gowermatrix.flatten(order='A')

        if calltype == "old":
            test_control = test_control.sort_values(
                by="Gower_Distance", ascending=True)
            test_control = test_control.groupby(
                'Test_store_'+self._storemstrmapping["partner_id"]).head(1).reset_index(drop=True)
        if calltype == "new":
            test_control = test_control.sort_values(
                by="Gower_Distance", ascending=True)
            if corrbased == 1:
                min_gower_dist_pair = test_control.drop_duplicates(
                    subset=['Test_store_'+self._storemstrmapping["partner_id"]])
                min_gower_dist_pair['Gower_Distance'] = min_gower_dist_pair['Gower_Distance']+0.05
                min_gower_dist_pair = min_gower_dist_pair.drop(
                    columns=[self._storemstrmapping["partner_id"]]).rename(columns={'Gower_Distance': 'Min_Gower_dist'})
                test_control = test_control.merge(
                    min_gower_dist_pair, on=['Test_store_'+self._storemstrmapping["partner_id"]])
                test_control['flag'] = test_control['Gower_Distance'] < test_control['Min_Gower_dist']
                top_5_percent_store = test_control.groupby(
                    ['Test_store_'+self._storemstrmapping["partner_id"]])['flag'].sum().reset_index()
                top_5_percent_store = top_5_percent_store[top_5_percent_store['flag'] >= reqcontrolstores][[
                    'Test_store_'+self._storemstrmapping["partner_id"]]]
                test_control = test_control.merge(
                    top_5_percent_store, how='left', on='Test_store_'+self._storemstrmapping["partner_id"], indicator=True)
                df1 = test_control[(test_control['_merge'] == 'both') & (
                    test_control['flag'] == True)]
                df2 = test_control[test_control['_merge'] == 'left_only'].groupby(
                    'Test_store_'+self._storemstrmapping["partner_id"]).head(reqcontrolstores)
                test_control = pd.concat([df1, df2], sort=False, ignore_index=True)
                test_control.drop(columns=['_merge', 'flag', 'Min_Gower_dist'], inplace=True)
            else:
                test_control = test_control.groupby(
                    'Test_store_'+self._storemstrmapping["partner_id"]).head(reqcontrolstores).reset_index(drop=True)
        test_control["Similarity_Measure"] = 1-test_control["Gower_Distance"]
        test_control["Similarity_Measure"] = test_control["Similarity_Measure"].round(2)
        test_control["Gower_Distance"] = test_control["Gower_Distance"].round(2)
        return test_control

    @final
    def _get_test_control_stores_correlation(self, dfA=None, dfB=None, test_control_stores=None, weekcolumns=None, num_cntrl_rejected=None, corrbased=None, reqcontrolstores=None):
        """
            get_test_control_stores_correlation
        """
        print(" in get_test_control_stores_correlation")
        dfA = dfA[dfA[self._storemstrmapping["partner_id"]].isin(
            test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]].unique())]
        dfB = dfB[dfB[self._storemstrmapping["partner_id"]].isin(
            test_control_stores[self._storemstrmapping["partner_id"]].unique())]
        A = dfA[weekcolumns].values.T
        B = dfB[weekcolumns].values.T
        # time1 = time.process_time()
        N = B.shape[0]
        sA = A.sum(0)
        sB = B.sum(0)
        p1 = N*np.einsum('ij,ik->kj', A, B)
        p2 = sA*sB[:, None]
        p3 = N*((B**2).sum(0)) - (sB**2)
        p4 = N*((A**2).sum(0)) - (sA**2)
        pcorr = ((p1 - p2)/np.sqrt(p4*p3[:, None]))
        test_store_dict = dict(zip(dfA[self._storemstrmapping["partner_id"]].values.tolist(), range(dfA[self._storemstrmapping["partner_id"]].nunique())))

        control_store_dict = dict(zip(dfB[self._storemstrmapping["partner_id"]].values.tolist(), range(dfB[self._storemstrmapping["partner_id"]].nunique())))


        test_control_stores['Correlation'] = test_control_stores[['Test_store_'+self._storemstrmapping["partner_id"], self._storemstrmapping["partner_id"]]]\
            .apply(lambda x: pcorr[control_store_dict[x[self._storemstrmapping["partner_id"]]]][test_store_dict[x['Test_store_'+self._storemstrmapping["partner_id"]]]], axis=1)
        test_control_stores = test_control_stores.sort_values(
            by=["Test_store_"+self._storemstrmapping["partner_id"], "Similarity_Measure"], ascending=False)
        if corrbased == 1:
            test_control_stores = test_control_stores.sort_values(
                by=["Test_store_"+self._storemstrmapping["partner_id"], "Correlation"], ascending=False)
        if num_cntrl_rejected is None:
            test_control_stores = test_control_stores.groupby(
                ["Test_store_"+self._storemstrmapping["partner_id"]], as_index=False, sort=False).head(reqcontrolstores)
        else:
            test_control_stores = test_control_stores.groupby(
                ["Test_store_"+self._storemstrmapping["partner_id"]]).apply(lambda x: x.head(1)).reset_index(drop=True)
        test_control_stores[['Gower_Distance', 'Similarity_Measure', 'Correlation']] = test_control_stores[[
            'Gower_Distance', 'Similarity_Measure', 'Correlation']].round(2)
        return test_control_stores

    def _get_max_required_control_stores(self, reqcontrolstores, applicability_criteria)->int:
        if ("advanced_control_mapping" in applicability_criteria)and \
            len(applicability_criteria['advanced_control_mapping'].values()) > 0:
                return max(reqcontrolstores, max(int(val) for val in applicability_criteria['advanced_control_mapping'].values()))
        return reqcontrolstores

    def _handle_control_per_store_attribute(self, control_stores, one_to_one=False,
            control_per_store_attribute=None)->Tuple[pd.DataFrame, str, bool]:
        if  control_per_store_attribute is not None:
            if 'store_attribute' not in self._config["feature_parameter"]['advanced_control_mapping']:
                return pd.DataFrame(), "Error in config!! store_attribute key missing from config['feature_parameter']['advanced_control_mapping']", False
            req_store_attribute = 'Test_store_'+self._config["feature_parameter"]['advanced_control_mapping']['store_attribute']
            req_columns = ['Test_store_'+self._storemstrmapping['partner_id'], req_store_attribute]
            if len(set(req_columns).intersection(set(control_stores.columns))) != len(req_columns):
                return pd.DataFrame(), "control store passed to function doesnot have following attributes: {}".format(req_columns), False
            test_store_store_attribute_dict = dict(
                        zip(control_stores['Test_store_'+self._storemstrmapping['partner_id']],
                         control_stores[req_store_attribute]))
            cs_updated = pd.DataFrame()
            for store_identifier in list(test_store_store_attribute_dict.keys()):
                if test_store_store_attribute_dict[store_identifier] in (list(control_per_store_attribute.keys())):
                    j = control_per_store_attribute[test_store_store_attribute_dict[store_identifier]]
                else:
                    j = 1
                cs_updated = pd.concat([
                                        control_stores.loc[
                                            (control_stores['Test_store_'+self._storemstrmapping['partner_id']] == store_identifier)
                                            ].sort_values(by=['Similarity_Difference'],
                                                        ascending=False).head(j),
                                        cs_updated],
                                        ignore_index=True)

            df1 = cs_updated.groupby("Test_store_" + self._storemstrmapping["partner_id"],
                                        as_index=False,
                                        group_keys=False).apply(lambda x: x.iloc[0])
            df2 = cs_updated.groupby("Test_store_" + self._storemstrmapping["partner_id"],
                                        as_index=False,
                                        group_keys=False).apply(lambda x: x.iloc[1:])
        else:
            df1 = control_stores.groupby("Test_store_" + self._storemstrmapping["partner_id"],
                                            as_index=False,
                                            group_keys=False).apply(lambda x: x.iloc[0])
            df2 = control_stores.groupby("Test_store_" + self._storemstrmapping["partner_id"],
                                            as_index=False,
                                            group_keys=False).apply(lambda x: x.iloc[1:])

        if one_to_one == True:
            df1["Checked_Flag"] = 1
            df2["Checked_Flag"] = 0
            df1["is_recommended"] = 1
            df2["is_recommended"] = 0

        else:
            df1["Checked_Flag"] = 1
            df2["Checked_Flag"] = 1
            df1["is_recommended"] = 1
            df2["is_recommended"] = 1

        return pd.concat([df1, df2]), "Handled control stores per test stores", True

    def identify_control_stores_util(self, teststores, business_categories,stores_master_df, annualrsvliftdf, consideryearweeks, valid_sales_stores, summary_sales_weeks, sales_weeks, compare_variables,target_variable, max_date_data_available, control_store_pool, reqcontrolstores):

        if control_store_pool is not None and len(control_store_pool)>0:
            self._control_pool = control_store_pool


        stores_master_df = self._store_object.filter_active_test_control_stores(stores_master_df=stores_master_df.copy(deep=True),
                                                                                         remove_type=self._config["feature_parameter"]["active_store_filter_type"],
                                                                                         max_week_data_available=max_date_data_available)
        if stores_master_df.shape[0] ==0 :
            return pd.DataFrame(), "All stores are actively participating in other test", False
        stores_master_df = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(valid_sales_stores[self._tarvarmapping['partner_id']].unique())]

        filtered = valid_sales_stores[valid_sales_stores[self._tarvarmapping['week']].isin(consideryearweeks[summary_sales_weeks:])]
        pivoteddf = pd.pivot_table(filtered, index=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]], columns=self._tarvarmapping['week'], values=target_variable).reset_index().rename_axis(None, axis=1)
        weekcolumns = [col for col in pivoteddf.columns.tolist() if col not in [self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]]]
        stores_master_df = stores_master_df.merge(pivoteddf, on=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]])

        filtercolumns = [self._tarvarmapping["partner_id"]] + [target_variable+' Year 1', target_variable+' Year 2', target_variable+' Lift']
        if self._config["feature_parameter"]["is_product_present"] == 1:
            filtercolumns.extend(["CBU_Category_"+target_variable+' Year 1', "CBU_Category_"+target_variable+' Year 2', "CBU_Category_"+target_variable+" Lift"])
            compare_variables_cbu_category = compare_variables.copy()
            compare_variables_cbu_category.extend(["CBU_Category_"+target_variable+' Year 1', "CBU_Category_"+target_variable+' Year 2',
                                            "CBU_Category_"+target_variable+" Lift"])

        if (len(business_categories)!=0) & (len(business_categories)<self._metadata['test_planning']["business_categories_count"]):
            common_category_specific = list(set(self._metadata['test_planning']["business_category_specific_compare"]) & set(compare_variables))
            if len(common_category_specific)>0:
                features_list = [[j+"_"+i for j in common_category_specific] for i in business_categories]
                category_specific_features = [item for elem in features_list for item in elem]
                compare_variables.extend(category_specific_features)
                compare_variables_cbu_category.extend(category_specific_features)

        stores_master_df = stores_master_df.merge(annualrsvliftdf[filtercolumns], left_on=self._storemstrmapping["partner_id"], right_on=self._tarvarmapping["partner_id"])
        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(), "Population stores do not have sales", False

        compare_variables.extend([target_variable+" Year 1", target_variable+" Year 2", target_variable+" Lift"])

        # Scaling Store Features Column values on the Entire Population set
        scaler = StandardScaler()
        nonscalingcolumns = [str_col for str_col in stores_master_df.columns if stores_master_df[str_col].dtypes == 'object']
        nonscalingcolumns = list(set(nonscalingcolumns) - set([self._storemstrmapping['partner_id']]))
        scale_cols = [item for item in compare_variables if item not in nonscalingcolumns]

        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(), "All population stores are actively participating in other test", False

        if len(scale_cols) > 0:
            scaler = scaler.fit(stores_master_df[scale_cols])

        teststores = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(
            teststores[self._tarvarmapping['partner_id']].unique())]

        # ELIMINATING THE TESTSTORES FROM POPULATION
        stores_master_df = stores_master_df[~(stores_master_df[self._storemstrmapping["partner_id"]].isin(
            teststores[self._storemstrmapping["partner_id"]]))]

        # IF Control Store Pool Available then filter for only those stores
        if control_store_pool is not None:
            stores_master_df = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(control_store_pool)]

        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(),"No valid control stores satisfying the criteria to proceed further.", False
        # Adding Additional Check for Req Control Stores
        if reqcontrolstores > stores_master_df[self._storemstrmapping["partner_id"]].nunique():
            reqcontrolstores = stores_master_df[self._storemstrmapping["partner_id"]].nunique()

        refA = teststores.copy(deep=True)
        refB = stores_master_df.copy(deep=True)

        useA = refA[compare_variables].copy(deep=True)
        useB = refB[compare_variables].copy(deep=True)

        if len(scale_cols) > 0:
            useA[scale_cols] = scaler.transform(useA[scale_cols])
            useB[scale_cols] = scaler.transform(useB[scale_cols])

        filter_columns = set(self._metadata['test_planning']["teststores_columns"])
        del annualrsvliftdf, valid_sales_stores
        # Vectorize implementation
        control_df = pd.DataFrame(columns=[self._storemstrmapping["partner_id"]],
                                    data=refB[self._storemstrmapping["partner_id"]].values)

        control_df['key'] = 1
        control_stores = self._prepare_test_control_stores_vecotrize(useA=useA,
                                                                useB=useB,
                                                                test_df=refA[[self._storemstrmapping["partner_id"]]],
                                                                control_df=control_df, calltype="new",
                                                                reqcontrolstores=reqcontrolstores,
                                                                corrbased=1)
        control_stores = control_stores.merge(refB[filter_columns], on=[self._storemstrmapping["partner_id"]])
        teststores_column_rename = ["Test_store_" + col for col in self._metadata['test_planning']["teststores_columns"]]
        teststores_df = refA[self._metadata['test_planning']["teststores_columns"]]
        teststores_df.columns = teststores_column_rename
        control_stores = control_stores.merge(teststores_df,
                                                on=['Test_store_' + self._storemstrmapping["partner_id"]])

        # Add CBU_Category Similarity Scores

        test_store_dict = dict(zip(refA[self._storemstrmapping["partner_id"]].values.tolist(
        ), range(0, refA[self._storemstrmapping["partner_id"]].nunique(), 1)))
        control_store_dict = dict(zip(refB[self._storemstrmapping["partner_id"]].values.tolist(
        ), range(0, refB[self._storemstrmapping["partner_id"]].nunique(), 1)))
        control_stores['Gower_Distance'] = control_stores['Gower_Distance'].round(2)
        if self._config["feature_parameter"]["is_product_present"] == 1:
            useA_cbu_category = refA[compare_variables_cbu_category].copy(
            deep=True)
            useB_cbu_category = refB[compare_variables_cbu_category].copy(
            deep=True)

            gowermatrix_cbu = gower_matrix(useA_cbu_category, useB_cbu_category)

            control_stores['Gower_Distance(CBU)'] = control_stores[['Test_store_'+self._storemstrmapping["partner_id"], self._storemstrmapping["partner_id"]]]\
                .apply(lambda x: gowermatrix_cbu[test_store_dict[x['Test_store_'+self._storemstrmapping["partner_id"]]]][control_store_dict[x[self._storemstrmapping["partner_id"]]]], axis=1)
            control_stores['Similarity_Measure(CBU)'] = 1 - \
                control_stores['Gower_Distance(CBU)']
            control_stores['Similarity_Difference'] = control_stores[
                "Similarity_Measure(CBU)"]-control_stores['Similarity_Measure']
            control_stores[['Gower_Distance(CBU)', 'Similarity_Measure(CBU)', 'Similarity_Difference']] = control_stores[['Gower_Distance(CBU)', 'Similarity_Measure(CBU)',
                                                                                                                            'Similarity_Difference']].round(2)
            control_stores.sort_values(
                by=['Similarity_Difference'], ascending=False, inplace=True)
        else:
            control_stores.sort_values(
                by=['Similarity_Measure'], ascending=False, inplace=True)
        control_stores = self._get_test_control_stores_correlation(dfA=refA.copy(deep=True),
                                                                dfB=refB.copy(
                                                                    deep=True),
                                                                test_control_stores=control_stores.copy(
                                                                    deep=True),
                                                                weekcolumns=weekcolumns,
                                                                num_cntrl_rejected=None,
                                                                corrbased=1, reqcontrolstores=reqcontrolstores)

        control_stores['Gower_Distance'] = control_stores['Gower_Distance'].round(2)
        control_stores['Similarity_Measure'] = control_stores['Similarity_Measure'].round(2)

        return control_stores, "Control stores are generated successfully!", True


    def test_control_similarity_measurement(self, test_control_pairs, prewindow_target_data, target_variable, postwindow_target_data):
        metrics_dict = {}

        test_stores_pre = test_control_pairs.merge(prewindow_target_data,
                                                    left_on=["Test_store_" + self._storemstrmapping["partner_id"],
                                                            "Test_store_" + self._storemstrmapping["banner"]],
                                                    right_on=[
                                                        self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]],
                                                    how="left")
        test_group_pre = test_stores_pre.groupby(self._tarvarmapping["week"])[
            target_variable].mean().reset_index().rename(
            columns={target_variable: 'Average_' + target_variable})
        test_group_pre['Window'] = 'Pre'
        test_group_pre['Group'] = 'Test'
        # test group postperiod weekly target data
        test_stores_post = test_control_pairs.merge(postwindow_target_data,
                                                    left_on=["Test_store_" + self._storemstrmapping["partner_id"],
                                                            "Test_store_" + self._storemstrmapping["banner"]],
                                                    right_on=[self._tarvarmapping["partner_id"],
                                                            self._tarvarmapping["banner"]],
                                                    how="left")
        test_group_post = test_stores_post.groupby(self._tarvarmapping["week"])[
            target_variable].mean().reset_index().rename(
            columns={target_variable: 'Average_' + target_variable})
        test_group_post['Window'] = 'Post'
        test_group_post['Group'] = 'Test'

        # control group preperiod weekly target data
        control_stores_pre = test_control_pairs.merge(prewindow_target_data,
                                                    left_on=[self._storemstrmapping["partner_id"],
                                                                self._storemstrmapping["banner"]],
                                                    right_on=[self._tarvarmapping["partner_id"],
                                                                self._tarvarmapping["banner"]],
                                                    how="left")
        control_group_pre = control_stores_pre.groupby(self._tarvarmapping["week"])[
            target_variable].mean().reset_index().rename(
            columns={target_variable: 'Average_' + target_variable})
        control_group_pre['Window'] = 'Pre'
        control_group_pre['Group'] = 'Control'

        # control group postperiod weekly target data
        control_stores_post = test_control_pairs.merge(postwindow_target_data,
                                                        left_on=[self._storemstrmapping["partner_id"],
                                                                self._storemstrmapping["banner"]],
                                                        right_on=[self._tarvarmapping["partner_id"],
                                                                self._tarvarmapping["banner"]],
                                                        how="left")
        control_group_post = control_stores_post.groupby(self._tarvarmapping["week"])[
            target_variable].mean().reset_index().rename(columns={target_variable: 'Average_' + target_variable})
        control_group_post['Window'] = 'Post'
        control_group_post['Group'] = 'Control'

        # Pre and post period test and control group averages
        combined_avg = pd.concat([test_group_pre, test_group_post, control_group_pre, control_group_post],
                                axis=0).reset_index(drop=True)
        combined_avg['Average_' + target_variable] = round(
            combined_avg['Average_' + target_variable], 2)
        combined_avg["Week"] = combined_avg["Week"].astype(int)
        combined_avg["Week"] = combined_avg["Week"].apply(
            lambda x: str(x)[:4] + " Week " + str('%02d' % int(str(x)[-2:])))
        # Average similarity & correlation
        testcontrolstores = test_control_pairs.copy(deep=True)
        avg_similarity = testcontrolstores['Similarity_Measure'].mean()
        avg_correlation = testcontrolstores['Correlation'].mean()
        metrics_dict["Avg_Similarity"] = str(round(avg_similarity, 2))
        metrics_dict["Avg_Correlation"] = str(round(avg_correlation, 2))
        return metrics_dict, combined_avg, "Calculated Successfully", True


    def recompute_control_stores_util(self, target_variable, reqcontrolstores, test_control_stores, stores_master_df, max_date_data_available, annualrsvliftdf, valid_sales_stores,
                                     consideryearweeks, compare_variables, include_cbu_features, business_categories):
        accepted = test_control_stores.groupby(
            "Test_store_"+self._storemstrmapping["partner_id"]).filter(lambda x: (x['Checked_Flag'] == 1).any())
        rejected = test_control_stores[~test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]].isin(
            accepted["Test_store_"+self._storemstrmapping["partner_id"]])]
        if rejected.shape[0] == 0:
            return pd.DataFrame(), "Please unselect all the control stores for a test store to recompute.", False
        rejected["is_recommended"]=0
        num_cntrl_rejected = rejected.groupby(
            "Test_store_"+self._storemstrmapping["partner_id"]).aggregate({self._storemstrmapping["partner_id"]:"nunique"}).reset_index()

        stores_master_df = self._store_object.filter_active_test_control_stores(stores_master_df=stores_master_df.copy(deep=True),
                                                                                         remove_type=self._config["feature_parameter"]["active_store_filter_type"],
                                                                                         max_week_data_available=max_date_data_available)


        stores_master_df = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(
            valid_sales_stores[self._tarvarmapping["partner_id"]].unique())]
        # -----------------------------------------------New code-------------------------------------------------------------
        # check
        filtered = valid_sales_stores[valid_sales_stores[self._tarvarmapping['week']].isin(consideryearweeks[:])]
        pivoteddf = pd.pivot_table(filtered, index=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]], columns=self._tarvarmapping['week'], values=target_variable).reset_index().rename_axis(None, axis=1)
        weekcolumns = [col for col in pivoteddf.columns.tolist() if col not in [self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]]]
        stores_master_df = stores_master_df.merge(pivoteddf, on=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]])
        # ------------------------------------------------New code-------------------------------------------------------------

        filter_columns = [self._tarvarmapping["partner_id"]] + [target_variable+' Year 1', target_variable+' Year 2', target_variable+' Lift']
        if self._config["feature_parameter"]["is_product_present"] == 1:
            filter_columns.extend(["CBU_Category_"+target_variable+' Year 1', "CBU_Category_"+target_variable+' Year 2',
                                                        "CBU_Category_"+target_variable+" Lift"])
            compare_variables_cbu_category = compare_variables.copy()
            compare_variables_cbu_category.extend(["CBU_Category_"+target_variable+' Year 1', "CBU_Category_"+target_variable+' Year 2',
                                            "CBU_Category_"+target_variable+" Lift"])

        if (len(business_categories)!=0) & (len(business_categories)<self._metadata['test_planning']["business_categories_count"]):
            common_category_specific = list(set(self._metadata['test_planning']["business_category_specific_compare"]) & set(compare_variables))
            if len(common_category_specific)>0:
                features_list = [[j+"_"+i for j in common_category_specific] for i in business_categories]
                category_specific_features = [item for elem in features_list for item in elem]
                compare_variables.extend(category_specific_features)
                compare_variables_cbu_category.extend(category_specific_features)

        stores_master_df = stores_master_df.merge(
            annualrsvliftdf[filter_columns], left_on=self._storemstrmapping["partner_id"], right_on=self._tarvarmapping["partner_id"])
        if include_cbu_features == 1:
            compare_variables.extend([target_variable+' Year 1', target_variable+" Year 2", target_variable+" Lift",
                                "CBU_Category_"+target_variable+' Year 1', "CBU_Category_"+target_variable+' Year 2',
                                "CBU_Category_"+target_variable+" Lift"])
        else:
            compare_variables.extend(
                [target_variable+' Year 1', target_variable+" Year 2", target_variable+" Lift"])
        # Scaling Store Features Column values on the Entire Population set
        scaler = StandardScaler()
        nonscalingcolumns = [str_col for str_col in stores_master_df.columns if stores_master_df[str_col].dtypes == 'object']
        nonscalingcolumns = list(set(nonscalingcolumns) - set([self._storemstrmapping['partner_id']]))

        scale_cols = [item for item in compare_variables if item not in nonscalingcolumns]
        if len(scale_cols) > 0:
            scaler = scaler.fit(stores_master_df[scale_cols])

        teststores = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(
            test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]].unique())]

        # ELIMINATING THE TESTSTORES FROM POPULATION
        stores_master_df = stores_master_df[~(stores_master_df[self._storemstrmapping["partner_id"]].isin(teststores[self._storemstrmapping["partner_id"]]))]


        refA = teststores.copy(deep=True)
        refB = stores_master_df.copy(deep=True)

        useA = refA[compare_variables].copy(deep=True)
        useB = refB[compare_variables].copy(deep=True)

        if len(scale_cols) > 0:
            useA[scale_cols] = scaler.transform(useA[scale_cols])
            useB[scale_cols] = scaler.transform(useB[scale_cols])

        gowermatrix = gower_matrix(useA, useB)
        rejected_with_control_left = {}
        # Filtering out Test stores which have no more control store left to be mapped
        teststores_with_exhausted_control = num_cntrl_rejected[num_cntrl_rejected[self._storemstrmapping["partner_id"]]+1 > refB.shape[0]].index.tolist()
        rejected.loc[~rejected["Test_store_"+self._storemstrmapping["partner_id"]].isin(teststores_with_exhausted_control), "is_recommended"] = 0
        num_cntrl_rejected = num_cntrl_rejected.to_dict()
        rejected_with_control_left = rejected[~rejected["Test_store_" +
                                                        self._storemstrmapping["partner_id"]].isin(teststores_with_exhausted_control)]
        if rejected_with_control_left.shape[0] == 0:
            return pd.DataFrame(),"All Control Stores are exhausted for all the Test stores"
        rejected_with_control_left = rejected_with_control_left.groupby(
            "Test_store_"+self._storemstrmapping["partner_id"])[self._storemstrmapping["partner_id"]].unique()
        rejected_with_control_left = rejected_with_control_left.to_dict()

        # Identifying similar stores
        filter_columns = self._metadata['test_planning']["teststores_columns"].copy()
        df_list = []
        for test_pid, row in zip(refA[self._storemstrmapping["partner_id"]], gowermatrix):
            if test_pid in rejected_with_control_left.keys():
                df_list.append(df_list.append(self.prepare_test_control_stores(dfA=refA[filter_columns].copy(deep=True),
                                                                        dfB=refB[filter_columns].copy(deep=True),
                                                                        teststoreid=test_pid, gowerdistances=row,
                                                                        num_cntrl_rejected=num_cntrl_rejected, calltype="new",
                                                                        rejected_with_control_left=rejected_with_control_left, corrbased=1,
                                                                        reqcontrolstores=reqcontrolstores)))

        control_stores = pd.concat(df_list)
        control_stores = control_stores[~control_stores["Test_store_" +
                                                        self._storemstrmapping["partner_id"]].isin(teststores_with_exhausted_control)]
        control_stores["Checked_Flag"] = 1
        control_stores["is_recommended"] = 1
        control_stores["test_id"] = self._test_id
        # Add CBU_Category Similarity Scores
        if self._config["feature_parameter"]["is_product_present"] == 1:
            useA_cbu_category = refA[compare_variables_cbu_category].copy(deep=True)
            useB_cbu_category = refB[compare_variables_cbu_category].copy(deep=True)
            gowermatrix_cbu = gower_matrix(useA_cbu_category, useB_cbu_category)
            test_store_dict = dict(zip(refA[self._storemstrmapping["partner_id"]].values.tolist(
            ), range(0, refA[self._storemstrmapping["partner_id"]].nunique(), 1)))
            control_store_dict = dict(zip(refB[self._storemstrmapping["partner_id"]].values.tolist(
            ), range(0, refB[self._storemstrmapping["partner_id"]].nunique(), 1)))
            control_stores['Gower_Distance(CBU)'] = control_stores[['Test_store_'+self._storemstrmapping["partner_id"], self._storemstrmapping["partner_id"]]]\
                .apply(lambda x: gowermatrix_cbu[test_store_dict[x['Test_store_'+self._storemstrmapping["partner_id"]]]][control_store_dict[x[self._storemstrmapping["partner_id"]]]], axis=1)
            control_stores['Similarity_Measure(CBU)'] = 1 - \
                control_stores['Gower_Distance(CBU)']
            control_stores['Similarity_Difference'] = control_stores[
                "Similarity_Measure(CBU)"] - control_stores['Similarity_Measure']
            control_stores[['Gower_Distance(CBU)', 'Similarity_Measure(CBU)', 'Similarity_Difference']] = control_stores[['Gower_Distance(CBU)', 'Similarity_Measure(CBU)',
                                                                                                                        'Similarity_Difference']].round(2)
            control_stores.sort_values(
                by=['Similarity_Difference'], ascending=False, inplace=True)

        control_stores = self._get_test_control_stores_correlation(dfA=refA.copy(deep=True), dfB=refB.copy(deep=True),
                                                            test_control_stores=control_stores.copy(
                                                                deep=True),
                                                            weekcolumns=weekcolumns, num_cntrl_rejected=num_cntrl_rejected, corrbased=1)

        control_stores = pd.concat([control_stores, rejected, accepted])
        return control_stores, "Successfully recomputed!!", True

    def control_summary_util(self, stores_master_df, test_control_mapping, summary_sales_weeks, consideryearweeks, weekly_target_sales, business_categories, compare_variables, target_variable)->Tuple[dict,dict,dict, str, bool]:
        # Create variables
        variables_metrics_dict = {}
        feature_thresholds_dict = {}
        feature_bounds_dict = {}
        test_stores = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(test_control_mapping["Test_store_"+self._storemstrmapping["partner_id"]])]
        control_stores = stores_master_df.merge(test_control_mapping[[self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]]], on=[
                                                self._storemstrmapping["partner_id"], self._storemstrmapping["banner"]])

        weeks = consideryearweeks[summary_sales_weeks:]
        weeklyrsvdatayear = weekly_target_sales[weekly_target_sales[self._tarvarmapping["week"]].isin(
            weeks)]
        weeklyrsvdatayear["Year"] = "Year1"
        # To Free Space
        del weekly_target_sales

        aggdict = {k: sum for k in [
            self._tarvarmapping['rsv'], self._tarvarmapping['volume']]}
        groupbycolumns = [self._tarvarmapping["partner_id"]] + \
            [self._tarvarmapping["banner"]]+[self._tarvarmapping['year']]
        annualrsvdatayear = weeklyrsvdatayear.groupby(
            groupbycolumns).agg(aggdict).reset_index()

        mergecolumns = [self._tarvarmapping["partner_id"]] + \
            [self._tarvarmapping['rsv'], self._tarvarmapping['volume']]
        test_stores = test_stores.merge(annualrsvdatayear[mergecolumns],
                                        left_on=self._storemstrmapping["partner_id"],
                                        right_on=self._tarvarmapping["partner_id"])
        control_stores = control_stores.merge(annualrsvdatayear[mergecolumns],
                                                left_on=self._storemstrmapping["partner_id"],
                                                right_on=self._tarvarmapping["partner_id"])



        if (len(business_categories)!=0) & (len(business_categories)<self._metadata['test_planning']["business_categories_count"]):
            common_category_specific = list(set(self._metadata['test_planning']["business_category_specific_compare"]) & set(compare_variables))
            if len(common_category_specific)>0:
                features_list = [[j+"_"+i for j in common_category_specific] for i in business_categories]
                category_specific_features = [item for elem in features_list for item in elem]
                compare_variables.extend(category_specific_features)
        compare_variables.append(target_variable)

        allstores = pd.concat([test_stores, control_stores])
        variable_features = allstores[compare_variables].nunique(
        )[allstores[compare_variables].nunique() > 1].index.to_list()
        compare_variables = list(
            set(compare_variables).intersection(variable_features))
        for col in compare_variables:
            if test_stores[col].dtype == 'object':
                pass
            variables_metrics_dict[col] = {}
            tStat, pVal = stats.ttest_ind(
                test_stores[col], control_stores[col], nan_policy='omit')

            variables_metrics_dict[col]["Test Mean"] = round(
                test_stores[col].mean(), 2)
            variables_metrics_dict[col]["Control Mean"] = round(
                control_stores[col].mean(), 2)
            variables_metrics_dict[col]["Test Std Dev"] = round(
                test_stores[col].std(), 2)
            variables_metrics_dict[col]["Control Std Dev"] = round(
                control_stores[col].std(), 2)

        xcols = [x for x in compare_variables if x != target_variable]
        X_train = allstores[xcols].values
        y_train = allstores[target_variable].values.ravel()

        X_train = sm.add_constant(X_train)
        model = sm.OLS(y_train, X_train)
        results = model.fit()

        summary_df = results.summary2().tables[1]
        summary_df.index = ['Constant'] + list(xcols)
        pvalue_dict = dict(
            zip(summary_df.index.values.tolist(), summary_df["P>|t|"].values.tolist()))

        # Calculate feature thresholds
        feature_thresholds_dict = self._get_feature_thresholds(
                                                                test_stores, control_stores, compare_variables)

        for key, value in feature_thresholds_dict.items():
            feature_bounds_dict[key] = [
                variables_metrics_dict[key]["Test Mean"]-value, variables_metrics_dict[key]["Test Mean"]+value]

        return variables_metrics_dict,feature_thresholds_dict,feature_bounds_dict, "Successfully calculated!!", True

    def test_control_upload_util(self, filtered_rsv_stores_df, valid_sales_stores, stores_master_df, consideryearweeks, target_variable, applicability_criteria, store_features, test_control_stores):

        store_features.extend([target_variable + " Year 1", target_variable + " Year 2", target_variable + " Lift"])
        store_features_cbu_category = store_features.copy()
        store_features_cbu_category.extend(
                                            ["CBU_Category_" + target_variable + ' Year 1',
                                            "CBU_Category_" + target_variable + ' Year 2',
                                            "CBU_Category_" + target_variable + " Lift"])
        tv = test_control_stores[test_control_stores["Test_store_"+self._storemstrmapping["partner_id"]].isin(filtered_rsv_stores_df[self._storemstrmapping["partner_id"]])]
        if len(tv) == 0:
            return pd.DataFrame(), "Test stores uploaded are not present in Store Master database", False

        # valid controlstores
        cv = test_control_stores[test_control_stores["Control_store_"+self._storemstrmapping["partner_id"]].isin(filtered_rsv_stores_df[self._storemstrmapping["partner_id"]])]
        if len(cv) == 0:
            return pd.DataFrame(), "Control stores uploaded are not present in Store Master database", False

        to_drop = tv[~tv["Control_store_"+self._storemstrmapping["partner_id"]].isin(cv["Control_store_"+self._storemstrmapping["partner_id"]])]
        # Final valid test-control pairs
        filtered_testcontrol_stores = tv[~tv.isin(to_drop)].dropna()
        #message = "No of test-control pairs satisfying the criteria to proceed further are {}".format(filtered_testcontrol_stores.shape[0])
        if filtered_testcontrol_stores.shape[0] == 0:
            message = "No test-control pairs satisfying the criteria to proceed further."
            return pd.DataFrame(), message, False

        filtered_testcontrol_stores['order'] = list(range(filtered_testcontrol_stores.shape[0]))

        filtered = valid_sales_stores[valid_sales_stores[self._tarvarmapping["week"]].isin(consideryearweeks[self._sales_object.get_summary_sales_weeks(applicability_criteria):])]
        pivoteddf = pd.pivot_table(filtered,
                                index=[self._storemstrmapping["partner_id"],
                                self._storemstrmapping["banner"]],
                                columns=self._tarvarmapping["week"],
                                values=target_variable).reset_index().rename_axis(None, axis=1)
        filtered_rsv_stores_df = filtered_rsv_stores_df.merge(pivoteddf, on=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]])
        scaler = StandardScaler()
        nonscalingcolumns = [str_col for str_col in stores_master_df.columns if stores_master_df[str_col].dtypes == 'object']
        nonscalingcolumns = list(set(nonscalingcolumns) - set([self._storemstrmapping['partner_id']]))

        scale_cols = [item for item in store_features if item not in nonscalingcolumns]
        if len(scale_cols) > 0:
            scaler = scaler.fit(filtered_rsv_stores_df[scale_cols])


        teststores = filtered_rsv_stores_df.merge(
                                                    filtered_testcontrol_stores,
                                                    left_on=self._storemstrmapping["partner_id"],
                                                    right_on='Test_store_'+self._storemstrmapping["partner_id"],
                                                    how='right')

        controlstores = filtered_rsv_stores_df.merge(
                                                    filtered_testcontrol_stores,
                                                    left_on=self._storemstrmapping["partner_id"],
                                                    right_on='Control_store_'+self._storemstrmapping["partner_id"],
                                                    how='right')
        controlstores = controlstores.set_index('order')
        controlstores = controlstores.reindex(index=teststores['order'])
        controlstores = controlstores.reset_index()

        # checks that the order of test-control pairs in both files matches

    # #     # Weekly sales for all stores for the past 1 year (52 weeks)

        cols = ["order", self._storemstrmapping['partner_id'], self._storemstrmapping['banner'], 'Test_store_' +
                self._storemstrmapping['partner_id'], 'Control_store_'+self._storemstrmapping['partner_id']]
        mergecols = [self._storemstrmapping['partner_id'], self._storemstrmapping['banner']]
        test_stores_wksales = teststores[cols].merge(pivoteddf, on=mergecols)
        control_stores_wksales = controlstores[cols].merge(pivoteddf, on=mergecols)
        control_stores_wksales = control_stores_wksales.set_index('order')
        control_stores_wksales = control_stores_wksales.reindex(index=test_stores_wksales['order'])
        control_stores_wksales = control_stores_wksales.reset_index()

        corrlist = []
        for j in range(controlstores.shape[0]):
            array1 = np.array(test_stores_wksales.loc[j, test_stores_wksales.columns[~test_stores_wksales.columns.isin(cols)]].astype(float))
            array2 = np.array(control_stores_wksales.loc[j, control_stores_wksales.columns[~control_stores_wksales.columns.isin(cols)]].astype(float))
            corrlist.append(round(pd.np.corrcoef(array1, array2)[0][1], 2))
        teststores["Correlation"] = corrlist
        # population stores after excluding teststores
        pop_stores = filtered_rsv_stores_df[~filtered_rsv_stores_df[self._storemstrmapping['partner_id']].isin(
            teststores['Test_store_'+self._storemstrmapping['partner_id']])]

        # Similarity Calculation
        refA = teststores.copy(deep=True)
        refB = pop_stores.copy(deep=True)
        useA = refA[store_features].copy(deep=True)
        useB = refB[store_features].copy(deep=True)
        if len(scale_cols) > 0:
            useA[scale_cols] = scaler.transform(useA[scale_cols])
            useB[scale_cols] = scaler.transform(useB[scale_cols])

        gowermatrix = gower_matrix(useA, useB)

        useA = refA[store_features_cbu_category].copy(deep=True)
        useB = refB[store_features_cbu_category].copy(deep=True)


        gowermatrix_cbu = gower_matrix(useA, useB)

        # Identifying similar stores
        df_list = list()

        for i in range(refA.shape[0]):

            teststoreid = refA[self._storemstrmapping["partner_id"]][i]
            gowerdistances = gowermatrix[i]
            gowerdistances_cbu = gowermatrix_cbu[i]
            dfA = refA.copy(deep=True)
            dfB = refB.copy(deep=True)

            dfB["Gower_Distance"] = list(gowerdistances)
            dfB["Gower_Distance(CBU)"] = list(gowerdistances_cbu)
            #dfB = dfB.sort_values(by="Gower_Distance",ascending=True)
            filteredteststoredf = dfA.loc[i,:].reset_index().T.reset_index(drop=True)
            filteredteststoredf.columns = filteredteststoredf.iloc[0, :]
            filteredteststoredf = filteredteststoredf.drop(0)
            filteredteststoredf = filteredteststoredf.reset_index(drop=True)

            for col in self._metadata['test_planning']["teststores_columns"]:
                dfB["Test_store_"+col] = filteredteststoredf[col].values[0]

            dfB["Gower_Distance"] = dfB["Gower_Distance"].apply(
                lambda x: round(x, 2))
            dfB["Similarity_Measure"] = dfB["Gower_Distance"].apply(lambda x: 1-x)
            dfB["Gower_Distance(CBU)"] = dfB["Gower_Distance(CBU)"].round(2)
            dfB["Similarity_Measure(CBU)"] = dfB["Gower_Distance(CBU)"].apply(
                lambda x: 1 - x)
            dfB["Similarity_Measure(CBU)"] = dfB["Similarity_Measure(CBU)"].round(
                2)
            dfB['Similarity_Difference'] = dfB['Similarity_Measure(CBU)'] - \
                dfB['Similarity_Measure']
            dfB['Similarity_Difference'] = dfB['Similarity_Difference'].round(2)
            df_append = dfB[dfB[self._storemstrmapping['partner_id']].values ==
                            filteredteststoredf['Control_store_'+self._storemstrmapping['partner_id']].values]
            df_append['Correlation'] = filteredteststoredf['Correlation'].values[0]
            df_list.append(df_append)
        control_test_pairs = pd.concat(df_list)
        control_test_pairs['Checked_Flag'] = 1
        return control_test_pairs, "Control stores computed Successfully", True