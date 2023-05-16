import base64
import json
import os

import fitz  # this is pymupdf
import requests
import xmltodict
from lxml import etree
from lxml.builder import E
from PIL import Image

# def extract_images_from_pdf(pdf_filepath):
#     doc = fitz.open(pdf_filepath)
#     images = []

#     for i in range(len(doc)):
#         for img in doc.get_page_images(i):
#             xref = img[0]
#             base = img[1]
#             img_data = doc.extract_image(xref)
#             images.append((i, base, img_data['image']))

#     return images


def extract_images_from_coordinates(pdf_filepath, coordinates, output_dir):
    doc = fitz.open(pdf_filepath)
    images = []

    for coordinate in coordinates:
        id, coords_string = coordinate
        coords_list = coords_string.split(";")
        for i, coords in enumerate(coords_list):
            page_number, *rect = map(float, coords.split(","))
            page = doc[int(page_number)]
            x, y, w, h = rect
            pix = page.get_pixmap(clip=fitz.Rect(x, y, x + w, y + h))
            print(f"Pix width: {pix.width}, Pix height: {pix.height}, Rect: {rect}")
            if pix.colorspace.name == "DeviceRGB":
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            elif pix.colorspace.name == "DeviceGray":
                img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
            else:
                continue  # skip unsupported colorspaces
            images.append((id, img))
            img.save(os.path.join(output_dir, f"{id}_{i}.png"))  # Save image

    return images


def get_image_data_url(image_tuple):
    # image_tuple format: (page_number, image_name, image_data)
    image_data = image_tuple[2]
    image_format = "png"  # assume PNG format, you might need to adjust this

    # base64-encode the image data
    encoded_data = base64.b64encode(image_data).decode()

    # construct the data URL
    data_url = f"data:image/{image_format};base64,{encoded_data}"

    return data_url


def convert_xml_to_tei(xml_filepath, xslt_filepath):
    # Parse the XSLT file
    xslt_root = etree.parse(xslt_filepath)
    transform = etree.XSLT(xslt_root)

    # Parse the XML data
    xml_root = etree.parse(xml_filepath)

    # Transform the XML data to HTML
    result_tree = transform(xml_root)

    return str(result_tree)


# def extract_data_from_pdf(file_path):
#     url = 'http://localhost:8070/api/processFulltextDocument'
#     files = {'input': open(file_path, 'rb')}
#     data = {
#         'teiCoordinates': ['persName', 'figure', 'ref', 'biblStruct', 'formula'],
#         'consolidateHeader': 1,
#         'consolidateCitations': 1,
#         'processImages': 1  # Add this line to enable image extraction

#     }
#     response = requests.post(url, files=files, data=data)
#     return response.text

import subprocess


def extract_data_from_pdf(file_path, output_dir):
    grobid_root = "./grobid-0.7.3"
    grobid_home = f"{grobid_root}/grobid-home"  # Replace with the actual path to your Grobid installation
    grobid_jar = f"{grobid_root}/grobid-core/build/libs/grobid-core-0.7.3-onejar.jar"  # Replace with the correct Grobid JAR file
    input_dir = "./grobid-input"
    output_dir = "./grobid-output"

    # Verify if the JAR file exists
    if os.path.exists(grobid_jar):
        print("Grobid JAR file exists")
    else:
        print("Grobid JAR file does not exist", grobid_jar)

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

    print(command)

    # Execute the Grobid batch command
    subprocess.run(command)

    return "Extraction completed."


def extract_coordinates_from_tei_file(tei_filepath):
    tei = etree.parse(tei_filepath)
    # Get the root of the tree
    root = tei.getroot()
    # Get the namespace
    ns = {
        "tei": root.tag.split("}")[0].strip("{"),
        "xml": "http://www.w3.org/XML/1998/namespace",
    }

    figures = root.findall(".//tei:figure", ns)
    figure_coordinates = [
        (figure.get("{http://www.w3.org/XML/1998/namespace}id"), figure.get("coords"))
        for figure in figures
    ]
    return figure_coordinates


def write_to_file(data, filepath):
    with open(filepath, "w") as xml_file:
        xml_file.write(xml_data)


TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
NSMAP = {"tei": TEI_NAMESPACE}


def copy_element(src, dst_parent):
    new_element = etree.Element(src.tag.split("}")[-1])
    new_element.text = src.text
    for child in src:
        copy_element(child, new_element)
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


def transform_tree(src, dst_parent, head_level=2):
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
                transform_tree(child, div, min(head_level + 1, 6))
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
            copy_element(child, dst_parent)


def convert_tei_to_html(tei_file, html_file):
    tei_tree = etree.parse(tei_file)
    html_root = etree.Element("html")
    head = etree.SubElement(html_root, "head")
    body = etree.SubElement(html_root, "body")

    abstract = tei_tree.find(".//tei:abstract", namespaces=NSMAP)
    if abstract is not None:
        transform_tree(abstract, body)

    tei_body = tei_tree.find(".//tei:body", namespaces=NSMAP)
    if tei_body is not None:
        transform_tree(tei_body, body)

    with open(html_file, "wb") as f:
        f.write(etree.tostring(html_root, method="html", pretty_print=True))


# usage
file_path = "./test.pdf"
tei_filepath = "./output.tei.html"
output_filepath = "./output.html"
json_filepath = "./output.json"
xslt_filepath = "./tei/json/jsonlib.xsl"
image_dir = "./extracted-images/"

# images = extract_images_from_pdf(file_path)

xml_data = extract_data_from_pdf(file_path, "./output")
write_to_file(xml_data, tei_filepath)

# tei_data = convert_xml_to_tei(tei_filepath, xslt_filepath)
# coords = extract_coordinates_from_tei_file(tei_filepath)
# print(coords)
# images = extract_images_from_coordinates(file_path, coords, image_dir)
# print(images)

# html = convert_tei_to_html(tei_filepath, output_filepath)
# print(html)

# json_data = convert_tei_to_json(tei_filepath, json_filepath)
# print(html_data)
