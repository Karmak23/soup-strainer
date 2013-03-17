from __future__ import absolute_import
import io

from . import support
from html5lib import html5parser
from html5lib.constants import namespaces
from html5lib.treebuilders import dom

import unittest

# tests that aren't autogenerated from text files
class MoreParserTests(unittest.TestCase):

  def test_assertDoctypeCloneable(self):
    parser = html5parser.HTMLParser(tree=dom.TreeBuilder)
    doc = parser.parse(u'<!DOCTYPE HTML>')
    self.assert_(doc.cloneNode(True))
  test_assertDoctypeCloneable.func_annotations = {}

  def test_line_counter(self):
    # http://groups.google.com/group/html5lib-discuss/browse_frm/thread/f4f00e4a2f26d5c0
    parser = html5parser.HTMLParser(tree=dom.TreeBuilder)
    parser.parse(u"<pre>\nx\n&gt;\n</pre>")
  test_line_counter.func_annotations = {}

  def test_namespace_html_elements_0(self): 
    parser = html5parser.HTMLParser(namespaceHTMLElements=True)
    doc = parser.parse(u"<html></html>")
    self.assert_(doc.childNodes[0].namespace == namespaces[u"html"])
  test_namespace_html_elements_0.func_annotations = {}

  def test_namespace_html_elements_1(self): 
    parser = html5parser.HTMLParser(namespaceHTMLElements=False)
    doc = parser.parse(u"<html></html>")
    self.assert_(doc.childNodes[0].namespace == None)
  test_namespace_html_elements_1.func_annotations = {}

  def test_unicode_file(self):
    parser = html5parser.HTMLParser()
    doc = parser.parse(io.StringIO(u"a"))
  test_unicode_file.func_annotations = {}

def buildTestSuite():
  return unittest.defaultTestLoader.loadTestsFromName(__name__)
buildTestSuite.func_annotations = {}

def main():
    buildTestSuite()
    unittest.main()
main.func_annotations = {}

if __name__ == u'__main__':
    main()