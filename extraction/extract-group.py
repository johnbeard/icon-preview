#!/usr/bin/env python

import argparse
from lxml import etree

class GroupExtractor():

    def __init__(self):
        pass

    def run(self, infile, outfile, layer):
        self.infile = infile
        self.outfile = outfile
        self.layer = layer

        tree = etree.parse(self.infile)
        self.svg = tree.getroot()

        #lxml doesn't like the None entry in the normal map...
        self.ns = {'sodipodi': self.svg.nsmap['sodipodi'],
            'inkscape': self.svg.nsmap['inkscape'],
            'svg': self.svg.nsmap['svg']
        }

        nv = self.svg.find('sodipodi:namedview', self.ns)
        self.strip_namedview(nv)

        self.del_other_layers(layer)

        self.resize_canvas(96)

        # write out
        out_data = etree.tostring(self.svg, encoding='utf-8')
        open(self.outfile, 'w').write(out_data.decode('utf-8'))

        print("Written: %s" % self.outfile)

    def strip_namedview(self, nv):
        # don't need the guides
        tn = '{' + self.ns['sodipodi'] + '}' + 'guide'
        etree.strip_elements(nv, tn)

    def _is_layer(self, el):
        is_layer = False

        if el.tag == '{%s}g' % self.ns['svg']:
            try:
                group_mode = el.attrib['{%s}groupmode' % self.ns['inkscape']]

                # remove other layers
                if group_mode == "layer":
                    is_layer = True
            except  KeyError:
                # leave non-layers alone
                pass

        return is_layer

    def del_other_layers(self, to_keep):
        print ("Clearing layers != %s" % to_keep)

        for el in self.svg:

            # for layers in the top level
            if self._is_layer(el):
                try:
                    group_name = el.attrib['{%s}label' % self.ns['inkscape']]

                    if group_name != to_keep:
                        el.getparent().remove(el)
                except KeyError:
                    pass

    def resize_canvas(self, new_size):
        w = int(self.svg.attrib['width'])
        h = int(self.svg.attrib['height'])

        print ("Current canvas: %d x %d" % (w, h))

        # note: the pages  is resized from top left, not bottom left
        # so you'd better have the group aligned on the top edge!
        self.svg.attrib['width'] = str(new_size)
        self.svg.attrib['height'] = str(new_size)
        self.svg.attrib['viewBox'] = '0 0 %d %d' % (new_size, new_size)

        print ("New canvas: %d x %d" % (new_size, new_size))

def main():

    parser = argparse.ArgumentParser(description='Isolate a layer from an SVG and trim the canvas')
    parser.add_argument('-i', '--input', metavar='SVG', type=str,
                       help='the input file')
    parser.add_argument('-o', '--output', metavar='SVG', type=str,
                       help='the output file')
    parser.add_argument('-l', '--layer', metavar='LAYER', type=str,
                        help='the layer to preserve')

    args = parser.parse_args()

    ge =  GroupExtractor()
    ge.run(args.input, args.output, args.layer)

if __name__ == "__main__":
    main()
