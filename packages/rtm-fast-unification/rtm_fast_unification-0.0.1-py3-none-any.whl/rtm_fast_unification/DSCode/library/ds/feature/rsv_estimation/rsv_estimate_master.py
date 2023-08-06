"""
    About module: Handles all the features that are limited to RSV estimate
    Classes:
        RSVEstimate
"""

from datetime import datetime
from typing import Tuple
import pandas as pd


class RSVEstimate:
    """
    A class to represent features of RSVEstimate.
    ...

    Attributes
    ----------
    config : configuration present in config_data either for a region or overall
    region: key present in config
    sales_implementation : Object of sales class
    store_implementation : Object of store class

    Methods
    -------
    data_extract(): to calculate required sales/volume and get the store details in population
    calculate_rsv(): calculate the RSV value required and estimate number of stores in population
    get_breakeven_lift(): estimates the breakeven lift% value
    get_cost(): estimates the cost of implementing RTM activity if breakeven lift is known
    """

    def __init__(self, config, region, sales_implementation, store_implemenation) -> None:
        """
        Constructs all the necessary attributes for the rsv estimate object.

        Parameters
        ----------
            config : configuration present in config_data either for a region or overall
            region: key present in config
            sales_implementation : Object of sales class
            store_implementation : Object of store class
        """
        self._config = config[region] if region in config else config
        self._sales_implementation = sales_implementation
        self._store_implemenation = store_implemenation
        self._metadata = self._config["metadata"]["test_configuration"]
        self._tarvarmapping = self._config["weekly_target_variable"]
        self._storemstrmapping = self._config["store_mstr_columns"]
        self._rsvestimate = 0.0
        self._weekly_target_data = pd.DataFrame()
        self._breakevenliftpercentage = 0.0

    def data_extract(self, target_variable, timeframestart, timeframeend, storelist,
                     applicability_criteria,
                     uploaded_file_df=None) -> Tuple[pd.DataFrame, list, str, bool]:
        """
            About function
            --------------
            This function fetches the population stores details (filter selected/uploaded)
            along with calculating the required sales for the stores

            calls
            1) filter_population
            2) get_sales_calculate_rsv

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
            dataframe with CBU/overall sales,
            list of weeks on which sales is calculated,
            message
            success flag
        """
        if (timeframestart is not None) & (timeframeend is not None) \
                                        & (target_variable is not None):
            timeframeend_date = datetime.strptime(
                timeframeend, '%Y-%m-%d').date()
            timeframestart_date = datetime.strptime(
                timeframestart, '%Y-%m-%d').date()
            timeframe_weeknumbers = self._sales_implementation\
                .find_weeks(timeframestart_date, timeframeend_date)

            if len(storelist) == 0:
                stores_master_df = self._store_implemenation\
                    .filter_population(applicability_criteria=applicability_criteria,
                                       storelist=storelist,
                                       uploaded_file_df=uploaded_file_df)
                if stores_master_df.shape[0] == 0:
                    return pd.DataFrame(), list(),\
                        "No stores found matching population criteria", False

                storelist = list(
                    stores_master_df[self._storemstrmapping["partner_id"]].unique())
            self._weekly_target_data = pd.DataFrame()
            consideryearweeks = list()
            self._weekly_target_data, consideryearweeks \
                                            = self._sales_implementation.get_sales_calculate_rsv(
                                                stores=storelist,
                                                target_variable=target_variable,
                                                applicability_criteria=applicability_criteria,
                                                consideryearweeks=timeframe_weeknumbers)
            if self._weekly_target_data.shape[0] == 0:
                return self._weekly_target_data, consideryearweeks,\
                                        "No sales found between the timeperiod selected!!", False
            return self._weekly_target_data, consideryearweeks,\
                                        "Successfully Calculated!!", True
        return pd.DataFrame(), list(),\
            "One of these parameters is None timeframestart, timeframeend, target_variable", False

    def calculate_rsv(self, target_variable) -> Tuple[float, int]:
        """
            About function
            --------------
            This function calculates sum of sales on the target variable passed

            Parameters
            ----------
            target_variable: weekly sales column which is needs to be estimates (sales or volume),

            Return values
            -------
            total sales or volume,
            number of stores in population
        """
        store_count = self._weekly_target_data[self._tarvarmapping["partner_id"]].nunique(
        )
        self._rsvestimate = self._weekly_target_data[target_variable].sum().round(
            2)

        return self._rsvestimate, store_count

    def get_breakeven_lift(self, rsv_estimate, cost, num_of_teststores,
                           applicability_criteria, uploaded_file_df=None) -> Tuple[float, str]:
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
        if (rsv_estimate is not None) & (cost is not None):
            stores_master_df = self._store_implemenation.filter_population(
                                                applicability_criteria=applicability_criteria,
                                                uploaded_file_df=uploaded_file_df)
            print("Breakeven Lift - Population size: ", stores_master_df.shape)

            # Get the proportion of stores to be sampled for each banner
            if ("rawconvfactors" in self._metadata) & (len(self._metadata['rawconvfactors']) > 0):
                banner_label = self._tarvarmapping["banner"]
                partner_label = self._tarvarmapping["partner_id"]
                count_df = stores_master_df\
                            .groupby(banner_label)[partner_label]\
                            .count()\
                            .reset_index()\
                            .rename(columns={partner_label: "Count"})
                count_df["prop"] = count_df["Count"]/count_df["Count"].sum()
                count_df["stores_proportioned"] = count_df["prop"] * num_of_teststores
                count_df["stores_proportioned"] = count_df["stores_proportioned"].round(2)

                bannerwisestoresdict = dict(zip(count_df[banner_label],
                                                count_df["stores_proportioned"]))

                rawconvfactors = self._metadata["rawconvfactors"]
                numerator = sum([bannerwisestoresdict[k]*v for k,
                                v in rawconvfactors.items() if k in bannerwisestoresdict.keys()])
                denominator = sum(list(bannerwisestoresdict.values()))
                conversionfactor = numerator / denominator
            else:
                conversionfactor = 1
            cost = cost/conversionfactor
            self._breakevenliftpercentage = (cost/rsv_estimate)*100

            return self._breakevenliftpercentage, "Calculated breakeven lift successfully!!"

        return 0, "Parameter missing! Either Cost or RSV value not passed to function"

    def get_cost(self, rsv_estimate=None, breakevenliftpercentage=None) -> float:
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

        if (rsv_estimate is not None) & (breakevenliftpercentage is not None):
            self._rsvestimate = rsv_estimate
            cost = (breakevenliftpercentage*rsv_estimate)/100
            return round(cost, 2)
        return 0
