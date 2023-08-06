# -*- coding: utf-8 -*-
import csv
import errno
import json
import logging
import re
from pathlib import Path
from typing import Optional
from uuid import UUID
from xmlrpc.client import Boolean

from apistar.exceptions import ErrorResponse
from arkindex import ArkindexClient
from lxml import etree as ET
from lxml import objectify
from rich.progress import Progress, track

from arkindex_cli.argtypes import URLArgument
from arkindex_cli.auth import Profiles
from arkindex_cli.commands.upload.alto.parser import AltoElement, RootAltoElement

REGEX_IMAGE_ID = re.compile(r"0+(\d+)")

logger = logging.getLogger(__name__)


def add_alto_parser(subcommands):
    gallica = subcommands.add_parser(
        "gallica",
        help="The images are on Gallica IIIF server.",
    )
    gallica.add_argument(
        "--metadata-file",
        help="CSV that contains the metadata related to the Gallica import.",
        required=True,
        type=Path,
    )
    gallica.add_argument(
        "--alto-namespace",
        help="Specify an Alto namespace to use.",
        required=False,
        type=str,
    )
    gallica.add_argument(
        "path",
        help="Path to a directory which contains ALTO XML documents. Defaults to the current working directory.",
        type=Path,
        default=Path.cwd(),
    )
    gallica.add_argument(
        "--iiif-base-url",
        help="Base URL for the IIIF images, which will be prepended to all source image file names.",
        type=URLArgument(allow_query=False),
        required=True,
    )
    gallica.add_argument(
        "--parent-id",
        help="UUID of a parent folder under which page elements will be created.",
        type=UUID,
        required=True,
    )
    gallica.add_argument(
        "--json-summary",
        help="Build a JSON file creation report for each parsed ALTO file.",
        action="store_true",
    )
    types = gallica.add_mutually_exclusive_group(required=True)
    types.add_argument(
        "--create-types",
        help="Create an element type in the Arkindex corpus for each element type in the ALTO files.",
        action="store_true",
    )
    types.add_argument(
        "--existing-types",
        help='Specify correspondences between element types in the Arkindex corpus and in the ALTO files. Format: --existing-types="alto_type:arkindex_type alto_type_2:arkindex_type_2"',
        type=str,
    )
    gallica.set_defaults(func=run_gallica)
    alto = subcommands.add_parser(
        "alto",
        description="Upload ALTO XML documents to Arkindex.",
        help="Upload ALTO XML documents to Arkindex.",
    )
    alto.add_argument(
        "--alto-namespace",
        help="Specify an Alto namespace to use.",
        required=False,
        type=str,
    )
    alto.add_argument(
        "path",
        help="Path to a directory which contains ALTO XML documents. Defaults to the current working directory.",
        type=Path,
        default=Path.cwd(),
    )
    alto.add_argument(
        "--iiif-base-url",
        help="Base URL for the IIIF images, which will be prepended to all source image file names.",
        type=URLArgument(allow_query=False),
        required=True,
    )
    alto.add_argument(
        "--parent-id",
        help="UUID of a parent folder under which page elements will be created.",
        type=UUID,
        required=True,
    )
    alto.add_argument(
        "--json-summary",
        help="Build a JSON file creation report for each parsed ALTO file.",
        action="store_true",
    )
    types = alto.add_mutually_exclusive_group(required=True)
    types.add_argument(
        "--create-types",
        help="Create an element type in the Arkindex corpus for each element type in the ALTO files.",
        action="store_true",
    )
    types.add_argument(
        "--existing-types",
        help='Specify correspondences between element types in the Arkindex corpus and in the ALTO files. Format: --existing-types="alto_type:arkindex_type alto_type_2:arkindex_type_2"',
        type=str,
    )
    alto.set_defaults(func=run)


def check_element_type(corpus: dict, type_slug: str) -> None:
    types = {type["slug"] for type in corpus["types"]}
    if type_slug not in types:
        raise ValueError(f"Type {type_slug} not found.")
    return True


def create_iiif_image(client: ArkindexClient, url: str) -> str:
    try:
        image = client.request("CreateIIIFURL", body={"url": url})
        return image["id"]
    except ErrorResponse as e:
        # When the image already exists, its ID is returned in a HTTP 400
        if e.status_code == 400 and "id" in e.content:
            return e.content["id"]
        raise


