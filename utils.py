import os

import xmltodict


def process_pom(fn: str, processor):
    if os.path.exists(fn):
        with open(fn) as fp:
            xml_dict = xmltodict.parse(fp.read())
            processor(xml_dict)

def check_property(the_dict, k, v):
    properties = the_dict['project']['properties']
    if k in properties:
        assert properties[k] == v, 'the property %s does not match the value %s. Found %s, instead.  ' % (k, v , properties[k])
