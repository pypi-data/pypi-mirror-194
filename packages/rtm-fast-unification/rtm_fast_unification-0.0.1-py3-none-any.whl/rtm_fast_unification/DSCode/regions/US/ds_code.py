"""
    About module: All customizations done for US market wrt FastTool functions
    Classes:
        FastToolUS
"""
from typing import Tuple

import pandas as pd
from DSCode.library.ds_code_test_plan import FastTool
from DSCode.library.ds_code_test_measurement import FastToolMeasurement

class FastToolUS(FastTool):
    """
    A class to represent features of FastToolUS.

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

    def calculate_rsv_estimate(self, target_variable, timeframestart, timeframeend,\
            storelist, applicability_criteria,uploaded_file_df=None):
        if "channel" not in applicability_criteria:
            return -1, -1, "Pass channel in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]
        rsvestimate, store_count, message, flag = super().calculate_rsv_estimate(
            target_variable = target_variable,
            timeframestart = timeframestart,
            timeframeend = timeframeend,
            storelist = storelist,
            applicability_criteria = applicability_criteria,
            uploaded_file_df=uploaded_file_df)
        return rsvestimate, store_count, message, flag

    def set_sales_weeks(self, applicability_criteria):
        """This function in US market, returns the value of sales week parameter
         to be used based on channel value passed"""
        return self._config['metadata']['test_configuration']\
                ['sales_weeks'][applicability_criteria['channel']]

    def set_lift_sales_weeks(self, applicability_criteria):
        """This function in US market, returns the value of sales week for lift calculation,
        parameter to be used based on channel value passed"""

        return self._config['metadata']['test_configuration']\
            ['sales_lifts_sales_weeks'][applicability_criteria['channel']]

    def set_summary_sales_weeks(self, applicability_criteria):
        """This function in US market, returns the value of sales week for summary calculation,
        parameter to be used based on channel value passed"""

        return self._config['metadata']\
                    ['test_planning']['summary_sales_weeks']\
                    [applicability_criteria['channel']]

    def set_test_vs_pop_comp(self, applicability_criteria):
        """This function in US market, returns the list of store attributes to be used for
        comparing test and population stores
        parameter to be used based on channel and team value passed"""

        return self._config['metadata']\
            ["test_planning"]["test_vs_population_compare"]\
            [applicability_criteria['team']]\
            [applicability_criteria['channel']].copy()
    def set_test_vs_pop_comp_sum(self, applicability_criteria):
        """This function in US market, returns the list of store attributes to be used for
        comparing test and population stores for summary page,
        parameter to be used based on channel and team value passed"""

        return self._config['metadata']['test_planning']\
                    ['test_vs_population_compare_summary']\
                    [applicability_criteria['channel']].copy()

    def set_test_vs_cntrl_comp(self, applicability_criteria):
        """This function in US market, returns the list of store attributes to be used for
        comparing test and control stores
        parameter to be used based on channel and team value passed"""

        return self._config['metadata']\
            ["test_planning"]["test_vs_control_compare"]\
            [applicability_criteria['team']]\
            [applicability_criteria['channel']].copy()

    def set_test_vs_cntrl_comp_sum(self, applicability_criteria):
        """This function in US market, returns the list of store attributes to be used for
        comparing test and control stores for summary page
        parameter to be used based on channel and team value passed"""

        return self._config['metadata']\
            ["test_planning"]["test_vs_control_compare_summary"]\
            [applicability_criteria['channel']].copy()

    def get_test_parameter(self, confidence_level, margin_of_error, num_of_teststores,\
            target_variable, test_type, applicability_criteria,\
            uploaded_file_df=None) -> Tuple[float, str, bool]:
        if "channel" not in applicability_criteria:
            return 0, "Pass channel", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                        ["weekly_mstr"]\
                                        [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                        .set_sales_weeks(applicability_criteria)

        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                        .set_lift_sales_weeks(applicability_criteria)

        test_parameter, message, success_flag = super()\
                                .get_test_parameter( confidence_level=confidence_level,
                                    margin_of_error=margin_of_error,
                                    num_of_teststores=num_of_teststores,
                                    target_variable=target_variable,
                                    test_type=test_type,
                                    applicability_criteria=applicability_criteria,
                                    uploaded_file_df=uploaded_file_df,
                                    )
        return test_parameter, message, success_flag


    def power_marginoferror_calculation(self, num_of_teststores, target_variable, \
            test_type, applicability_criteria, \
            uploaded_file_df=None) -> Tuple[float, float, float, str, bool]:
        if "channel" not in applicability_criteria:
            return 0, 0, 0, "Pass channel", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                            ["weekly_mstr"]\
                                            [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                .set_lift_sales_weeks(applicability_criteria)

        num_of_teststores, power_moferr_df, margin_of_error, message, success_flag = super()\
            .power_marginoferror_calculation(num_of_teststores = num_of_teststores,
                                            target_variable=target_variable,
                                            test_type=test_type,
                                            applicability_criteria=applicability_criteria,
                                            uploaded_file_df=uploaded_file_df
                                            )
        return num_of_teststores, power_moferr_df, margin_of_error, message, success_flag


    def teststores_sample_size(self, margin_of_error, target_variable, test_type,\
            applicability_criteria, uploaded_file_df=None) -> Tuple[float, float, str, bool]:
        if "channel" not in applicability_criteria:
            return 0, 0, 0, "Pass channel", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                ["weekly_mstr"]\
                                                [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self.set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                .set_lift_sales_weeks(applicability_criteria)

        number_test_stores_req, power_stores_df, message, success_flag = super()\
                                                .teststores_sample_size(
                                                    margin_of_error=margin_of_error,
                                                    target_variable=target_variable,
                                                    test_type=test_type,
                                                    applicability_criteria=applicability_criteria,
                                                    uploaded_file_df=uploaded_file_df)
        return number_test_stores_req, power_stores_df, message, success_flag


    def identify_test_stores(self, num_of_teststores, target_variable, test_type,\
         applicability_criteria, stratification_variables, uploaded_file_df=None) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, \
                    pd.DataFrame, pd.DataFrame, list, str, bool]:

        if "channel" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                [],"Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                [], "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_population_compare'] = self\
                                                    .set_test_vs_pop_comp(applicability_criteria)
        teststores, stores_master_df, annualrsvlifts, valid_sales_stores,\
             weekly_total_sales, consideryearweeks, message, success_flag = super()\
                .identify_test_stores(num_of_teststores = num_of_teststores,
                    target_variable=target_variable,
                    test_type=test_type,
                    applicability_criteria=applicability_criteria,
                    stratification_variables = stratification_variables,
                    uploaded_file_df=uploaded_file_df)
        return teststores, stores_master_df, annualrsvlifts, valid_sales_stores,\
                weekly_total_sales, consideryearweeks, message, success_flag

    def test_population_mapping(self, teststores, target_variable, test_type,\
         applicability_criteria, uploaded_file_df=None) -> Tuple[pd.DataFrame, str, bool]:
        if "channel" not in applicability_criteria:
            return pd.DataFrame(), "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                            .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                            .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['summary_sales_weeks'] = self\
                                            .set_summary_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_population_compare'] = self\
                                            .set_test_vs_pop_comp(applicability_criteria)
        return super().test_population_mapping( teststores=teststores,
                                                target_variable=target_variable,
                                                test_type=test_type,
                                                applicability_criteria=applicability_criteria,
                                                uploaded_file_df=uploaded_file_df)

    def test_store_summary(self, teststores, target_variable, test_type, \
            applicability_criteria, uploaded_file_df=None) -> Tuple[dict, dict, dict, str, bool]:
        if "channel" not in applicability_criteria:
            return {},{},{}, "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return {},{},{}, "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]["weekly_mstr"]\
                                                [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['summary_sales_weeks'] = self\
                                                .set_summary_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_population_compare_summary'] = self\
                                                .set_test_vs_pop_comp_sum(applicability_criteria)

        return super().test_store_summary(teststores = teststores,
                                        target_variable=target_variable,
                                        test_type=test_type,
                                        applicability_criteria=applicability_criteria,
                                        uploaded_file_df=uploaded_file_df)

    def test_store_comparison_summary(self, test_stores, target_variable, test_type, \
            applicability_criteria, uploaded_file_df=None) -> Tuple[pd.DataFrame, dict, str, bool]:
        if "channel" not in applicability_criteria:
            return pd.DataFrame(), {}, "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), {}, "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]["weekly_mstr"]\
                                                [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        combined_avg, metrics_dict, message, success_flag = super().test_store_comparison_summary(
                                    test_stores = test_stores,
                                    target_variable = target_variable,
                                    test_type = test_type,
                                    applicability_criteria = applicability_criteria,
                                    uploaded_file_df=uploaded_file_df)
        return combined_avg, metrics_dict, message, success_flag



    def test_stores_format_check(self, target_variable, num_of_teststores, test_type, applicability_criteria, teststores_data, uploaded_file_df=None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, int, bool]:

        if "channel" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                [],"Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                [], "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_population_compare'] = self\
                                                    .set_test_vs_pop_comp(applicability_criteria)
        teststores,annualrsvlifts,valid_sales_stores,consideryearweeks,message,\
            num_of_teststores,success_flag = super().test_stores_format_check(target_variable, num_of_teststores, test_type, applicability_criteria, teststores_data, uploaded_file_df)

        return teststores,annualrsvlifts,valid_sales_stores,consideryearweeks,message,\
            num_of_teststores,success_flag

    def manual_teststores_selection(self, test_type, target_variable, applicability_criteria, uploaded_file_df=None):

        if "channel" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                [],"Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), \
                [], "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_population_compare'] = self\
                                                    .set_test_vs_pop_comp(applicability_criteria)

        teststores,valid_sales_stores,consideryearweeks,num_of_teststores,margin_of_error,\
            confidence_interval,power_of_test,message,success_flag \
                = super().manual_teststores_selection(test_type, target_variable, applicability_criteria, uploaded_file_df)

        return teststores,valid_sales_stores,consideryearweeks,num_of_teststores,margin_of_error,\
            confidence_interval,power_of_test,message,success_flag


    """CONTROL STORES"""
    def identify_control_stores(self, teststores, target_variable, applicability_criteria,
                                test_type,one_to_one=True, business_categories=[],
                                reqcontrolstores=1, control_store_pool=None,
                                len_control_pool=None, uploaded_file_df=None)\
        -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, str, bool]:

        if "channel" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)

        applicability_criteria['test_vs_control_compare'] = self\
                                                    .set_test_vs_cntrl_comp(applicability_criteria)


        return super().identify_control_stores(teststores = teststores,
                                            target_variable = target_variable,
                                            applicability_criteria = applicability_criteria.copy(),
                                            test_type = test_type, one_to_one = one_to_one,
                                            business_categories = business_categories,
                                            reqcontrolstores = reqcontrolstores,
                                            control_store_pool = control_store_pool,
                                            len_control_pool = len_control_pool,
                                            uploaded_file_df = uploaded_file_df)

    def average_weekly_target_similarity_correlation(self, test_control_data,
                                                    target_variable,
                                                    applicability_criteria,
                                                    business_categories=[])\
        -> Tuple[dict, pd.DataFrame, str, bool]:

        if "channel" not in applicability_criteria:
            return {},pd.DataFrame(),\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return {},pd.DataFrame(),\
                 "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        return super().average_weekly_target_similarity_correlation(test_control_data = test_control_data,
                                                                    target_variable = target_variable,
                                                                    applicability_criteria = applicability_criteria,
                                                                    business_categories = business_categories)

    def control_store_summary(self, test_type, test_control_mapping_stores, business_categories,\
         target_variable, applicability_criteria, uploaded_file_df=None)\
             -> Tuple[dict, dict, dict, str, bool]:

        if "channel" not in applicability_criteria:
            return {},{},{},\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return {},{},{},\
                 "Pass team in applicability criteria", False
        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['summary_sales_weeks'] = self\
                                                    .set_summary_sales_weeks(applicability_criteria)

        applicability_criteria['test_vs_control_compare_summary'] = self\
                                                    .set_test_vs_cntrl_comp_sum(applicability_criteria)


        return super().control_store_summary(test_type = test_type,
                                            test_control_mapping_stores = test_control_mapping_stores,
                                            business_categories = business_categories,
                                            target_variable = target_variable,
                                            applicability_criteria = applicability_criteria.copy(),
                                            uploaded_file_df = uploaded_file_df)

    def manual_upload_control_store_pool(self,control_store_pool_data,
                                        teststores, target_variable,
                                        applicability_criteria, test_type,
                                        business_categories=[],
                                        reqcontrolstores=1,
                                        one_to_one=True, uploaded_file_df=None)\
        -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, str, bool]:


        if "channel" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                 "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_control_compare'] = self\
                                                    .set_test_vs_cntrl_comp(applicability_criteria)

        return super().manual_upload_control_store_pool(control_store_pool_data = control_store_pool_data,
                                                        teststores = teststores,
                                                        test_type= test_type,
                                                        target_variable = target_variable,
                                                        applicability_criteria = applicability_criteria,
                                                        business_categories = business_categories,
                                                        reqcontrolstores = reqcontrolstores,
                                                        one_to_one = one_to_one,
                                                        uploaded_file_df =uploaded_file_df)

    def recompute_control_stores(self, test_control_stores, target_variable, business_categories,\
                                include_cbu_features,reqcontrolstores, applicability_criteria,\
                                test_type,uploaded_file_df=None)\
        -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame,str,bool]:

        if "channel" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                 "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)

        applicability_criteria['test_vs_control_compare'] = self\
                                                    .set_test_vs_cntrl_comp(applicability_criteria)


        return super().recompute_control_stores(test_control_stores = test_control_stores,
                                                target_variable = target_variable,
                                                business_categories = business_categories,
                                                include_cbu_features = include_cbu_features,
                                                reqcontrolstores = reqcontrolstores,
                                                test_type = test_type,
                                                applicability_criteria = applicability_criteria,
                                                uploaded_file_df = uploaded_file_df)

    def manual_teststore_controlstore_upload(self, target_variable, test_control_store_data, test_type,
                                    applicability_criteria, uploaded_file_df=None, business_categories = None,)-> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str, bool]:

        if "channel" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),\
                 "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        applicability_criteria['sales_weeks'] = self\
                                                    .set_sales_weeks(applicability_criteria)
        applicability_criteria['sales_lifts_sales_weeks'] = self\
                                                    .set_lift_sales_weeks(applicability_criteria)
        applicability_criteria['summary_sales_weeks'] = self.set_summary_sales_weeks(applicability_criteria)
        applicability_criteria['test_vs_control_compare'] = self\
                                                    .set_test_vs_cntrl_comp(applicability_criteria)
        control_test_pairs, stores_master_df, annualrsvlifts, message, success_flag = super().manual_teststore_controlstore_upload(target_variable = target_variable,
                            test_control_store_data = test_control_store_data,
                             test_type = test_type,
                                    applicability_criteria = applicability_criteria,
                                     uploaded_file_df=uploaded_file_df, business_categories = business_categories)
        if success_flag is True:
            control_test_pairs = control_test_pairs.merge(stores_master_df[[self._storemstrmapping['partner_id'], 'TDLinx_No', 'StoreNumber']].rename(columns={self._storemstrmapping['partner_id']:'Test_store_'+self._storemstrmapping['partner_id'], 'StoreNumber':'Test_store_StoreNumber', 'TDLinx_No':'Test_store_TDLinx_No'}), on='Test_store_'+self._storemstrmapping['partner_id'])
            control_test_pairs = control_test_pairs.merge(stores_master_df[[self._storemstrmapping['partner_id'], 'TDLinx_No', 'StoreNumber']].rename(columns={'StoreNumber':'Control_store_StoreNumber', 'TDLinx_No':'Control_store_TDLinx_No'}), on=self._storemstrmapping['partner_id'])
        return control_test_pairs, stores_master_df, annualrsvlifts, message, success_flag

class FastToolMsrmtUS(FastToolMeasurement):
    def __init__(self, fast_tool_plan, config, region, test_id):
        super().__init__(fast_tool_plan = fast_tool_plan, config = config, region = region, test_id = test_id)

    def get_test_vs_control_linegraph(self, teststores, target_variable, test_type, applicability_criteria, weeks_before=None, weeks_after=None,control_stores_sales_method='Approach1', business_categories=None) -> Tuple[dict, str, bool]:
        if "channel" not in applicability_criteria:
            return dict(), "Pass channel in applicability criteria", False

        if "businessType" not in applicability_criteria:
            return dict(), "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return dict(), "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]

        return super().get_test_vs_control_linegraph(teststores = teststores,
                                                    target_variable = target_variable,
                                                    test_type = test_type,
                                                    applicability_criteria = applicability_criteria,
                                                     control_stores_sales_method = control_stores_sales_method,
                                                      business_categories = business_categories,
                                                      weeks_after=weeks_after,
                                                      weeks_before=weeks_before)

    def _get_cost(self, test_master_table, population_store_weekly_sales=None, target_variable=None)->float:
        rsv_estimate = population_store_weekly_sales[target_variable].sum()
        break_even_lift = float(test_master_table['break_even_lift'].values[0])
        return self._fast_tool_plan.get_cost(rsv_estimate=rsv_estimate, breakevenliftpercentage=break_even_lift)

    def get_target_variable_analysis_results(self, teststores, target_variable, test_type, applicability_criteria,control_stores_sales_method='Approach1',
         outlier_column=None, business_categories=None, uploaded_file_df=None)-> Tuple[float, str, pd.DataFrame, pd.DataFrame, dict, dict, str, bool]:
        if "channel" not in applicability_criteria:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), "Pass channel in applicability criteria", False

        if "businessType" not in applicability_criteria:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), "Pass channel in applicability criteria", False

        if "team" not in applicability_criteria:
            return 0.0, "", pd.DataFrame(), pd.DataFrame(), dict(), dict(), "Pass team in applicability criteria", False

        applicability_criteria['sales_table'] = self._config["tables"]\
                                                    ["weekly_mstr"]\
                                                    [applicability_criteria['channel']]
        applicability_criteria['store_table'] = self._config["tables"]["store_mstr"]
        applicability_criteria['product_table'] = self._config["tables"]["weekly_data_table"]
        return super().get_target_variable_analysis_results(teststores = teststores,
                                                            target_variable = target_variable,
                                                            test_type = test_type,
                                                            applicability_criteria = applicability_criteria,
                                                            control_stores_sales_method=control_stores_sales_method,
                                                            outlier_column=outlier_column,
                                                            business_categories=business_categories,
                                                            uploaded_file_df=uploaded_file_df)
