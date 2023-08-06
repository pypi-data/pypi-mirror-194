from enum import Enum


class PispgatewayLegacyPaymentContextPaymentContextCode(str, Enum):
    BILLPAYMENT = "BILLPAYMENT"
    Bill_Payment = "BillPayment"
    ECOMMERCEGOODS = "ECOMMERCEGOODS"
    ECOMMERCESERVICES = "ECOMMERCESERVICES"
    Ecommerce_Goods = "EcommerceGoods"
    Ecommerce_Services = "EcommerceServices"
    OTHER = "OTHER"
    Other = "Other"
    PARTYTOPARTY = "PARTYTOPARTY"
    Party_To_Party = "PartyToParty"

    def __str__(self) -> str:
        return str(self.value)
