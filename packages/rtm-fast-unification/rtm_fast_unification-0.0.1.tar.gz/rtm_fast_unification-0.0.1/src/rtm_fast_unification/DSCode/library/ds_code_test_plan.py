"""
About module: this module is responsible for flow of the tool.
App team may call functions present in the class present (FastTool) in this file
or functions present in child class of FastTool.

If a DS code developer for any region wants to modify the existing flow can override
the functions present here.

Classes:
        FastTool
"""

from typing import Tuple

import pandas as pd
from DSCode.common_function import check_path
from DSCode.library.ds.feature.cntrl_store_gen.cntrl_stores_master import \
    CntrlStoreSelectionFeature
from DSCode.library.ds.feature.target_estimation.target_estimate_master import \
    TargetEstimate
from DSCode.library.ds.feature.test_store_gen.test_stores_master import \
    TestStoreSelectionFeature
from DSCode.library.object_creation.create_object import (get_sales_object,
                                                          get_store_object)


class FastTool:
    """
    A class to represent features of Fast tool. Here, the objects of Store, Sales and tool
    features interact with one another to define a flow.
    ...

    Attributes
    ----------
    config : configuration present in config_data either for a region or overall
    sales_object : Object of sales class
    store_object : Object of store class
    test_id: current test identifier
    _rsv_estimate: Object of TargetEstimate class
    _test_stores_features: Object of TestStoreSelectionFeature
    _control_stores_features: Object of ControlStoreSelectionFeature
    """

    def __init__(self, config, region, test_id):
        """
        Constructs all the necessary attributes for the tool flow.

        Parameters
        ----------
            config : configuration present in config_data either for a region or overall
            region: key present in config
            sales_query_parameter : optional attribute, to provide flexibility in query selection
            stores_query_parameter : optional attribute, to provide flexibility in query selection
        """
        self._config = config[region] if region in config else config
        self._metadata = self._config["metadata"]
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]

        self._sales_object = get_sales_object(config=self._config,
                                                      test_id=test_id)
        self._store_object = get_store_object(config=self._config,
                                                      test_id=test_id)
        self._test_id = test_id
        self._rsv_estimate = TargetEstimate(config=self._config,
                                         region=region,
                                         sales_object=self._sales_object,
                                         store_object=self._store_object)

        self._test_stores_features = TestStoreSelectionFeature(
                                            config=self._config,
                                            region=region,
                                            sales_object=self._sales_object,
                                            store_object=self._store_object,
                                            test_id=test_id)
        self._control_stores_features = CntrlStoreSelectionFeature(
                                            config=self._config,
                                            region=region,
                                            sales_object = self._sales_object,
                                            store_object = self._store_object,
                                            test_id=test_id)
    def _get_test_vs_control_compare(self, applicability_criteria)-> list:

        # this function returns the compare variable for comparing test and control stores

        if 'test_vs_control_compare' in applicability_criteria:
            return applicability_criteria['test_vs_control_compare']
        return self._metadata["test_planning"]["test_vs_control_compare"].copy()

    def _get_test_vs_control_compare_sum(self, applicability_criteria)-> list:

        # this function returns the compare variable test and control stores summary

        if 'test_vs_control_compare_summary' in applicability_criteria:
            return applicability_criteria['test_vs_control_compare_summary']
        return self._metadata["test_planning"]["test_vs_control_compare_summary"].copy()

    def _get_test_vs_population_compare(self, applicability_criteria):
        """This function is to get the test_vs_population comparison
        attributes from the config"""
        if "test_vs_population_compare" not in applicability_criteria:
            return self._metadata["test_planning"]\
                                            ['test_vs_population_compare'].copy()
        return applicability_criteria['test_vs_population_compare']

    def _get_test_vs_population_compare_sum(self, applicability_criteria):

        if "test_vs_population_compare_summary" not in applicability_criteria:
            return self._metadata["test_planning"]\
                                            ['test_vs_population_compare_summary'].copy()
        return applicability_criteria['test_vs_population_compare_summary']

    def calculate_rsv_estimate(self, target_variable, timeframestart,
                                timeframeend, storelist, applicability_criteria,
                                uploaded_file_df=None)->Tuple[float, int, str, bool]:
        """
            About function
            --------------
            This function called through FAST UI estimate the total annual RSV and total
            stores in the population.

            Refers RSVEstimate object and calls method:
            1) data_extract
            2) calculate_rsv

            Parameters
            ----------
            target_variable: weekly sales column which is needs to be estimates (sales or volume),
            timeframestart: date from which preperiod starts,
            timeframeend: date on which preperiod ends,
            stores: list of stores for which sales to be calculated; by default pass empty list
            applicability_criteria: the product and stores attributes selected
                                    at tool in dictionary format,
            uploaded_file_df: optional parameter; its for DS people to use
                                    uploaded store as population in case not connected to DB

            Return values
            -------
            total sales or volume
            number of stores in population,
            message
            success flag
        """
        _, _, message, flag = self._rsv_estimate\
                                    .data_extract(target_variable=target_variable,
                                        storelist=storelist,
                                        timeframestart=timeframestart,
                                        timeframeend=timeframeend,
                                        applicability_criteria=applicability_criteria,
                                        uploaded_file_df=uploaded_file_df)
        if flag is False:
            return 0, 0, message, False
        rsvestimate, store_count = self._rsv_estimate.calculate_rsv(target_variable=target_variable)
        return rsvestimate, store_count, "Calculated Successfully!!", True

    def get_breakeven_lift(self, rsv_estimate, cost, applicability_criteria,
                         num_of_teststores,uploaded_file_df=None)->Tuple[float, str, bool]:

        """
            About function
            --------------
            This function estimates the break even lift

            Parameters
            ----------
            rsv_estimate: total sales/volume sold in annual RSV period;
                            got from calculate_rsv function
            cost: esimated cost of activity on population stores,
            num_of_teststores: number of stores considering in the test
            applicability_criteria: the product and stores attributes selected
                                    at tool in dictionary format,
            uploaded_file_df: optional parameter; its for DS people to use
                            uploaded store as population in case not connected to DB

            Return values
            -------
            floating estimated breakeven lift,
            message,
            booelan success flag
        """
        breakevenliftpercentage, message = self._rsv_estimate\
                                            .get_breakeven_lift(rsv_estimate = rsv_estimate,
                                                cost = cost,
                                                num_of_teststores = num_of_teststores,
                                                applicability_criteria = applicability_criteria,
                                                uploaded_file_df=uploaded_file_df)
        return breakevenliftpercentage, message, True

    def get_cost(self, rsv_estimate=None, breakevenliftpercentage=None) -> Tuple[float, str, bool]:
        """
            About function
            --------------
            This function estimates the cost of implementing the RTM activity on population stores.
            This function to be used when breakevenlift is known but cost is unknow

            Parameters
            ----------
            rsv_estimate: total sales or volume in annual RSV period
            breakevenliftpercentage: known break even lift

            Return values
            -------
            floating value of cost
        """
        return self._rsv_estimate.get_cost(rsv_estimate=rsv_estimate,
                                            breakevenliftpercentage=breakevenliftpercentage)

    def manual_upload_population(self, population_stores,
                 applicability_criteria) -> Tuple[str, pd.DataFrame, pd.DataFrame, bool]:
        """
            About function
            --------------
            This function is responsible for the checks to be applied on the stores uploaded
            in the applicability criteria page

            Checks:
            1) Checks the format of the uploaded file;
                validate_uploaded_stores_format of Store class
            2) Checks if the stores uploaded are present in the Store master;
                validate_uploaded_presence_store_master of Store class
            3) Checks if the stores are active in other test;
                validate_uploaded_stores_active_stores of Store class
            Parameters
            ----------
            population_stores: dataframe of the stores user has uploaded
            applicability_criteria: dictionary of the parameters selected by user

            Return values
            -------
            message,
            stores uploaded
            stores verified
            success flag
        """
        relative_path = self._config['filePath']["RSV_STORES"]["file_name"]
        population_ref = pd.read_excel(check_path(relative_path))
        population = population_stores
        # Number of columns check
        uploaded_store_identifier = self._metadata["test_planning"]["upload_stores_identifier"]
        reference_columns = list(self._metadata['test_planning']
                                                ['user_populationstores_columns'].items())
        message, success_flag = self._store_object\
                                        .validate_uploaded_stores_format(
                                            reference_file=population_ref,
                                            uploaded_file=population,
                                            columns=reference_columns)
        if success_flag is True:

            store_master_mapped, message2, success_flag = self._store_object\
                .validate_uploaded_presence_store_master(
                    uploaded_stores=population,
                    store_identifier=uploaded_store_identifier,
                    applicability_criteria=applicability_criteria)

            message = message2+"\n"+message
            if success_flag is False:
                return message, pd.DataFrame(), pd.DataFrame(), False
            max_week_data_available = self._sales_object\
                            .get_max_week_config_master(applicability_criteria)

            max_date_data_avlbl = self._sales_object\
                            .convert_week_to_date(week=max_week_data_available)

            _, message2, success_flag = self._store_object\
                                                    .validate_uploaded_stores_active_stores(
                                                        stores_df=store_master_mapped,
                                                        max_date_data_available=max_date_data_avlbl,
                                                        active_stores_filter_type="both")

            if success_flag is False:
                return message2, pd.DataFrame(), pd.DataFrame(), False
            message = message2+"\n"+message
            return message, population, store_master_mapped, True
        return message, pd.DataFrame(), pd.DataFrame(), False

    def get_test_parameter(self, confidence_level, margin_of_error, num_of_teststores,
                         target_variable,test_type, applicability_criteria,
                         uploaded_file_df=None)->Tuple[float, str, bool]:
        '''
            get_test_parameter
        '''
        if target_variable is not None:
            arg_req = [confidence_level, margin_of_error, num_of_teststores]
            if sum(v is not None for v in arg_req) == 2:
                annual_sales_lifts,_, _, _, stores_master_df,_, _,\
             message, success_flag = self\
                            ._test_stores_features.data_extract(
                                                target_variable=target_variable,
                                                applicability_criteria=applicability_criteria,
                                                test_type=test_type,
                                                uploaded_file_df=uploaded_file_df)
                if success_flag is False:
                    return 0, message, False
                store_identifier_sales = self._tarvarmapping["partner_id"]
                store_identifier = self._storemstrmapping["partner_id"]
                annual_sales_lifts = annual_sales_lifts[annual_sales_lifts[store_identifier_sales]\
                                            .isin(stores_master_df[store_identifier].unique())]

                standard_deviation = annual_sales_lifts[target_variable+" Lift"].std()
                test_parameter, message2, success_flag = self._test_stores_features\
                                        .test_parameter_calculation(
                                                confidence_level=confidence_level,
                                                margin_of_error=margin_of_error,
                                                num_of_teststores=num_of_teststores,
                                                standard_deviation=standard_deviation)
                if success_flag is False:
                    return 0, message2 + '\n'+message, False
                return test_parameter, message2+'\n'+message, True
            return 0, "Input error!! Please pass exactly of two options", False

        return 0, "target variable is not passed", False

    def power_marginoferror_calculation(self, num_of_teststores, target_variable, test_type, \
                applicability_criteria, uploaded_file_df=None) \
                                                -> Tuple[float, float, float, str, bool]:
        '''
            This function returns the table containing the margin of errors for different
             power values
        '''

        annual_sales_lifts,_, _, _, stores_master_df,_, _,\
             message, success_flag = self._test_stores_features\
                .data_extract(applicability_criteria=applicability_criteria,
                                        target_variable=target_variable,
                                        test_type=test_type,
                                        uploaded_file_df=uploaded_file_df)
        if success_flag is False:
            return 0, 0, 0, message, False
        store_identifier_saletbl = self._tarvarmapping["partner_id"]
        store_identifier_strtbl = self._storemstrmapping['partner_id']
        annual_sales_lifts = annual_sales_lifts[annual_sales_lifts[store_identifier_saletbl].isin(
            stores_master_df[store_identifier_strtbl].unique())]
        # Sample Size calculation with power and confidence level fixed
        standard_deviation = annual_sales_lifts[target_variable+" Lift"].std()
        power_of_test = self._metadata["test_planning"]["power_of_test"]
        confidence_level = self._metadata["test_planning"]["confidence_level"]

        margin_of_error_req, _, \
            success_flag = self._test_stores_features.test_parameter_calculation(
                                            confidence_level=confidence_level,
                                            margin_of_error=None,
                                            power_of_test=power_of_test,
                                            num_of_teststores=num_of_teststores,
                                            standard_deviation=standard_deviation)

        # Power vs sample size table
        power_values = self._metadata["test_planning"]["power_values"]
        margin_of_error_list = []
        for i in power_values:
            temp_margin_of_error,\
                 _, _ = self._test_stores_features.test_parameter_calculation(
                                                confidence_level=confidence_level,
                                                margin_of_error=None,
                                                power_of_test=i/100,
                                                num_of_teststores=num_of_teststores,
                                                standard_deviation=standard_deviation)
            margin_of_error_list.append(temp_margin_of_error)
        power_moferr_df = pd.concat([pd.Series(power_values), pd.Series(
            margin_of_error_list)], axis=1).rename(columns={0: "Power %",
                                                             1: "Margin of Error"})

        return num_of_teststores, power_moferr_df,\
                     margin_of_error_req, "Margin of error calculated successfully!!", True

    def teststores_sample_size(self, margin_of_error, target_variable, test_type,
                                applicability_criteria, uploaded_file_df=None)\
                                                        -> Tuple[float, float, str, bool]:
        '''
            This function returns the table containing the sample sizes
             for different power values - No uk specific coe in it
        '''
        annual_sales_lifts,_, _, _, stores_master_df,_, _,\
             message, success_flag = self._test_stores_features.data_extract(
                                        applicability_criteria=applicability_criteria,
                                        target_variable=target_variable,
                                        test_type=test_type,
                                        uploaded_file_df=uploaded_file_df)
        if success_flag is False:
            return 0, 0, message, success_flag
        annual_sales_lifts = annual_sales_lifts[annual_sales_lifts[self._tarvarmapping["partner_id"]].isin(
            stores_master_df[self._storemstrmapping["partner_id"]].unique())]

        # Sample Size calculation with power and confidence level fixed
        standard_deviation = annual_sales_lifts[target_variable + ' Lift'].std()
        power_of_test = self._metadata["test_planning"]["power_of_test"]
        confidence_level = self._metadata["test_planning"]["confidence_level"]

        number_test_stores_req,\
             _, success_flag = self._test_stores_features.test_parameter_calculation(
                                confidence_level=confidence_level,
                                margin_of_error=margin_of_error,
                                power_of_test=power_of_test,
                                num_of_teststores=None,
                                standard_deviation=standard_deviation)

        # Power vs sample size table
        power_values = self._metadata["test_planning"]["power_values"]
        sample_size_list = []
        for _ in power_values:
            num_of_teststores,\
                 _, success_flag = self._test_stores_features.test_parameter_calculation(
                                                    confidence_level=confidence_level,
                                                    margin_of_error=margin_of_error,
                                                    power_of_test=power_of_test,
                                                    num_of_teststores=None,
                                                    standard_deviation=standard_deviation)
            sample_size_list.append(num_of_teststores)

        power_stores_df = pd.concat([pd.Series(power_values), pd.Series(
            sample_size_list)], axis=1).rename(columns={0: "Power %",
                                                        1: "Number of Stores"})

        return number_test_stores_req, power_stores_df,\
                                    "Number of test stores calculated successfully!!", True

    # In case developer wants to modify the validation of sample stores they can override
    # this function
    def _test_store_identification_util(self, compare_variables, stratification_variable,
                                        filtered_population_sales,population_sales,
                                        filtered_stores_df, num_of_teststores):
        return self._test_stores_features.test_store_identification(
                                    compare_variables=compare_variables,
                                    stratification_variable=stratification_variable,
                                    filtered_population_sales=filtered_population_sales,
                                    population_sales=population_sales,
                                    filtered_stores_df=filtered_stores_df,
                                    num_of_teststores=num_of_teststores)

    def identify_test_stores(self, num_of_teststores, target_variable, test_type,
                            applicability_criteria, stratification_variables,
                            uploaded_file_df=None) \
                                    -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,
                                                pd.DataFrame, pd.DataFrame,list, str, bool]:
        '''identify_test_stores'''
        sales_week = self._sales_object.get_sales_weeks(applicability_criteria)
        sales_lifts_sales_weeks  = self._sales_object.get_lift_sales_weeks(applicability_criteria)

        compare_variables = self._get_test_vs_population_compare(applicability_criteria)

        message = ""
        compare_variables.append(target_variable)

        # """Fetch the population details along with lift values"""

        annual_sales_lifts, valid_sales_stores, weekly_ovrl_sales, _,stores_master_df, test_master_df,\
            consideryearweeks, message, success_flag = self._test_stores_features\
                                    .data_extract(
                                    applicability_criteria=applicability_criteria,
                                    target_variable=target_variable,
                                    test_type=test_type,
                                    uploaded_file_df=uploaded_file_df)
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 pd.DataFrame(), pd.DataFrame(),list(), message, False

        # """For the current test, check if test stores are finalized"""
        finalised_flag = False if test_master_df.shape[0] == 0 else \
                                                    test_master_df['is_finalize'].values[0]
        # """For the current test, get the test stores selected"""
        teststore_map_df = self._store_object.\
                                            read_test_map_table_by_test_ids(self._test_id)
        active_tests_df = pd.DataFrame(columns=['test_id']) if test_master_df.shape[0] == 0\
                                    else test_master_df[test_master_df["is_active"] == 1]

        store_identifier = self._storemstrmapping["partner_id"]
        # """Filter the population and keep stores that are not participating in other tests """
        max_week_data_available = self._sales_object.get_max_week_config_master(
            applicability_criteria)
        max_date_data_available = self._sales_object.convert_week_to_date(
            week=max_week_data_available)
        filtered_stores_df = self._store_object.filter_active_test_control_stores(
                                        stores_master_df=stores_master_df,
                                        remove_type='both',
                                        max_week_data_available=max_date_data_available)
        if filtered_stores_df.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 pd.DataFrame(), list(),"All Stores are participating in other test", False
        message = "Total stores in population: {}\n".format(
            stores_master_df[store_identifier].nunique()) + message

        # Get the proportion of stores to be sampled for each banner
        stores_got_removed = set(stores_master_df[store_identifier].unique(
        )) - set(filtered_stores_df[store_identifier])
        message = """Number of Stores participating in other tests (Test + control stores):
        {}\n""".format(len(stores_got_removed))+message
        message = "Number of Stores have continues data: {}\n".format(
            annual_sales_lifts[store_identifier].nunique())+message
        filtered_stores_df = filtered_stores_df[filtered_stores_df[store_identifier].isin(
            annual_sales_lifts[store_identifier].unique())]

        # """Keep buffer in population for control stores"""
        cntrl_store_buffer = self._config['feature_parameter']['control_store_buffer']
        if filtered_stores_df.shape[0] < (num_of_teststores)*cntrl_store_buffer:
            message = """Required number of test stores are greater than the population.
                                    Please change the selections and continue.\n"""+message
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 pd.DataFrame(), list(), message, False

        filtercolumns = [self._tarvarmapping["partner_id"]] + \
            [self._tarvarmapping['rsv']+' Year 2']

        filtered_rsv_stores_df = filtered_stores_df.merge(
                                            annual_sales_lifts[filtercolumns],
                                            left_on=store_identifier,
                                            right_on=store_identifier)
        filtered_rsv_stores_df.rename(columns={
                                      self._tarvarmapping['rsv']+' Year 2':
                                       self._tarvarmapping['rsv']}, inplace=True)
        # """get the weekly sales of the population stores"""


        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 pd.DataFrame(),list(), message, False
        weeks = consideryearweeks[sales_lifts_sales_weeks:]
        weeklyrsvdatayear = weekly_ovrl_sales[weekly_ovrl_sales[
                                    self._tarvarmapping["week"]].isin(weeks)]
        weeklyrsvdatayear[self._tarvarmapping['year']] = "Year1"
        aggdict = {k: sum for k in [
            self._tarvarmapping["rsv"], self._tarvarmapping["volume"]]}
        groupbycolumns = [self._tarvarmapping["partner_id"],
                          self._tarvarmapping["banner"], self._tarvarmapping['year']]
        # """Yearly sales of the stores"""
        annualrsvdatayear = weeklyrsvdatayear.groupby(
            groupbycolumns).agg(aggdict).reset_index()
        population_sales = stores_master_df.merge(
                                        annualrsvdatayear,
                                        left_on=self._storemstrmapping["partner_id"],
                                        right_on=self._tarvarmapping["partner_id"])
        annualrsvdatayear = annualrsvdatayear[annualrsvdatayear[
                    self._tarvarmapping["partner_id"]]\
                .isin(filtered_stores_df[self._storemstrmapping["partner_id"]].unique())]

        # Handles if teststores are already generated then fetch details from the database and mark them selected
        if (self._test_id in active_tests_df["test_id"].values.tolist()) \
            & (finalised_flag is not None) & (teststore_map_df.shape[0] != 0):
            if finalised_flag == 0:
                current_teststores = teststore_map_df[teststore_map_df['test_id_id']
                                                      == self._test_id]
                current_teststores = filtered_stores_df[filtered_stores_df[
                    self._storemstrmapping["partner_id"]]\
                        .isin(current_teststores['teststore_id'].unique())]
                current_teststores["is_teststore"] = 1
                filtered_rsv_stores_df["is_teststore"] = 0
                teststores = pd.concat(
                    [current_teststores, filtered_rsv_stores_df])
            else:
                current_teststores = teststore_map_df[teststore_map_df['test_id_id']
                                                      == self._test_id]
                current_teststores = filtered_stores_df[filtered_stores_df
                            [self._storemstrmapping["partner_id"]]\
                                .isin(current_teststores['teststore_id'].unique())]
                current_teststores["is_teststore"] = 1
                teststores = current_teststores
        else:
            # Generate best sample for test stores
            teststores = self._test_store_identification_util(
                compare_variables=compare_variables,
                stratification_variable=stratification_variables,
                filtered_population_sales=filtered_rsv_stores_df,
                filtered_stores_df=filtered_stores_df,
                population_sales=population_sales,
                num_of_teststores = num_of_teststores)

        message = 'Identified Test Stores Successfully\n'+message
        return teststores, stores_master_df, annual_sales_lifts, valid_sales_stores, \
            weekly_ovrl_sales, consideryearweeks, message, True

    # Test store to population similarity and correlation
    def test_population_mapping(self,teststores, target_variable, test_type, applicability_criteria,
                                    uploaded_file_df=None)-> Tuple[pd.DataFrame, str, bool]:
        '''API - selected_store_correlation'''

        if teststores is None or teststores.shape[0] == 0:
            return pd.DataFrame(), "Please pass test stores to the function", False
        if "is_teststore" not in teststores.columns:
            return pd.DataFrame(), \
                "Passed test store doesnt have is_teststore column", False
        if 0 in teststores['is_teststore'].unique():
            return pd.DataFrame(), \
                "Passed stores are not filtered for selected stores", False

        compare_variables = self._get_test_vs_population_compare(applicability_criteria)
        summary_sales_weeks = self._sales_object.get_summary_sales_weeks(applicability_criteria)
        annual_sales_lifts,valid_sales_stores, _, _, stores_master_df,_, consideryearweeks,\
             message, success_flag = self._test_stores_features\
                .data_extract(applicability_criteria=applicability_criteria,
                                target_variable=target_variable,
                                test_type=test_type,
                                uploaded_file_df=uploaded_file_df)
        if success_flag is False:
            return pd.DataFrame(), message, False

        filtercolumns = [self._tarvarmapping["partner_id"], target_variable + ' Year 1',
                            target_variable+' Year 2',target_variable+' Lift']
        print(annual_sales_lifts.columns)
        stores_master_df = stores_master_df.merge(
                                            annual_sales_lifts[filtercolumns],
                                            left_on=self._storemstrmapping["partner_id"],
                                            right_on=self._tarvarmapping["partner_id"])
        print(stores_master_df.columns)
        # Adding extra features as comparison features
        print(f"compare variables {compare_variables}")
        compare_variables.extend(
            [target_variable+" Year 2", target_variable+" Lift"])
        print(f"compare variables {compare_variables}")
        test_population_compare = self._test_stores_features\
            .test_population_mapping_util(teststores=teststores,
                                        stores_master_df=stores_master_df,
                                        valid_stores_sales=valid_sales_stores,
                                        compare_variables=compare_variables,
                                        consideryearweeks=consideryearweeks,
                                        summary_sales_weeks=summary_sales_weeks,
                                        target_variable=target_variable)
        return test_population_compare, 'Correlation calculated Successfully!!', True

    def test_store_summary(self, teststores, target_variable, test_type,
                applicability_criteria, uploaded_file_df=None)\
                        -> Tuple[dict, dict, dict, str, bool]:
        '''
        # This function corresponds to the test vs population summary module in the tool
        #  - No uk specific code in it
        '''
        if teststores is None or teststores.shape[0] == 0:
            return {},{},{}, "Please pass test stores to the function", False
        sales_week = self._sales_object.get_sales_weeks(applicability_criteria)
        compare_variables = self._get_test_vs_population_compare_sum(applicability_criteria)

        summary_sales_weeks = self._sales_object.get_summary_sales_weeks(applicability_criteria)
        stores_master_df = self._store_object.filter_population(
            uploaded_file_df=uploaded_file_df, applicability_criteria=applicability_criteria)
        if stores_master_df.shape[0] == 0:
            return {},{},{}, "No stores found in the population", False

        test_master_df=self._store_object.read_test_master_table_by_test_ids(test_id=self._test_id)
        weekly_target_variables_file, consideryearweeks, message, success_flag = self._sales_object\
            .get_total_weekly_target_data(target_variable = target_variable,
                                            test_master_df = test_master_df,
                                            stores_list = list(stores_master_df\
                                                [self._storemstrmapping['partner_id']].unique()),
                                            test_type = test_type,
                                            sales_week = sales_week,
                                            applicability_criteria = applicability_criteria,
                                            )

        if success_flag is False:
            return {}, {}, {}, message, False
        weeks = consideryearweeks[summary_sales_weeks:]
        weeklyrsvdatayear = weekly_target_variables_file[\
            weekly_target_variables_file[self._tarvarmapping["week"]].isin(weeks)]
        weeklyrsvdatayear[self._tarvarmapping['year']] = "Year1"
        # To Free Space
        variables_metrics_dict, feature_bounds_dict,\
             pvalue_dict = self._test_stores_features\
                    .test_store_summary_util(weekly_rsv_sales=weeklyrsvdatayear,
                                            population_stores=stores_master_df,
                                            test_stores=teststores,
                                            compare_variables=compare_variables,
                                            target_variable=target_variable)
        return variables_metrics_dict, feature_bounds_dict, \
            pvalue_dict, "Successfully Calculated!!", True

    # Test vs population summary graph

    def test_store_comparison_summary(self, test_stores,target_variable,  test_type,\
         applicability_criteria, uploaded_file_df=None) -> Tuple[pd.DataFrame, dict, str, bool]:
        '''# This function corresponds to the test vs population summary module in the tool

        '''
        print(test_type)
        stores_master_df = self._store_object.filter_population(
            applicability_criteria=applicability_criteria, uploaded_file_df=uploaded_file_df)
        if stores_master_df.shape[0] == 0:
            return pd.DataFrame(), {}, "No stores found in the population", False

        test_master_df = self._store_object.read_test_master_table_by_test_ids(test_id=self._test_id)

        store_identifier = self._storemstrmapping["partner_id"]
        prewindow_target_data, postwindow_target_data, \
                        _, _,message, success_flag = self._sales_object\
                                .get_weekly_targetvariables_data(target_variable=target_variable,
                                            test_master_df=test_master_df,
                                            stores=list(
                                                    stores_master_df[store_identifier].unique()),
                                            applicability_criteria=applicability_criteria)
        if success_flag is False:
            return pd.DataFrame(), {}, message, False
        combined_avg, metrics_dict, _ , success_flag = self._test_stores_features\
            .test_store_comparison_summary_util(
                            test_stores=test_stores,
                            target_variable=target_variable,
                            prewindow_target_data=prewindow_target_data,
                            postwindow_target_data=postwindow_target_data,
                            population_stores=stores_master_df)

        return combined_avg, metrics_dict, "Summary calculated successfully!!", True



    def test_stores_format_check(self,target_variable,num_of_teststores,test_type,applicability_criteria\
        ,teststores_data,uploaded_file_df = None) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,list,str,int,bool]:
        """
        This Function is related to uploaded teststores,validate the format of uploaded teststores
        """

        if 'bypass_active_test_control' in applicability_criteria:
            bypass_active_test_control = applicability_criteria['bypass_active_test_control']
        else:
            bypass_active_test_control = 0

        # Test stores reference file to check for the format of the user uploaded file
        relative_path = self._config["filePath"]["TestStore"]["file_name"]
        format_ref_file = pd.read_excel(check_path(relative_path))

        # User uploaded test stores
        teststores = teststores_data.copy(deep=True)
        if "store_identifier_attribute" not in applicability_criteria:
            applicability_criteria[
                "store_identifier_attribute"
            ] = self._storemstrmapping["partner_id"]

        # represents the column name
        store_identifier = self._metadata["test_planning"][
            "upload_teststores_identifier"
        ]
        # Represents the column value type
        store_identifier_type = applicability_criteria["store_identifier_attribute"]
        (
            message,
            success_flag,
        ) = self._store_object.validate_uploaded_stores_format(
            reference_file=format_ref_file,
            uploaded_file=teststores,
            columns=list(
                self._metadata["test_planning"]["user_teststores_columns"].items()
            ),
        )
        if success_flag is True:
            message = (
                f"Number of uploaded stores {teststores[store_identifier].nunique()}\n"
                + message
            )
            """Fetch details of the uploaded stores"""

            (
                test_stores_details,
                message2,
                success_flag,
            ) = self._store_object.validate_uploaded_presence_store_master(
                uploaded_stores=teststores,
                store_identifier=store_identifier,
                applicability_criteria=applicability_criteria,
            )
            if success_flag is False:
                return pd.DataFrame,pd.DataFrame,pd.DataFrame,list,message2 +"\n"+ message,0,False

            message = message2 + "\n" + message
            annualrsvlifts,valid_sales_stores, _, _, stores_master_df,_, consideryearweeks,\
             message3, success_flag = self._test_stores_features.data_extract(
                applicability_criteria=applicability_criteria,
                target_variable=target_variable,
                test_type=test_type,
                uploaded_file_df=uploaded_file_df,
            )

            if success_flag is False:
                return pd.DataFrame,pd.DataFrame,pd.DataFrame,list,message3 +"\n"+ message,0,False
            message = message3 + "\n" + message
            if store_identifier_type not in stores_master_df.columns:
                return (
                    pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                    "store_identifier_attribute passed is not present in store master columns",
                    0,
                    False,
                )

            message = (
                "Uploaded stores that are not in population: {}\n".format(
                    set(test_stores_details[store_identifier_type].values.tolist())
                    - set(stores_master_df[store_identifier_type].values.tolist())
                )
                + message
            )
            test_stores_details = stores_master_df[
                stores_master_df[store_identifier_type].isin(
                    test_stores_details[store_identifier_type].values.tolist()
                )
            ]

            if test_stores_details.shape[0] == 0:
                return (
                    pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                    "All uploaded test store are not part of the population",
                    0,
                    False,
                )
            # this check is to handle rtm-impact test case if rtm Impact test then bypass
            if bypass_active_test_control == 0:
                """Eliminate stores that are actively test or control stores in other test"""
                max_week_data_available = (
                    self._sales_object.get_max_week_config_master(
                        applicability_criteria
                    )
                )
                max_date_data_available = self._sales_object.convert_week_to_date(
                    week=max_week_data_available
                )
                """Filter the stores with active stores"""
                filtered_stores = (
                    self._store_object.filter_active_test_control_stores(
                        stores_master_df=stores_master_df.copy(deep=True),
                        remove_type="both",
                        max_week_data_available=max_date_data_available,
                    )
                )

                check_active = filtered_stores[
                    filtered_stores[store_identifier_type].isin(
                        test_stores_details[store_identifier_type].values.tolist()
                    )
                ]
                if check_active.shape[0] == 0:
                    return (
                        pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                        "All uploaded stores are pariticipating in other active tests.\n"
                        + message,
                        -1,
                        False,
                    )
                message = (
                    "Uploaded stores that are in active tests: {}\n".format(
                        set(test_stores_details[store_identifier_type].values.tolist())
                        - set(filtered_stores[store_identifier_type].values.tolist())
                    )
                    + message
                )
                test_stores_details = check_active
            # in case of RTM Impact Test
            else:
                filtered_stores = stores_master_df
            annualrsvlifts = annualrsvlifts.merge(
                stores_master_df,
                left_on=[
                    self._tarvarmapping["partner_id"],
                    self._tarvarmapping["banner"],
                ],
                right_on=[
                    self._storemstrmapping["partner_id"],
                    self._storemstrmapping["banner"],
                ],
            )
            annualrsvlifts = annualrsvlifts[
                annualrsvlifts[store_identifier_type].isin(
                    stores_master_df[store_identifier_type].unique()
                )
            ]
            if annualrsvlifts.shape[0] == 0:
                return (
                    pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                    "All the population stores dont have sales in the weekly master"
                    + "\n"
                    + message,
                    -1,
                    False,
                )
            test_stores_details = annualrsvlifts[
                annualrsvlifts[self._tarvarmapping["partner_id"]].isin(
                    test_stores_details[self._storemstrmapping["partner_id"]].unique()
                )
            ]
            standard_deviation = annualrsvlifts[target_variable + " Lift"].std()

            (
                num_of_teststores,
                message4,
                success_flag,
            ) = self._test_stores_features.test_parameter_calculation(
                confidence_level=self._metadata["test_planning"]["confidence_level"],
                margin_of_error=self._metadata["test_planning"]["margin_of_error"],
                power_of_test=self._metadata["test_planning"]["power_of_test"],
                num_of_teststores=None,
                standard_deviation=standard_deviation,
            )

            filtered_stores_df = annualrsvlifts[
                annualrsvlifts[self._tarvarmapping["partner_id"]].isin(
                    filtered_stores[self._storemstrmapping["partner_id"]].unique()
                )
            ]
            if filtered_stores_df.shape[0] < self._config["feature_parameter"][
                "control_store_buffer"
            ] * (test_stores_details[self._storemstrmapping["partner_id"]].nunique()):
                return (
                   pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                    "Required num of teststores are greater than the population.\
                        Please upload less number of teststores.\n"
                    + message,
                    0,
                    False,
                )
            message = message4 + "\n" + message
            filtered_rsv_stores_df = filtered_stores_df
            if filtered_rsv_stores_df.shape[0] == 0:
                return (
                    pd.DataFrame,pd.DataFrame,pd.DataFrame,list,
                    "The stores dont have continuous sales\n" + message,
                    0,
                    False,
                )

            message = (
                "Uploaded stores that dont have continuous sales: {}\n".format(
                    set(test_stores_details[store_identifier_type].values.tolist())
                    - set(filtered_rsv_stores_df[store_identifier_type].values.tolist())
                )
                + message
            )
            filtered_teststores = filtered_rsv_stores_df[
                filtered_rsv_stores_df[store_identifier_type].isin(
                    test_stores_details[store_identifier_type].unique()
                )
            ]
            #             filtered_teststores = filtered_teststores[filtered_teststores[storemstrmapping["banner"]]]
            filtered_teststores["is_teststore"] = 1
            message1 = "Recommendation Note: The number of required teststores suggested for the\
                 confidence level:{}, margin of error: {} and power of test: {} are {}".format(
                self._metadata["test_planning"]["confidence_level"],
                self._metadata["test_planning"]["margin_of_error"],
                self._metadata["test_planning"]["power_of_test"],
                num_of_teststores,
            )
            message2 = f"No of uploaded teststores satisfying the criteria to proceed further are\
                 {filtered_teststores[store_identifier_type].nunique()}\n"
            return (
                filtered_teststores,
                annualrsvlifts,
                valid_sales_stores,
                consideryearweeks,
                message1 + "\n" + message2 + "\n" + message,
                num_of_teststores,
                True,
            )

        return (
            pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),list,
            "The uploaded file/data format doesn't match with the expected format",
            0,
            False,
        )


    def manual_teststores_selection(
        self,
        test_type,
        target_variable,
        applicability_criteria,
        uploaded_file_df = None
    ):
        """
        # This is the function related to the manual test stores selection component in the tool
        # Read the files
        # Need to make Change here as per interaction with Database (Starting from here)
        """

        if 'bypass_active_control_test' in applicability_criteria:
            bypass_active_control_test = applicability_criteria['bypass_active_control_test']
        else:
            bypass_active_control_test = 0

        test_master_df = self._store_object.read_test_master_table_by_test_ids(
            test_id=self._test_id
        )
        finalised_flag = (
            False if test_master_df.shape[0] == 0 else test_master_df.iloc[0]["is_finalize"]
        )
        teststore_map_df = self._store_object.read_test_map_table_by_test_ids(
            test_id=self._test_id
        )
        # Need to make Change here as per interaction with Database (to here)

        active_tests_df = (
            pd.DataFrame(columns=["test_id"])
            if test_master_df.shape[0] == 0
            else test_master_df[test_master_df["is_active"] == True]
        )

        # Filter the stores only from the input filters
        annualrsvlifts,valid_sales_stores, _, _, stores_master_df,_, consideryearweeks,\
             message, success_flag = self._test_stores_features.data_extract(
            applicability_criteria=applicability_criteria,
            target_variable=target_variable,
            test_type=test_type,
            uploaded_file_df=uploaded_file_df,
        )
        if success_flag is False:
            message = "Not sufficient data found for the selected Filters"
            return (
                annualrsvlifts,
                valid_sales_stores,
                consideryearweeks,
                0,
                self._metadata["test_planning"]["margin_of_error"],
                self._metadata["test_planning"]["confidence_level"],
                self._metadata["test_planning"]["power_of_test"],
                message,
                success_flag,
            )

        standard_deviation = annualrsvlifts[target_variable + " Lift"].std()

        (
            num_of_teststores,
            _,
            success_flag,
        ) = self._test_stores_features.test_parameter_calculation(
            confidence_level=self._metadata["test_planning"]["confidence_level"],
            margin_of_error=self._metadata["test_planning"]["margin_of_error"],
            power_of_test=self._metadata["test_planning"]["power_of_test"],
            num_of_teststores=None,
            standard_deviation=standard_deviation,
        )
        if bypass_active_control_test == 0:
            max_week_data_available = self._sales_object.get_max_week_config_master(
                applicability_criteria
            )
            max_date_data_available = self._sales_object.convert_week_to_date(
                week=max_week_data_available
            )

            filtered_stores_df = (
                self._store_object.filter_active_test_control_stores(
                    stores_master_df=stores_master_df.copy(deep=True),
                    remove_type="both",
                    max_week_data_available=max_date_data_available,
                )
            )
        else:
            filtered_stores_df = stores_master_df
        # Considering only those stores which have continous sales in the last two years
        filtered_rsv_stores_df = filtered_stores_df[
            filtered_stores_df[self._storemstrmapping["partner_id"]].isin(
                annualrsvlifts[self._tarvarmapping["partner_id"]].unique()
            )
        ]

        message = "The number of teststores suggested for confidence level:{}, margin of error: {}\
             and power of test: {} are {}".format(
            self._metadata["test_planning"]["confidence_level"],
            self._metadata["test_planning"]["margin_of_error"],
            self._metadata["test_planning"]["power_of_test"],
            num_of_teststores,
        )

        if (self._test_id in active_tests_df["test_id"].values.tolist()) & (
            finalised_flag is not None
        ):
            if finalised_flag == 0:
                current_teststores = teststore_map_df[
                    teststore_map_df["test_id_id"] == self._test_id
                ]
                current_teststores["is_teststore"] = 1
                filtered_rsv_stores_df["is_teststore"] = 0
                teststores = pd.concat([current_teststores, filtered_rsv_stores_df])
                return (
                    teststores,
                    valid_sales_stores,
                    consideryearweeks,
                    num_of_teststores,
                    self._metadata["test_planning"]["margin_of_error"],
                    self._metadata["test_planning"]["confidence_level"],
                    self._metadata["test_planning"]["power_of_test"],
                    message,
                    True,
                )
            current_teststores = teststore_map_df[
                teststore_map_df["test_id_id"] == self._test_id
            ]
            current_teststores["is_teststore"] = 1
            teststores = current_teststores
            return (
                teststores,
                valid_sales_stores,
                consideryearweeks,
                num_of_teststores,
                self._metadata["test_planning"]["margin_of_error"],
                self._metadata["test_planning"]["confidence_level"],
                self._metadata["test_planning"]["power_of_test"],
                message,
                True,
            )
        filtered_rsv_stores_df["is_teststore"] = 0
        return (
            filtered_rsv_stores_df,
            valid_sales_stores,
            consideryearweeks,
            num_of_teststores,
            self._metadata["test_planning"]["margin_of_error"],
            self._metadata["test_planning"]["confidence_level"],
            self._metadata["test_planning"]["power_of_test"],
            message,
            True,
        )

    def _handle_control_per_store_attribute(self, applicability_criteria, control_stores, one_to_one=False)->Tuple[pd.DataFrame, str, bool]:
        if ("advanced_control_mapping" in applicability_criteria) and \
            (len(applicability_criteria["advanced_control_mapping"].keys())>0):
                control_per_store_attribute = applicability_criteria["advanced_control_mapping"]
        else:
            control_per_store_attribute = None
        control_stores, message, success_flag =  self._control_stores_features\
                                                ._handle_control_per_store_attribute(control_stores = control_stores,
                                                                                    one_to_one=one_to_one,
                                                                                    control_per_store_attribute=control_per_store_attribute)
        return control_stores, message, success_flag

    def _handle_control_stores_similarity(self, control_stores, applicability_criteria)->Tuple[pd.DataFrame, str, bool]:
        req_column = ['similarity_threshold', 'correlation_threshold']
        similarity = -1
        correlation = -1
        if len(set(req_column).intersection(set(applicability_criteria.keys()))) == len(req_column):
            similarity = applicability_criteria['similarity_threshold']
            correlation = applicability_criteria['correlation_threshold']
        elif "control_store_threshold" in self._config['feature_parameter']:
            temp = self._config['feature_parameter']['control_store_threshold']
            if not isinstance(temp, dict):
                return control_stores, "Wrong config!! config['feature_parameter']['control_store_threshold'] is not type dictionary", False
            if  len(set(req_column).intersection(set(temp.keys()))) != len(req_column):
                return control_stores, "Wrong config!! config['feature_parameter']['control_store_threshold'] missing keys {}".format(req_column),False
            correlation = temp['similarity_threshold']
            similarity = temp['correlation_threshold']
        control_stores.loc[(control_stores['Similarity_Measure'] < similarity) | (
                control_stores['Correlation'] < correlation), 'Checked_Flag'] = 0
        return control_stores, "Applied thresholds successfully!", True

    def identify_control_stores(self, teststores, target_variable, applicability_criteria, test_type,\
                                one_to_one=False, business_categories=[],reqcontrolstores=1, \
                                control_store_pool=None,len_control_pool=None, uploaded_file_df=None) \
                                -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        '''identify_control_stores'''
        if teststores is None or teststores.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(),"Please pass valid test stores", False
        message = ""
        if control_store_pool is not None:
            stores_req_sales = control_store_pool[:]
            stores_req_sales.extend(list(teststores[self._storemstrmapping['partner_id']].unique()))
        else:
            stores_req_sales = []

        reqcontrolstores = self._control_stores_features._get_max_required_control_stores(reqcontrolstores=reqcontrolstores,
                                                                             applicability_criteria = applicability_criteria)
        annualrsvlifts, valid_sales_stores, consideryearweeks,\
                _,stores_master_df, message, success_flag = self._control_stores_features.data_extract(applicability_criteria=applicability_criteria,
                                                                                        target_variable=target_variable,
                                                                                        store_list=stores_req_sales,
                                                                                        test_type=test_type,
                                                                                        uploaded_file_df=uploaded_file_df,
                                                                                        )
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(), message, False

        if (control_store_pool is not None)\
            and(valid_sales_stores[valid_sales_stores[self._storemstrmapping['partner_id']].isin(control_store_pool)].shape[0] == 0):
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(), "Control pool stores dont have continuous sales", False

        max_week_data_available = self._sales_object.get_max_week_config_master(applicability_criteria)
        max_date_data_available = self._sales_object.convert_week_to_date(week=max_week_data_available)
        sales_weeks = self._sales_object.get_sales_weeks(applicability_criteria)
        sales_lifts_sales_weeks = self._sales_object.get_lift_sales_weeks(applicability_criteria)
        compare_variables = self._get_test_vs_control_compare(applicability_criteria)

        """Filter the stores with active stores"""

        control_stores, message2, success_flag = self._control_stores_features.identify_control_stores_util(teststores = teststores, business_categories=business_categories,
                                                                                                            stores_master_df=stores_master_df,
                                                                                                            annualrsvliftdf=annualrsvlifts,
                                                                                                            consideryearweeks=consideryearweeks,
                                                                                                            valid_sales_stores=valid_sales_stores,
                                                                                                            summary_sales_weeks=sales_lifts_sales_weeks,
                                                                                                            sales_weeks=sales_weeks,
                                                                                                            compare_variables=compare_variables,
                                                                                                            target_variable=target_variable,
                                                                                                            max_date_data_available=max_date_data_available,
                                                                                                            control_store_pool=control_store_pool,
                                                                                                            reqcontrolstores=reqcontrolstores)


        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(), message, False

        message = message2+'\n'+message
        control_stores, message3, success_flag = self._handle_control_per_store_attribute(applicability_criteria = applicability_criteria,
                                                                    control_stores = control_stores,
                                                                    one_to_one=one_to_one)
        message = message3+'\n'+message

        if success_flag is False:
            return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores,\
                            control_store_pool, message, success_flag

        control_stores, message4, success_flag = self._handle_control_stores_similarity(control_stores = control_stores,
                                                                applicability_criteria=applicability_criteria)
        message = message4+'\n'+message

        if success_flag is False:
            return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores,\
                    control_store_pool,message, True
        if control_store_pool is not None:
            control_store_pool = list(valid_sales_stores[valid_sales_stores[self._storemstrmapping['partner_id']]\
                                    .isin(control_store_pool)][self._storemstrmapping['partner_id']]\
                                    .unique())
        else:
            control_store_pool = []

        if len(control_store_pool)>0:
            message5 = "Out of {} Control Stores in Pool, {} of them are valid control stores".format(
                len_control_pool, len(control_store_pool))
            return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores,\
                    control_store_pool,message5+'\n'+message, True

        return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores,\
                control_store_pool,message, True
        #control_store_pool its a list

    def average_weekly_target_similarity_correlation(self, test_control_data, target_variable, applicability_criteria, business_categories = [])->Tuple[dict, pd.DataFrame, str, bool]:
        """
            average_weekly_target_similarity_correlation
        """
        test_measurement_table = self._store_object.read_test_measurement_table_by_test_ids(
            test_id=self._test_id)

        test_control_mapping_stores = self._store_object.read_control_store_by_test_ids(test_id=self._test_id)
        teststore_map_df = self._store_object.read_test_map_table_by_test_ids(test_id=self._test_id)

        # Getting the parameters from the Test Measurement Table based on Testid
        target_variable = str(test_measurement_table["mesmetric_name"].values[0])
        stores = list(test_control_data["Test_store_" + self._tarvarmapping["partner_id"]].unique())
        stores.extend(list(test_control_data[self._storemstrmapping["partner_id"]].unique()))
        prewindow_target_data, postwindow_target_data, _,\
                _, message, success_flag = self._sales_object.get_weekly_targetvariables_data(target_variable=target_variable,
                                                                                                    test_measurement_df=test_measurement_table,
                                                                                                    stores=stores,
                                                                                                    applicability_criteria=applicability_criteria)


        if success_flag is False:
            return dict(), pd.DataFrame(), message, success_flag
        test_control_stores = test_control_mapping_stores[test_control_mapping_stores["test_id_id"] == int(
            self._test_id)]
        test_control_stores = test_control_stores[
            test_control_stores["Test_store_" + self._storemstrmapping["partner_id"]].isin(
                teststore_map_df["teststore_id"].values.tolist())]
        # test group preperiod weekly target data

        metrics_dict, combined_avg, message, success_flag = self._control_stores_features.test_control_similarity_measurement(test_control_pairs = test_control_data,
                                                                                                                                prewindow_target_data=prewindow_target_data,
                                                                                                                                target_variable=target_variable,
                                                                                                                                postwindow_target_data=postwindow_target_data)
        return metrics_dict, combined_avg, message, success_flag


    def control_store_summary(self, test_type, test_control_mapping_stores, business_categories, target_variable,applicability_criteria, uploaded_file_df=None)->Tuple[dict, dict, dict, str, bool]:

        '''control_store_summary'''

        if test_control_mapping_stores is None or test_control_mapping_stores.shape[0] == 0:
            return dict(), dict(), dict(), dict(), "Please pass appropriate parameters", False
        test_master_table = self._store_object.read_test_master_table_by_test_ids(
            test_id=self._test_id)

        # Stores Master File
        # Need to make Change here as per interaction with Database (Starting from here)
        stores = list(test_control_mapping_stores["Test_store_"+self._storemstrmapping["partner_id"]].unique())
        stores.extend(list(test_control_mapping_stores[self._storemstrmapping["partner_id"]].unique()))

        ### Deb please add filter in django model here to filter the StoreMaster for StoreId in stores
        stores_master_df = self._store_object.filter_population(applicability_criteria = applicability_criteria,
                                                                            storelist=stores,
                                                                            uploaded_file_df = uploaded_file_df)
        if stores_master_df.shape[0] == 0:
            return dict(), dict(), dict(), "Stores information is not found", False
        # Need to make Change here as per interaction with Database (to here)

        sales_weeks = self._sales_object.get_sales_weeks(applicability_criteria)
        summary_sales_weeks = self._sales_object.get_summary_sales_weeks(applicability_criteria)
        compare_variables = self._get_test_vs_control_compare_sum(applicability_criteria)

        weekly_target_variables_file, consideryearweeks, message, success_flag =\
             self._sales_object.get_total_weekly_target_data(test_master_df =test_master_table, target_variable = target_variable,\
                test_type = test_type,sales_week = sales_weeks, stores_list = stores,applicability_criteria = applicability_criteria)


        variables_metrics_dict, feature_bounds_dict, pvalue_dict, message, success_flag =\
             self._control_stores_features.control_summary_util(stores_master_df = stores_master_df,\
                test_control_mapping = test_control_mapping_stores,summary_sales_weeks = summary_sales_weeks,\
                consideryearweeks = consideryearweeks,weekly_target_sales = weekly_target_variables_file,\
                business_categories = business_categories,compare_variables = compare_variables,\
                target_variable = target_variable)

        return variables_metrics_dict, feature_bounds_dict, pvalue_dict, message, success_flag

    def manual_upload_control_store_pool(self, control_store_pool_data, teststores, target_variable,\
                                        applicability_criteria,test_type, business_categories=[],
                                        reqcontrolstores=1,  one_to_one=False, uploaded_file_df=None)\
                                        ->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:


        '''manual_upload_control_store_pool'''
        if 'store_identifier_attribute' not in applicability_criteria:
            print("Store identififer not passed")
            applicability_criteria['store_identifier_attribute'] = self._storemstrmapping['partner_id']
        relative_path = self._config['filePath']['controlStore_Pool']['file_name']
        control_stores_pool_ref = pd.read_excel(check_path(relative_path))
        # represents the column name
        store_identifier = self._metadata["test_planning"]["upload_controlstores_identifier"]
        # Represents the column value type
        store_identifier_type = applicability_criteria['store_identifier_attribute']
        # User uploaded test-control pairs
        control_stores_pool = control_store_pool_data.copy(deep=True)
        message, success_flag = self._store_object.validate_uploaded_stores_format(
            reference_file=control_stores_pool_ref, uploaded_file=control_stores_pool, columns=list(self._metadata['test_planning']['control_storespool_columns'].items()))

        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(),message, False

        control_stores_details, message2, success_flag2 = self._store_object.validate_uploaded_presence_store_master(uploaded_stores=control_stores_pool,
                                                                                                                    store_identifier=store_identifier,
                                                                                                                    applicability_criteria=applicability_criteria)
        message = message2 + '\n' + message
        if success_flag2 is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(),message, False
        if control_stores_details.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(),"Stores uploaded are not found in Store master table\n"+message, False
        max_week_data_available = self._sales_object.get_max_week_config_master(applicability_criteria)
        max_date_data_available = self._sales_object.convert_week_to_date(week=max_week_data_available)

        temp_check, message3, success_flag3 = self._store_object.validate_uploaded_stores_active_stores(control_stores_details.copy(deep=True), max_date_data_available = max_date_data_available, active_stores_filter_type=self._config["feature_parameter"]["active_store_filter_type"])
        message = message3 + '\n' + message
        if success_flag3 is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),list(),message,False
        if temp_check.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),list(),"All stores are active in other tests",False
        message = "Uploaded stores that are actively participating in test: {}\n".format(set(control_stores_details[store_identifier_type].values.tolist())-set(temp_check[store_identifier_type].values.tolist()))+ message

        test_store_map = self._store_object.read_test_map_table_by_test_ids(test_id=self._test_id)

        test_store_details = self._store_object.get_uploaded_stores_info(
                                                                stores_list = list(test_store_map['teststore_id'].unique()),
                                                                applicability_criteria=applicability_criteria)

        common_stores = control_stores_details[control_stores_details[store_identifier_type].isin(test_store_details[store_identifier_type].unique())]
        if common_stores.shape[0] == control_stores_details.shape[0]:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), list(), "All uploaded control store pool are same as test stores. Control pool and test stores cannot be same", False

        message = "Test stores found in pool: {}\n".format(set(common_stores[store_identifier_type].unique()))+message

        control_stores_details = control_stores_details[~control_stores_details[store_identifier_type].isin(common_stores[store_identifier_type].unique())]

        control_stores, stores_master_df, annualrsvlifts, valid_sales_stores, control_store_pool, message4, success_flag = self.identify_control_stores(
                                                        teststores = teststores,
                                                        target_variable = target_variable,
                                                        applicability_criteria = applicability_criteria,
                                                        test_type = test_type,
                                                        one_to_one=one_to_one,
                                                        business_categories=business_categories,
                                                        reqcontrolstores=reqcontrolstores,
                                                        control_store_pool=list(control_stores_details[self._storemstrmapping["partner_id"]].unique()),
                                                        len_control_pool=control_store_pool_data[store_identifier].nunique(),
                                                        uploaded_file_df=uploaded_file_df,
                                                        )
        return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores, control_store_pool, message4+'\n'+message, True


    def recompute_control_stores(self, test_control_stores, target_variable, business_categories,include_cbu_features, reqcontrolstores,
                            test_type, applicability_criteria,
                            uploaded_file_df=None)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, str, bool]:

        compare_variables = self._get_test_vs_control_compare(applicability_criteria)
        annualrsvlifts, valid_sales_stores, consideryearweeks,\
                _,stores_master_df, message, success_flag = self._control_stores_features.data_extract(applicability_criteria=applicability_criteria,
                                                                                        target_variable=target_variable,
                                                                                        store_list=[],
                                                                                        test_type=test_type,
                                                                                        uploaded_file_df=uploaded_file_df,
                                                                                        )
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), message, False

        # stores_master_df = filter_active_test_control_stores(stores_master_df, config=config)
        max_week_data_available = self._sales_object.get_max_week_config_master(applicability_criteria)
        max_date_data_available = self._sales_object.convert_week_to_date(
            week=max_week_data_available)
        control_stores, message, success_flag = self._control_stores_features.recompute_control_stores_util(target_variable = target_variable,
                                                                                                            reqcontrolstores = reqcontrolstores,
                                                                                                            test_control_stores = test_control_stores,
                                                                                                            stores_master_df = stores_master_df,
                                                                                                            max_date_data_available = max_date_data_available,
                                                                                                            annualrsvliftdf = annualrsvlifts,
                                                                                                            valid_sales_stores = valid_sales_stores,
                                                                                                            consideryearweeks = consideryearweeks,
                                                                                                            compare_variables = compare_variables,
                                                                                                            include_cbu_features = include_cbu_features,
                                                                                                            business_categories = business_categories)
        return control_stores, stores_master_df, annualrsvlifts, valid_sales_stores, message, success_flag

    def manual_teststore_controlstore_upload(self, target_variable, test_control_store_data, test_type,
                                    applicability_criteria, uploaded_file_df=None, business_categories = None)-> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str, bool]:

        '''manual_teststore_controlstore_upload'''
        if 'store_identifier_attribute' not in applicability_criteria:
            applicability_criteria['store_identifier_attribute'] = self._storemstrmapping['partner_id']
        store_features = self._get_test_vs_control_compare(applicability_criteria)
        relative_path = self._config["filePath"]["controlStore"]["file_name"]
        #test control stores reference file
        test_control_stores_ref = pd.read_excel(check_path(relative_path))
        # User uploaded test-control pairs
        test_control_stores = test_control_store_data.copy(deep=True)

        # represents the column name
        control_store_identifier = self._metadata["test_planning"]["upload_controlstores_identifier"]
        test_store_identifier = self._metadata["test_planning"]["upload_teststores_identifier"]
        # Represents the column value type
        store_identifier_type = applicability_criteria['store_identifier_attribute']

        columns_req = list(self._metadata['test_planning']['user_testcontrolstores_columns'].items())
        message, success_flag = self._store_object.validate_uploaded_stores_format(
                                            reference_file=test_control_stores_ref,
                                            uploaded_file=test_control_store_data,
                                            columns=columns_req)

        if success_flag is False:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(), "The uploaded file/data format doesn't match with the expected format", False
        """Validate there should not be an intersection between test and control stores"""
        if len(set(test_control_stores[test_store_identifier].unique()).intersection(set(test_control_stores[control_store_identifier].unique())))>=1:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),\
                 'Test and control stores cannot have common stores {}'.format(set(test_control_stores[test_store_identifier].unique()).intersection(set(test_control_stores[control_store_identifier].unique()))), False

        test_control_store_list = list(test_control_stores[test_store_identifier].unique())
        test_control_store_list.extend(list(test_control_stores[control_store_identifier].unique()))
        test_control_store_df = pd.DataFrame(data=test_control_store_list, columns=[store_identifier_type])


        test_control_stores_details, message2, success_flag = self._store_object.validate_uploaded_presence_store_master(
                                                    uploaded_stores=test_control_store_df,
                                                    store_identifier=store_identifier_type,
                                                    applicability_criteria=applicability_criteria)
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), message2+'\n'+message, False

        test_stores_details = test_control_stores_details[test_control_stores_details[store_identifier_type].isin(test_control_stores[test_store_identifier].unique())]
        control_stores_details = test_control_stores_details[test_control_stores_details[store_identifier_type].isin(test_control_stores[control_store_identifier].unique())]

        message = message2+'\n'+message

        test_store_map = self._store_object.read_test_map_table_by_test_ids(test_id=self._test_id)

        if len(set(test_store_map['teststore_id'].unique()).intersection(test_stores_details[self._storemstrmapping['partner_id']].unique())) == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "All uploaded test stores are different from saved test stores\n"+message, False
        if len(set(test_store_map['teststore_id'].unique()).intersection(test_stores_details[self._storemstrmapping['partner_id']].unique())) < test_store_map['teststore_id'].nunique():
            message3 = "Please add control stores for these test stores: {}".format(stores_master_df[stores_master_df[self._storemstrmapping['partner_id']].isin(set(test_store_map['teststore_id'].unique())-set(test_stores_details[self._storemstrmapping['partner_id']].unique()))][store_identifier_type].unique())
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), message3+'\n'+message, False


        message = "Extra test stores uploaded (will not be considered): {}\n".format(set(test_stores_details[store_identifier_type].unique()) - set(test_stores_details[test_stores_details[self._tarvarmapping['partner_id']].isin(test_store_map['teststore_id'].unique())][store_identifier_type].unique())) + message

        test_stores_details = test_stores_details[test_stores_details[self._storemstrmapping['partner_id']].isin(test_store_map['teststore_id'])]

        message = "Uploaded Control Stores that dont have details: {}\n".format(set(test_control_stores[control_store_identifier].unique())-set(control_stores_details[store_identifier_type].unique()))+message

        test_control_store_list = list(test_stores_details[self._storemstrmapping['partner_id']].unique())
        test_control_store_list.extend(list(control_stores_details[self._storemstrmapping['partner_id']].unique()))
        annualrsvlifts, valid_sales_stores,consideryearweeks,_,\
             stores_master_df, message2, success_flag = self._control_stores_features.data_extract(applicability_criteria=applicability_criteria,
                                                                                    target_variable=target_variable,
                                                                                    store_list=test_control_store_list,
                                                                                    test_type=test_type,
                                                                                    uploaded_file_df=uploaded_file_df)
        message = message2+'\n'+message
        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), message, False
        if annualrsvlifts.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "Lift of stores could not be calculated; please check stores uploaded or time period selected \n"+message, False

        max_week_data_available = self._sales_object.get_max_week_config_master(applicability_criteria)
        max_date_data_available = self._sales_object.convert_week_to_date(week=max_week_data_available)
        check_control, message3, _ = self._store_object.validate_uploaded_stores_active_stores(control_stores_details.copy(deep=True),
                                                max_date_data_available = max_date_data_available,
                                                active_stores_filter_type=self._config["feature_parameter"]["active_store_filter_type"])
        message = message3+'\n'+message
        if check_control.shape[0] == 0:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),"All control stores uploaded are participating as test store in other tests\n"+message, False
        message = "Uploaded control stores that are actively participating in other tests: {}\n".format(set(control_stores_details[store_identifier_type].unique())-set(check_control[store_identifier_type].unique())) + message
        control_stores_details = check_control

        #creating population stores which is mix of test and avaiable control stores only
        filtered_stores_df = test_stores_details
        filtered_stores_df = filtered_stores_df.append(control_stores_details)
        ##Join test store and control store information with test_control_store uploaded
        test_control_stores.rename(columns={test_store_identifier:'Test_store_'+store_identifier_type, control_store_identifier:'Control_store_'+store_identifier_type}, inplace=True)
        test_stores_details.rename(columns = {self._tarvarmapping['partner_id']:'Test_store_'+self._tarvarmapping['partner_id'], store_identifier_type:'Test_store_'+store_identifier_type}, inplace=True)
        control_stores_details.rename(columns = {self._tarvarmapping['partner_id']:'Control_store_'+self._tarvarmapping['partner_id'], store_identifier_type:'Control_store_'+store_identifier_type}, inplace=True)
        # test_control_stores.rename(columns={'Test_store_'+self._tarvarmapping['partner_id']:'Test_store_'+store_identifier_type, 'Control_store_'+self._tarvarmapping['partner_id']:'Control_store_'+store_identifier_type}, inplace=True)
        req_test_columns = set(['Test_store_'+store_identifier_type, 'Test_store_'+self._tarvarmapping['partner_id']])
        req_control_columns = set(['Control_store_'+store_identifier_type, 'Control_store_'+self._tarvarmapping['partner_id']])
        test_control_stores = test_control_stores.merge(test_stores_details[req_test_columns], how='inner', on='Test_store_'+store_identifier_type)
        test_control_stores = test_control_stores.merge(control_stores_details[req_control_columns], how='inner', on='Control_store_'+store_identifier_type)


        filtercolumns = [self._tarvarmapping["partner_id"],
                            target_variable + ' Year 1',
                            target_variable + ' Year 2',
                            target_variable + ' Lift']
        if self._config['feature_parameter']["is_product_present"] is 1:
            filtercolumns.extend(["CBU_Category_" + target_variable + ' Year 1',
                                    "CBU_Category_" + target_variable + ' Year 2',
                                    "CBU_Category_" + target_variable + " Lift"])
        filtered_rsv_stores_df = filtered_stores_df.merge(annualrsvlifts[filtercolumns],
                                                            left_on=self._storemstrmapping["partner_id"],
                                                            right_on=self._tarvarmapping["partner_id"])
        message = "Uploaded control stores that dont have continuous sales: {}\n".format(set(control_stores_details["Control_store_"+store_identifier_type].unique())-set(filtered_rsv_stores_df[store_identifier_type].unique())) + message



        # Test & Control Stores Characteristics from storemaster df
        control_test_pairs, message4, success_flag = self._control_stores_features.test_control_upload_util(filtered_rsv_stores_df = filtered_rsv_stores_df,valid_sales_stores = valid_sales_stores,
                                                                                stores_master_df = stores_master_df,
                                                                                consideryearweeks = consideryearweeks,
                                                                                target_variable = target_variable,
                                                                                applicability_criteria = applicability_criteria,
                                                                                store_features = store_features,
                                                                                test_control_stores = test_control_stores)
        # control_test_pairs = control_test_pairs[control_test_pairs['Test_store_'+storemstrmapping['partner_id']].isin(test_store_map['Test_store_'+storemstrmapping['partner_id']].unique())]
        message = "Out of {} Test-Control Pairs, {} of them are valid\n".format(test_control_store_data.shape[0],control_test_pairs.shape[0]) + message4 + '\n' +message
        return control_test_pairs,stores_master_df, annualrsvlifts, message, success_flag

