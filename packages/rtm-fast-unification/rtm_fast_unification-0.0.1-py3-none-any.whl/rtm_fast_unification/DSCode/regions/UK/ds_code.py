"""
    About module: All customizations done for UK market wrt FastTool functions
    Classes:
        FastToolUK
"""
from datetime import datetime
from typing import Tuple

import pandas as pd
from DSCode.library.ds_code_test_plan import FastTool


class FastToolUK(FastTool):
    """
    A class to represent features of FastToolUK.

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
    def __init__(self, config, region,  test_id):
        super().__init__(config=config, region=region, test_id=test_id)

    def calculate_rsv_estimate(self, target_variable, timeframestart, timeframeend, storelist,\
         applicability_criteria, uploaded_file_df=None) -> Tuple[float, int, str, bool]:
        if "Customer_Status" not in applicability_criteria:
            return -1, -1, "Customer_Status not passed!!", False
        applicability_criteria['test_type'] = None

        rsvestimate, store_count, message, flag = super().calculate_rsv_estimate(
            target_variable = target_variable,
            timeframestart=timeframestart,
            timeframeend=timeframeend,
            storelist=storelist,
            applicability_criteria=applicability_criteria,
            uploaded_file_df=uploaded_file_df)
        return rsvestimate, store_count, message, flag

    def get_breakeven_lift(self, rsv_estimate, cost, applicability_criteria,\
                num_of_teststores, uploaded_file_df=None) -> Tuple[float, str, bool]:
        if "Customer_Status" not in applicability_criteria:
            return -1, "Customer_Status not passed!!", False

        applicability_criteria['test_type'] = None
        return super().get_breakeven_lift(rsv_estimate=rsv_estimate,
                                        cost=cost,
                                        applicability_criteria = applicability_criteria,
                                        num_of_teststores=num_of_teststores,
                                        uploaded_file_df=uploaded_file_df)

    def get_test_parameter(self, confidence_level, margin_of_error,\
         num_of_teststores, target_variable, test_type, \
            applicability_criteria, uploaded_file_df=None) -> Tuple[float, str, bool]:
        test_type = None
        if "Customer_Status" not in applicability_criteria:
            applicability_criteria['Customer_Status'] = ['Active']
        applicability_criteria['test_type'] = test_type
        test_parameter, message, success_flag = super().get_test_parameter(
                                                confidence_level = confidence_level,
                                                margin_of_error = margin_of_error,
                                                num_of_teststores = num_of_teststores,
                                                target_variable = target_variable,
                                                test_type = test_type,
                                                applicability_criteria = applicability_criteria,
                                                uploaded_file_df = uploaded_file_df)
        return test_parameter, message, success_flag

    def power_marginoferror_calculation(self, num_of_teststores, target_variable, test_type, \
            applicability_criteria, uploaded_file_df=None) -> Tuple[float, float, float, str, bool]:
        if "Customer_Status" not in applicability_criteria:
            return -1, -1, -1, 'Customer_Status not passed!!', False

        test_type = None
        applicability_criteria['test_type'] = None
        return super().power_marginoferror_calculation(
            num_of_teststores=num_of_teststores,
            target_variable=target_variable,
            test_type = test_type,
            applicability_criteria = applicability_criteria,
            uploaded_file_df = uploaded_file_df)

    def teststores_sample_size(self, margin_of_error, target_variable,\
         test_type, applicability_criteria, uploaded_file_df=None)\
             -> Tuple[float, float, str, bool]:

        if "Customer_Status" not in applicability_criteria:
            return -1, -1, 'Customer_Status not passed!!', False
        test_type = None
        applicability_criteria['test_type'] = None
        return super().teststores_sample_size(margin_of_error=margin_of_error,
                                            target_variable = target_variable,
                                            test_type = test_type,
                                            applicability_criteria = applicability_criteria,
                                            uploaded_file_df = uploaded_file_df)

    def _calculate_sales_imputation_values(self, \
            valid_sales_stores_imputed)->Tuple[pd.DataFrame, pd.DataFrame]:
        number_of_weeks_imputed_dict = dict()
        number_of_complete_week_dict = dict()
        store_identifier = self._storemstrmapping['partner_id']
        for store_number in valid_sales_stores_imputed[store_identifier].unique():
            sales_filter = valid_sales_stores_imputed[store_identifier] == store_number
            store_records = valid_sales_stores_imputed[sales_filter]

            number_of_weeks_imputed_dict[store_number] = \
                                int(store_records[store_records['imputed'] == 1].shape[0])
            number_of_complete_week_dict[store_number] = \
                                int(round(store_records[store_records['imputed'] == 0]\
                                        .shape[0]/store_records.shape[0], 2))
        df_no_of_store_imputed = pd.DataFrame(
                                        {'Customer_Number': number_of_weeks_imputed_dict.keys(),
                                        'No_of_weeks_imputed_Test_Store': \
                                            number_of_weeks_imputed_dict.values()
                                        })
        df_data_completeness = pd.DataFrame(
                                        {"Customer_Number": number_of_complete_week_dict.keys(),
                                        "Data_Completeness_Test_Store": \
                                                number_of_complete_week_dict.values()
                                        })

        return df_no_of_store_imputed, df_data_completeness


    def identify_test_stores(self, num_of_teststores, target_variable, test_type,\
         applicability_criteria, stratification_variables, uploaded_file_df=None) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,\
                 pd.DataFrame, pd.DataFrame, list, str, bool]:

        if "Customer_Status" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 pd.DataFrame(), list(), 'Customer_Status not passed!!', False
        if test_type == 'RTM Impact Test':
            applicability_criteria['test_type'] = 'RTM Impact Test'
            # """Get sales, stores and lift values"""
            annualrsvlifts, valid_sales_stores, _, _,stores_master_df, _,\
            consideryearweeks, message1, success_flag = self._test_stores_features\
                            .data_extract(applicability_criteria=applicability_criteria,
                                            test_type = test_type,
                                            target_variable = target_variable,
                                            uploaded_file_df = uploaded_file_df)
            if success_flag is False:
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                            pd.DataFrame(), list(), message1, False
            #"""Filter annual rsv lift for stores with valid sales only"""

            store_identifier = self._tarvarmapping['partner_id']
            annualrsvlifts = annualrsvlifts[annualrsvlifts[store_identifier]\
                                            .isin(stores_master_df[store_identifier].unique())]

            filtercolumns = [self._tarvarmapping["partner_id"], \
                            self._tarvarmapping['rsv'] + ' Year 2']
            # """Merge stores master with annual rsv lifts"""
            filtered_rsv_stores_df = stores_master_df\
                                .merge(annualrsvlifts[filtercolumns],
                                        left_on=self._storemstrmapping["partner_id"],
                                        right_on=self._tarvarmapping["partner_id"])

            if filtered_rsv_stores_df.shape[0] == 0:
                return pd.DataFrame(), stores_master_df, annualrsvlifts, valid_sales_stores, \
                        pd.DataFrame(), consideryearweeks,\
                    "No store with Customer Status Active has valid sales", False
            # """rename columns"""
            filtered_rsv_stores_df.rename(columns={
                                    self._tarvarmapping['rsv']+' Year 2':self._tarvarmapping['rsv']
                                    },
                                    inplace=True)
            # """all stores that have customer status as Active and have valid
            #  sales are considered as test stores"""
            filtered_rsv_stores_df["is_teststore"] = 1
            valid_sales_stores_imputed = valid_sales_stores[
                                    valid_sales_stores[self._storemstrmapping['week']]\
                                        .isin(consideryearweeks[0:])
                                    ]

            df_no_of_store_imputed, df_data_completeness = self\
                                ._calculate_sales_imputation_values(valid_sales_stores_imputed)
            filtered_rsv_stores_df = filtered_rsv_stores_df\
                                            .merge(df_no_of_store_imputed,
                                                on=self._storemstrmapping['partner_id'])
            filtered_rsv_stores_df = filtered_rsv_stores_df\
                                            .merge(df_data_completeness,
                                                on=self._storemstrmapping['partner_id'])

            return filtered_rsv_stores_df, stores_master_df, annualrsvlifts, valid_sales_stores, \
             pd.DataFrame(), consideryearweeks,"Test store identified successfully!!", True

        applicability_criteria['test_type'] = None
        teststores, stores_master_df, annualrsvlifts, valid_sales_stores,\
        weekly_target_variables_file, consideryearweeks,\
            message, success_flag = super().identify_test_stores(
                                        num_of_teststores = num_of_teststores,
                                        target_variable = target_variable,
                                        test_type = test_type,
                                        applicability_criteria = applicability_criteria,
                                        stratification_variables = stratification_variables,
                                        uploaded_file_df = uploaded_file_df)

        if success_flag is False:
            return teststores, stores_master_df, annualrsvlifts, valid_sales_stores, \
                    weekly_target_variables_file, consideryearweeks, message, True
        valid_sales_stores_imputed = valid_sales_stores[valid_sales_stores[
                                self._tarvarmapping['week']].isin(consideryearweeks[52:])]

        df_no_of_store_imputed, df_data_completeness = self\
            ._calculate_sales_imputation_values(valid_sales_stores_imputed)
        teststores = teststores.merge(df_no_of_store_imputed,
                                        on=self._storemstrmapping['partner_id'])
        teststores = teststores.merge(df_data_completeness,
                                        on=self._storemstrmapping['partner_id'])

        return teststores, stores_master_df, annualrsvlifts, valid_sales_stores, \
            weekly_target_variables_file, consideryearweeks, message, True

    def test_population_mapping(self, teststores, target_variable, test_type,\
                applicability_criteria, uploaded_file_df=None) -> Tuple[pd.DataFrame, str, bool]:
        test_type = None
        applicability_criteria['test_type'] = None
        return super().test_population_mapping(teststores = teststores,
                                            target_variable = target_variable,
                                            test_type = test_type,
                                            applicability_criteria = applicability_criteria,
                                            uploaded_file_df = uploaded_file_df)



    def test_store_summary(self, teststores, target_variable, test_type,\
         applicability_criteria, uploaded_file_df=None) -> Tuple[dict, dict, dict, str, bool]:
        '''
        # This function corresponds to the test vs population summary module
        # in the tool - No uk specific code in it
        '''
        if teststores is None or teststores.shape[0] == 0:
            return dict(), dict(), dict(), "Please pass test stores to the function", False

        sales_week = self._sales_object.get_sales_weeks(applicability_criteria)

        summary_sales_weeks = self._sales_object.get_summary_sales_weeks(applicability_criteria)
        compare_variables = self._get_test_vs_population_compare_sum(applicability_criteria)

        if "Customer_Status" not in applicability_criteria:
            return dict(), dict(), dict(), "Customer Status not passed!!", False

        applicability_criteria['test_type'] = test_type

        stores_master_df = self._store_object.filter_population(
            uploaded_file_df=uploaded_file_df,
            applicability_criteria=applicability_criteria)

        if stores_master_df.shape[0] == 0:
            return dict(), dict(), dict(), "No stores found in the population", False
        test_master_df = self._store_object\
                    .read_test_master_table_by_test_ids(test_id = self._test_id)

        if test_type == 'RTM Impact Test':
            prewindow_start =datetime.strptime(test_master_df['pre_start'].values[0],
                                            '%Y-%m-%d').date()
            prewindow_end = datetime.strptime(test_master_df['pre_start'].values[0],
                                            '%Y-%m-%d').date()
            consideryearweeks = self._sales_object\
                                .find_weeks(prewindow_start,
                                           prewindow_end)
        else:
            consideryearweeks = []
        store_identifier = self._storemstrmapping['partner_id']
        weekly_target_variables_file, consideryearweeks, message, success_flag = self._sales_object\
            .get_total_weekly_target_data(
                    test_master_df = test_master_df,
                    stores_list = list(stores_master_df[store_identifier].unique()),
                    sales_week = sales_week,
                    target_variable = target_variable,
                    applicability_criteria = applicability_criteria,
                    test_type = test_type,
                    consideryearweeks = consideryearweeks)

        if success_flag is False:
            return dict(), dict(), dict(), message, False
        weeks = consideryearweeks[summary_sales_weeks:]

        week_filter = weekly_target_variables_file[self._tarvarmapping["week"]].isin(weeks)
        weeklyrsvdatayear = weekly_target_variables_file[week_filter]
        weeklyrsvdatayear[self._tarvarmapping['year']] = "Year1"
        # To Free Space
        variables_metrics_dict, feature_bounds_dict, pvalue_dict = self._test_stores_features\
            .test_store_summary_util(weekly_rsv_sales=weeklyrsvdatayear,
                                                    population_stores=stores_master_df,
                                                    test_stores=teststores,
                                                    compare_variables=compare_variables,
                                                    target_variable=target_variable)
        return variables_metrics_dict, feature_bounds_dict, pvalue_dict,\
                     "Successfully Calculated!!", True

    def test_store_comparison_summary(self, test_stores, target_variable, test_type,\
         applicability_criteria,uploaded_file_df=None) \
                    -> Tuple[pd.DataFrame, dict, str, bool]:
        if "Customer_Status" not in applicability_criteria:
            return pd.DataFrame(), dict(), "Please pass the Customer Status", False
        test_type = None
        applicability_criteria['test_type'] = None
        return super().test_store_comparison_summary(test_stores,
                                                        target_variable,
                                                        test_type,
                                                        applicability_criteria,\
                                                        uploaded_file_df)

    def test_stores_format_check(self, target_variable, num_of_teststores, test_type,\
         applicability_criteria, teststores_data, uploaded_file_df=None) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, int, bool]:

        if 'Customer_Status' not in applicability_criteria:
            applicability_criteria['Customer_Status'] = 'Active'
        if test_type == "RTM Impact Test":
            applicability_criteria["bypass_active_test_control"] = 1
        applicability_criteria['test_type'] = test_type
        teststores,annualrsvlifts,valid_sales_stores,consideryearweeks,message,\
            num_of_teststores,success_flag = super().test_stores_format_check(target_variable = target_variable,
                                                                    num_of_teststores = num_of_teststores,
                                                                    test_type = test_type,
                                                                    applicability_criteria = applicability_criteria,
                                                                    teststores_data = teststores_data,
                                                                    uploaded_file_df = uploaded_file_df)
        if success_flag is True:
            # Imputation check
            if test_type == "RTM Impact Test":
                weeks = consideryearweeks[0]
            else:
                weeks = consideryearweeks[52:]
            valid_sales_stores_imputed = valid_sales_stores[valid_sales_stores[\
                self._tarvarmapping["week"]].isin(weeks)]
            df_no_of_store_imputed,df_data_completeness = \
                self._calculate_sales_imputation_values(valid_sales_stores_imputed)
            teststores = pd.merge(teststores,
                                df_no_of_store_imputed,
                                on=self._storemstrmapping["partner_id"])
            teststores = pd.merge(teststores,df_data_completeness,
                                on=self._storemstrmapping["partner_id"])
        return (
                teststores,
                annualrsvlifts,
                valid_sales_stores,
                consideryearweeks,
                message,
                num_of_teststores,
                success_flag,
            )

    def manual_teststores_selection(
        self,
        test_type,
        target_variable,
        applicability_criteria,
        uploaded_file_df=None,
    ) -> Tuple[
        pd.DataFrame, pd.DataFrame, list, int, float, float, float, str, bool
    ]:

        if "Customer_Status" not in applicability_criteria:
            applicability_criteria["Customer_Status"] = "Active"
        if test_type == "RTM Impact Test":
            applicability_criteria["bypass_active_test_control"] = 1
        # to handle the test type check in filter population
        applicability_criteria['test_type'] = test_type
        teststores,valid_sales_stores,consideryearweeks,num_of_teststores\
            ,margin_of_error,confidence_interval,power_of_test,message,success_flag = \
                super().manual_teststores_selection(test_type=test_type,target_variable=target_variable,\
                    applicability_criteria=applicability_criteria.copy(),uploaded_file_df=uploaded_file_df)
        if success_flag is True:
            # Imputation check
            if test_type == "RTM Impact Test":
                weeks = consideryearweeks[0]
            else:
                weeks = consideryearweeks[52:]
            valid_sales_stores_imputed = valid_sales_stores[
                valid_sales_stores[self._tarvarmapping["week"]].isin(weeks)
            ]
            (
                df_no_of_store_imputed,
                df_data_completeness,
            ) = self._calculate_sales_imputation_values(valid_sales_stores_imputed)
            teststores = pd.merge(
                teststores,
                df_no_of_store_imputed,
                on=self._storemstrmapping["partner_id"],
            )
            teststores = pd.merge(
                teststores,
                df_data_completeness,
                on=self._storemstrmapping["partner_id"],
            )
        return (
            teststores,
            valid_sales_stores,
            consideryearweeks,
            num_of_teststores,
            margin_of_error,
            confidence_interval,
            power_of_test,
            message,
            success_flag,
        )
