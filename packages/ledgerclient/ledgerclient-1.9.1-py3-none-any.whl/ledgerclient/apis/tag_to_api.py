import typing_extensions

from ledgerclient.apis.tags import TagValues
from ledgerclient.apis.tags.accounts_api import AccountsApi
from ledgerclient.apis.tags.balances_api import BalancesApi
from ledgerclient.apis.tags.ledger_api import LedgerApi
from ledgerclient.apis.tags.logs_api import LogsApi
from ledgerclient.apis.tags.mapping_api import MappingApi
from ledgerclient.apis.tags.script_api import ScriptApi
from ledgerclient.apis.tags.server_api import ServerApi
from ledgerclient.apis.tags.stats_api import StatsApi
from ledgerclient.apis.tags.transactions_api import TransactionsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.LEDGER: LedgerApi,
        TagValues.LOGS: LogsApi,
        TagValues.MAPPING: MappingApi,
        TagValues.SCRIPT: ScriptApi,
        TagValues.SERVER: ServerApi,
        TagValues.STATS: StatsApi,
        TagValues.TRANSACTIONS: TransactionsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.LEDGER: LedgerApi,
        TagValues.LOGS: LogsApi,
        TagValues.MAPPING: MappingApi,
        TagValues.SCRIPT: ScriptApi,
        TagValues.SERVER: ServerApi,
        TagValues.STATS: StatsApi,
        TagValues.TRANSACTIONS: TransactionsApi,
    }
)