def get_element_type(
    client: ArkindexClient,
    corpus_id: UUID,
    node_name: str,
    types_dict: Optional[dict],
    create_types: Boolean = False,
):
    """
    Retrieve or create an alto node's corresponding Arkindex element type.
    """
    arkindex_corpus_types = [
        item["slug"] for item in client.request("RetrieveCorpus", id=corpus_id)["types"]
    ]
    if types_dict is not None:
        if node_name not in types_dict:
            logger.info(
                f"Skipping alto element {node_name}: not in given types dictionary."
            )
        else:
            return types_dict[node_name]
    elif create_types:
        if node_name not in arkindex_corpus_types:
            logger.info(
                f"Creating element type {node_name} in target corpus {corpus_id}…"
            )
            try:
                client.request(
                    "CreateElementType",
                    body={
                        "slug": node_name,
                        "display_name": node_name,
                        "corpus": corpus_id,
                    },
                )
            except ErrorResponse as e:
                logger.error(
                    f"Failed to create element type {node_name} in target corpus {corpus_id}."
                )
                raise Exception(e.content)
        else:
            logger.info(
                f"Element type {node_name} exists in target corpus {corpus_id}."
            )
        return node_name


def create_elements(
    client, item, image_id, element_name, corpus, parent_id, types_dict, create_types
):
    # Specific handling of the Page node, which is the "base" element created from the
    # image on Arkindex, and which is parent to all other elements.
    if type(item) == AltoElement and item.node_name == "page":
        page_node = item
        # For page nodes, a polygon can be defined by WIDTH, HEIGHT, V_POS and H_POS
        # like other nodes, or from WIDTH and HEIGHT only.
        if page_node.polygon:
            page_polygon = page_node.polygon
        else:
            page_polygon = [
                [0, 0],
                [0, page_node.height],
                [page_node.width, page_node.height],
                [page_node.width, 0],
                [0, 0],
            ]
        logger.info(f"Creating page {element_name}…")
        page = client.request(
            "CreateElement",
            body={
                "corpus": corpus["id"],
                "parent": str(parent_id),
                "type": get_element_type(
                    client,
                    corpus["id"],
                    page_node.node_name,
                    types_dict,
                    create_types,
                ),
                "name": element_name,
                "image": image_id,
                "polygon": page_polygon,
            },
            slim_output=True,
        )
        # Publish ALTO ID as metadata
        client.request(
            "CreateMetaData",
            id=page["id"],
            body={"name": "Alto ID", "value": page_node.name, "type": "reference"},
        )
        page_subelements = page_node.serialized_children
        elements = {page_node.name: page["id"]}
        for subelement in page_subelements:
            elements.update(
                create_elements(
                    client=client,
                    item=subelement,
                    image_id=image_id,
                    element_name=None,
                    corpus=corpus,
                    parent_id=page["id"],
                    types_dict=types_dict,
                    create_types=create_types,
                )
            )
    elif type(item) == dict:
        elements = {}
        if "polygon" in item:
            base_dict = item.copy()
            base_dict.pop("children")
            base_dict.pop("text", None)
            element_name = "0"
            if "name" in base_dict:
                element_name = base_dict["name"]
            element_type = get_element_type(
                client, corpus["id"], base_dict["type"], types_dict, create_types
            )
            if element_type:
                element_body = {
                    "type": element_type,
                    "name": element_name,
                    "parent": parent_id,
                    "corpus": corpus["id"],
                    "image": image_id,
                    "polygon": base_dict["polygon"],
                }
                logger.info(f"Creating {element_type} {element_name}…")
                try:
                    created_element = client.request(
                        "CreateElement", body=element_body, slim_output=True
                    )
                    # Publish ALTO ID as metadata
                    client.request(
                        "CreateMetaData",
                        id=created_element["id"],
                        body={
                            "name": "Alto ID",
                            "value": element_name,
                            "type": "reference",
                        },
                    )

                    parent_id = created_element["id"]
                    elements[element_name] = parent_id

                except ErrorResponse as e:
                    raise Exception(
                        f"Could not create the element {element_name} with type {element_type}: HTTP {e.status_code} - {e.content}"
                    )

                # Create transcription if there is one
                if "text" in item:
                    transcription_body = {"text": item["text"]}
                    logger.info(
                        f"Creating transcription {item['text']} for {element_type} {element_name}…"
                    )
                    try:
                        client.request(
                            "CreateTranscription",
                            id=created_element["id"],
                            body=transcription_body,
                        )
                    except ErrorResponse as e:
                        logger.error(
                            f"Could not create the transcription for element {created_element['id']}: HTTP {e.status_code} - {e.content}"
                        )
            else:
                parent_id = parent_id
        if len(item["children"]) > 0:
            for child in item["children"]:
                elements.update(
                    create_elements(
                        client,
                        child,
                        image_id,
                        None,
                        corpus,
                        parent_id,
                        types_dict,
                        create_types,
                    )
                )
    return elements


