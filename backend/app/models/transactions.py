from pydantic import BaseModel

from datetime import date


class Transaction(BaseModel):
    account_id: str
    amount: float
    iso_currency_code: str
    date: date
    name: str
    transaction_id: str
    pending: bool

    @classmethod
    def from_plaid(cls, plaid_transaction):
        transaction = cls(
            account_id=plaid_transaction.account_id,
            amount=plaid_transaction.amount,
            iso_currency_code=plaid_transaction.iso_currency_code,
            date=plaid_transaction.date,
            name=plaid_transaction.name,
            transaction_id=plaid_transaction.transaction_id,
            pending=plaid_transaction.pending,
        )

        # Use authorized date instead of date if avaliable
        if plaid_transaction.authorized_date is not None:
            transaction.date = plaid_transaction.authorized_date

        # Use merchent name instead of name if avaliable
        if plaid_transaction.merchant_name is not None:
            transaction.name = plaid_transaction.merchant_name

        return transaction
