# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ledgerclient.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    _INFO = "/_info"
    LEDGER__INFO = "/{ledger}/_info"
    LEDGER_ACCOUNTS = "/{ledger}/accounts"
    LEDGER_ACCOUNTS_ADDRESS = "/{ledger}/accounts/{address}"
    LEDGER_ACCOUNTS_ADDRESS_METADATA = "/{ledger}/accounts/{address}/metadata"
    LEDGER_MAPPING = "/{ledger}/mapping"
    LEDGER_SCRIPT = "/{ledger}/script"
    LEDGER_STATS = "/{ledger}/stats"
    LEDGER_TRANSACTIONS = "/{ledger}/transactions"
    LEDGER_TRANSACTIONS_TXID = "/{ledger}/transactions/{txid}"
    LEDGER_TRANSACTIONS_TXID_METADATA = "/{ledger}/transactions/{txid}/metadata"
    LEDGER_TRANSACTIONS_TXID_REVERT = "/{ledger}/transactions/{txid}/revert"
    LEDGER_TRANSACTIONS_BATCH = "/{ledger}/transactions/batch"
    LEDGER_BALANCES = "/{ledger}/balances"
    LEDGER_AGGREGATE_BALANCES = "/{ledger}/aggregate/balances"
    LEDGER_LOGS = "/{ledger}/logs"
