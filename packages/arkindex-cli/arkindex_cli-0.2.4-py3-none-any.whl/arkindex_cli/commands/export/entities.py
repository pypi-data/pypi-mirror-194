# -*- coding: utf-8 -*-
import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from rich.console import Console
from rich.progress import track

from arkindex_cli.commands.export.db import transcription_entities

logger = logging.getLogger(__name__)


def tr_ent_dict(item, instance_url):
    element_url = f"{instance_url.rstrip('/')}/element/{item.element_id}"
    return {
        "transcription_id": item.transcription_id,
        "element_id": item.element_id,
        "element_url": element_url,
        "entity_id": item.entity_id,
        "entity_value": item.entity_value,
        "entity_type": item.entity_type,
        "entity_metas": item.entity_metas,
        "offset": item.offset,
        "length": item.length,
    }


def run(
    database_path: Path,
    output_path: Path,
    instance_url: str,
    profile_slug: Optional[str] = None,
):
    database_path = database_path.absolute()
    assert database_path.is_file(), f"Database at {database_path} not found"

    parsed_url = urlparse(instance_url)
    assert parsed_url.scheme and parsed_url.netloc, f"{instance_url} is not a valid url"

    csv_header = [
        "transcription_id",
        "element_id",
        "element_url",
        "entity_id",
        "entity_value",
        "entity_type",
        "entity_metas",
        "offset",
        "length",
    ]
    tr_entities = transcription_entities(database_path)

    writer = csv.DictWriter(output_path, fieldnames=csv_header)
    writer.writeheader()
    for trent in track(
        tr_entities,
        description="Exporting transcription entities",
        console=Console(file=sys.stderr),
    ):
        serialized_ent = tr_ent_dict(trent, instance_url)
        writer.writerow(serialized_ent)

    logger.info(
        f"Exported transcription entities successfully written to {output_path.name}."
    )


def add_entities_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "entities",
        help="Export entities from a given Arkindex project.",
        description="Export a project's transcription entities.",
    )
    parser.add_argument(
        "--output",
        help="Path to the CSV file which will be created",
        default=sys.stdout,
        type=argparse.FileType("w", encoding="UTF-8"),
        dest="output_path",
    )
    parser.add_argument(
        "--instance-url",
        help="URL of the Arkindex instance of the exported project.",
        type=str,
        required=True,
    )
    parser.set_defaults(func=run)
