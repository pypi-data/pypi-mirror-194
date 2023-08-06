"""
    About module: All customizations done for UK market wrt Sales and Store functions

    Classes:
        FastStoresUK
        FastSalesUK
"""
from datetime import datetime
from typing import Tuple

import pandas as pd
from DSCode.library.sql.sales_master import Sales
from DSCode.library.sql.stores_master import Stores


class FastStoresUK(Stores):
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
        self._config = config
        super().__init__(
            config=self._config, test_id=test_id
        )
    def filter_population(self, applicability_criteria, \
                storelist=None, uploaded_file_df=None) -> pd.DataFrame:
        if storelist is None:
            storelist = []
        stores_master_df = super().filter_population(
                        storelist=storelist,
                        applicability_criteria=applicability_criteria,
                        uploaded_file_df=uploaded_file_df
        )

        if applicability_criteria["test_type"] != "RTM Impact Test":
            stores_master_df = stores_master_df[
                stores_master_df['Customer_Status'].isin(applicability_criteria['Customer_Status'])
            ]
        return stores_master_df

    def get_filtered_stores(self, applicability_criteria) -> pd.DataFrame:
        applicability_criteria["banners"].append("")
        applicability_criteria["segments"].append("")
        applicability_criteria["store_segments"].append("")
        applicability_criteria["territories"].append("")
        applicability_criteria["Customer_Status"].append("")

        filter_store_query = """Select * from {table}
                            where Customer_Group IN {banners}
                            and Sub_Channel IN {segments}
                            and Customer_Chain IN {store_segments}
                            and Territory IN {territories}
                            and Customer_Status IN {Customer_Status}"""

        return self.execute_sql_query(filter_store_query, data={
            "table": self._config['tables']['store_mstr'],
            "banners": tuple(applicability_criteria["banners"]),
            "segments": tuple(applicability_criteria["segments"]),
            "store_segments": tuple(applicability_criteria["store_segments"]),
            "territories": tuple(applicability_criteria["territories"]),
            "Customer_Status": tuple(applicability_criteria["Customer_Status"])
            })

    def get_uploaded_stores_info(self, stores_list, applicability_criteria) -> pd.DataFrame:
        """Returns the store information of uploaded population"""

        # applicability_criteria["store_value"] = tuple(stores_list)
        query_uploaded_population = "SELECT * FROM {table} WHERE Customer_Number IN {store_value}"
        # table=applicability_criteria["store_table"]

        return self.execute_sql_query(query_uploaded_population, data={
                "table": self._config['tables']['store_mstr'],
                "store_value": tuple(stores_list)})

