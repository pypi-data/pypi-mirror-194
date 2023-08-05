from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests
import concurrent.futures
import math
import time
import numpy as np
import json
import pandas as pd
import os
from tqdm import tqdm
from vcore.constants import *
from web3_multicall import Multicall
from retrying import retry
import logging


class Vcore:
    def __init__(self, bsc_url):
        self.web3 = Web3(Web3.HTTPProvider(bsc_url))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account_api = "https://api.venus.io/api/vToken/info?page="
        self.comptrollerAddress = "0xfd36e2c2a6789db23113685031d7f16329158384"
        self.multi = Multicall(self.web3.eth)
        self.pool_abi = "pool_abi"

    @staticmethod
    def load_abi(abi_name):
        abi_path = os.path.join(os.path.dirname(__file__), "abi", f"{abi_name}.py")
        with open(abi_path, "r") as f:
            abi = json.load(f)
        return abi

    @staticmethod
    def get_all_underlying():
        return UNDERLYING_ADDRESS

    @staticmethod
    def get_all_underlying_ddress():
        return list(UNDERLYING_ADDRESS.values())

    @staticmethod
    def get_all_market():
        return MARKET_ADDRESS

    @staticmethod
    def get__all_market_address():
        return list(MARKET_ADDRESS.values())

    @staticmethod
    def get_market_address_by_symbol(symbol):
        return MARKET_ADDRESS[symbol]

    @staticmethod
    def get_underlying_address_by_symbol(symbol):
        return UNDERLYING_ADDRESS[symbol]

    @staticmethod
    def get_chainlink_addresses():
        return CHAINLINK_ADDRESSES

    # Processing the data
    def __process_row(self, dataframe_row):
        if dataframe_row["symbol"] == "vDOGE":
            exchangeRateCurrent_adjusted = dataframe_row["exchangeRateCurrent"] / 1e18
            totalBorrows_adjusted = dataframe_row["totalBorrows"] / (
                10 ** dataframe_row["decimals"]
            )
            snapshot_borrow_bal = dataframe_row["snapshot_BorrowBalance"] / (
                10 ** dataframe_row["decimals"]
            )
        else:
            exchangeRateCurrent_adjusted = dataframe_row["exchangeRateCurrent"] / 1e28
            totalBorrows_adjusted = dataframe_row["totalBorrows"] / (
                10 ** (dataframe_row["decimals"] + 10)
            )
            snapshot_borrow_bal = dataframe_row["snapshot_BorrowBalance"] / (
                10 ** (dataframe_row["decimals"] + 10)
            )
        totalSupply_adjusted = (
            dataframe_row["totalSupply"]
            / (10 ** dataframe_row["decimals"])
            * exchangeRateCurrent_adjusted
        )
        snapshot_supply_token_bal = (
            dataframe_row["snapshot_vTokenBalance"]
            / (10 ** dataframe_row["decimals"])
            * exchangeRateCurrent_adjusted
        )

        utilization_rate = totalBorrows_adjusted / totalSupply_adjusted
        a1 = dataframe_row["multiplierPerBlock"] * dataframe_row["blocksPerYear"] / 1e18
        a2 = (
            dataframe_row["jumpMultiplierPerBlock"]
            * dataframe_row["blocksPerYear"]
            / 1e18
        )
        b = dataframe_row["baseRatePerBlock"] * dataframe_row["blocksPerYear"] / 1e18
        kink_readable = dataframe_row["kink"] / 1e18
        r = dataframe_row["reserveFactorMantissa"] / 1e18
        return pd.Series(
            [
                utilization_rate,
                a1,
                a2,
                b,
                kink_readable,
                r,
                snapshot_supply_token_bal,
                snapshot_borrow_bal,
            ]
        )

    @retry(stop_max_attempt_number=3)
    def __load_account_page(self, page_no):
        account_api = self.account_api + str(page_no)
        return json.loads(requests.get(account_api).text)

    def __fetch_information(self, market_address, user_address, market_abi_name):
        if not self.web3:
            return "Connection not successfull"
        tmp = {}
        market_contract = self.load_contract(market_abi_name, market_address)
        interestRateModel = market_contract.functions.interestRateModel().call()
        int_contract = self.web3.eth.contract(
            address=interestRateModel, abi=self.load_abi("init_abi")
        )

        calls = [
            market_contract.functions.decimals(),
            market_contract.functions.totalSupply(),
            market_contract.functions.totalBorrows(),
            market_contract.functions.borrowIndex(),
            market_contract.functions.exchangeRateCurrent(),
            market_contract.functions.exchangeRateStored(),
            market_contract.functions.getCash(),
            market_contract.functions.interestRateModel(),
            int_contract.functions.baseRatePerBlock(),
            int_contract.functions.blocksPerYear(),
            int_contract.functions.isInterestRateModel(),
            int_contract.functions.multiplierPerBlock(),
            market_contract.functions.isVToken(),
            market_contract.functions.name(),
            market_contract.functions.reserveFactorMantissa(),
            market_contract.functions.symbol(),
            market_contract.functions.totalBorrowsCurrent(),
            market_contract.functions.totalReserves(),
        ]

        result = self.multi.aggregate(calls)
        result = result.json["results"]

        tmp["decimals"] = result[0]["results"][0]
        tmp["totalSupply"] = result[1]["results"][0]
        tmp["totalBorrows"] = result[2]["results"][0]
        tmp["borrowIndex"] = result[3]["results"][0]
        tmp["exchangeRateCurrent"] = result[4]["results"][0]
        tmp["exchangeRateStored"] = result[5]["results"][0]
        tmp["getCash"] = result[6]["results"][0]
        snapshot = market_contract.functions.getAccountSnapshot(user_address).call()
        tmp["snapshot_error"] = snapshot[0]
        tmp["snapshot_vTokenBalance"] = snapshot[1]
        tmp["snapshot_BorrowBalance"] = snapshot[2]
        tmp["snapshot_exchangeRateMantissa"] = snapshot[3]
        tmp["interestRateModel"] = result[7]["results"][0]
        tmp["baseRatePerBlock"] = result[8]["results"][0]
        tmp["blocksPerYear"] = result[9]["results"][0]
        tmp["isInterestRateModel"] = result[10]["results"][0]
        try:
            tmp[
                "jumpMultiplierPerBlock"
            ] = int_contract.functions.jumpMultiplierPerBlock().call()
        except Exception as e:
            tmp["jumpMultiplierPerBlock"] = np.nan
        try:
            tmp["kink"] = int_contract.functions.kink().call()
        except Exception as e:
            tmp["kink"] = np.nan
        tmp["multiplierPerBlock"] = result[11]["results"][0]
        tmp["isVToken"] = result[12]["results"][0]
        tmp["name"] = result[13]["results"][0]
        tmp["reserveFactorMantissa"] = result[14]["results"][0]
        tmp["symbol"] = result[15]["results"][0]
        tmp["totalBorrowsCurrent"] = result[16]["results"][0]
        tmp["totalReserves"] = result[17]["results"][0]
        if tmp["symbol"] == "vDOGE":
            exchangeRateCurrent_adjusted = tmp["exchangeRateCurrent"] / 1e18
            tmp["snapshot_borrow_bal"] = tmp["snapshot_BorrowBalance"] / (
                10 ** tmp["decimals"]
            )
        else:
            exchangeRateCurrent_adjusted = tmp["exchangeRateCurrent"] / 1e28
            tmp["snapshot_borrow_bal"] = tmp["snapshot_BorrowBalance"] / (
                10 ** (tmp["decimals"] + 10)
            )
        tmp["snapshot_supply_token_bal"] = (
            tmp["snapshot_vTokenBalance"]
            / (10 ** tmp["decimals"])
            * exchangeRateCurrent_adjusted
        )
        result_df = pd.DataFrame(tmp, index=[1])
        return result_df

    def __format_prices_json(self, map, priceDict):
        tmp = {}
        tmp["chainlink_address"] = priceDict["contract_address"]
        tmp["asset"] = map[priceDict["contract_address"].lower()].replace("/USD", "")
        tmp["price_usd"] = priceDict["results"][1] / 10**8
        return pd.DataFrame(tmp, index=[0])

    def __format_collateral_flag(self, aDict):
        user_address = aDict["inputs"][0]["value"]
        if len(aDict["results"]) != 1:
            raise ValueError("Check here format_collateral_flag.")
        else:
            market_list = aDict["results"][0]["py/tuple"]
            if len(market_list) == 0:
                return pd.DataFrame(
                    columns=["user_address", "market_address", "isCollateral"]
                )
            else:
                df_list = []
                for m in market_list:
                    tmp = {}
                    tmp["user_address"] = user_address
                    tmp["market_address"] = m
                    tmp["isCollateral"] = 1
                    df_list.append(pd.DataFrame(tmp, index=[0]))
                result_df = pd.concat(df_list, ignore_index=True)
                return result_df

    def __extract_json_single_result(self, aDict):
        tmp = {}
        tmp["user_address"] = aDict["inputs"][0]["value"].lower()
        tmp["market_address"] = aDict["contract_address"].lower()
        results = aDict["results"]
        tmp["error"] = results[0]
        tmp["vTokenBalance"] = results[1]
        tmp["BorrowBalance"] = results[2]
        tmp["exchangeRateMantissa"] = results[3]
        result_df = pd.DataFrame(tmp, index=[0])

        return result_df

    def __extract_json_info(self, snapshot_result):
        executor = concurrent.futures.ThreadPoolExecutor(23)
        df_list = list(
            executor.map(
                lambda a: self.__extract_json_single_result(a),
                snapshot_result.json["results"],
            )
        )
        return pd.concat(df_list, ignore_index=True)

    def __create_df(self, aDict):
        tmp = {}
        tmp["market_address"] = aDict["contract_address"]
        tmp[aDict["function_name"]] = aDict["results"][0]
        return pd.DataFrame(tmp, index=[0])

    def __get_market_conversion(self, decimal_df, exchange_df, symbol_df):
        df = pd.merge(decimal_df, exchange_df, on="market_address")
        df = pd.merge(df, symbol_df, on="market_address")
        df["supply_factor"] = df.apply(
            lambda x: self.get_market_supply_factor(x), axis=1
        )
        df["borrow_divider"] = df.apply(
            lambda x: self.get_market_borrow_division(x), axis=1
        )
        return df

    def load_contract(self, abi_name, market_address=None, Symbol=None):
        """
        Load a smart contract instance with the given ABI and address or symbol.

        Args:
            abi_name (str): The name of the ABI file to load.
            market_address (Optional[str]): The Ethereum address of the market contract to load. If None, `Symbol` must be provided instead.
            Symbol (Optional[str]): The symbol of the market contract to load. If None, `market_address` must be provided instead.

        Returns:
            An instance of the `web3.eth.Contract` class representing the smart contract.

        Raises:
            ValueError: If both `market_address` and `Symbol` are None.
            ValueError: If no market contract can be found for the given symbol.
            ConnectionError: If the web3 connection is not successful.
            FileNotFoundError: If the ABI file cannot be found.
        """

        if not self.web3:
            return "Connection not successfull"
        if not market_address and not Symbol:
            return "Provide address or symbol"
        if Symbol:
            market_address = self.getMarketAddressBySymbol(Symbol)
        abi = self.load_abi(abi_name)
        return self.web3.eth.contract(
            address=Web3.toChecksumAddress(market_address), abi=abi
        )

    def get_asset_prices(self, chainlink_map):
        """
        Fetches the latest prices of assets from the Chainlink oracle network,
        using the provided `chainlink_map` to determine which asset contracts to query.

        Args:
        - `chainlink_map` (dict): A dictionary where the keys are the addresses of the Chainlink
            price feed contracts, and the values are the symbols of the assets being tracked.

        Returns:
        - `prices_df` (pandas.DataFrame): A DataFrame containing the latest prices for each asset,
            with columns for the asset symbol, price, and timestamp.
        """
        cl_contracts = []
        for address in chainlink_map.keys():
            cl_contracts.append(self.load_contract("chainlink", address))
        calls = []
        for contract in cl_contracts:
            try:
                calls.append(contract.functions.latestRoundData())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        prices_df = pd.concat(
            [
                self.__format_prices_json(chainlink_map, x)
                for x in result.json["results"]
            ],
            ignore_index=True,
        )
        return prices_df

    def get_collateral_flag(self, users):
        """
        The get_collateral_flag function returns a dataframe of the user's collateral flag.
        The function takes in a list of addresses and returns the address, asset, and collateral flag for each user.


        :param self: Access the class attributes
        :param users: Get the list of addresses that are to be checked for collateral
        :return: A dataframe with the collateral flag for each user
        """
        comptroller_contract = self.load_contract(
            "comptroller", self.comptrollerAddress
        )
        calls = []
        for u in users:
            try:
                calls.append(comptroller_contract.functions.getAssetsIn(u))
            except Exception as ex:
                logging.warning(f"checking collateral failed, {ex} for user {u}")
        result = self.multi.aggregate(calls)
        collateral_df = pd.concat(
            [self.__format_collateral_flag(x) for x in result.json["results"]],
            ignore_index=True,
        )
        return collateral_df

    def get_snapshot(self, marketAddresses, user_address):
        """
        The get_snapshot function returns the account snapshot of user in each market.
        The function takes in a list of token addresses and returns a dataframe with the following columns:

        :param self: Reference the class object
        :param marketAddresses: Get the address of the market contract
        :param user_address: Get the balance of a particular address
        :return: The account snapshot of each market
        """

        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.getAccountSnapshot(user_address))
            except Exception as ex:
                logging.warning(
                    f"vToken balance failed for address {user_address}, {ex}"
                )
        return self.multi.aggregate(calls)

    def get_market_decimals(self, marketAddresses):
        """
        Fetches the number of decimals for each market contract specified in `marketAddresses`.
        Uses the `decimals()` function of each market contract to retrieve this information.

        Args:
        - `marketAddresses` (list): A list of addresses for the market contracts to query.

        Returns:
        - `result_df` (pandas.DataFrame): A DataFrame containing the number of decimals for each
            market contract, with columns for the contract address and the number of decimals.
        """

        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.decimals())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        result_df = pd.concat(
            [self.__create_df(x) for x in result.json["results"]], ignore_index=True
        )
        return result_df

    def get_market_totalBorrows(self, marketAddresses):
        """
        Fetches the total amount borrowed in each market specified in `marketAddresses`.
        Uses the `totalBorrows()` function of each market contract to retrieve this information.

        Args:
        - `marketAddresses` (list): A list of addresses for the market contracts to query.

        Returns:
        - `result_df` (pandas.DataFrame): A DataFrame containing the total amount borrowed for each
            market contract, with columns for the contract address and the total amount borrowed.
        """
        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.totalBorrows())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        result_df = pd.concat(
            [self.__create_df(x) for x in result.json["results"]], ignore_index=True
        )
        return result_df

    def get_market_totalSupply(self, marketAddresses):
        """
        Fetches the total supply of each market specified in `marketAddresses`.
        Uses the `totalSupply()` function of each market contract to retrieve this information.

        Args:
        - `marketAddresses` (list): A list of addresses for the market contracts to query.

        Returns:
        - `result_df` (pandas.DataFrame): A DataFrame containing the total supply for each
            market contract, with columns for the contract address and the total supply.
        """
        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.totalSupply())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        result_df = pd.concat(
            [self.__create_df(x) for x in result.json["results"]], ignore_index=True
        )
        return result_df

    def get_market_exchangeRateCurrent(self, marketAddresses):
        """
        Fetches the current exchange rate for each market specified in `marketAddresses`.
        Uses the `exchangeRateCurrent()` function of each market contract to retrieve this information.

        Args:
        - `marketAddresses` (list): A list of addresses for the market contracts to query.

        Returns:
        - `result_df` (pandas.DataFrame): A DataFrame containing the current exchange rate for each
            market contract, with columns for the contract address and the current exchange rate.
        """
        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.exchangeRateCurrent())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        result_df = pd.concat(
            [self.__create_df(x) for x in result.json["results"]], ignore_index=True
        )
        return result_df

    def get_market_symbol(self, marketAddresses):
        """
        Fetches the symbol for each market specified in `marketAddresses`.
        Uses the `symbol()` function of each market contract to retrieve this information.

        Args:
        - `marketAddresses` (list): A list of addresses for the market contracts to query.

        Returns:
        - `result_df` (pandas.DataFrame): A DataFrame containing the symbol for each
            market contract, with columns for the contract address and the symbol.
        """
        market_contracts = []
        for m in marketAddresses:
            market_contracts.append(self.load_contract(self.pool_abi, m))
        calls = []
        for contract in market_contracts:
            try:
                calls.append(contract.functions.symbol())
            except Exception as ex:
                logging.warning(f"vToken decimals failed, {ex}")
        result = self.multi.aggregate(calls)
        result_df = pd.concat(
            [self.__create_df(x) for x in result.json["results"]], ignore_index=True
        )
        return result_df

    def get_market_borrow_division(self, dataframe_row):
        """
        Calculates the borrow division factor for a given market, based on its symbol and decimals.

        Args:
        - `dataframe_row` (pandas.Series): A row of a DataFrame containing the `symbol` and `decimals`
            for a single market contract.

        Returns:
        - `borrow_division` (int): The borrow division factor for the specified market, which is used
            to convert from the raw borrow balance returned by the contract to a more readable value.
            This factor is calculated based on the market's `symbol` and `decimals` values.
        """
        if dataframe_row["symbol"] == "vDOGE":
            borrow_division = 10 ** dataframe_row["decimals"]
        else:
            borrow_division = 10 ** (dataframe_row["decimals"] + 10)
        return borrow_division

    def get_market_supply_factor(self, dataframe_row):
        """
        Calculates the supply factor for a given market, based on its exchange rate and decimal places.

        Parameters:
        -----------
        dataframe_row : pandas.Series
            A row of a Pandas DataFrame containing information about a specific market, including its
            symbol, exchange rate, and decimal places.

        Returns:
        --------
        float
            The supply factor for the given market, calculated as the exchange rate adjusted for the number
            of decimal places, divided by 10 raised to the power of the number of decimal places.
        """

        if dataframe_row["symbol"] == "vDOGE":
            exchangeRateCurrent_adjusted = dataframe_row["exchangeRateCurrent"] / 1e18
        else:
            exchangeRateCurrent_adjusted = dataframe_row["exchangeRateCurrent"] / 1e28
        supply_factor = exchangeRateCurrent_adjusted / (10 ** dataframe_row["decimals"])
        return supply_factor

    def get_venus_user_addresses(self):
        """
        Gets the list of Venus user addresses from the connected web3 instance.

        :return: A pandas DataFrame with the user addresses.
        :rtype: pandas.DataFrame

        :raises: Returns an error message as a string if the connection to web3 fails.

        This method retrieves the user addresses associated with the Venus protocol from the connected web3 instance.
        It first checks if the web3 instance is successfully connected, and if not, returns an error message.

        If the connection is successful, the method loads the account page and extracts the data of the first page.
        It then iterates through the remaining pages and appends the data to a list of DataFrames.

        Finally, it concatenates all the DataFrames into a single DataFrame and returns it.
        """
        if not self.web3:
            return "Connection not successfull"

        account_js = self.__load_account_page(1)
        total_page = account_js["data"]["totalPage"]
        df_list = []
        df_list.append(pd.DataFrame(account_js["data"]["data"]))
        i = 2

        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            futures = []

            for i in range(i, int(total_page) + 1):
                future = executor.submit(self.__load_account_page, i)
                futures.append(future)

            with tqdm(total=len(futures)) as pbar:
                for future in concurrent.futures.as_completed(futures):
                    account_js = future.result()
                    df_list.append(pd.DataFrame(account_js["data"]["data"]))
                    pbar.update(1)

        df_total = pd.concat(df_list, ignore_index=True)
        return df_total

    def get_market_user_information(self, market_address, user_address, enriched):
        """
        Gets market and user information for a given market and user address.
        :param market_address: The address of the market.
        :type market_address: str
        :param user_address: The address of the user.
        :type user_address: str
        :param enriched: Whether to include additional data in the output DataFrame. Default is True.
        :type enriched: bool
        :return: A pandas DataFrame with the market and user information.
        :rtype: pandas.DataFrame

        :raises: Returns an error message as a string if the connection to web3 fails.

        This method retrieves the market and user information for a given market and user address from the connected web3 instance.

        It first checks if the web3 instance is successfully connected, and if not, returns an error message.

        If the connection is successful, the method fetches the market and user data using the given addresses and the pool ABI.
        It adds the pool ABI to the DataFrame to allow for future processing.

        If `enriched` is True, the method processes the DataFrame to include additional data related to market utilization, lending parameters, and user account balances.
        If `enriched` is False, the DataFrame only contains the basic market and user information.

        Finally, the method returns the resulting DataFrame.
        """
        if not self.web3:
            return "Connection not successfull"
        df_list = []
        token_df = self.__fetch_information(
            market_address, Web3.toChecksumAddress(user_address), self.pool_abi
        )
        token_df["abi"] = self.pool_abi
        df_list.append(token_df)
        market_df = pd.concat(df_list)
        if enriched:
            market_df[
                [
                    "utilization_rate",
                    "a1",
                    "a2",
                    "b",
                    "kink_readable",
                    "reserve_factor",
                    "account_supply_underlying_token",
                    "account_borrow_underlying_token",
                ]
            ] = market_df.apply(lambda x: self.__process_row(x), axis=1)
        return market_df

    def get_accounts_raw_snapshot(self, address_list):
        """
        Gets the raw snapshot data for a list of addresses.

        :param address_list: A list of addresses to fetch the snapshot data for.
        :type address_list: list of str
        :return: A pandas DataFrame with the raw snapshot data.
        :rtype: pandas.DataFrame

        :raises: Returns an error message as a string if the connection to web3 fails.

        This method retrieves the raw snapshot data for a list of addresses from the connected web3 instance.
        The method uses a thread pool executor to fetch and extract the snapshot data in parallel.

        It first checks if the web3 instance is successfully connected, and if not, returns an error message.

        The method calculates the number of runs required to fetch the snapshot data for all the addresses, based on the maximum number of addresses that can be fetched in a single run.
        It then uses a thread pool executor to fetch the snapshot data for each run, with up to 40 threads in parallel.
        It also includes a delay of 10 seconds between each run to prevent overloading the web3 instance.

        Once all the snapshot data is fetched, the method extracts the JSON information from each snapshot and combines it into a single DataFrame.
        The resulting DataFrame contains the raw snapshot data for all the addresses.
        """
        if not self.web3:
            return "Connection not successfull"

        no_run = math.ceil(len(address_list) / 4000)
        df_list2 = []
        with tqdm(total=no_run) as pbar:
            for i in range(no_run):
                executor = concurrent.futures.ThreadPoolExecutor(40)
                start_id = i * 4000
                end_id = min(len(address_list), (i + 1) * 4000)
                snapshot_list = list(
                    executor.map(
                        lambda a: self.get_snapshot(
                            MARKET_ADDRESS.values(), Web3.toChecksumAddress(a)
                        ),
                        address_list[start_id:end_id],
                    )
                )
                executor2 = concurrent.futures.ThreadPoolExecutor(40)
                df_list = list(
                    executor2.map(lambda a: self.__extract_json_info(a), snapshot_list)
                )
                df_list2.append(pd.concat(df_list, ignore_index=True))
                pbar.update(1)
                time.sleep(10)
        snapshot_data = pd.concat(df_list2, ignore_index=True)
        return snapshot_data

    def process_accounts_snapshot(self, snapshot_data):
        """
        Process the accounts snapshot data and return the processed snapshot data.

        Args:
            snapshot_data (pandas.DataFrame): The snapshot data to be processed.

        Returns:
            pandas.DataFrame: The processed snapshot data with additional columns for supply and borrow amounts in underlying and USD, and prices for vTokens and underlying assets.

        Raises:
            None
        """
        if not self.web3:
            return "Connection not successfull"

        result1 = self.get_market_decimals(MARKET_ADDRESS.values())
        result2 = self.get_market_exchangeRateCurrent(MARKET_ADDRESS.values())
        result3 = self.get_market_symbol(MARKET_ADDRESS.values())

        market_conversion = self.__get_market_conversion(result1, result2, result3)
        market_conversion["market_address"] = market_conversion.apply(
            lambda x: x["market_address"].lower(), axis=1
        )

        prices = self.get_asset_prices(CHAINLINK_ADDRESSES)

        prices["symbol"] = prices.apply(lambda x: "v" + x["asset"], axis=1)
        snapshot_data["BorrowBalance"] = snapshot_data["BorrowBalance"].astype(float)
        snapshot_data = pd.merge(
            snapshot_data, market_conversion, on="market_address", how="left"
        )
        snapshot_data = pd.merge(snapshot_data, prices, on="symbol", how="left")
        snapshot_data["supplyInUnderlying"] = snapshot_data.apply(
            lambda x: x["vTokenBalance"] * x["supply_factor"], axis=1
        )
        snapshot_data["borrowsInUnderlying"] = snapshot_data.apply(
            lambda x: x["BorrowBalance"] / x["borrow_divider"], axis=1
        )
        snapshot_data["supplyInUSD"] = snapshot_data.apply(
            lambda x: x["supplyInUnderlying"] * x["price_usd"], axis=1
        )
        snapshot_data["borrowsInUSD"] = snapshot_data.apply(
            lambda x: x["borrowsInUnderlying"] * x["price_usd"], axis=1
        )
        return snapshot_data

    def get_collateral_flag_snapshot(self, address_list):
        """
        Get a snapshot of the collateral flags for a list of Venus users.

        Parameters:
        -----------
        address_list : list of str
            List of Ethereum addresses of Venus users.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing the collateral flags for each user in the address_list.
            The DataFrame has the following columns:
                - address: the Ethereum address of the user
                - flag: a boolean indicating whether the user is using their assets as collateral or not
        """
        if not self.web3:
            return "Connection not successfull"
        no_run2 = math.ceil(len(address_list) / 100)
        df_list3 = []
        with tqdm(total=no_run2) as pbar, concurrent.futures.ThreadPoolExecutor(
            max_workers=40
        ) as executor:
            futures = []
            for i in range(no_run2):
                start_id = i * 100
                end_id = min(len(address_list), (i + 1) * 100)
                future = executor.submit(
                    self.get_collateral_flag, address_list[start_id:end_id]
                )
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                df_list3.append(future.result())
                pbar.update(1)
        collateral_flag_df = pd.concat(df_list3, ignore_index=True)
        return collateral_flag_df

    def get_verify_snapshot(self, snapshot_data):
        """
        Get verification snapshot for the given snapshot data.

        Args:

            snapshot_data: A pandas dataframe containing the snapshot data of users' balances and transactions.

        Returns:

            aggregated_data: A pandas dataframe containing the aggregated data of users' balances and transactions, along with
            additional information such as the total supply and total borrows for each market. The dataframe also includes
            two additional columns "check_borrow" and "check_supply", which represent the percentage difference between the
            calculated total borrows and total supply for each market, and the actual total borrows and total supply obtained
            from the blockchain.
        """

        if not self.web3:
            return "Connection not successfull"

        totalSupply_df = self.get_market_totalSupply(MARKET_ADDRESS.values())
        totalBorrows_df = self.get_market_totalBorrows(MARKET_ADDRESS.values())
        totalSupply_df["market_address"] = totalSupply_df.apply(
            lambda x: x["market_address"].lower(), axis=1
        )

        totalBorrows_df["market_address"] = totalBorrows_df.apply(
            lambda x: x["market_address"].lower(), axis=1
        )
        aggregated_data = (
            snapshot_data.groupby(["market_address", "symbol", "asset"])[
                [
                    "vTokenBalance",
                    "BorrowBalance",
                    "supplyInUnderlying",
                    "borrowsInUnderlying",
                    "supplyInUSD",
                    "borrowsInUSD",
                ]
            ]
            .sum()
            .reset_index()
        )
        aggregated_data = pd.merge(
            aggregated_data, totalSupply_df, on="market_address", how="inner"
        )
        aggregated_data = pd.merge(
            aggregated_data, totalBorrows_df, on="market_address", how="inner"
        )

        aggregated_data["check_borrow"] = aggregated_data.apply(
            lambda x: (x["BorrowBalance"] - x["totalBorrows"]) / x["totalBorrows"],
            axis=1,
        )
        aggregated_data["check_supply"] = aggregated_data.apply(
            lambda x: (x["vTokenBalance"] - x["totalSupply"]) / x["totalSupply"], axis=1
        )

        return aggregated_data
