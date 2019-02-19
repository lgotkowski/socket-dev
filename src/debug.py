from language import analyse
from language import grammars

text_analyser = analyse.TextAnalyser()

s = ["Bring me the yellow banana Fussel",
     "Can you get me a yellow banana Fussel",
     "Fussel go to the banana and take it to me",
     "Get the yellow banana and bring it to me",
     "Fussel go to the table and bring me the banana",
     "Fussel go to the table and bring it to me",
     "Go to the table fussel and bring me the banana",
     "Bring me the banana from the table fussel",
     "Fussel, do you see the yellow banana, bring it to me"]


for text in s:
    text_analyser._build_grammar_tree(text, grammar=grammars.gramar3)