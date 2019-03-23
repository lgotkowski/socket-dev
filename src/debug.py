from language import analyse
from language import grammars
from language import languageutils


# ADD would, could
text_analyser = analyse.TextAnalyser()
s = languageutils.get_example_text("sentences3.txt")
for i in range(0, len(s)):
     #print(text)
     text = s[i]
     print("--- Index: {} | {}".format(i, text))
     text_analyser.actions_from_text(text, grammars.grammar7, draw_tree=True)

