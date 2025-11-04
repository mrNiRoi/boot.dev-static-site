# import unittest

# from textnode import TextNode, TextType, text_node_to_html_node

# class TestTextNode_text(unittest.TestCase):
#     def test_text(self):
#         node = TextNode("This is a text node", TextType.TEXT)
#         html_node = text_node_to_html_node(node)
#         self.assertEqual(html_node.tag, None)
#         self.assertEqual(html_node.value, "This is a text node")

# if __name__ == "__main__":
#     unittest.main()


# import unittest

# from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

# class Test_split_nodes(unittest.TestCase):
#     def test_split_nodes_code(self):
#         node = TextNode("This is text with a `code block` word", TextType.TEXT)
#         result = split_nodes_delimiter([node], "`", TextType.CODE)
#         assert [n.text for n in result] == ["This is text with a ", "code block", " word"]
#         assert [n.text_type for n in result] == [TextType.TEXT, TextType.CODE, TextType.TEXT]

#     def test_split_nodes_bold(self):
#         node = TextNode("This is **bold** text", TextType.TEXT)
#         result = split_nodes_delimiter([node], "**", TextType.BOLD)
#         assert [n.text for n in result] == ["This is ", "bold", " text"]

#     def test_split_nodes_italic(self):
#         node = TextNode("Some _italic_ here", TextType.TEXT)
#         result = split_nodes_delimiter([node], "_", TextType.ITALIC)
#         assert [n.text for n in result] == ["Some ", "italic", " here"]


# if __name__ == "__main__":
#     unittest.main()

# import unittest

# from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

# class Test_split_nodes(unittest.TestCase):
#     def test_extract_markdown_images(self):
#         matches = extract_markdown_images(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
#         )
#         self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


# if __name__ == "__main__":
#     unittest.main()

# import unittest
# from textnode import TextNode, TextType
# from functions import split_nodes_image, split_nodes_link


# class TestSplitNodes(unittest.TestCase):
#     def test_split_images(self):
#         node = TextNode(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#             TextType.TEXT,
#         )
#         new_nodes = split_nodes_image([node])
#         self.assertListEqual(
#             [
#                 TextNode("This is text with an ", TextType.TEXT),
#                 TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
#                 TextNode(" and another ", TextType.TEXT),
#                 TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
#             ],
#             new_nodes,
#         )

#     def test_split_links(self):
#         node = TextNode(
#             "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#             TextType.TEXT,
#         )
#         new_nodes = split_nodes_link([node])
#         self.assertListEqual(
#             [
#                 TextNode("This is text with a link ", TextType.TEXT),
#                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#                 TextNode(" and ", TextType.TEXT),
#                 TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
#             ],
#             new_nodes,
#         )

#     def test_no_links_or_images(self):
#         node = TextNode("Just some plain text", TextType.TEXT)
#         self.assertListEqual([node], split_nodes_link([node]))
#         self.assertListEqual([node], split_nodes_image([node]))

#     def test_mixed_nodes(self):
#         nodes = [
#             TextNode("Text before ![img](url.png)", TextType.TEXT),
#             TextNode("Other node", TextType.BOLD),
#         ]
#         new_nodes = split_nodes_image(nodes)
#         self.assertEqual(len(new_nodes), 3)
#         self.assertEqual(new_nodes[0].text, "Text before ")
#         self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
#         self.assertEqual(new_nodes[2].text_type, TextType.BOLD)

#     def test_adjacent_links(self):
#         node = TextNode(
#             "[One](https://one.com)[Two](https://two.com)", TextType.TEXT
#         )
#         new_nodes = split_nodes_link([node])
#         self.assertListEqual(
#             [
#                 TextNode("One", TextType.LINK, "https://one.com"),
#                 TextNode("Two", TextType.LINK, "https://two.com"),
#             ],
#             new_nodes,
#         )


# if __name__ == "__main__":
#     unittest.main()

# import unittest
# from textnode import TextNode, TextType
# from functions import text_to_textnodes


# class TestTextToTextNodes(unittest.TestCase):
#     def test_full_conversion(self):
#         text = (
#             "This is **text** with an _italic_ word and a `code block` "
#             "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
#             "and a [link](https://boot.dev)"
#         )
#         result = text_to_textnodes(text)

#         expected = [
#             TextNode("This is ", TextType.TEXT),
#             TextNode("text", TextType.BOLD),
#             TextNode(" with an ", TextType.TEXT),
#             TextNode("italic", TextType.ITALIC),
#             TextNode(" word and a ", TextType.TEXT),
#             TextNode("code block", TextType.CODE),
#             TextNode(" and an ", TextType.TEXT),
#             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#             TextNode(" and a ", TextType.TEXT),
#             TextNode("link", TextType.LINK, "https://boot.dev"),
#         ]

#         self.assertListEqual(expected, result)


# if __name__ == "__main__":
#     unittest.main()

# import unittest
# from textnode import TextNode, TextType, BlockType
# from functions import text_to_textnodes, markdown_to_blocks, block_to_block_type


# class TestBlockToBlockType(unittest.TestCase):
#     def test_heading(self):
#         self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
#         self.assertEqual(block_to_block_type("###### Deep heading"), BlockType.HEADING)

#     def test_code(self):
#         self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

#     def test_quote(self):
#         self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)

#     def test_unordered_list(self):
#         self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

#     def test_ordered_list(self):
#         self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.ORDERED_LIST)

#     def test_paragraph(self):
#         self.assertEqual(block_to_block_type("This is just normal text."), BlockType.PARAGRAPH)


    
# if __name__ == "__main__":
#     unittest.main()

# if __name__ == "__main__":
#     unittest.main()

import unittest
from textnode import TextNode, TextType, BlockType
from functions import text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node


import unittest
import textwrap
from functions import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )


if __name__ == "__main__":
    unittest.main()
