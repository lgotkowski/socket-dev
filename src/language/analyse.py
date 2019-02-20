from language import languageutils
import nltk
from language import grammars
from network.event import Event
import threading


class TextAnalyser(object):
    on_analyse_finished = Event()

    def __init__(self, actions=None, items=None, chars=None, extra_func=None):
        self._characters = chars or ["fussel", "dimitri", "phine", "marianne", "justin"]

        self._items = items or ["tree", "apple", "door", "window", "chair", "table"]

        self._actions = actions or [{"name": "walk", "args": ["actors", "destination", "distance"]},
                                    {"name": "bring", "args": ["actors", "items", "destination"]},
                                    {"name": "take", "args": ["actors", "items"]},
                                    {"name": "climb", "args": ["actors", "direction", "distance", "destination"]},
                                    {"name": "smile", "args": ["actors"]},
                                    {"name": "wave", "args": ["actors"]},
                                    {"name": "be", "args": ["actors", "mood"]}]

        self._extra_func = extra_func or [{"name": "biggest", "args": ["item"]},
                                          {"name": "smallest", "args": ["item"]},
                                          {"name": "closest", "args": ["item"]},
                                          {"name": "farthest", "args": ["item"]}]

        self._threads = []

    @property
    def actions(self):
        return self._actions

    @property
    def characters(self):
        return self._characters

    @property
    def items(self):
        return self._items

    def add_thread(self, thread):
        self._threads.append(thread)

    def actions_from_text(self, text, grammar=None, draw_tree=False, threaded=False):
        if threaded:
            thread = threading.Thread(target=self.actions_from_text, args=(text, grammar, draw_tree))
            self.add_thread(thread)
            thread.start()
        else:
            return self._actions_from_text(text, grammar, draw_tree)

    def _actions_from_text(self, text, grammar=None, draw_tree=False):
        print("Input Client: {}".format(text))
        grammar_tree = self._build_grammar_tree(text, grammar)
        self._actions_from_grammar_tree(grammar_tree)

        if draw_tree:
            grammar_tree.draw()
        self.on_analyse_finished.emit(sender=self)
        print("Output Server: ({})".format(text))
        return "Output Server: ({})".format(text)

    def _build_grammar_tree(self, text, grammar):
        text_tagged = self._tag_text(text)
        print("Tags: {}".format(text_tagged))

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

    def _actions_from_grammar_tree(self, grammar_tree):
        grammar_data = self._tree_to_list_tuple(grammar_tree)
        print("Grammar Data: {}".format(grammar_data))

        characters = []
        actions = []
        items = []

        labels = ["Action", "Char", "Item", "ActDesc", "CharDesc", "ItemDesc"]
        for label in labels:
            content = self._extract_label(target_label=label, list_tuple=grammar_data)
            print("{}: {}".format(label, content))

        act_desc_list = self._extract_label(target_label="ActDesc", list_tuple=grammar_data)
        for act_desc in act_desc_list:
            action = self._extract_label(target_label="Action", list_tuple=act_desc)
            print("Action: {} | Desc: {}".format(action, act_desc))


        print("")

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

    def _extract_label(self, target_label, list_tuple, output_list=None):
        if output_list is None:
            output_list = []

        for i in range(len(list_tuple)):
            element = list_tuple[i]

            if isinstance(element, tuple):
                label = element[0]
                content = element[1]
                #print("Label: '{}'".format(label))
                if target_label == label:
                    output_list.append(content)
                elif isinstance(content, list):
                    self._extract_label(target_label=target_label, list_tuple=content,
                                        output_list=output_list)
            elif isinstance(element, list):
                content = element[1]
                self._extract_label(target_label=target_label, list_tuple=content,
                                    output_list=output_list)
        return output_list
