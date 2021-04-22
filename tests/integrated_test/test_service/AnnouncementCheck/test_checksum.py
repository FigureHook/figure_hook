import pytest

from src.Services.AnnouncementCheck.checksum import GSCChecksum, SiteChecksum


@pytest.mark.usefixtures("session")
class BaseTestChecksum:
    __checksum_class__ = None

    def test_initialize(self):
        site_checksum = self.__checksum_class__()
        assert site_checksum

    def test_property(self):
        site_checksum = self.__checksum_class__()
        assert hasattr(site_checksum, "current")
        assert hasattr(site_checksum, "previous")
        assert hasattr(site_checksum, "is_changed")

    def test_checksum_generation(self):
        site_checksum: SiteChecksum = self.__checksum_class__()
        checksum = site_checksum._generate_checksum()
        assert checksum

    def test_update_checksum(self):
        site_checksum: SiteChecksum = self.__checksum_class__()
        site_checksum.update()
        assert not site_checksum.is_changed

        fetched_site_checksum: SiteChecksum = self.__checksum_class__()
        assert site_checksum.current == fetched_site_checksum.previous


class TestGSC(BaseTestChecksum):
    __checksum_class__ = GSCChecksum

    def test_feature(self):
        site_checksum: GSCChecksum = self.__checksum_class__()
        assert hasattr(site_checksum, "feature")
        assert isinstance(site_checksum.feature, list)