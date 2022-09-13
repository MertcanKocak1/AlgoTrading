from Account.Account import Account
from Data import DataManagement


def decimal_formatter(number):
    return format(number, '.8f')


if __name__ == '__main__':
    account = Account()
    dm = DataManagement.DataManagement()
    dm.InitilazeAllData()
    dm.InitilazeAllIndicators()
    while True:
        dm.RefreshLastRow()
