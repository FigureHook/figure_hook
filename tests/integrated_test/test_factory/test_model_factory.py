from datetime import date

import pytest
from pytest_mock import MockerFixture

from src.constants import ReleaseInfoStatus
from src.Factory import ProductModelFactory
from src.Factory.model_factory import rebuild_release_infos
from src.Models import Product
from src.Models.product import ProductReleaseInfo
from src.Parsers.extension_class import HistoricalReleases, Release
from src.utils.comparater import compare_release_infos


@pytest.fixture
def product_base():
    class MockProductBase:
        release_infos = []

    return MockProductBase()


@pytest.mark.usefixtures("product", "session")
class TestProdcutModelFactory:
    def test_create(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        assert isinstance(p, Product)

    def test_update(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        up = ProductModelFactory.updateProduct(product, p)
        assert isinstance(up, Product)


@pytest.mark.usefixtures("session")
class TestReleaseInfoComparater:
    def test_delay(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 2, 2), 12000)
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 1, 2),
                    price=12000
                )
            ]
        )
        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.DELAY

    def test_same(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(None, 12000),
            Release(date(2020, 2, 2), 12000),
            Release(date(2023, 2, 2), 12000),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.SAME

    def test_stalled(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(None, 12000),
            Release(date(2020, 2, 2), 12000),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.STALLED

    def test_alter(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.ALTER

    def test_new_release(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
            Release(date(2028, 2, 2), 12000),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.NEW_RELEASE

    def test_conflict(self, product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2024, 2, 2),
                    price=12000
                ),
            ]
        )

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.CONFLICT


@pytest.mark.usefixtures("session")
def test_rebuild_release_infos(product_base):
    product_base.release_infos = HistoricalReleases([
        Release(date(2020, 1, 2), 13000),
        Release(date(2023, 2, 2), 12000),
    ])

    p_m = Product.create(
        name="foo",
        release_infos=[
            ProductReleaseInfo(
                initial_release_date=date(2020, 2, 2),
                price=12000
            ),
            ProductReleaseInfo(
                initial_release_date=date(2023, 2, 2),
                price=12000
            ),
        ]
    )

    rebuild_release_infos(product_base.release_infos, p_m.release_infos)

    for dr, pr in zip(product_base.release_infos, p_m.release_infos):
        assert dr.release_date == pr.initial_release_date
        assert dr.price == pr.price