def format_url(path: Path, iiif_base_url: str, folders_ark_id_dict: dict = None):
    """
    This function is used to create the url to get the image from the Gallica IIIF server
    """
    # The path.name looks like 18840615_1-0003.xml with the folder id being the 18840615 which we use to
    # find the ark_id in order to get the folder from the Gallica server in this case it is ark:/12148/bpt6k7155522
    # the image id is 3 which we add to the url to get the image within the folder on Gallica so this gives us ark:/12148/bpt6k7155522/f3
    # the final link will be http://gallica.bnf.fr/iiif/ark:/12148/bpt6k7155522/f1
    if "-" in path.name:
        basename = path.name.split("-")[1]
        file_extension = path.name.split("-")[0]
        folder_id = file_extension.split("_")[0]
    else:
        # path looks like <folder_id>/ocr/image_id.xml
        folder_id = str(path).split(sep="/")[0]
        basename = path.name
    image_id = basename.replace(".xml", "")
    ark_id = folders_ark_id_dict[folder_id]
    return f"{iiif_base_url}{ark_id}/f{parse_image_idx(image_id)}"


def parse_image_idx(image_id):
    # Remove leading 0s
    image_idx = REGEX_IMAGE_ID.search(image_id)
    assert image_idx, f"Could not parse the image IDX from `{image_id}`"
    return image_idx.group(1)


def upload_alto_file(
    path: Path,
    client: ArkindexClient,
    iiif_base_url: str,
    corpus: dict,
    parent_id: UUID,
    types_dict: Optional[dict],
    create_types: Boolean,
    gallica: bool = False,
    folders_ark_id_dict: dict = None,
    alto_namespace: str = None,
    json_summary: bool = False,
) -> None:
    with open(path) as file:
        # This ensures that comments in the XML files do not cause the
        # "no Alto namespace found" exception.
        parser = ET.XMLParser(remove_comments=True)
        tree = objectify.parse(file, parser=parser)
        root = RootAltoElement(tree.getroot(), alto_namespace=alto_namespace)

    # Skip empty files immediately
    if not len(root.content):
        logger.warning(f"No content found in file {path}")
        return

    page_nodes = root.content.findall(".//{*}Page", namespaces=root.namespaces)
    if len(page_nodes) == 1:
        # We use + here and not urljoin or path.join to create image URLs
        # because the base URL could contain a portion of the identifier:
        # 'http://server/iiif/root%2Fdirectory'
        # urljoin or path.join would erase that identifier prefix.
        if gallica:
            url = format_url(path, iiif_base_url, folders_ark_id_dict)
            image_id = create_iiif_image(client, url)
        else:
            image_id = create_iiif_image(client, iiif_base_url + root.filename)
        page_name = root.filename
        page_node = AltoElement(page_nodes[0], alto_namespace=alto_namespace)
        page_node.parse_children()
        elements = create_elements(
            client,
            page_node,
            image_id,
            page_name,
            corpus,
            parent_id,
            types_dict,
            create_types,
        )
    elif len(page_nodes) > 1:
        elements = {}
        for page_node in page_nodes:
            page_node = AltoElement(page_node, alto_namespace=alto_namespace)
            if page_node.page_image_id is None:
                logger.warning(
                    "Attribute PHYSICAL_IMG_NR was not set for this Page node. Skipping…"
                )
                return
            image_id = create_iiif_image(
                client, iiif_base_url + page_node.page_image_id
            )
            page_name = page_node.name
            elements.update(
                create_elements(
                    client,
                    page_node,
                    image_id,
                    page_name,
                    corpus,
                    parent_id,
                    types_dict,
                    create_types,
                )
            )
    else:
        logger.warning(f"No Page node found in file {root.filename}. Skipping…")
        return

    if json_summary:
        with open(path.with_suffix(".json"), "w") as f:
            json.dump(
                {
                    "alto_file": str(path),
                    "arkindex_api_url": client.document.url,
                    "elements": elements,
                },
                f,
                sort_keys=True,
                indent=4,
            )