class FastSalesUK(Sales):
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
        self._config = config
        super().__init__(
            config=config, test_id=test_id
        )
    def get_cbu_sales(self, stores, applicability_criteria, weeks) -> pd.DataFrame:
        cbu_lvl_query = (
            "Select CBU_Lvl1_Mapping from {table} where CBU_Lvl1 IN {cat_list}"
        )
        data = {
            "cat_list": tuple(applicability_criteria["cbu_lvl1_categories"]),
            "table": self._config["tables"]["cbu_mstr"],
        }

        cbu_lvl1_mapping_list = pd.DataFrame(self.execute_sql_query(cbu_lvl_query, data=data))
        cbu_lvl1_mapping_list = cbu_lvl1_mapping_list["CBU_Lvl1_Mapping"].to_list(
        )

        pack_format_query = (
            "Select Pack_Format_Mapping from {table} where Pack_Format IN {cat_list}"
        )
        data = {
            "cat_list": tuple(applicability_criteria["pack_lvl_categories"]),
            "table": self._config["tables"]["pack_mstr"],
        }
        pack_format_mapping_list = pd.DataFrame(
            self.execute_sql_query(pack_format_query, data=data))
        pack_format_mapping_list = pack_format_mapping_list["Pack_Format_Mapping"].to_list()
        pack_format_mapping_list.append(-1)
        cbu_lvl1_mapping_list.append(-1)

        customer_list = stores
        sqlquery = """SELECT Customer_Group,Customer_Number, Week, SUM(RSV) as RSV, SUM(Volume) as Volume
                        FROM {table}
                        WHERE Week IN {weeks_val} AND CBU_Lvl1_Mapping IN {cbu_lvl_val}
                        AND Pack_Format_Mapping IN {pack_format_val} AND Customer_Number IN {stores_val}
                        GROUP By Customer_Group, Customer_Number, Week """
        data = {
            "table": self._config["tables"]["weekly_mstr"],
            "weeks_val": tuple(weeks),
            "cbu_lvl_val": tuple(cbu_lvl1_mapping_list),
            "pack_format_val": tuple(pack_format_mapping_list),
            "stores_val": tuple(customer_list),
        }

        return pd.DataFrame(self.execute_sql_query(sqlquery, data=data))
    def get_overall_sales(self, stores, applicability_criteria, weeks):

        sqlquery = """SELECT Customer_Group,Customer_Number, Week, SUM(RSV) as RSV,
                            SUM(Volume) as Volume,imputed
                        FROM {weekly_mstr_table}
                        WHERE Week IN {weeks_val} AND Customer_Number IN {stores_val}
                        GROUP By Customer_Group, Customer_Number, Week,imputed"""

        return pd.DataFrame(self.execute_sql_query(sqlquery,
                                data={"weekly_mstr_table": self._config['tables']['weekly_mstr'],
                                        "weeks_val": tuple(weeks), "stores_val": tuple(stores)}))

    def get_valid_weekly_target_data(self, stores, applicability_criteria,\
         target_variable, test_master_df,test_type, sales_week,\
             consideryearweeks=None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        prewindow_start = datetime.strptime(test_master_df["pre_start"]\
                                .values[0], '%Y-%m-%d').date()
        prewindow_end = datetime.strptime(test_master_df["pre_end"]\
            .values[0], '%Y-%m-%d').date()
        postwindow_start = datetime.strptime(test_master_df["testwin_start"]\
            .values[0], '%Y-%m-%d').date()
        postwindow_end = datetime.strptime(test_master_df["testwin_end"]\
            .values[0], '%Y-%m-%d').date()

        if test_type == "RTM Impact Test":
            pre_window_yearweeks = self.find_weeks(prewindow_start,
                                                   prewindow_end)

            post_window_yearweeks = self.find_weeks(postwindow_start,
                                                    postwindow_end)
            max_week_data_available = self.get_max_week_config_master(
                applicability_criteria)

            post_window_yearweeks = [
                i for i in post_window_yearweeks if i <= int(max_week_data_available)]
            if len(applicability_criteria['banners']) == 1 and\
                                     'POUNDLAND'.upper() in map(str.upper,
                                                        applicability_criteria['banners']):
                if 201739 in pre_window_yearweeks:
                    pre_window_yearweeks.remove(201739)
            all_weeks = set(pre_window_yearweeks).union(post_window_yearweeks)

            weekly_merged_level_sales, weekly_overal_level_sales, weekly_cbu_level_sales,consideryearweeks, \
                message, success_flag = super().get_valid_weekly_target_data(
                                            stores = stores,
                                            applicability_criteria=applicability_criteria,
                                            target_variable=target_variable,
                                            test_master_df = test_master_df,
                                            test_type = test_type,
                                            sales_week = sales_week,
                                            consideryearweeks = all_weeks)

            return weekly_merged_level_sales, weekly_overal_level_sales, weekly_cbu_level_sales,consideryearweeks, \
                message, success_flag
        else:
            yearweeks = self.find_last104_weeks_from_baseline_end(prewindow_end)
            if len(applicability_criteria['banners']) == 1 \
                and 'POUNDLAND'.upper() in map(str.upper, applicability_criteria['banners']):
                if 201739 in yearweeks:
                    yearweeks.remove(201739)
            yearweeks.sort(reverse=True)
            consideryearweeks = yearweeks[:sales_week]
            consideryearweeks.sort(reverse=False)
            weekly_merged_level_sales, weekly_overal_level_sales, weekly_cbu_level_sales,_, \
                message, success_flag = super().get_valid_weekly_target_data(
                            stores = stores,
                            applicability_criteria=applicability_criteria,
                            target_variable=target_variable,
                            test_master_df = test_master_df,
                            test_type = test_type,
                            sales_week = sales_week,
                            consideryearweeks = consideryearweeks)
        return weekly_merged_level_sales, weekly_overal_level_sales, weekly_cbu_level_sales,consideryearweeks, \
                message, success_flag

    def get_annual_rsv_lifts(self, target_variable, test_master_df, stores,\
         applicability_criteria, test_type) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list, str, bool]:
        """
            get_annual_rsv_lifts
        """

        # Getting the the target varaibles file
        sales_week = self.get_sales_weeks(applicability_criteria)
        sales_lifts_sales_weeks = self.get_lift_sales_weeks(applicability_criteria)

        weekly_ovrl_cbu_sales,weekly_overall_sales, weekly_cbu_sales, consideryearweeks,\
             message, success_flag = self.get_valid_weekly_target_data(
                        stores = stores,
                        applicability_criteria=applicability_criteria,
                        target_variable=target_variable,
                        test_master_df = test_master_df,
                        test_type = test_type,
                        sales_week = sales_week)

        if success_flag is False:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), consideryearweeks, message, False

        if test_type == "RTM Impact Test":
            weeks1 = consideryearweeks[0]
            weeks2 = consideryearweeks[1]
        else:
            weeks1 = consideryearweeks[:sales_lifts_sales_weeks]
            weeks2 = consideryearweeks[sales_lifts_sales_weeks:]

        annualrsvdatamerged, _, success_flag = self\
            ._lift_calculation_util(weekly_sales = weekly_ovrl_cbu_sales,
                                    first_half_weeks=weeks1,
                                    second_half_weeks=weeks2,
                                    target_variable=target_variable)
        return annualrsvdatamerged, weekly_ovrl_cbu_sales,weekly_overall_sales, weekly_cbu_sales,\
             consideryearweeks, "Annual Lift calculated Successfully!", True
