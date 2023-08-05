# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from ledgerclient.paths.ledger_accounts_address_metadata import Api

from ledgerclient.paths import PathValues

path = PathValues.LEDGER_ACCOUNTS_ADDRESS_METADATA