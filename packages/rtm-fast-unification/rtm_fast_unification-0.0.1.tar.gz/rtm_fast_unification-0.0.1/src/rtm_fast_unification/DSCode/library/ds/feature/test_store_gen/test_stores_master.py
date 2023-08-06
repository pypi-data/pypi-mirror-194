import math
from typing import Tuple

import numpy as np
import pandas as pd
import statsmodels.api as sm
from DSCode.library.ds_common_functions import gower_matrix
from scipy import stats
from sklearn.preprocessing import StandardScaler


class TestStoreSelectionFeature:
    def __init__(self, config, region,sales_object, store_object,test_id) -> None:
        self._config = config[region] if region in config else config
        self._sales_object = sales_object
        self._store_object = store_object
        self._metadata = self._config["metadata"]
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]
        self._test_id = test_id

    def data_extract(self, applicability_criteria, test_type, target_variable,
             uploaded_file_df=None)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame,pd.DataFrame, pd.DataFrame,list, str, bool]:
        test_master = self._store_object.read_test_master_table_by_test_ids(test_id=self._test_id)
        test_master = test_master[test_master['test_id'] == self._test_id]
        if test_master.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),[],\
                     """No records found for the current test in Test Master table!!""", False

        stores_master_df = self._store_object.filter_population(applicability_criteria=applicability_criteria,
                                                                uploaded_file_df = uploaded_file_df)# 5 seconds
        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),pd.DataFrame(),[], "No stores found in the population", False
        annualrsvlifts, valid_sales_stores, weekly_overall_sales, weekly_cbu_sales, consideryearweeks,\
                 message, success_flag = self._sales_object.get_annual_rsv_lifts(
                                        target_variable=target_variable,
                                        test_master_df = test_master,
                                        stores = list(stores_master_df[self._storemstrmapping["partner_id"]].unique()),
                                        applicability_criteria=applicability_criteria,
                                        test_type=test_type
                                    )
        if success_flag is False:
            return annualrsvlifts, valid_sales_stores, weekly_overall_sales, weekly_cbu_sales,  stores_master_df, test_master,consideryearweeks,\
                                    message, success_flag
        if annualrsvlifts.shape[0] == 0:
            return annualrsvlifts, valid_sales_stores,weekly_overall_sales, weekly_cbu_sales, stores_master_df,test_master,consideryearweeks,\
                            "No stores have valid sales for lift calculations!", False
        return annualrsvlifts,valid_sales_stores, weekly_overall_sales, weekly_cbu_sales, stores_master_df,test_master, consideryearweeks,\
             "Sales computed Successfully!", True

    # def data_extract(self, applicability_criteria, target_variable, prewindow_start, prewindow_end, postwindow_start, postwindow_end, test_type, uploaded_file_df=None, sales_week=None, sales_lifts_sales_weeks=None)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,list, str, bool]:
    #     stores_master_df = self._store_object.filter_population(applicability_criteria=applicability_criteria, uploaded_file_df = uploaded_file_df)
    #     if stores_master_df.shape[0] == 0:
    #         return pd.DataFrame(), pd.DataFrame(),pd.DataFrame(),[], "No stores found in the population", False
    #     annualrsvlifts, valid_sales_stores, consideryearweeks, message, success_flag = self._sales_object.get_annual_rsv_lifts(
    #                                                                             target_variable=target_variable,
    #                                                                             prewindow_start=prewindow_start,
    #                                                                             prewindow_end=prewindow_end,
    #                                                                             postwindow_start=postwindow_start,
    #                                                                             postwindow_end=postwindow_end,
    #                                                                             stores = list(stores_master_df[self._storemstrmapping["partner_id"]].unique()),
    #                                                                             applicability_criteria=applicability_criteria,
    #                                                                             test_type=test_type,
    #                                                                             sales_week = sales_week,
    #                                                                             sales_lifts_sales_weeks = sales_lifts_sales_weeks
    #                                                                         )
    #     if success_flag is False:
    #         return annualrsvlifts, valid_sales_stores, stores_master_df, consideryearweeks, message, success_flag
    #     if annualrsvlifts.shape[0] == 0:
    #         return annualrsvlifts, valid_sales_stores,stores_master_df,consideryearweeks, "No stores have valid sales for lift calculations!", False
    #     return annualrsvlifts, valid_sales_stores,stores_master_df,consideryearweeks, "Sales computed Successfully!", True

    def test_parameter_calculation(self, confidence_level, margin_of_error, num_of_teststores, standard_deviation, power_of_test = None)->Tuple[float, str, bool]:
        if power_of_test is None:
                power_of_test = self._metadata["test_configuration"]["power_of_test"]
        if confidence_level is None:
            value1 = num_of_teststores
            confidence_level = round(1 - 2*(1 - stats.norm.cdf(np.sqrt(value1/2) * (
                margin_of_error)/standard_deviation-stats.norm.ppf(power_of_test))), 2)

            test_parameter = confidence_level
            message = "Confidence level calculated successfully!!"

        if margin_of_error is None:

            value1 = num_of_teststores
            margin_of_error = round((stats.norm.ppf((1 - (1 - confidence_level) / 2))+stats.norm.ppf(
                power_of_test)) * standard_deviation / (np.sqrt(value1/2)), 2)

            test_parameter = margin_of_error
            message = "Margin of error calculated successfully!!"

        if num_of_teststores is None:

            value1 = 2 * np.power((stats.norm.ppf((1 - (1 - confidence_level) / 2))+stats.norm.ppf(
                self._metadata["test_configuration"]["power_of_test"])) * standard_deviation / (margin_of_error), 2)
            num_of_teststores = math.ceil(value1)
            if num_of_teststores < self._metadata["test_configuration"]["min_teststores"]:
                test_parameter = self._metadata["test_configuration"]["min_teststores"]
                message = "Calculated samplesize is less than {} (Minimum required samplesize).Hence we suggest 30 as the sample size.".format(self._metadata["test_configuration"]["min_teststores"])
            else:
                test_parameter = num_of_teststores
                message = "Number of stores calculated successfully!!"

        return test_parameter, message, True

    def test_store_identification(self, compare_variables, stratification_variable, filtered_population_sales,  population_sales, filtered_stores_df, num_of_teststores) -> Tuple[pd.DataFrame]:
        """Count number of stores need to be pciked from each Stratification condition"""
        first_stratification_output = filtered_stores_df.groupby(stratification_variable[0])[self._storemstrmapping["partner_id"]].count().reset_index().rename(columns={self._storemstrmapping["partner_id"]: "Count"})
        first_stratification_output["prop"] = first_stratification_output["Count"]/first_stratification_output["Count"].sum()
        first_stratification_output["stores_proportioned"] = first_stratification_output["prop"] * num_of_teststores
        first_stratification_output["stores_proportioned"] = first_stratification_output["stores_proportioned"].apply(lambda x: round(x))

        test = {'testStoresList': [], 'thresholdCount': []}
        teststores = pd.DataFrame()
        for iteration in list(range(0, self._metadata["test_planning"]["sampling_iterations"])):
            intermedeate_stores = pd.DataFrame()
            for stratification_value in filtered_population_sales[stratification_variable[0]].unique():
                banner_num_of_teststores = first_stratification_output[first_stratification_output[stratification_variable[0]]== stratification_value]["stores_proportioned"].values[0]
                banner_filter = (filtered_population_sales[stratification_variable[0]] == stratification_value)

                store_clusters = filtered_population_sales[banner_filter].groupby(stratification_variable[-1])[self._storemstrmapping["partner_id"]].count().reset_index()
                store_clusters["proportion"] = (store_clusters[self._storemstrmapping["partner_id"]]/store_clusters[self._storemstrmapping["partner_id"]].sum())
                store_clusters["stores_proportioned"] = store_clusters["proportion"] * \
                    banner_num_of_teststores
                store_clusters["stores_proportioned"] = store_clusters["stores_proportioned"].apply(lambda x: round(x))
                clusterwise_stores_dict = store_clusters.groupby(stratification_variable[-1])["stores_proportioned"].sum().to_dict()
                filtered_rsv_banner_filter = (filtered_population_sales[stratification_variable[0]] == stratification_value)
                banner_test_stores = filtered_population_sales[filtered_rsv_banner_filter].groupby(stratification_variable[-1]).apply(lambda x: x.sample(min(
                    clusterwise_stores_dict[x.name], filtered_population_sales[filtered_population_sales[stratification_variable[0]] == stratification_value][self._storemstrmapping["partner_id"]].nunique()), replace=False)).reset_index(drop=True)

                intermedeate_stores = intermedeate_stores.append(banner_test_stores)
            """Validate the sample with similarity columns to decide which batch is best"""
            threshold_count = self.validate_test_stores(sample_stores_sales=intermedeate_stores,
                                                        compare_variables = compare_variables,
                                                        population_stores_sales=population_sales)
            test['testStoresList'].append(intermedeate_stores)
            test['thresholdCount'].append(threshold_count)
        teststores = test['testStoresList'][test['thresholdCount'].index(max(test['thresholdCount']))]
        teststores["is_teststore"] = 1
        stores_otherthan_teststores = filtered_population_sales[~filtered_population_sales[self._storemstrmapping["partner_id"]].isin(
            teststores[self._storemstrmapping["partner_id"]])]
        stores_otherthan_teststores["is_teststore"] = 0
        teststores = pd.concat([teststores, stores_otherthan_teststores])
        return teststores

    def validate_test_stores(self, sample_stores_sales, compare_variables, population_stores_sales)->Tuple[int]:
        """
            validate_test_stores
        """
        # This function returns the count of features satisfying the pvalue criteria - No uk specific code in the function

        if not (sample_stores_sales is not None) & (len(compare_variables) != 0):
            return 0
        # Pvalue count
        count = 0

        """Create threshold dict for all variables used to similarity check"""

        variables_thresholds_dict = {k: self._metadata["test_planning"]["test_vs_population_pvalue"] for k in compare_variables}


        for col in compare_variables:
            test_stores_col = sample_stores_sales[col].copy()
            stores_master_df_col = population_stores_sales[col].copy()
            if test_stores_col.dtype == 'object':
                catagorical_values = population_stores_sales[col].unique()
                observed = []
                expected = []
                for value in catagorical_values:
                    expected.append(
                        population_stores_sales[population_stores_sales[col] == value][col].count())
                    observed.append(
                        sample_stores_sales[sample_stores_sales[col] == value][col].count())

                _, pVal, _, _ = stats.chi2_contingency(
                    [expected, observed])
                pVal = round(pVal, 2)
                if pVal >= 0.50:
                    count += 1
            else:
                tStat, pVal = stats.ttest_ind(
                    test_stores_col, stores_master_df_col, nan_policy='omit')
                pVal = round(pVal, 2)
                if pVal >= variables_thresholds_dict[col]:
                    count += 1

        return count

    #Store attributes, sales --> range of column
    def test_population_mapping_util(self, teststores, stores_master_df, valid_stores_sales, compare_variables, consideryearweeks, summary_sales_weeks, target_variable)->Tuple[pd.DataFrame]:
        scaler = StandardScaler()
        nonscalingcolumns = [str_col for str_col in stores_master_df.columns if stores_master_df[str_col].dtypes == 'object']
        nonscalingcolumns = list(set(nonscalingcolumns) - set([self._storemstrmapping['partner_id']]))
        print("compare variables {}".format(compare_variables))
        scale_cols = [item for item in compare_variables if item not in nonscalingcolumns]

        print(stores_master_df.columns)
        if len(scale_cols) > 0:
            scaler = scaler.fit(stores_master_df[scale_cols])

        for col in scale_cols:
            if stores_master_df[col].dtypes == 'object':
                check_if_categorical_data = True
            else:
                check_if_categorical_data = False

        teststores = stores_master_df[stores_master_df[self._storemstrmapping["partner_id"]].isin(teststores[self._storemstrmapping["partner_id"]].unique())]
        # ELIMINATING THE TESTSTORES FROM POPULATION
        stores_master_df = stores_master_df[~(stores_master_df[self._storemstrmapping["partner_id"]].isin(teststores[self._storemstrmapping["partner_id"]]))]
        # Weekly sales for all stores for the past 1 year (52 weeks)
        week_values = consideryearweeks[summary_sales_weeks:]
        filtered_week_sales = valid_stores_sales[valid_stores_sales[self._tarvarmapping["week"]].isin(week_values)]
        pivoteddf = pd.pivot_table(filtered_week_sales, index=[self._tarvarmapping["partner_id"], self._tarvarmapping["banner"]],
                                columns=self._tarvarmapping["week"], values=target_variable).reset_index().rename_axis(None, axis=1)
        pivoteddf.columns = [self._tarvarmapping["partner_id"],
                            self._tarvarmapping["banner"]] + week_values
        mergecols = [self._storemstrmapping['partner_id'],
                    self._storemstrmapping['banner']]

        store_master_wksales = stores_master_df[mergecols].merge(pivoteddf, on=mergecols)
        test_stores_wksales = teststores[mergecols].merge(pivoteddf, on=mergecols)
        store_master_wksales_avg = store_master_wksales[week_values].mean().values

        # Sales Correlation between the weekly sales for each test store & the average weekly sales for all the population stores
        test_stores_week_sales_values = test_stores_wksales[week_values].values
        population_stores_week_sales_values = store_master_wksales_avg
        upper = np.sum(
            (test_stores_week_sales_values - np.mean(test_stores_week_sales_values, axis=1)[:, None]) * (population_stores_week_sales_values - np.mean(population_stores_week_sales_values)), axis=1)
        lower = np.sqrt(np.sum(np.power(
            test_stores_week_sales_values - np.mean(test_stores_week_sales_values, axis=1)[:, None], 2), axis=1) * np.sum(np.power(population_stores_week_sales_values - np.mean(population_stores_week_sales_values), 2)))
        corrlist = upper / lower
        teststores["Correlation"] = np.round(corrlist, 2)

        # Similarity Measure Calculations
        refA = teststores.copy(deep=True)
        refB = stores_master_df.copy(deep=True)

        useA = refA[compare_variables].copy(deep=True)
        useB = refB[compare_variables].copy(deep=True)

        if len(scale_cols) > 0:
            useA[scale_cols] = scaler.transform(useA[scale_cols])
            useB[scale_cols] = scaler.transform(useB[scale_cols])

        pop_summary = useB.describe(include='all')
        if check_if_categorical_data is True:
            pop_summary = pop_summary.loc['top'].combine_first(
                pop_summary.loc['mean']).reset_index().T.reset_index(drop=True)
        else:
            pop_summary = pop_summary.loc['mean'].reset_index().T.reset_index(drop=True)
        pop_summary.columns = pop_summary.iloc[0, :]
        pop_summary = pop_summary.drop(0)
        pop_summary = pop_summary.reset_index(drop=True)

        gowermatrix = gower_matrix(useA, pop_summary)

        refA["Gower_Distance"] = [i[0] for i in gowermatrix]
        refA = refA.sort_values(by="Gower_Distance", ascending=True)
        refA["Gower_Distance"] = refA["Gower_Distance"].apply(
            lambda x: round(x, 2))
        refA["Similarity_Measure"] = refA["Gower_Distance"].apply(
            lambda x: round(1-x, 2))
        # "needs to be removed from the production code"
        refA = refA.dropna(subset=['Correlation'])
        return refA

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

    def test_store_summary_util(self, weekly_rsv_sales, population_stores, test_stores,compare_variables, target_variable)->Tuple[dict, dict, dict]:
        variables_metrics_dict = {}
        feature_bounds_dict = {}
        pvalue_dict = {}
        aggdict = {k: sum for k in [self._tarvarmapping["rsv"], self._tarvarmapping["volume"]]}
        groupbycolumns = [self._tarvarmapping["partner_id"]] + [self._tarvarmapping["banner"]]+[self._tarvarmapping['year']]
        annualrsvdatayear = weekly_rsv_sales.groupby(groupbycolumns).agg(aggdict).reset_index()

        mergecolumns = [self._tarvarmapping["partner_id"]] + [self._tarvarmapping["rsv"], self._tarvarmapping["volume"]]
        population_stores = population_stores.merge(annualrsvdatayear[mergecolumns],
                                                left_on=self._storemstrmapping["partner_id"],
                                                right_on=self._tarvarmapping["partner_id"])

        test_stores = population_stores[population_stores[self._storemstrmapping["partner_id"]].isin(
            list(test_stores[self._storemstrmapping["partner_id"]].unique()))]

        compare_variables.append(target_variable)
        variables_metrics_dict = {}
        feature_thresholds_dict = {}
        feature_bounds_dict = {}
        for col in compare_variables:
            if test_stores[col].dtype == 'object':
                continue
            variables_metrics_dict[col] = {}

            # tStat, pVal = stats.ttest_ind(test_stores[col], population_stores[col], nan_policy='omit')

            variables_metrics_dict[col]["Test Mean"] = round(
                test_stores[col].mean(), 2)
            variables_metrics_dict[col]["Population Mean"] = round(
                population_stores[col].mean(), 2)
            variables_metrics_dict[col]["Test Std Dev"] = round(
                test_stores[col].std(), 2)
            variables_metrics_dict[col]["Population Std Dev"] = round(
                population_stores[col].std(), 2)

        # Get banner wise no of stores
        variables_metrics_dict["Test stores split"] = test_stores.groupby([self._storemstrmapping["banner"]])[self._storemstrmapping["partner_id"]].count().to_dict()

        modelstores = population_stores[population_stores[self._storemstrmapping["partner_id"]].isin(test_stores[self._storemstrmapping["partner_id"]].unique())]

        variable_features = modelstores[compare_variables].nunique(
        )[modelstores[compare_variables].nunique() > 1].index.to_list()
        compare_variables = list(
            set(compare_variables).intersection(variable_features))
        xcols = [x for x in compare_variables if x != target_variable]
        X_train = modelstores[xcols].values
        y_train = modelstores[target_variable].values.ravel()

        X_train = sm.add_constant(X_train)
        model = sm.OLS(y_train, X_train)
        results = model.fit()

        summary_df = results.summary2().tables[1]
        summary_df.index = ['Constant'] + list(xcols)
        pvalue_dict = dict(
            zip(summary_df.index.values.tolist(), summary_df["P>|t|"].values.tolist()))

        # Calculate feature thresholds
        feature_thresholds_dict = self._get_feature_thresholds(teststores=test_stores, controlstores=population_stores, features=compare_variables)
        for key, value in feature_thresholds_dict.items():
            feature_bounds_dict[key] = [variables_metrics_dict[key]["Population Mean"] -
                                        value, variables_metrics_dict[key]["Population Mean"]+value]
        return variables_metrics_dict, feature_bounds_dict, pvalue_dict


    def test_store_comparison_summary_util(self, test_stores, prewindow_target_data, target_variable, postwindow_target_data, population_stores)->Tuple[pd.DataFrame, dict, str , bool]:
        # test group preperiod weekly target data
        if 'Similarity_Measure' not in test_stores.columns:
            return pd.DataFrame(), dict(), \
                "Please pass similarity measure!!! Test stores passed doesnt have similarity measure column in it" ,\
                    True
        metrics_dict = {}
        test_stores_pre = test_stores.merge(prewindow_target_data,
                                            left_on=[self._storemstrmapping["partner_id"],
                                                     self._storemstrmapping["banner"]],
                                            right_on=[self._tarvarmapping["partner_id"],
                                                    self._tarvarmapping["banner"]],
                                            how="left")
        test_group_pre = test_stores_pre.groupby(self._tarvarmapping["week"])\
                                                    [target_variable]\
                                                    .mean()\
                                                    .reset_index()\
                                                    .rename(columns={target_variable: 'Average_'+target_variable})
        test_group_pre['Window'] = 'Pre'
        test_group_pre['Group'] = 'Test'

        # test group postperiod weekly target data
        test_stores_post = test_stores.merge(postwindow_target_data,
                                            left_on=[self._storemstrmapping["partner_id"],
                                                    self._storemstrmapping["banner"]],
                                            right_on=[self._tarvarmapping["partner_id"],
                                                    self._tarvarmapping["banner"]],
                                            how="left")
        test_group_post = test_stores_post.groupby(self._tarvarmapping["week"])\
                                                    [target_variable]\
                                                    .mean()\
                                                    .reset_index()\
                                                    .rename(columns={target_variable: 'Average_'+target_variable})
        test_group_post['Window'] = 'Post'
        test_group_post['Group'] = 'Test'

        # control group preperiod weekly target data
        pop_stores_pre = population_stores.merge(prewindow_target_data,
                                                left_on=[self._storemstrmapping["partner_id"],
                                                        self._storemstrmapping["banner"]],
                                                right_on=[self._tarvarmapping["partner_id"],
                                                         self._tarvarmapping["banner"]],
                                                how="left")
        pop_group_pre = pop_stores_pre.groupby(self._tarvarmapping["week"])\
                                    [target_variable]\
                                    .mean()\
                                    .reset_index()\
                                    .rename(columns={target_variable: 'Average_'+target_variable})
        pop_group_pre['Window'] = 'Pre'
        pop_group_pre['Group'] = 'Population'

        # control group postperiod weekly target data
        pop_stores_post = population_stores.merge(postwindow_target_data,
                                                left_on=[self._storemstrmapping["partner_id"],
                                                             self._storemstrmapping["banner"]],
                                                right_on=[self._tarvarmapping["partner_id"],
                                                         self._tarvarmapping["banner"]],
                                                how="left")
        pop_group_post = pop_stores_post.groupby(self._tarvarmapping["week"])[target_variable].mean(
        ).reset_index().rename(columns={target_variable: 'Average_'+target_variable})
        pop_group_post['Window'] = 'Post'
        pop_group_post['Group'] = 'Population'

        # Pre and post period test and control group averages
        combined_avg = pd.concat([test_group_pre, test_group_post,
                                pop_group_pre, pop_group_post], axis=0).reset_index(drop=True)
        combined_avg['Average_' +
                    target_variable] = round(combined_avg['Average_'+target_variable], 2)
        combined_avg["Week"] = combined_avg["Week"].astype(int)
        combined_avg["Week"] = combined_avg["Week"].apply(
            lambda x: str(x)[:4] + " Week " + str('%02d' % int(str(x)[-2:])))
        # Average similarity & correlation
        avg_similarity = test_stores['Similarity_Measure'].mean()
        avg_correlation = test_stores['Correlation'].mean()

        metrics_dict["Avg_Similarity"] = avg_similarity
        metrics_dict["Avg_Correlation"] = avg_correlation
        return combined_avg, metrics_dict, "Calculated Successfully!!" , True
