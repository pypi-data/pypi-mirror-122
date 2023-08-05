import requests

from vripper.parser._common import parse
from vripper.parser._def import parser


@parser("imagebam.com")
def p(url, timeout):
    def pcb(tree):
        cont_nodes = tree.xpath("//a[@title='Continue to your image']")
        assert len(cont_nodes) == 1

        return requests.get(cont_nodes[0].attrib["href"], timeout=timeout)

    return parse(url, timeout, "//meta[@property='og:image']", "content", post_callback=pcb)
