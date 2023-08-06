"""

    Convex API

"""

import json
import logging
import re
import secrets
import time

from urllib.parse import urljoin

import requests

from convex_api.account import Account

from convex_api.exceptions import (
    ConvexAPIError,
    ConvexRequestError
)
from convex_api.key_pair import KeyPair
from convex_api.registry import Registry
from convex_api.utils import (
    is_account,
    remove_0x_prefix,
    to_address
)

# min amount to do a topup account
TOPUP_ACCOUNT_MIN_BALANCE = 10000000

logger = logging.getLogger(__name__)


class API:

    LANGUAGE_LISP = 'convex-lisp'
    # Convex Scrypt Language disabled
    # LANGUAGE_SCRYPT = 'convex-scrypt'
    LANGUAGE_ALLOWED = [LANGUAGE_LISP]

    def __init__(self, url, language=LANGUAGE_LISP):
        self._url = url

        if language not in API.LANGUAGE_ALLOWED:
            raise ValueError(f'Invalid language: {language}')
        self._language = language
        self._registry = Registry(self)

    def create_account(self, key_pair, sequence_retry_count=20):
        """

        Create a new account address on the convex network.

        :param `KeyPair` key_pair: :class:`.KeyPair` object that you whish to use as the signing account.
            The :class:`.KeyPair` object contains the public/private keys to access and submit commands
            on the convex network.


        :param sequence_retry_count: Number of retries to create the account. If too many clients are trying to
            create accounts on the same node, then we will get sequence errors.
        :type sequence_retry_count: int, optional

        :returns: A new :class:`.Account` object, or copy of the :class:`.Account` object with a new `address` property value set


        .. code-block:: python

            >>> from convex_api import API
            >>> convex = API('https://convex.world')
            >>> # Create a new account with new public/priavte keys and address
            >>> key_pair = KeyPair()
            >>> account = convex.create_account(key_pair)
            >>> print(account.address)
            >>> 42

            >>> #create a new account address, but use the same keys as `account`
            >>> new_account_address = convex.create_account(account=account)
            >>> print(new_account.address)
            >>> 43


        """

        if key_pair and not isinstance(key_pair, KeyPair):
            raise TypeError(f'key_pair value {key_pair} must be a type convex_api.KeyPair')

        create_account_url = urljoin(self._url, '/api/v1/createAccount')
        account_data = {
            'accountKey': key_pair.public_key_api,
        }

        logger.debug(f'create_account {create_account_url} {account_data}')
        result = self._transaction_post(create_account_url, account_data)
        logger.debug(f'create_account result {result}')
        account = Account(key_pair, to_address(result['address']))
        return account

    def load_account(self, name, key_pair):
        """

        Load an account using the correct name. If successfull return the :class:`.Account` object with the address set.

        This is a Query operation, so no convex tokens are used in loading the account.

        :param str name: name of the account to load
        :param KeyPair key_pair: :class:`.KeyPair` object to import for the account

        :results: :class:`.Account` object with the address and name set and key_pair, if not found then return None


        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> import_account = Account.import_from_file('my_account.pem', 'secret')
            >>> account = convex.load_account('my_account, import_account)
            >>> print(account.name)
            my_account
            >>> print(account.address)
            930

        """
        address = self.resolve_account_name(name)
        if address:
            new_account = Account(key_pair, address, name=name)
            return new_account

    def setup_account(self, name, key_pair, register_account=None):
        """

        Convenience method to create or load an account based on the account name.
        If the account name cannot be found then account will be created and account name registered,
        if the name is found, then account and it's address with that name will be loaded.

        :param str name: name of the account to create or load
        :param KeyPair key_pair: :class:`.KeyPair` object to use to sign for the account.
        :param Account register_account: Optional :class:`.Account` object to use for registration of the account

        :results: :class:`.Account` object with the address and name set, if not found then return None

        **Note** If you do not provide a register_account, then this method calls the
        :meth:`.topup_account` method to get enougth funds to register an account name.


        .. code-block:: python

            >>> import_key_pair = KeyPair.import_from_file('my_account.pem', 'secret')
            >>> # create or load the account named 'my_account'
            >>> account = convex.setup_account('my_account', import_key_pair)
            >>> print(account.name)
            my_account

        """

        # check to see if we can resolve the account name
        if self.resolve_account_name(name):
            # if so just load the account
            account = self.load_account(name, key_pair)
        else:
            # new name , so first create the account
            account = self.create_account(key_pair)
            if not register_account:
                # make sure we have enougth funds to do the registration
                self.topup_account(account)
                register_account = account
            account = self.register_account_name(name, account, register_account)
        return account

    def register_account_name(self, name, address_account, account=None):
        """

        Register or update an account address with an account name.

        This call will submit to the CNS (Convex Name Service), a name in the format
        "`account.<your_name>`". You need to have some convex balance in your account, and
        a valid account address.

        :param str name: name of the account to register.
        :param number|Account account_address: Account or address to register.
        :param Account account: :class:`.Account` object to register the account name.

        .. code-block:: python

            >>> # load the register account
            >>> register_account = convex.load_account('register_account', key_pair)
            >>> account = convex.create_account(key_pair)
            >>> print(account.address)
            1024
            >>> account = convex.register_account('my_new_account', account.address, register_account)
            >>> print(account.address)
            1024

            # or you can call with only one account, this will use the address of that account
            >>> print(register_account.address)
            404
            >>> account = convex.register_account('my_new_account', register_account)
            >>> print(account.address)
            404

        """

        # is the address_account field only an address?
        address = to_address(address_account)
        if is_account(address_account) and account is None:
            account = address_account

        # we must have a valid account to do the registration
        if not account:
            raise ValueError('you need to provide a registration account to register an account name')

        if not address:
            raise ValueError('You need to provide a valid address to register an account name')

        self._registry.register(f'account.{name}', address, account)
        return Account(account.key_pair, address=address, name=name)

    def send(self, transaction, account, language=None, sequence_retry_count=20):
        """
        Send transaction code to the block chain node.

        :param str transaction: The transaction as a string to send

        :param Account account: The account that needs to sign the message to send

        :param language: Language to use for this transaction. Defaults to LANGUAGE_LISP.
        :type language: str, optional

        :param sequence_retry_count: Number of retries to do if a SEQUENCE error occurs.
            When sending multiple send requsts on the same account, you can get SEQUENCE errors,
            This send method will automatically retry again
        :type sequence_retry_count: int, optional

        :returns: The dict returned from the result of the sent transaction.


        .. code-block:: python

            >>> from convex_api import API, KeyPair
            >>> convex = API('https://convex.world')

            >>> # Create a new account with new public/private keys and address
            >>> key_pair = KeyPair()
            >>> account = convex.create_account(key_pair)

            >>> # request some funds to do stuff
            >>> print(convex.request_funds(100000, account))
            100000

            >>> # submit a transaction using the new account
            >>> print(convex.send('(map inc [ 1 2 3 4])', account))
            {'value': [2, 3, 4, 5]}


        """
        if not transaction:
            raise ValueError('You need to provide a valid transaction')
        if not isinstance(transaction, str):
            raise TypeError('The transaction must be a type str')

        result = None
        max_sleep_time_seconds = 1
        while sequence_retry_count >= 0:
            try:
                hash_data = self._transaction_prepare(transaction, account.address, language=language)
                signed_data = account.sign(hash_data['hash'])
                result = self._transaction_submit(account.address, account.key_pair.public_key_api, hash_data['hash'], signed_data)
            except ConvexAPIError as error:
                if error.code == 'SEQUENCE':
                    if sequence_retry_count == 0:
                        raise
                    sequence_retry_count -= 1
                    # now sleep < 1 second for at least 1 millisecond
                    sleep_time = secrets.randbelow(round(max_sleep_time_seconds * 1000)) / 1000
                    time.sleep(sleep_time + 1)
                else:
                    raise
            else:
                break
        return result

    def query(self, transaction, address_account, language=None):
        """

        Run a query transaction on the block chain. Since this does not change the network state, and
        the account does not need to sign the transaction. No funds will be used when executing
        this query. For this reason you can just pass the account address, or if you want to the :class:`.Account` object.

        :param str transaction: Transaction to execute. This can only be a read only transaction.

        :param address_account: :class:`.Account` object or int address of an account to use for running this query.
        :type address_account: Account, int, str

        :param language: The type of language to use, if not provided the default language set will be used.
        :type language: str, optional

        :returns: Return the resultant query transaction


        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()

            >>> # submit a query transaction using the account address

            >>> print(convex_api.query(f'(balance {account.address})', account.address))
            {'value': 0}

            >>> # request some funds to do stuff
            >>> print(convex_api.request_funds(100000, account))
            100000
            >>> print(convex_api.query(f'(balance {account.address})', account.address))
            {'value': 100000}

        """
        address = to_address(address_account)

        return self._transaction_query(address, transaction, language)

    def request_funds(self, amount, account):
        """

        Request funds for an account from the block chain faucet.

        :param number amount: The amount of funds to request

        :param Account account: The :class:`.Account` object to receive funds too

        :returns: The amount transfered to the account


        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> # request some funds to do stuff
            >>> print(convex_api.request_funds(100000, account))
            100000

        """
        faucet_url = urljoin(self._url, '/api/v1/faucet')
        faucet_data = {
            'address': account.address,
            'amount': amount
        }
        logger.debug(f'request_funds {faucet_url} {faucet_data}')
        result = self._transaction_post(faucet_url, faucet_data)
        logger.debug(f'request_funds result {result}')
        if result['address'] != account.address:
            raise ValueError(f'request_funds: returned account is not correct {result["address"]}')
        return result['amount']

    def topup_account(self, account, min_balance=TOPUP_ACCOUNT_MIN_BALANCE, retry_count=8):
        """

        Topup an account from the block chain faucet, so that the balance of the account is above or equal to
        the `min_balanace`.

        :param Account account: The :class:`.Account` object to receive funds for

        :param min_balance: Minimum account balance that will allowed before a topup occurs
        :type min_balance: number, optional

        :param retry_count: The number of times the faucet will be called to get above or equal to the  `min_balance`
        :type retry_count: number, optional

        :returns: The amount transfered to the account

        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> # request some funds to do stuff
            >>> print(convex_api.topup_account(account, 100000))
            100000
            >>> # try again, but only return 0 topup amount credited
            >>> print(convex_api.topup_account(account, 100000))
            0

        """

        request_amount = min(TOPUP_ACCOUNT_MIN_BALANCE, min_balance)
        retry_count = min(5, retry_count)
        transfer_amount = 0
        while min_balance > self.get_balance(account) and retry_count > 0:
            transfer_amount += self.request_funds(request_amount, account)
            retry_count -= 1
        return transfer_amount

    def get_address(self, function_name, address_account):
        """

        Query the network for a contract ( function ) address. The contract must have been deployed
        by the account address provided. If not then no address will be returned

        :param str function_name: Name of the contract/function

        :param address_account: :class:`.Account` object or str address of an account to use for running this query.
        :type address_account: Account, int, str


        :returns: Returns address of the contract

        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> # find the address of a contract
            >>> print(convex_api.get_address('my_contract', account))

        """

        line = f'(address {function_name})'
        """
        if self._language == API.LANGUAGE_SCRYPT:
            line = f'address({function_name})'
        """
        result = self.query(line, address_account)
        if result and 'value' in result:
            return to_address(result['value'])

    def get_balance(self, address_account, account_from=None):
        """

        Get a balance of an account.

        At the moment the account needs to have a balance to get the balance of it's account or any
        other account. Event though this is using a query request.

        :param address_account: Address or :class:`.Account` object to get the funds for.
        :type address_account: Account, int, str

        :param account_from: Optional :class:`.Account` object or account address to make the request.
        :type account_from: Account, int, str, optional


        :returns: Return the current balance of the address or account `address_account`

        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> # get the balance of the contract
            >>> print(convex_api.get_balance(account))
            0
            >>> print(convex_api.request_funds(100000, account))
            100000
            >>> print(convex_api.get_balance(account))
            100000

        """
        value = 0
        address = to_address(address_account)

        address_from = address
        if account_from:
            address_from = to_address(account_from)
        line = f'(balance #{address})'
        """
        if self._language == API.LANGUAGE_SCRYPT:
            line = f'balance(#{address})'
        """
        try:

            result = self._transaction_query(address_from, line)
        except ConvexAPIError as error:
            if error.code != 'NOBODY':
                raise
        else:
            value = result['value']
        return value

    def transfer(self, to_address_account, amount, account):
        """

        Transfer funds from on account to another.

        :param to_address_account: Address or :class:`.Account` object to send the funds too
        :type to_address_account: Account, int, str

        :param number amount: Amount to transfer

        :param Account account: :class:`.Account` object to send the funds from

        :returns: The transfer record sent back after the transfer has been made

        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> print(convex_api.request_funds(10000000, account))
            10000000
            >>> print(convex_api.get_balance(account))
            10000000

            >>> my_account = convex_api.create_account()
            >>> # transfer some funds to my_account
            >>> print(convex_api.transfer(my_account, 100, account))
            100
            >>> print(convex_api.get_balance(my_account))
            100
            >>> print(convex_api.get_balance(account))
            9998520

        """
        transfer_to_address = to_address(to_address_account)
        if not to_address:
            raise ValueError(f'You must provide a valid to account/address ({transfer_to_address}) to transfer funds too')

        line = f'(transfer #{transfer_to_address} {amount})'
        """
        if self._language == API.LANGUAGE_SCRYPT:
            line = f'transfer(#{transfer_to_address}, {amount})'
        """
        result = self.send(line, account)
        if result and 'value' in result:
            return result['value']
        return 0

    def transfer_account(self, from_account, to_account):
        """

        **WARNING**
        If you do not save the `from_account` keys for later use, this call can stop you
        from accessing your transfered `to_account`.

        Transfer and copy the keys from the `from_account` over too the `to_acount`.

        :param Account from_account: :class:`.Account` object that has public/private keys you with to copy

        :param Account to_account: :class:`.Account` object that has an address and you wish to change to now
        use the `to_account` access keys.


        :returns: A new account object that has the same name and address as the `to_account`, but with
        the access keys of the `from_account`.


        .. code-block:: python

            # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> account.public_key
            '0xae4c019e68591e085d52cdb41924bde067d864cecb1780faa37142054b0fd8ef'

            # get a saved account keys
            >>> import_account = Account.import_from_file('my_account.pem', 'secret')
            >> import_account.public_key
            '5288fec4153b702430771dfac8aed0b21cafca4344dae0d47b97f0bf532b3306'


            # transfer the loaded keys from the `import_account`, to `account`
            >>> account = convex.transfer_account(import_account, account)
            >>> account.public_key
            '5288fec4153b702430771dfac8aed0b21cafca4344dae0d47b97f0bf532b3306'

        """
        if not isinstance(to_account, Account):
            raise TypeError('The to account must be a type Convex API Account Class')
        if not isinstance(from_account, Account):
            raise TypeError('The from account must be a type Convex API Account Class')

        if not to_account.address:
            raise ValueError('You need to have the to account registered with an address')

        line = f'(set-key {from_account.key_pair.public_key_checksum})'
        """
        if self._language == API.LANGUAGE_SCRYPT:
            line = f'set-key({from_account.key_pair.public_key_checksum})'
        """
        result = self.send(line, to_account)
        if result and 'value' in result and from_account.key_pair.is_equal(result['value']):
            return Account(from_account.key_pair, to_account.address, to_account.name)

    def get_account_info(self, address_account):
        """

        Get account information. This will only work with an account that has a balance or has had some transactions
        processed on the convex network. New accounts with no transfer or transactions will raise:

            ConvexRequestError(404, 'The Account for this Address does not exist.') error

        The returned information is dictionary of account information.

        :param address_account: :class:`.Account` object or address of an account to get current information on.
        :type address_account: Account, int, str

        :returns: dict of information, such as

        .. code-block:: python

            >>> # Create a new account with new public/priavte keys and address
            >>> account = convex_api.create_account()
            >>> # get the balance of the contract
            >>> print(convex_api.get_account_info(account))

            {'environment': {}, 'address': 1178, 'memorySize': 0, 'balance': 0,
            'isLibrary': False, 'isActor': False, 'allowance': 0,
            'sequence': 0, 'type': 'user'}

        """
        address = to_address(address_account)

        account_url = urljoin(self._url, f'/api/v1/accounts/{address}')
        logger.debug(f'get_account_info {account_url}')

        response = requests.get(account_url)
        if response.status_code != 200:
            raise ConvexRequestError('get_account_info', response.status_code, response.text)

        result = response.json()
        logger.debug(f'get_account_info repsonse {result}')
        return result

    def resolve_account_name(self, name):
        """
        Resolves an account name to an address.
        :param string name Name of the account to resolve.

        .. code-block:: python

            >>> convex.resolve_account_name('my_account')
            405

        """
        return self._registry.resolve_address(f'account.{name}')

    def resolve_name(self, name):
        """
        Resolves any Convex Name Services to an address.
        :param string name Name of the the CNS Service.

        .. code-block:: python

            >>> convex.resolve_name('convex.nft-tokens')
            25

        """
        return self._registry.resolve_address(name)

    def load_contract(self, name):
        from convex_api.contract import Contract

        contract = Contract(self)
        if contract.load(name=name):
            return contract

    def _transaction_post(self, url, data, sequence_retry_count=20):
        max_sleep_time_seconds = 1
        while sequence_retry_count >= 0:
            response = requests.post(url, data=json.dumps(data))
            if response.status_code == 200:
                result = response.json()
                break
            elif response.status_code == 400:
                if not re.search(':SEQUENCE ', response.text):
                    raise ConvexRequestError('_transaction_post', response.status_code, response.text)

                if sequence_retry_count == 0:
                    raise ConvexRequestError('_transaction_post', response.status_code, response.text)
                sequence_retry_count -= 1
                # now sleep < 1 second for at least 1 millisecond
                sleep_time = secrets.randbelow(round(max_sleep_time_seconds * 1000)) / 1000
                time.sleep(sleep_time + 1)
            else:
                raise ConvexRequestError('_transaction_post', response.status_code, response.text)
        return result

    def _transaction_prepare(self, transaction, address, language=None, sequence_number=None):
        """

        """
        if language is None:
            language = self._language
        prepare_url = urljoin(self._url, '/api/v1/transaction/prepare')
        data = {
            'address': to_address(address),
            'lang': language,
            'source': transaction,
        }
        if sequence_number:
            data['sequence'] = sequence_number
        logger.debug(f'_transaction_prepare {prepare_url} {data}')

        result = self._transaction_post(prepare_url, data)

        logger.debug(f'_transaction_prepare repsonse {result}')
        if 'errorCode' in result:
            raise ConvexAPIError('_transaction_prepare', result['errorCode'], result['value'])

        return result

    def _transaction_submit(self, address, public_key, hash_data, signed_data):
        """

        """
        submit_url = urljoin(self._url, '/api/v1/transaction/submit')
        data = {
            'address': to_address(address),
            'accountKey': public_key,
            'hash': hash_data,
            'sig': remove_0x_prefix(signed_data)
        }
        logger.debug(f'_transaction_submit {submit_url} {data}')
        result = self._transaction_post(submit_url, data)
        logger.debug(f'_transaction_submit response {result}')
        if 'errorCode' in result:
            raise ConvexAPIError('_transaction_submit', result['errorCode'], result['value'])
        return result

    def _transaction_query(self, address, transaction, language=None):
        """

        """
        if language is None:
            language = self._language

        query_url = urljoin(self._url, '/api/v1/query')
        query_data = {
            'address': address,
            'lang': language,
            'source': transaction,
        }
        logger.debug(f'_transaction_query {query_url} {query_data}')
        result = self._transaction_post(query_url, query_data)
        logger.debug(f'_transaction_query repsonse {result}')
        if 'errorCode' in result:
            raise ConvexAPIError('_transaction_query', result['errorCode'], result['value'])
        return result

    @property
    def language(self):
        """

        Returns the default language to use when calling the API commands

        """
        return self._language

    @property
    def registry(self):
        return self._registry
