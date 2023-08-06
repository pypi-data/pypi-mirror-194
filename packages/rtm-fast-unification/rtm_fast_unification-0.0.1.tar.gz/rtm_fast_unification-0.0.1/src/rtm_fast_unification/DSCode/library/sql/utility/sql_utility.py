import threading
from datetime import timedelta, datetime
from DSCode.common_function import run_query
import numpy as np
import pandas as pd
from typing import final, Tuple

class SqlUtility:
    """This class is the parent class for database interaction with common functions"""
    def __init__(self, config):
        self._config = config
        self._tarvarmapping = self._config['store_mstr_columns']

    @final
    def set_config(self, config):
        """This function sets the config"""
        if self._config is None:
            self._config = config
    @final
    def find_weeks(self, start, end)->set:
        """
            find_weeks
        """
        list_year_weeks = []
        for day in range((end-start).days + 1):
            iso_date = (start+timedelta(days=day+1)).isocalendar()[:2]  # e.g. (2011, 52)
            yearweek = '{}{:02}'.format(*iso_date)  # e.g. "201152"
            list_year_weeks.append(int(yearweek))
        return sorted(set(list_year_weeks))

    @final
    def find_last104_weeks_from_baseline_end(self, baseline_end)->set:
        """
            find_last104_weeks_from_baseline_end
        """
        baseline_end_prev104weeks = baseline_end - timedelta(weeks=104)
        yearweeks_timeline = []
        for day in range((baseline_end-baseline_end_prev104weeks).days + 1):
            iso_date = (baseline_end_prev104weeks+timedelta(days=day+1)).isocalendar()[:2]
            yearweek = '{}{:02}'.format(*iso_date)  # e.g. "201152"
            yearweeks_timeline.append(int(yearweek))
        return sorted(set(yearweeks_timeline))

    def __get_data_threaded(self, return_data, thread_id, query, data):
        """To break the query on store identifier and run multiple threads"""
        return_data[thread_id] = run_query(query = query, params=data)
        return query

    def __create_batches(self, stores)->list:
        """Breaks the list of stores into chunks"""
        len_stores = len(stores)
        if (len_stores >= 2000) & (len_stores <= 5000):
            stores_splitted = list(np.array_split(stores, 2))
        elif len_stores > 5000:
            stores_splitted = list(np.array_split(stores, 4))
        else:
            stores_splitted = [stores]
        return stores_splitted

    def __fetch_data_threads(self, stores=None, query=None, data=None)->pd.DataFrame:
        """Function creates batches on store identifier and creates threads on queries"""
        return_data = {}
        list_thread = []
        # Loop over the batch of the stores
        for index, stores_sublist in enumerate(self.__create_batches(stores)):
            data["store_value"] = tuple(stores_sublist)
            thread = threading.Thread(target=self.__get_data_threaded,
                                        args=(return_data, index,query, data))
            # Start the thread
            thread.start()
            # add the thread to list
            list_thread.append(thread)

        for thread in list_thread:
            thread.join()
        # DataFrame to store the results
        results = pd.DataFrame()

        for thread in return_data.items():
            results = results.append(thread[1])
        return results

    @final
    def convert_week_to_date(self, week):
        """This function converts YYYYWW to datetime format"""
        return datetime.strptime(week + '-1', "%Y%W-%w").strftime("%Y-%m-%d")

    def execute_sql_query(self,query, data, stores=None)->pd.DataFrame:
        """This function will execute the query and fetch results"""

        data_req = data.copy()
        # if stores is None:
        if stores is not None:
            data_req['store_value'] = tuple(stores)
        return run_query(query=query,params=data_req)
        # return self.__fetch_data_threads(stores=stores, query=query,data=data_req)
    def _convert_sales_pre_post(self, weekly_sales, stores_date_info_dict_list, target_variable, test_control_map_table)->Tuple[pd.DataFrame, pd.DataFrame]:
        req_pre_sales = pd.DataFrame()
        req_post_sales = pd.DataFrame()
        for record in stores_date_info_dict_list:
            test_store_preperiod_sales = weekly_sales[(weekly_sales[self._tarvarmapping["partner_id"]] == int(record['Test_store_'+self._tarvarmapping["partner_id"]]))&(weekly_sales['Week'].isin(record['pre_period_weeks_required']))]
            control_store_preperiod_sales = weekly_sales[(weekly_sales[self._tarvarmapping["partner_id"]] == int(record[self._tarvarmapping["partner_id"]]))&(weekly_sales['Week'].isin(record['pre_period_weeks_required']))]
            test_control_pre_sales = test_store_preperiod_sales.merge(control_store_preperiod_sales, on=['Week'], how='outer')
            test_control_pre_sales.rename(columns={target_variable+'_x':'Test group - Pre Period Average',
                                                    target_variable+'_y':'Control group - Pre Period Average',
                                                self._tarvarmapping["partner_id"]+'_x':'Test_store_'+self._tarvarmapping["partner_id"],
                                                self._tarvarmapping["partner_id"]+'_y':self._tarvarmapping["partner_id"]}, inplace=True)
            test_control_pre_sales.fillna(0, inplace=True)
            test_control_pre_sales['Pre_period_weeks'] = len(record['pre_period_weeks_required'])

            req_pre_sales = req_pre_sales.append(test_control_pre_sales)

            control_store_postperiod_sales = weekly_sales[(weekly_sales[self._tarvarmapping["partner_id"]] == int(record[self._tarvarmapping["partner_id"]]))&(weekly_sales['Week'].isin(record['post_period_weeks_required']))]
            test_store_postperiod_sales = weekly_sales[(weekly_sales[self._tarvarmapping["partner_id"]] == int(record['Test_store_'+self._tarvarmapping["partner_id"]]))&(weekly_sales['Week'].isin(record['post_period_weeks_required']))]
            test_control_post_sales = test_store_postperiod_sales.merge(control_store_postperiod_sales, on=['Week'], how='outer')
            test_control_post_sales.rename(columns={target_variable+'_x':'Test group - Post Period Average',
                                                    target_variable+'_y':'Control group - Post Period Average',
                                                self._tarvarmapping["partner_id"]+'_x':'Test_store_'+self._tarvarmapping["partner_id"],
                                                self._tarvarmapping["partner_id"]+'_y':self._tarvarmapping["partner_id"]}, inplace=True)
            test_control_post_sales.fillna(0, inplace=True)
            test_control_post_sales['Post_period_weeks'] = len(record['post_period_weeks_required'])
            req_post_sales = req_post_sales.append(test_control_post_sales)

    
        return req_pre_sales, req_post_sales