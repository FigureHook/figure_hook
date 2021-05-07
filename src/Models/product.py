from datetime import date, datetime
from typing import Union

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        SmallInteger, String)
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from .base import PkModel, PkModelWithTimestamps
from .relation_table import product_paintwork_table, product_sculptor_table

__all__ = [
    "ProductOfficialImage",
    "ProductReleaseInfo",
    "Product"
]


class ProductOfficialImage(PkModel):
    __tablename__ = "product_official_image"

    url = Column(String)
    order = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    def create_image_list(cls: 'ProductOfficialImage', image_urls: list[str]) -> list['ProductOfficialImage']:
        images = []

        for url in image_urls:
            image = cls.create(url=url)
            images.append(image)

        return images


class ProductReleaseInfo(PkModelWithTimestamps):
    __tablename__ = "product_release_info"

    price = Column(Integer)
    initial_release_date = Column(Date, nullable=True)
    delay_release_date = Column(Date)
    announced_at = Column(Date)
    release_at = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    def postpone_release_date_to(self, delay_date: Union[date, datetime, None]):
        if not delay_date:
            return

        if isinstance(delay_date, datetime):
            delay_date = delay_date.date()

        valid_type = isinstance(delay_date, date)
        if not valid_type:
            raise TypeError(f"{delay_date} must be `date` or `datetime`")

        has_init_release_date = bool(self.initial_release_date)

        if not has_init_release_date:
            self.update(delay_release_date=delay_date)
        if has_init_release_date:
            if self.initial_release_date < delay_date:
                self.update(delay_release_date=delay_date)
            if self.initial_release_date > delay_date:
                raise ValueError(
                    f"delay_date {delay_date} should be later than initial_release_date {self.initial_release_date}"
                )

    def stall(self):
        self.update(initial_release_date=None, delay_release_date=None)


class Product(PkModelWithTimestamps):
    """
    ## Column
    + checksum: MD5 value, one of methods to check the product should be updated.
    """
    __tablename__ = "product"

    # ---native columns---
    name = Column(String, nullable=False)
    size = Column(SmallInteger)
    scale = Column(SmallInteger)
    resale = Column(Boolean)
    adult = Column(Boolean)
    copyright = Column(String)
    url = Column(String)
    jan = Column(String(13), unique=True)
    id_by_official = Column(String)
    checksum = Column(String(32))
    order_period_start = Column(DateTime(timezone=True))
    order_period_end = Column(DateTime(timezone=True))
    # ---Foreign key columns---
    series_id = Column(Integer, ForeignKey("series.id"))
    series = relationship("Series", backref="products")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", backref="products")

    manufacturer_id = Column(Integer, ForeignKey("company.id"))

    releaser_id = Column(Integer, ForeignKey("company.id"))

    distributer_id = Column(Integer, ForeignKey("company.id"))
    # ---relationships field---
    release_infos = relationship(
        ProductReleaseInfo,
        backref="product",
        order_by="nulls_first(asc(ProductReleaseInfo.initial_release_date))",
        cascade="all, delete",
        passive_deletes=True,
    )
    official_images = relationship(
        ProductOfficialImage,
        backref="product",
        order_by="ProductOfficialImage.order",
        collection_class=ordering_list("order", count_from=1),
        cascade="all, delete",
        passive_deletes=True
    )
    sculptors = relationship(
        "Sculptor",
        secondary=product_sculptor_table,
        backref="products",
    )
    paintworks = relationship(
        "Paintwork",
        secondary=product_paintwork_table,
        backref="products",
    )

    def last_release(self) -> Union[ProductReleaseInfo, None]:
        release_infos = self.release_infos
        if release_infos:
            return release_infos[-1]
        return None

    def check_checksum(self, checksum: str) -> bool:
        return checksum == self.checksum
