from language import languageutils
from utils import utils
import nltk
from language import grammars
from network.event import Event
import threading


class TextAnalyser(object):
    on_analyse_finished = Event()

    def __init__(self, actions=None, items=None, chars=None, extra_func=None):
        self._characters = chars or ["fussel", "dimitri", "phine", "marianne", "justin"]

        self._items = items or ["tree", "apple", "door", "window", "chair", "table"]

        self._actions = actions or [
                                    {"name": "walk", "args": ["actors", "directions"]},
                                    {"name": "bring", "args": ["actors", "items", "directions=me"]},
                                    {"name": "take", "args": ["actors", "items"]},
                                    {"name": "switch", "args": ["actors", "items", "direction"]},
                                    {"name": "climb", "args": ["actors", "items", "direction=up"]},
                                    {"name": "smile", "args": ["actors"]},
                                    {"name": "wave", "args": ["actors"]},
                                    {"name": "be", "args": ["actors", "mood"]},
                                    {"name": "stop", "args": ["actors", "action_name=None"]}
                                    ]

        self._extra_func = extra_func or [{"name": "biggest", "args": ["item"]},
                                          {"name": "smallest", "args": ["item"]},
                                          {"name": "closest", "args": ["item"]},
                                          {"name": "farthest", "args": ["item"]}]

    @property
    def actions(self):
        return self._actions

    @property
    def characters(self):
        return self._characters

    @property
    def items(self):
        return self._items

    def actions_from_text(self, text, grammar=None, draw_tree=False):
        print("Input Client: {}".format(text))
        grammar_tree = self._build_grammar_tree(text, grammar)
        action_with_args = self._actions_from_grammar_tree(grammar_tree)

        if draw_tree:
            grammar_tree.draw()
        self.on_analyse_finished.emit(sender=self)
        return action_with_args

    def _build_grammar_tree(self, text, grammar):
        text_tagged = self._tag_text(text)

        cp = nltk.RegexpParser(grammar or grammars.grammar3)
        grammar_tree = cp.parse(text_tagged)

        return grammar_tree

    def _tag_text(self, text):
        text = text.lower()
        text_tagged = languageutils.stanford_pos_tag(text)

        # Hardcoded tag fixes
        for i in range(len(text_tagged)):
            word, tag = text_tagged[i]
            if word == "there":
                text_tagged[i] = (word, "PRP")
            if word in self._characters:
                text_tagged[i] = (word, "CHAR")
            if word == "please":
                text_tagged[i] = (word, "UH")

        return text_tagged

    def _tree_to_list_tuple(self, tree):
        tree_data = []
        for branch in tree:
            if isinstance(branch, tuple) and len(branch) == 2:
                tree_data.append(branch)
            elif isinstance(branch, nltk.Tree):
                tree_data.append((branch.label(), self._tree_to_list_tuple(branch)))
            else:
                raise Exception("Unexcpected tree entry in conversion from tree to list tuple")

        if len(tree_data) == 1 and isinstance(tree_data[0], tuple) and isinstance(tree_data[0][1], str):
            #print("Tree data: {}".format(tree_data))
            return tree_data[0]
        return tree_data

    def __tree_to_dict(self, tree):
        tdict = {}
        for t in tree:
            if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
                tdict[t.label()] = self.__tree_to_dict(t)
            elif isinstance(t, nltk.Tree):
                tdict[t.label()] = t[0]
        return tdict

    def _extract_label(self, target_labels, list_tuple, output_list=None, deep=True):

        if output_list is None:
            output_list = []

        for target_label in target_labels:
            for i in range(len(list_tuple)):
                element = list_tuple[i]

                if isinstance(element, tuple):
                    label = element[0]
                    content = element[1]
                    #print("Label: '{}'".format(label))
                    if target_label == label:
                        output_list.append(content)
                    elif isinstance(content, list) and deep:
                        self._extract_label(target_labels=[target_label], list_tuple=content,
                                            output_list=output_list)
                elif isinstance(element, list) and deep:
                    content = element[1]
                    self._extract_label(target_labels=[target_label], list_tuple=content,
                                        output_list=output_list)
        return output_list

    ######################

    def _get_item(self, item_data):
        data = {}
        for branch in item_data:
            if branch.label() == "ItemType":
                data["name"] = branch.leaves()[0][0]
            elif branch.label() == "Attr":
                data["attr"] = branch.leaves()[0][0]
        print("Char: {}".format(data))
        return data

    def _get_char(self, char_data):
        #print("Char: {}".format(char_data))
        data = {}
        for branch in char_data:
            if branch.label() == "CharName":
                data["name"] = branch.leaves()[0][0]
            elif branch.label() == "Attr":
                data["attr"] = branch.leaves()[0][0]
        print("Char: {}".format(data))
        return data

    def _get_action(self, action_data):
        data = {}
        for branch in action_data:
            if branch.label() == "ActionType":
                data["name"] = branch.leaves()[0][0]
            elif branch.label() == "Attr":
                data["attr"] = branch.leaves()[0][0]
        print("Action: {}".format(data))
        return data

    def _get_direction(self, direction_data):
        data = {}
        for branch in direction_data:
            if branch.label() == "Item":
                for child in branch:
                    if child.label() == "ItemType":
                        data["name"] = child.leaves()[0][0]
                    elif child.label() == "Attr":
                        data["attr"] = child.leaves()[0][0]

            elif branch.label() == "Char":
                for child in branch:
                    if child.label() == "CharName":
                        data["name"] = child.leaves()[0][0]
                    elif child.label() == "Attr":
                        data["attr"] = child.leaves()[0][0]

            elif branch.label() == "Pointer":
                data["name"] = branch.leaves()[0][0]
        print("Direction: {}".format(data))
        return data

    def _get_item_loc(self, locationSrc_data):
        data = {}
        for branch in locationSrc_data:
            if branch.label() == "Item":
                for child in branch:
                    if child.label() == "ItemType":
                        data["name"] = child.leaves()[0][0]
                    elif child.label() == "Attr":
                        data["attr"] = child.leaves()[0][0]

            elif branch.label() == "Char":
                for child in branch:
                    if child.label() == "CharName":
                        data["name"] = child.leaves()[0][0]
                    elif child.label() == "Attr":
                        data["attr"] = child.leaves()[0][0]

            elif branch.label() == "Pointer":
                data["name"] = branch.leaves()[0][0]
        print("Direction: {}".format(data))
        return data

    def _actions_from_grammar_tree(self, grammar_tree):
        chars = []
        items = []
        direction = {}
        action = {}
        locSrc = None

        for branch in grammar_tree:
            branch = branch
            if not isinstance(branch, nltk.tree.Tree):
                continue
            #print("Branch: {}".format(branch.label()))
            label = branch.label()

            if label == "Chars":
                for child in branch:
                    if not isinstance(child, nltk.tree.Tree) or child.label() != "Char":
                        continue
                    chars.append(self._get_char(child))
            elif label == "Char":
                chars.append(self._get_char(branch))

            elif label == "Action":
                action = self._get_action(branch)

            elif label == "Items":
                for child in branch:
                    if not isinstance(child, nltk.tree.Tree) or child.label() != "Item":
                        continue
                    items.append(self._get_item(child))

            elif label == "Item":
                items.append(self._get_item(branch))

            elif label == "Direction":
                direction = self._get_direction(branch)

            elif label == "LocationSrc":
                locSrc = self._get_item_loc(branch)

        items = {"items": items, "location": locSrc}

        data = {"action": action, "args": {"actors": chars, "direction": direction, "items": items}}
        print(data)

