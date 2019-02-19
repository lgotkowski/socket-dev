from language import languageutils
import nltk
from language import grammars


class TextAnalyser(object):
    def __init__(self, actions=None, subjects=None, chars=None):
        self._characters = chars or ["fussel", "dimitri", "phine", "marianne", "justin"]
        self._subjects = subjects or ["tree", "apple", "door", "window", "chair", "table"]

        self._actions = actions or [{"name": "walk", "args": ["destination", "distance"]},
                                    {"name": "take", "args": ["item"]},
                                    {"name": "climb", "args": ["direction", "distance"]},
                                    {"name": "smile"},
                                    {"name": "wave"},
                                    {"name": "be"}]
    @property
    def actions(self):
        return self._actions

    def actions_from_text(self, text, grammar=None):
        print("Speech: {}".format(text))

        grammar_tree = self._build_grammar_tree(text, grammar)
        self._actions_from_grammar_tree(grammar_tree)

        grammar_tree.draw()
        return "Server: ({})".format(text)

    def _tag_text(self, text):
        text = text.lower()
        text_tagged = languageutils.stanford_pos_tag(text)

        # Fix tag for '
        for i in range(len(text_tagged)):
            word, tag = text_tagged[i]
            if word == "there":
                text_tagged[i] = (word, "PRP")
            if word in self._characters:
                text_tagged[i] = (word, "CHAR")
            if word == "please":
                text_tagged[i] = (word, "UH")
        return text_tagged

    def _build_grammar_tree(self, text, grammar=None):
        text_tagged = self._tag_text(text)
        print("Tags: {}".format(text_tagged))

        cp = nltk.RegexpParser(grammar or grammars.gramar1)
        grammar_tree = cp.parse(text_tagged)
        return grammar_tree

    def _actions_from_grammar_tree(self, grammar_tree):
        grammar_dict = self._tree_to_dict(grammar_tree)
        print(grammar_dict)

        characters = []
        actions = []
        subjects = []

        print("Len: {}".format(len(grammar_dict)))

        for key, obj_type in grammar_dict.items():
            print(key, obj_type)
            if key == "SubDescList":
                pass
            if key == "ActRel":
                pass

    def _tree_to_dict(self, tree):
        tdict = {}
        for t in tree:
            if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
                tdict[t.label()] = self._tree_to_dict(t)
            elif isinstance(t, nltk.Tree):
                tdict[t.label()] = t[0]
        return tdict


def tree_to_disk(tree):
    tree_view = nltk.draw.tree.TreeView(tree)
    tree_view._cframe.print_to_file('output.ps')


if __name__ == "__main__":

    sentences = ["Happy Fussel, find the big blue tree and take it",
                 "Angry Fussel, find the boy and the girl and draw them",
                 "Blue Justin look for the boy and draw him",
                 "Holy Phine find the tree and go there",
                 "Holy Phine find the tree and go there and wave your hand"]

    sentences = ["Bring me a bear Fussel",
                 "Fussel walk to the door",
                 "Happy Fussel take the apple",
                 "Fussel walk to the window quickly",
                 "Fussel follow me",
                 "Fussel be happy",
                 "Come on Fussel follow me",
                 "Follow me Fussel",
                 "Fussel follow me",
                 "Fussel, Phine go the chair and sit down",
                 "Fussel do a trick",
                 "Fussel tell me a joke",
                 "tell me a joke fussel"]

    sentences = ["Bring me the yellow banana Fussel",
                 "Can you get me a yellow banana Fussel",
                 "Fussel go to the banana and take it to me",
                 "Get the yellow banana and bring it to me",
                 "Fussel go to the table and bring me the banana",
                 "Fussel go to the table and bring it to me",
                 "Go to the table fussel and bring me the banana",
                 "Bring me the banana from the table fussel",
                 "Fussel, do you see the yellow banana, bring it to me",]

    text_analyser = TextAnalyser()

    for sentence in sentences:
        text_analyser.actions_from_text(sentence, grammars.gramar2)
    print("End")
