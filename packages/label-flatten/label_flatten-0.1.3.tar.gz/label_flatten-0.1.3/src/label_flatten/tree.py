from .node import Node
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tree(object):
    def __init__(self, pth, rootname="root"):
        self.rootname = rootname
        self.data = self.load(pth)
        self.check()
        self.parse()
        logger.info("Parsed the data into a tree structure successfully")
    
    def __str__(self):
        return self.root.__str__()

    def load(self, pth):
        with open(pth, 'r') as f:
            return json.load(f)
    
    def check(self):
        """
        Check whether the first layer has templates and concepts, and whether the each deeper layer not has values other than concepts and templates
        """
        assert "templates" in self.data
        assert "concepts" in self.data
        self.check_helper(self.data["concepts"])
    
    def check_helper(self, concepts):
        """
        Check whether the each deeper layer not has values other than concepts and templates
        """
        for concept_name, concept_value in concepts.items():
            assert concept_value.keys() <= {"templates", "concepts"}
            try:
                self.check_helper(concept_value["concepts"])
            except KeyError:
                if not concept_value == {}:
                    raise ValueError("Concepts should only have templates or concepts as values, last layer should be empty")
    
    def parse(self):
        """
        Parse the data into a tree structure
        """
        self.root = Node(self.rootname, self.data["templates"], None, None) # root should not be labeled!
        self.parse_helper(self.root, self.data)
    
    def parse_helper(self, node, data):
        """
        Parse the data into a tree structure
        """
        templates = data["templates"] if "templates" in data else node.template.to_dict()
        concepts = data["concepts"] if "concepts" in data else {}
        if concepts == {}:
            node.end = True
            return
        for concept_name, concept_value in concepts.items():
            this_node = Node(concept_name, templates, node, None)
            node.children.append(this_node)
            try:
                self.parse_helper(this_node, concept_value)
            except KeyError:
                this_node.end = True

    def give_label(self, concept_names):
        """
        Give labels to the nodes in the tree
        And back to the root, rule: one of my children is labeled, I am labeled
        """
        self.give_label_helper(self.root, concept_names)
        return self
    
    def give_label_helper(self, node, concept_names):
        """
        Give labels to the nodes in the tree
        """
        if node.concept_name == concept_names:
            node.labeled = 1
            self.reverse_label(node)
        for child in node.children:
            self.give_label_helper(child, concept_names)
        
    def reverse_label(self, node):
        """
        Back to the root, rule: one of my children is labeled, I am labeled
        """
        if node.parent:
            node.parent.labeled = 1
            self.reverse_label(node.parent)

    def write(self,mode="all"):
        """
        Write some semantic sentences with labels
        """
        return self.write_helper(self.root,mode)
    
    def write_helper(self, node, mode):
        """
        Write some semantic sentences with labels
        """
        sentences = []
        if not node.concept_name == "root":
            if self.filter(node, mode):
                sentences.extend(node.write())
        for child in node.children:
            sentences.extend(self.write_helper(child, mode))
        # sort by second element
        sentences.sort(key=lambda x: x[1], reverse=True)
        return sentences

    def filter(self, node, mode):
        """
        Filter the nodes to be written
        """
        if mode == "all":
            return True
        elif mode == "labeled":
            return node.labeled
        elif mode == "end":
            return node.end
        else:
            raise ValueError("mode should be one of: all, labeled, end")
    
    def reduce_from_sentences(self, sentences):
        """
        Reduce the tree from sentences
        """
        sentences = {sen[0]:sen[1] for sen in sentences}
        self.reduce_from_sentences_helper(self.root, sentences)
        return self
    
    def reduce_from_sentences_helper(self, node, sentences):
        """
        Reduce the tree from sentences
        """
        if not node.concept_name == "root":
            pos_sen = node.write_pos()
            if sentences[pos_sen] == 1:
                node.labeled = 1
                self.reverse_label(node)
        for child in node.children:
            self.reduce_from_sentences_helper(child, sentences)

    def deepest_label(self, all_labels=False):
        """
        Find the deepest labeled = 1 nodes and return names
        """
        label_names = self.deepest_label_helper(self.root,[],all_labels)
        return list(set(label_names))
    
    def deepest_label_helper(self, node, names, all_labels=False):
        """
        Find the deepest labeled = 1 nodes and return names
        If all_labels is True, return all labeled nodes
        """
        if node.labeled == 1:
            if all_labels and node.concept_name != "root":
                names.append(node.concept_name)
            if node.children == []:
                names.append(node.concept_name)
            else:
                pos_cnt = 0
                for child in node.children:
                    if child.labeled == 1:
                        pos_cnt += 1
                    names = self.deepest_label_helper(child, names, all_labels)
                if pos_cnt == 0:
                    names.append(node.concept_name)
        return names
