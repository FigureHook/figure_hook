from src.custom_classes import Release
from src.Models import ProductReleaseInfo

__all__ = [
    "ReleaseToProductReleaseInfoModelAdapter"
]


class ReleaseToProductReleaseInfoModelAdapter(ProductReleaseInfo):
    def __init__(self, release: Release) -> None:
        price = release.price
        initial_release_date = release.release_date
        order_period_start = None
        order_period_end = None

        if release.order_period:
            order_period_start = release.order_period.start
            order_period_end = release.order_period.end

        super().__init__(
            price=price,
            order_period_start=order_period_start,
            order_period_end=order_period_end,
            initial_release_date=initial_release_date
        )
