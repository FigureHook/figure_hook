import pytest

from src.Factory import ProductBase, ProductDataProcessMixin, ProductUtils


@pytest.mark.usefixtures("product")
def test_product_base(product: ProductBase):
    p = product
    assert isinstance(product.as_dict(), dict)
    p.url = "https://somthingwrong.com"
    assert p.checksum == product.checksum


def test_product_data_process_mixin(mocker):
    attributes_be_tested = [
        "name",
        "series",
        "manufacturer",
        "releaser",
        "distributer",
        "paintworks",
        "sculptors"
    ]

    class MockProductBase:
        def __init__(self) -> None:
            for attr in attributes_be_tested:
                setattr(self, attr, False)

    class MockProduct(MockProductBase, ProductDataProcessMixin):
        ...

    mocker.patch.object(ProductUtils, "normalize_product_attr", return_value=True)
    mocker.patch.object(ProductUtils, "normalize_worker_attr", return_value=True)

    p = MockProduct()
    p.normalize_attrs()
    assert all([getattr(p, attr) for attr in attributes_be_tested])


class TestProductTextUtils:
    def test_general_attribute_normalization(self):
        text_should_be_half_width = "ＫＡＤＯＫＡＷＡ"
        text_with_duplicate_space = "too  much spaces Ver."
        text_with_weird_quotation = "hello ’there’"

        assert ProductUtils.normalize_product_attr(text_should_be_half_width) == "KADOKAWA"
        assert ProductUtils.normalize_product_attr(text_with_duplicate_space) == "too much spaces Ver."
        assert ProductUtils.normalize_product_attr(text_with_weird_quotation) == "hello 'there'"

    def test_worker_attribute_normalization(self):
        text_with_full_width_brackets = " (Hello, there)"
        text_with_no_space_before_bracket = "Master(HW)"
        text_with_no_space_before_square_bracket = "Newbie[NW]"

        assert ProductUtils.normalize_worker_attr(text_with_full_width_brackets) == "(Hello, there)"
        assert ProductUtils.normalize_worker_attr(text_with_no_space_before_bracket) == "Master (HW)"
        assert ProductUtils.normalize_worker_attr(text_with_no_space_before_square_bracket) == "Newbie (NW)"

    def test_list_attribute_normalization(self):
        attribute_in_list = ["Ｋ", "two  space", "’quote’"]
        assert ProductUtils.normalize_product_attr(attribute_in_list) == ["K", "two space", "'quote'"]

    def test_attribute_normalization_with_exception(self):
        with pytest.raises(TypeError):
            ProductUtils.normalize_product_attr(1)
            ProductUtils.normalize_product_attr([1, 2, 3])