def run_gallica(
    path: Path,
    iiif_base_url: str,
    parent_id: UUID,
    create_types: Boolean,
    existing_types: Boolean,
    metadata_file: Path = None,
    json_summary: bool = False,
    profile_slug: Optional[str] = None,
    alto_namespace: str = None,
):
    # If this is a Gallica import, load the metadata CSV file
    folders_ark_id_dict = dict()
    with open(metadata_file, "r") as file:
        reader = csv.reader(file)
        # Create a dictionary with the folder name as the id and the Gallica Ark ID as the value
        folders_ark_id_dict = {row[0]: row[1] for row in reader}
    run(
        path=path,
        iiif_base_url=iiif_base_url,
        parent_id=parent_id,
        create_types=create_types,
        existing_types=existing_types,
        folders_ark_id_dict=folders_ark_id_dict,
        gallica=True,
        profile_slug=profile_slug,
        alto_namespace=alto_namespace,
        json_summary=json_summary,
    )


def run(
    path: Path,
    iiif_base_url: str,
    parent_id: UUID,
    create_types: Boolean,
    existing_types: Boolean,
    folders_ark_id_dict: dict = None,
    profile_slug: Optional[str] = None,
    gallica: bool = False,
    alto_namespace: str = None,
    json_summary: bool = False,
) -> int:

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Loading API client")
        client = Profiles().get_api_client_or_exit(profile_slug)

    if not path.is_dir():
        logger.error(f"{path} is not a directory.")
        return errno.ENOTDIR

    file_paths = list(path.rglob("*.xml"))
    if not file_paths:
        logger.error(f"No XML files found in {path}.")

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Fetching parent element")
        try:
            parent = client.request("RetrieveElement", id=parent_id)
        except ErrorResponse as e:
            logger.error(
                f"Could not retrieve parent element {parent_id}: HTTP {e.status_code} - {e.content}"
            )
            return errno.EREMOTEIO

    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Fetching corpus")
        corpus_id = parent["corpus"]["id"]
        try:
            corpus = client.request("RetrieveCorpus", id=corpus_id)
        except ErrorResponse as e:
            logger.error(
                f"Could not retrieve corpus {corpus_id}: HTTP {e.status_code} - {e.content}"
            )
            return errno.EREMOTEIO

    types_dict = None
    if existing_types:
        split_str = existing_types.split(" ")
        types_dict = {}
        for item in split_str:
            split_item = item.split(":")
            types_dict[str(split_item[0]).lower()] = str(split_item[1]).lower()
        for key, arkindex_type in types_dict.items():
            try:
                check_element_type(corpus, arkindex_type)
            except ValueError as e:
                logger.error(str(e))
                return errno.EINVAL

    failed = 0
    for file_path in track(file_paths, description="Uploading"):
        try:
            upload_alto_file(
                gallica=gallica,
                folders_ark_id_dict=folders_ark_id_dict,
                path=file_path,
                client=client,
                iiif_base_url=iiif_base_url,
                corpus=corpus,
                parent_id=parent_id,
                types_dict=types_dict,
                create_types=create_types,
                alto_namespace=alto_namespace,
                json_summary=json_summary,
            )
        except ErrorResponse as e:
            logger.error(
                f"Upload failed for file {file_path}: HTTP {e.status_code} - {e.content}"
            )
            failed += 1
        except Exception as e:
            logger.error(f"Upload failed for file {file_path}: {e}")
            failed += 1
    # Return a non-zero error code when all files have failed
    return failed >= len(file_paths)
