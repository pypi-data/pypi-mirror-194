import typing_extensions

from ledgerclient.paths import PathValues
from ledgerclient.apis.paths.info import Info
from ledgerclient.apis.paths.ledger__info import LedgerInfo
from ledgerclient.apis.paths.ledger_accounts import LedgerAccounts
from ledgerclient.apis.paths.ledger_accounts_address import LedgerAccountsAddress
from ledgerclient.apis.paths.ledger_accounts_address_metadata import LedgerAccountsAddressMetadata
from ledgerclient.apis.paths.ledger_mapping import LedgerMapping
from ledgerclient.apis.paths.ledger_script import LedgerScript
from ledgerclient.apis.paths.ledger_stats import LedgerStats
from ledgerclient.apis.paths.ledger_transactions import LedgerTransactions
from ledgerclient.apis.paths.ledger_transactions_txid import LedgerTransactionsTxid
from ledgerclient.apis.paths.ledger_transactions_txid_metadata import LedgerTransactionsTxidMetadata
from ledgerclient.apis.paths.ledger_transactions_txid_revert import LedgerTransactionsTxidRevert
from ledgerclient.apis.paths.ledger_transactions_batch import LedgerTransactionsBatch
from ledgerclient.apis.paths.ledger_balances import LedgerBalances
from ledgerclient.apis.paths.ledger_aggregate_balances import LedgerAggregateBalances
from ledgerclient.apis.paths.ledger_logs import LedgerLogs

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues._INFO: Info,
        PathValues.LEDGER__INFO: LedgerInfo,
        PathValues.LEDGER_ACCOUNTS: LedgerAccounts,
        PathValues.LEDGER_ACCOUNTS_ADDRESS: LedgerAccountsAddress,
        PathValues.LEDGER_ACCOUNTS_ADDRESS_METADATA: LedgerAccountsAddressMetadata,
        PathValues.LEDGER_MAPPING: LedgerMapping,
        PathValues.LEDGER_SCRIPT: LedgerScript,
        PathValues.LEDGER_STATS: LedgerStats,
        PathValues.LEDGER_TRANSACTIONS: LedgerTransactions,
        PathValues.LEDGER_TRANSACTIONS_TXID: LedgerTransactionsTxid,
        PathValues.LEDGER_TRANSACTIONS_TXID_METADATA: LedgerTransactionsTxidMetadata,
        PathValues.LEDGER_TRANSACTIONS_TXID_REVERT: LedgerTransactionsTxidRevert,
        PathValues.LEDGER_TRANSACTIONS_BATCH: LedgerTransactionsBatch,
        PathValues.LEDGER_BALANCES: LedgerBalances,
        PathValues.LEDGER_AGGREGATE_BALANCES: LedgerAggregateBalances,
        PathValues.LEDGER_LOGS: LedgerLogs,
    }
)

path_to_api = PathToApi(
    {
        PathValues._INFO: Info,
        PathValues.LEDGER__INFO: LedgerInfo,
        PathValues.LEDGER_ACCOUNTS: LedgerAccounts,
        PathValues.LEDGER_ACCOUNTS_ADDRESS: LedgerAccountsAddress,
        PathValues.LEDGER_ACCOUNTS_ADDRESS_METADATA: LedgerAccountsAddressMetadata,
        PathValues.LEDGER_MAPPING: LedgerMapping,
        PathValues.LEDGER_SCRIPT: LedgerScript,
        PathValues.LEDGER_STATS: LedgerStats,
        PathValues.LEDGER_TRANSACTIONS: LedgerTransactions,
        PathValues.LEDGER_TRANSACTIONS_TXID: LedgerTransactionsTxid,
        PathValues.LEDGER_TRANSACTIONS_TXID_METADATA: LedgerTransactionsTxidMetadata,
        PathValues.LEDGER_TRANSACTIONS_TXID_REVERT: LedgerTransactionsTxidRevert,
        PathValues.LEDGER_TRANSACTIONS_BATCH: LedgerTransactionsBatch,
        PathValues.LEDGER_BALANCES: LedgerBalances,
        PathValues.LEDGER_AGGREGATE_BALANCES: LedgerAggregateBalances,
        PathValues.LEDGER_LOGS: LedgerLogs,
    }
)
