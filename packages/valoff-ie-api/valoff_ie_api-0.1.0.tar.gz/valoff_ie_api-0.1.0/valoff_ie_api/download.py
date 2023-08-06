import json
from pathlib import Path
import os
import requests
from requests import HTTPError
from typing import List
from typing import Union
from urllib.request import quote

from icontract import require
from loguru import logger

HERE = os.path.dirname(__file__)

with open(Path(HERE) / "local_authorities.json") as file:
    LOCAL_AUTHORITIES = [x["LaDesc"] for x in json.load(file)]

with open(Path(HERE) / "categories.json") as file:
    CATEGORIES = [x["categorydesc"] for x in json.load(file)]

FILETYPES = ["csv", "json", "geojson"]


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj

    return dec


def _standardise_group(group, global_group):
    if group == "all":
        group = global_group
    elif isinstance(group, str):
        group = [group]
    else:
        logger.debug(f"{group} unchanged")

    return group


def _create_dir(dirpath):
    if dirpath.exists():
        logger.info(f"Skipping creation of {dirpath} as already exists...")
    else:
        os.mkdir(dirpath)


def _make_get_request(local_authority, category, filetype):
    local_authority_without_whitespace = local_authority.replace(" ", r"%20")
    url = (
        "https://api.valoff.ie/api/Property/GetProperties?"
        "Fields=*"
        f"&LocalAuthority={local_authority_without_whitespace}"
        f"&CategorySelected={category}"
        f"&Format={filetype}"
        "&Download=true"
    )
    logger.debug(f"Request: {url}")
    try:
        response = requests.get(url)
    except HTTPError as error:
        logger.error(error)

    return response


def _download_categories(savepath, local_authorities, categories, filetype):
    for local_authority in local_authorities:
        for category in categories:
            response = _make_get_request(local_authority, category, filetype)
            category_without_slashes = category.replace("/", " or ")
            filepath = savepath / f"{local_authority} - {category_without_slashes}.{filetype}"
            logger.info(
                f"Downloading {local_authority} | {category} to '{filepath}'"
            )
            with open(filepath, "wb") as file:
                file.write(response.content)


@require(lambda filetype: filetype in FILETYPES)
@require(
    lambda local_authorities: local_authorities in LOCAL_AUTHORITIES + ["all"]
    or set(local_authorities).issubset(LOCAL_AUTHORITIES + ["all"]),
)
@require(
    lambda categories: categories in CATEGORIES + ["all"]
    or set(categories).issubset(CATEGORIES + ["all"]),
)
@docstring_parameter(Path.cwd(), LOCAL_AUTHORITIES, CATEGORIES, FILETYPES)
def download_valuation_office_categories(
    savedir: str = Path.cwd(),
    local_authorities: Union[List[str], str] = "all",
    categories: Union[List[str], str] = "all",
    filetype: str = "csv",
):
    """Download Valuation Office categories.

    Args:
        savedir (str): Path to save directory. Defaults to {0}
        local_authorities (List[str], optional): Any of {1}. Defaults to 'all'.
        categories (List[str], optional): Any of {2}. Defaults to 'all'.
        filetype (str, optional): Any of {3}. Defaults to 'csv'.
    """
    savepath = Path(savedir) / "valuation_office"
    _create_dir(savepath)
    local_authorities = _standardise_group(local_authorities, LOCAL_AUTHORITIES)
    categories = _standardise_group(categories, CATEGORIES)
    _download_categories(savepath, local_authorities, categories, filetype)
