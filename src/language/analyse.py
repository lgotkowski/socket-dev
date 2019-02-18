from language import utils
import nltk


def actions_from_text(text):
    print("Speech: {}".format(text))
    grammar_tree = build_grammar_tree(text)
    grammar_dict = tree_to_dict(grammar_tree)
    print(grammar_dict)
    grammar_tree.draw()
    tree_to_disk(grammar_tree)
    return "Server: ({})".format(text)


def get_grammar():
    grammar = """
                    Adv: {<RB>}
                    Adj: {<J.*>}
                    Subject: {<N.*>}
                    Action: {<V.*>}
                    Direction: {<RP>}
                    Prep: {<PRP.*>}
                    Desc: {<Adv|Adj>+}
                    Seq: {<CC|,>}
                    Rel: {<IN|TO>}

                    ActDesc: {<Desc>*<Action><Desc>*}
                    SubDesc: {<DT>*<Desc>*<Subject>}

                    ActPrep: {<ActDesc><Prep>}

                    SubDescList: {(<DT>*<SubDesc><Seq><DT>*<SubDesc>)+ | <DT>*<SubDesc>+}

                    ActRel: {<ActDesc><Rel>*<SubDescList><Seq><ActPrep> | <ActDesc|ActPrep><Rel>*<SubDescList>}
                    """
    return grammar


def build_grammar_tree( sentence):
    text_tagged = utils.stanford_pos_tag(sentence)

    # Fix tag for 'there'
    for i in range(len(text_tagged)):
        word, tag = text_tagged[i]
        if word == "there":
            text_tagged[i] = (word, "PRP")

    cp = nltk.RegexpParser(get_grammar())
    grammar_tree = cp.parse(text_tagged)
    return grammar_tree


def tree_to_dict(tree):
    tdict = {}
    for t in tree:
        if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
            tdict[t.label()] = tree_to_dict(t)
        elif isinstance(t, nltk.Tree):
            tdict[t.label()] = t[0]
    return tdict


def tree_to_disk(tree):
    tree_view = nltk.draw.tree.TreeView(tree)
    tree_view._cframe.print_to_file('output.ps')
    print("treeView: {}".format(tree_view))


if __name__ == "__main__":

    sentences = ["Happy Fussel, find the big blue tree and take it",
                 "Angry Fussel, find the boy and the girl and draw them",
                 "Blue Justin look for the boy and draw him",
                 "Holy Phine find the tree and go there",
                 "Holy Phine find the tree and go there and wave your hand"]

    sentences = ["Happy Fussel, find the big blue tree and take it"]

    for sentence in sentences:
        actions_from_text(sentence)
    print("End")
