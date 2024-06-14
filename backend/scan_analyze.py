import os
import re
from typing import List
import logging

from tqdm import tqdm
from analyzer import Analyzer
from globals import ALLOWED_IMAGE_EXTENSIONS, MEME_DIRECTORY

from utils import get_exif_data, get_file_dates
from vector_db import VectorDB

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init_dir_search(directory: str, existing_memes: List[str]):
    """
    1. list all files
    2. compare with existing -> find diff
    3. set a task list for memes to be analyzed

    Args:
        directory (str): _description_
    """
    # 1
    file_matching_regex = "(" + "|".join(ALLOWED_IMAGE_EXTENSIONS) + ")$"
    found_matching = []
    found_not_matching = []
    for _root, dirs, files in os.walk(directory, topdown=True):
        root = _root[len(directory) :]
        if root and root.split("/")[-1][0] == ".":  # skip hidden dirs
            continue
        logger.info(f"\n{root} - {len(files)}")
        for file in files:
            if re.search(file_matching_regex, file):
                found_matching.append(root + "/" + file)
            else:
                found_not_matching.append(root + "/" + file)

    total = len(found_matching) + len(found_not_matching)
    prcnt = int(len(found_not_matching) / total * 10000) / 100
    logger.info(
        f"""
***MEME SCAN RESULT***
Total found - {total}
Not matching - {len(found_not_matching)} ({prcnt}%)
"""
    )

    # 2. diff
    new_memes = list(
        set(found_matching).difference(set(existing_memes))
    )  # diff with old
    logger.info(f"New memes scheduled to be added: {len(new_memes)}")
    return new_memes


def add_new_memes_to_db(new_memes: List[str], db: VectorDB):
    analyzed_list = [False] * len(new_memes)
    keywords = [""] * len(new_memes)
    descriptions = [""] * len(new_memes)
    files_created_at = []
    exif_tags_list = []

    for meme in tqdm(new_memes, "populating db with new memes"):
        created_at, _ = get_file_dates(meme)
        exif_dict = get_exif_data(meme)
        files_created_at.append(created_at)
        exif_tags_list.append(exif_dict)

    db.add_memes(
        new_memes,
        descriptions,
        keywords,
        files_created_at,
        exif_tags_list,
        analyzed_list,
    )


def analyze_update_meme(img_path: str, db: VectorDB, analyzer: Analyzer):
    try:
        description, keywords = analyzer.analyze_image(img_path)
        created_at, _ = get_file_dates(img_path)
        exif_dict = get_exif_data(img_path)
        db.add_meme(
            img_path, description, keywords, created_at, exif_dict, analyzed=True
        )
    except Exception as exc:
        logger.error(f"Meme {img_path} hasn't been added due to {exc}.")


def bulk_analysis(img_paths: List[str], db: VectorDB):
    analyzer = Analyzer()
    for img_path in tqdm(img_paths,"Analysis progress"):
        analyze_update_meme(img_path, db, analyzer=analyzer)


def analyze_memes():
    logger.info("***ANALYSIS STARTS***")
    directory = MEME_DIRECTORY
    db = VectorDB()
    memes = init_dir_search(directory, existing_memes=db.get_all_memes()["ids"])
    if(len(memes)> 0):
        add_new_memes_to_db(memes, db)

    to_be_analyzed = db.get_unanalyzed_memes()
    bulk_analysis(to_be_analyzed, db)


if __name__ == "__main__":
    analyze_memes()
# logger.info("ANALYSIS:")
# for meme in tqdm(memes[:10]):
#     logger.debug(meme)
#     created_at, modified_at = get_file_dates(meme)
#     exif_dict = get_exif_data(meme)
#     description, keywords = analyzer.analyze_image(meme)
#     logger.debug(f"""  DESC: {description}\n  KEYWORDS: {keywords}\n CREATED_AT: {created_at}\n EXIF: {exif_dict}""")
#     db.add_meme(meme, description, keywords, created_at, exif_dict)
