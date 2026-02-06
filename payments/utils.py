from decimal import Decimal

SUBSCRIPTION_PRICING = {
    "ACCESS": {"amount": Decimal("1.00"), "days": 30},
    "ADVERT_DAY": {"amount": Decimal("0.50"), "days": 1},
    "ADVERT_WEEK": {"amount": Decimal("2.50"), "days": 7},
    "ADVERT_BIWEEK": {"amount": Decimal("4.00"), "days": 14},
    "ADVERT_MONTH": {"amount": Decimal("7.00"), "days": 30},
}
