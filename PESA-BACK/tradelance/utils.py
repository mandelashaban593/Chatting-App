from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

def dictionary_to_xml(tag,data):
    """
    Turn dictionary key,value pairs
    to xml
    """
    xml_declaration = "<?xml version='1.0' encoding='UTF-8'?>"

    element = Element(tag)
    xml_data = None

    # add dictionary key value pairs to tag
    for key,value in data.items():
        child = Element(key)
        child.text = str(value)
        element.append(child)

    element = tostring(element)
    xml_data = xml_declaration+element

    # if xml_declare:
    #     xml_data = xml_declaration+element
    # else:
    #     xml_data = element

    return xml_data
