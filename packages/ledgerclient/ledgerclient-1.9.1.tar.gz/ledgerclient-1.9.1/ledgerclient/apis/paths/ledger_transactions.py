from ledgerclient.paths.ledger_transactions.get import ApiForget
from ledgerclient.paths.ledger_transactions.post import ApiForpost
from ledgerclient.paths.ledger_transactions.head import ApiForhead


class LedgerTransactions(
    ApiForget,
    ApiForpost,
    ApiForhead,
):
    pass
