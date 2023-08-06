from unittest.mock import patch

from icontract import ViolationError
import pytest

from valuation_office_ireland.download import download_valuation_office_categories


invalid_inputs = [
    ([], [], None),
    ("X", "OFFICE", "csv"),
    ("CAVAN COUNTY COUNCIL", "OFFICE", None),
    ("CAVAN COUNTY COUNCIL", "X", "csv"),
]


@patch("valuation_office_ireland.download._download_categories")
@pytest.mark.parametrize("local_authorities,categories,filetype", invalid_inputs)
def test_download_fails_on_invalid_input(
    mock_download, local_authorities, categories, filetype, tmp_path,
):

    with pytest.raises(ViolationError):
        download_valuation_office_categories(
            savedir=tmp_path,
            local_authorities=local_authorities,
            categories=categories,
            filetype=filetype,
        )
