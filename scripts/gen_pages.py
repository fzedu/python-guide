#!/usr/bin/env python

from __future__ import annotations

import pathlib
import json
import yaml
import click
import logging
import re


root = pathlib.Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


def nb_convert(infile: str, outfile: str, lang = "ru"):
    """Convert ipynb file to markdown format.

    :param infile:
        Path to the ipynb file.
    :param outfile:
        Path to the output file.
    :param lang:
        Language of the content.
    """
    path = pathlib.Path(infile).resolve()
    notebook = json.load(open(path, "r"))
    markdown = open(pathlib.Path(outfile).resolve(), "w")

    #   templates
    header_tmpl = "---\nlayout: default\ntitle: {title}\nmathjax: true\n---\n\n"
    code_tmpl = "```{lang}\n{code}\n```\n"
    image_tmpl = '<p><img src="data:{mimetype};base64,{data}"></p>\n'
    html_tmpl = "<p>{content}</p>\n"

    #   file header
    title = path.name.replace(path.suffix, "")
    m = re.match("^\d+.", title)

    if m:
        title = title.replace(m.group(), "")

    markdown.write(header_tmpl.format(
        title = title
    ))

    #   content
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            markdown.write("".join(cell["source"]) + "\n")

        elif cell["cell_type"] == "code":
            #   source block
            markdown.write(code_tmpl.format(
                code = "".join(
                    [ "# In [{}]:\n".format(cell["execution_count"]) ] +
                    cell["source"]
                ),
                lang = "python"
            ))

            #
            markdown.write("\n")

            #   markdown block
            markdown.write("Out [{}]:\n".format(cell["execution_count"]))

            for outputs in cell["outputs"]:
                if outputs["output_type"] == "stream":
                    markdown.write(code_tmpl.format(
                        code = "".join(outputs["text"]),
                        lang = ""
                    ))

                elif outputs["output_type"] == "display_data":
                    for key in outputs["data"].keys():
                        if key.startswith("image"):
                            markdown.write(image_tmpl.format(
                                mimetype = key,
                                data = outputs["data"][key]
                            ))
                
                elif outputs["output_type"] == "execute_result":
                    if "text/html" in outputs["data"].keys():
                        markdown.write(html_tmpl.format(
                            content = "".join(outputs["data"]["text/html"])
                        ))
                    
                    elif "text/plain" in outputs["data"].keys():
                        markdown.write(code_tmpl.format(
                            code = "".join(outputs["data"]["text/plain"]),
                            lang = ""
                        ))
    
        markdown.write("\n")

    markdown.close()


def parse_header(path:str) -> dict | None:
    """Parse markdown file for the yaml header.

    :param path:
        Path to the file.
    :return:
        Parsed header or None if header is not found or empty.
    """
    path = pathlib.Path(path).resolve()

    assert path.is_file() and path.suffix in [".md", ".markdown"], \
        "Specify path to the markdown file"

    buffer = ""
    is_found = False
    infile = open(path, "r")

    for line in infile.readlines():
        if line.strip() == "---":
            if not is_found:
                is_found = True
                continue

            else:
                break

        if is_found:
            buffer += line

    infile.close()

    if not is_found:
        return
    
    else:
        return yaml.safe_load(buffer)


def construct_nav(path: str, root: str) -> dict:
    """Construct one layer navigation from the given
    directory.

    :param path:
        Path to the directory with markdown files.
    :param root:
        Path to the project root directory.
    :return:
        Dictionary with navigation.
    """
    path = pathlib.Path(path).resolve()

    assert path.is_dir(), "Specify path to the directory"

    navigation = []

    for file in path.iterdir():
        if file.is_file() and file.suffix in [".md", ".markdown"]:
            logger.debug("Parsing {}".format(file))
            header = parse_header(file)

            if header is not None:
                if not header.get("published", True):
                    continue
                    
                navigation.append({
                    "title": header["title"],
                    "url": "/" + str(file.relative_to(root)).replace(file.suffix, ".html")
                })
    
    return navigation


@click.command(help = "Convert notebooks to markdown files and create navigation file.")
@click.option("-d", "--debug", default = False, is_flag = True,
    help = "Enable debug messages.")
@click.option("--src-dir", default = root / "guide",
    help = "Specify directory with notebooks.")
@click.option("--out-dir", default = root / "guide",
    help = "Specify output directory for markdown files.")
@click.option("--nav-file", default = root / "_data/toc.yml",
    help = "Specify path for the navigation file.")
def gen_pages(debug, src_dir, out_dir, nav_file):

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    src_dir = pathlib.Path(src_dir).resolve()
    out_dir = pathlib.Path(out_dir).resolve()
    nav_file = pathlib.Path(nav_file).resolve()

    assert src_dir.is_dir()
    assert out_dir.is_dir()
    assert nav_file.is_file()

    logger.info("Converting notebooks to markdown files ...")

    for src in src_dir.iterdir():
        if src.is_file() and src.suffix == ".ipynb":
            outfile = src.parent / src.name.replace(src.suffix, ".md")
            logger.debug("{} -> {}".format(src, outfile))
            nb_convert(src, outfile)
    
    logger.info("Creating navigation file ...")
    yaml.dump(construct_nav(src_dir, root), open(nav_file, "w"))

    logger.info("Done.")


#   cli entry
if __name__ == "__main__":
    gen_pages()
