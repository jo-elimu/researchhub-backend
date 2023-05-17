import os
import shutil
import subprocess

from lxml import etree

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
NSMAP = {"tei": TEI_NAMESPACE}


def convert_xml_to_tei(xml_filepath, xslt_filepath):
    # Parse the XSLT file
    xslt_root = etree.parse(xslt_filepath)
    transform = etree.XSLT(xslt_root)

    # Parse the XML data
    xml_root = etree.parse(xml_filepath)

    # Transform the XML data to HTML
    result_tree = transform(xml_root)

    return str(result_tree)


def extract_data_from_pdf(input_dir, output_dir):
    grobid_root = "./grobid-0.7.3"
    grobid_home = f"{grobid_root}/grobid-home"  # Replace with the actual path to your Grobid installation
    grobid_jar = f"{grobid_root}/grobid-core/build/libs/grobid-core-0.7.3-onejar.jar"  # Replace with the correct Grobid JAR file

    # Construct the Grobid batch command
    command = [
        "java",
        "-Xmx4G",
        "-Djava.library.path={}/lib/lin-64:{}/lib/lin-64/jep".format(
            grobid_home, grobid_home
        ),
        "-jar",
        grobid_jar,
        "-gH",
        grobid_home,
        "-dIn",
        input_dir,
        "-dOut",
        output_dir,
        "-exe",
        "processFullText",
    ]

    # Execute the Grobid batch command
    subprocess.run(command)

    return True


def get_id_to_url_mapping(tei_filepath):
    tei = etree.parse(tei_filepath)
    # Get the root of the tree
    root = tei.getroot()
    # Get the namespace
    ns = {
        "tei": root.tag.split("}")[0].strip("{"),
        "xml": "http://www.w3.org/XML/1998/namespace",
    }

    figures = root.findall(".//tei:figure", ns)

    figure_urls = {}
    for figure in figures:
        figure_id = figure.get("{http://www.w3.org/XML/1998/namespace}id")
        graphic = figure.find(".//tei:graphic", ns)
        if graphic is not None:
            figure_urls[figure_id] = graphic.get("url")

    return figure_urls


def copy_element(src, dst_parent, id_to_url_mapping, assets_path):
    if src.tag == f"{{{TEI_NAMESPACE}}}ref" and src.get("type") == "figure":
        ref_id = src.get("target").lstrip("#")
        img_url = id_to_url_mapping.get(ref_id)
        if img_url is not None:
            new_element = etree.Element("img")
            new_element.set("src", f"{assets_path}/{img_url}")
            new_element.set(
                "style", "max-height: 300px; display: block; margin: 0 auto;"
            )
        else:
            new_element = etree.Element(src.tag.split("}")[-1])
    else:
        new_element = etree.Element(src.tag.split("}")[-1])
        new_element.text = src.text
    for child in src:
        copy_element(child, new_element, id_to_url_mapping, assets_path)
    if src.tail:
        if len(dst_parent):
            last_child = dst_parent[-1]
            if last_child.tail is None:
                last_child.tail = src.tail
            else:
                last_child.tail += src.tail
        else:
            if dst_parent.text is None:
                dst_parent.text = src.tail
            else:
                dst_parent.text += src.tail
    dst_parent.append(new_element)


def transform_tree(src, dst_parent, id_to_url_mapping, assets_path, head_level=2):
    for child in src:
        if child.tag == f"{{{TEI_NAMESPACE}}}div":
            div = etree.Element("div")
            if len(child) == 1 and child[0].tag == f"{{{TEI_NAMESPACE}}}head":
                if child.getparent().tag == "body":
                    head_level = 2
                else:
                    head_level = 3

                head = etree.Element(f"h{head_level}")
                head.text = child[0].text
                if child[0].tail:
                    if len(dst_parent):
                        last_child = dst_parent[-1]
                        if last_child.tail is None:
                            last_child.tail = child[0].tail
                        else:
                            last_child.tail += child[0].tail
                    else:
                        if dst_parent.text is None:
                            dst_parent.text = child[0].tail
                        else:
                            dst_parent.text += child[0].tail
                div.append(head)
                head_level = 2
            else:
                transform_tree(
                    child, div, id_to_url_mapping, assets_path, min(head_level + 1, 6)
                )
            dst_parent.append(div)
        elif child.tag == f"{{{TEI_NAMESPACE}}}head":
            head = etree.Element(f"h{head_level}")
            head.text = child.text
            if child.tail:
                if len(dst_parent):
                    last_child = dst_parent[-1]
                    if last_child.tail is None:
                        last_child.tail = child.tail
                    else:
                        last_child.tail += child.tail
                else:
                    if dst_parent.text is None:
                        dst_parent.text = child.tail
                    else:
                        dst_parent.text += child.tail
            dst_parent.append(head)
        else:
            copy_element(child, dst_parent, id_to_url_mapping, assets_path)


def convert_tei_to_html(tei_file, html_file, id_to_url_mapping, assets_path):
    tei_tree = etree.parse(tei_file)
    html_root = etree.Element("html")
    head = etree.SubElement(html_root, "head")
    body = etree.SubElement(html_root, "body")

    abstract = tei_tree.find(".//tei:abstract", namespaces=NSMAP)
    if abstract is not None:
        transform_tree(abstract, body, id_to_url_mapping, assets_path)

    tei_body = tei_tree.find(".//tei:body", namespaces=NSMAP)
    if tei_body is not None:
        transform_tree(tei_body, body, id_to_url_mapping, assets_path)

    with open(html_file, "wb") as f:
        f.write(etree.tostring(html_root, method="html", pretty_print=True))


def get_filename_without_extension(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def copy_file(file_path, output_dir):
    # Extract the filename without the path
    file_name = os.path.basename(file_path)

    # Construct the output file path in the destination directory
    output_path = os.path.join(output_dir, file_name)

    # Copy the file to the destination directory
    shutil.copy(file_path, output_path)

    return output_path


# Config
filepath = "./example2.pdf"
input_dir = "./grobid-input"
output_dir = "./grobid-output"

# Step 1: Copy file to input directory
filename = get_filename_without_extension(filepath)
copy_file(filepath, input_dir)

# Step 2: Extract data and images from PDF, and convert to TEI.
extract_data_from_pdf(input_dir, output_dir)

# Step 3: Get figure mapping
tei_filepath = f"{output_dir}/{filename}.tei.xml"
id_to_figure_mapping = get_id_to_url_mapping(tei_filepath)
print(id_to_figure_mapping)

# Step 3: Convert TEI to HTML

output_html_filepath = f"{output_dir}/{filename}.html"
assets_path = f"{filename}_assets"
convert_tei_to_html(
    tei_filepath, output_html_filepath, id_to_figure_mapping, assets_path
)
