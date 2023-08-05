# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path

import click
import cjkwrap
from bs4 import UnicodeDammit
from ebooklib import epub
from langdetect import detect

from txt2ebook import (
    __version__,
    IDEOGRAPHIC_SPACE,
    SPACE,
    ZH_NUMS_WORDS,
    ZH_FULLWIDTH_NUMS
)


logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True)
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option(
    "--title",
    "-t",
    default=None,
    show_default=True,
    help="Set the title of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    help="Set the author of the ebook.",
)
@click.option(
    "--cover",
    "-c",
    type=click.Path(exists=True),
    default=None,
    help="Set the cover of the ebook.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value=logging.DEBUG,
    show_default=True,
    help="Enable debugging log.",
)
@click.option(
    "--no-backup",
    "-nb",
    is_flag=True,
    flag_value=True,
    show_default=True,
    help="Do not backup source txt file.",
)
@click.option(
    "--no-wrapping",
    "-nw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--width",
    "-w",
    type=click.INT,
    show_default=True,
    help="Set the width for line wrapping.",
)
@click.option(
    "--delete-regex",
    "-dr",
    multiple=True,
    help="Regex to delete word or phrase.",
)
@click.option(
    "--replace-regex",
    "-rr",
    nargs=2,
    multiple=True,
    help="Regex to replace word or phrase.",
)
@click.option(
    "--delete-line-regex",
    "-dlr",
    multiple=True,
    help="Regex to delete whole line.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
def main(**kwargs):
    """
    Console tool to convert txt file to different ebook format.
    """
    logging.basicConfig(
        level=kwargs["debug"] or logging.INFO,
        format="[%(levelname).1s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        filename = Path(kwargs["input_file"])
        logger.info("Processing txt file: '%s'.", filename.resolve())

        with open(filename, "rb") as file:
            unicode = UnicodeDammit(file.read())
            logger.info("Encoding detected: '%s'.", unicode.original_encoding)
            content = unicode.unicode_markup

            if not content:
                raise RuntimeError(f"Empty file content in '{filename}'!")

            kwargs["language"] = kwargs["language"] or detect_language(content)
            kwargs["author"] = kwargs["author"] or detect_author(content)
            kwargs["title"] = kwargs["title"] or detect_book_title(content)
            output_filename = Path(
                kwargs["output_file"]
                or Path(kwargs["title"] or filename).stem + ".epub"
            )

            if kwargs["delete_regex"]:
                content = do_delete_regex(content, kwargs)

            if kwargs["replace_regex"]:
                content = do_replace_regex(content, kwargs)

            if kwargs["delete_line_regex"]:
                content = do_delete_regex(content, kwargs)

            if kwargs["no_wrapping"]:
                content = do_no_wrapping(content)

            if kwargs["width"]:
                content = do_wrapping(content, kwargs)

            chapters = parse_content(content)

        build_txt(filename, content, kwargs["no_backup"])
        if chapters:
            build_epub(output_filename, chapters, kwargs)

    except RuntimeError as error:
        click.echo(f"[E] {str(error)}!", err=True)


def detect_language(content):
    """
    Detect the language (ISO 639-1) of the content of the txt file.
    """
    language = detect(content)
    logger.info("Language detected: '%s'.", language)
    return language


def detect_book_title(content):
    """
    Extract book title from the content of the txt file.
    """
    regex = r"书名：(.*)|【(.*)】|《(.*)》"
    match = re.search(regex, content)
    if match:
        book_title = next(
            (title for title in match.groups() if title is not None)
        )
        logger.info("Found book title: '%s'.", book_title)
        return book_title

    logger.info("No book title found from file!")
    return False


def detect_author(content):
    """
    Extract author from the content of the txt file.
    """
    match = re.search(r"作者：(.*)", content)
    if match:
        author = match.group(1)
        logger.info("Found author: '%s'.", author)
        return author

    logger.info("No author found from file!")
    return False


def do_delete_regex(content, kwargs):
    """
    Remove words/phrases based on regex.
    """
    for delete_regex in kwargs["delete_regex"]:
        content = re.sub(
            re.compile(rf"{delete_regex}", re.MULTILINE), "", content
        )
    return content


def do_replace_regex(content, kwargs):
    """
    Replace words/phrases based on regex.
    """
    for search, replace in kwargs["replace_regex"]:
        content = re.sub(
            re.compile(rf"{search}", re.MULTILINE), rf"{replace}", content
        )
    return content


def do_delete_line_regex(content, kwargs):
    """
    Delete whole line based on regex.
    """
    for delete_line_regex in kwargs["delete_line_regex"]:
        content = re.sub(
            re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
            "",
            content,
        )
    return content


def do_no_wrapping(content):
    """
    Remove wrapping. Paragraph should be in one line.
    """
    # Convert to single spacing before we removed wrapping.
    lines = content.split("\n")
    content = "\n\n".join([line.strip() for line in lines if line])

    unwrapped_content = ""
    for line in content.split("\n\n"):
        # if a line contains more opening quote(「) than closing quote(」),
        # we're still within the same paragraph.
        # e.g.:
        # 「...」「...
        # 「...
        if line.count("「") > line.count("」"):
            unwrapped_content = unwrapped_content + line.strip()
        elif (
            re.search(r"[…。？！]{1}」?$", line)
            or re.search(r"」$", line)
            or re.match(r"^[ \t]*……[ \t]*$", line)
            or re.match(r"^「」$", line)
            or re.match(r".*[》：＊\*]$", line)
            or re.match(r".*[a-zA-Z0-9]$", line)
        ):
            unwrapped_content = unwrapped_content + line.strip() + "\n\n"
        elif re.match(chapter_regexs(), line):
            # replace full-width space with half-wdith space.
            # looks nicer on the output.
            header = line.replace(IDEOGRAPHIC_SPACE*2, SPACE).replace(
                IDEOGRAPHIC_SPACE, SPACE
            )
            unwrapped_content = (
                unwrapped_content + "\n\n" + header.strip() + "\n\n"
            )
        else:
            unwrapped_content = unwrapped_content + line.strip()

    return unwrapped_content


def do_wrapping(content, kwargs):
    """
    Wrapping and filling CJK text.
    """
    logger.info("Wrapping paragraph to width: %s.", kwargs["width"])

    paragraphs = []
    # We don't remove empty line and keep all formatting as it.
    for paragraph in content.split("\n"):
        paragraph = paragraph.strip()

        lines = cjkwrap.wrap(paragraph, width=kwargs["width"])
        paragraph = "\n".join(lines)
        paragraphs.append(paragraph)

    wrapped_content = "\n".join(paragraphs)
    return wrapped_content


# # Single spacing.
# lines = content.split("\n")
# content = "\n\n".join([line.strip() for line in lines if line])


def parse_content(content):
    """
    Parse the content into volumes (if exists) and chapters.
    """

    spaces = f"[{SPACE}\t{IDEOGRAPHIC_SPACE}]"
    volume_seq = f"[0-9{ZH_FULLWIDTH_NUMS}{ZH_NUMS_WORDS}]"
    volume_regex = f"^{spaces}*第{volume_seq}*[集卷册][^。~\n]*$"
    volume_pattern = re.compile(rf"{volume_regex}", re.MULTILINE)
    volume_headers = re.findall(volume_pattern, content)

    if not volume_headers:
        logger.info("Parsed 0 volumes.")
        parsed_content = parse_chapters(content)
        if parsed_content:
            logger.info("Parsed %s chapters.", len(parsed_content))
        else:
            logger.error("Parsed 0 chapters.")
    else:
        logger.info("Parsed %s volumes.", len(volume_headers))
        volume_bodies = re.split(volume_pattern, content)
        volumes = list(zip(volume_headers, volume_bodies[1:]))

        parsed_content = []
        for volume_header, body in volumes:
            parsed_body = parse_chapters(body)
            if parsed_body:
                parsed_content.append((volume_header, parsed_body))
            else:
                logger.error(
                    "Parsed 0 chapters for volume: '%s'.", volume_header
                )

    return parsed_content


def parse_chapters(content):
    """
    Split the content of txt file into chapters by chapter header.
    """
    chapter_regex = chapter_regexs()
    chapter_pattern = re.compile(rf"{chapter_regex}", re.MULTILINE)
    chapter_headers = re.findall(chapter_pattern, content)

    if not chapter_headers:
        return False

    bodies = re.split(chapter_pattern, content)
    chapters = list(zip(chapter_headers, bodies[1:]))

    return chapters


def chapter_regexs():
    """
    Regex rules for chapter headers.
    """
    spaces = f"[{SPACE}\t{IDEOGRAPHIC_SPACE}]"
    chapter_seq = f"[.0-9{ZH_FULLWIDTH_NUMS}{ZH_NUMS_WORDS}]"

    regexs = (
        f"^{spaces}*第{chapter_seq}*[章篇回折][^。\n]*$",
        f"^{spaces}*[楔引]子[^，].*$",
        f"^{spaces}*序[章幕曲]?.*$",
        f"^{spaces}*前言.*$",
        f"^{spaces}*[内容]*简介.*$",
        f"^{spaces}*[号番]外篇.*$",
        f"^{spaces}*尾声$",
    )
    return "|".join(regexs)


def build_txt(filename, parsed_content, no_backup):
    """
    Generate txt from parsed content from original txt file.
    """
    txt_filename = Path(filename)

    if not no_backup:
        ymd_hms = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = Path(
            txt_filename.resolve().parent.joinpath(
                txt_filename.stem + "_" + ymd_hms + ".bak.txt"
            )
        )
        os.rename(txt_filename, backup_filename)
        logger.info("Backup txt file: '%s'.", backup_filename)

    with open(txt_filename, "w") as file:
        file.write(parsed_content)
        logger.info("Overwrite txt file: '%s'.", txt_filename.resolve())


def build_epub(output_filename, parsed_content, kwargs):
    """
    Generate epub from the parsed chapters from txt file.
    """

    book = epub.EpubBook()

    if kwargs["title"]:
        book.set_title(kwargs["title"])

    if kwargs["language"]:
        book.set_language(kwargs["language"])

    if kwargs["author"]:
        book.add_author(kwargs["author"])

    if kwargs["cover"]:
        with open(kwargs["cover"], "rb") as image:
            book.set_cover("cover.jpg", image.read())
            book.spine += ["cover"]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine += ["nav"]
    for header, body in parsed_content:
        if isinstance(body, list):
            logger.debug(header)
            html_chapters = []
            for chapter_title, chapter_body in body:
                html_chapter = build_html_chapter(
                    chapter_title, chapter_body, header
                )
                book.add_item(html_chapter)
                book.spine += [html_chapter]
                html_chapters.append(html_chapter)
            book.toc += [(epub.Section(header), html_chapters)]
        else:
            html_chapter = build_html_chapter(header, body)
            book.add_item(html_chapter)
            book.spine += [html_chapter]
            book.toc += [html_chapter]

    output_filename.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(output_filename, book, {})
    logger.info("Generating epub file: '%s'.", output_filename)


def build_html_chapter(title, body, volume=None):
    """
    Generates the whole chapter to HTML.
    """
    if volume:
        filename = f"{volume}_{title}"
        logger.debug("%s%s" % SPACE*2, title)
    else:
        filename = title
        logger.debug(title)

    filename = filename.replace(SPACE, "_")

    html = f"<h2>{title}</h2>"
    for paragraph in body.split("\n\n"):
        paragraph = paragraph.replace(SPACE, "").replace("\n", "")
        html = html + f"<p>{paragraph}</p>"

    return epub.EpubHtml(
        title=title,
        content=html,
        file_name=filename + ".xhtml",
    )


if __name__ == "__main__":
    main()
