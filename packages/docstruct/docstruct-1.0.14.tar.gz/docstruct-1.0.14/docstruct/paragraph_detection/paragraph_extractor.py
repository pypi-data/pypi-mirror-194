import logging

import attr

from ..bounding_box import BoundingBox
from ..constants import PARAGRAPH_HORIZONTAL_SCALE, PARAGRAPH_VERTICAL_SCALE
from ..graph import Graph, Node
from ..segment import Segment
from ..text_block import Line, Paragraph


@attr.s(auto_attribs=True)
class ParagraphIndexed:
    """
    Connected component of lines.
    """

    lines_indexes: list[int]
    bounding_box: BoundingBox


class ParagraphMerger:
    def __init__(self, paragraphs: list[ParagraphIndexed]):
        self.paragraphs = paragraphs
        self.num_nodes = len(paragraphs)
        self.graph: Graph = None

    def is_directed_edge(self, first_node: Node, second_node: Node):
        first_bb = self.paragraphs[first_node.index].bounding_box
        second_bb = self.paragraphs[second_node.index].bounding_box
        return first_bb.intersect(second_bb)

    def build_graph(self):
        nodes = [Node(i) for i in range(self.num_nodes)]
        self.graph = Graph(nodes)

        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if self.is_directed_edge(nodes[i], nodes[j]):
                    nodes[i].add_neighbor(nodes[j])

    def merge_paragraphs(self) -> list[ParagraphIndexed]:
        self.build_graph()
        nodes = self.graph.nodes
        ccs: list[list[Node]] = self.graph.get_connected_components(nodes)
        merged_paragraphs: list[ParagraphIndexed] = []
        for cc in ccs:
            paragraph = self.merge_cc(cc)
            merged_paragraphs.append(paragraph)
        return merged_paragraphs

    def merge_cc(self, cc: list[Node]) -> ParagraphIndexed:
        lines_indexes = []
        bounding_boxes = []
        for node in cc:
            lines_indexes.extend(self.paragraphs[node.index].lines_indexes)
            bounding_boxes.append(self.paragraphs[node.index].bounding_box)
        bounding_box = BoundingBox.compose_bounding_boxes(bounding_boxes)
        return ParagraphIndexed(lines_indexes, bounding_box)


class ParagraphExtractor:
    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.num_nodes = len(lines)
        self.graph: Graph = None

    def build_graph(self):
        nodes = [Node(i) for i in range(self.num_nodes)]
        self.graph = Graph(nodes)

        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if self.are_adjacent(nodes[i], nodes[j]):
                    nodes[i].add_neighbor(nodes[j])
                    nodes[j].add_neighbor(nodes[i])

    def are_adjacent(self, first_node: Node, second_node: Node) -> bool:
        first_scaled_bb = self.lines[first_node.index].bounding_box.scale(
            PARAGRAPH_HORIZONTAL_SCALE, PARAGRAPH_VERTICAL_SCALE
        )
        second_scaled_bb = self.lines[second_node.index].bounding_box.scale(
            PARAGRAPH_HORIZONTAL_SCALE, PARAGRAPH_VERTICAL_SCALE
        )
        return first_scaled_bb.intersect(second_scaled_bb)

    def convert_ccs_to_paragraphs(
        self, ccs: list[list[Node]]
    ) -> list[ParagraphIndexed]:
        paragraphs = []
        for cc in ccs:
            lines_indexes = [node.index for node in cc]
            bounding_boxes = [self.lines[i].bounding_box for i in lines_indexes]
            bounding_box = BoundingBox.compose_bounding_boxes(bounding_boxes)
            paragraphs.append(ParagraphIndexed(lines_indexes, bounding_box))
        return paragraphs

    def convert_paragraphs_indexed_to_paragraphs(
        self, paragraphs_indexed: list[ParagraphIndexed]
    ) -> list[Paragraph]:
        paragraphs = []
        for paragraph in paragraphs_indexed:
            lines = [self.lines[i] for i in paragraph.lines_indexes]
            paragraph = Paragraph(children=lines)
            paragraph.set_bounding_box()
            paragraphs.append(paragraph)
        return paragraphs

    def extract_paragraphs(self) -> list[Paragraph]:
        if not self.lines:
            return []
        self.build_graph()
        ccs: list[list[Node]] = self.graph.get_connected_components()
        paragraphs: list[ParagraphIndexed] = self.convert_ccs_to_paragraphs(ccs)
        paragraph_merger = ParagraphMerger(paragraphs)
        merged_paragraphs: list[ParagraphIndexed] = paragraph_merger.merge_paragraphs()
        paragraphs = self.convert_paragraphs_indexed_to_paragraphs(merged_paragraphs)
        return paragraphs
