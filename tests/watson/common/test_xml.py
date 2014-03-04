# -*- coding: utf-8 -*-
from watson.common import xml


class TestXml(object):
    def test_to_string(self):
        data = {
            'test': {
                'nodes': {
                    'node': [
                        'Testing',
                        'Another node'
                    ]
                },
            }
        }
        x = xml.from_dict(data)
        s = xml.to_string(x)
        expected_output = '<test><nodes><node>Testing</node><node>Another node</node></nodes></test>'
        declaration = '<?xml version="1.0" encoding="utf-8" ?>'
        assert s == expected_output
        assert xml.to_string(x, xml_declaration=True) == declaration + expected_output
