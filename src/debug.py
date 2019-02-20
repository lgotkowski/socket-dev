from language import analyse
from language import grammars


s = ["Fussel bring me the banana",
     "Bring me the banana Fussel",
     "Please bring me the yellow banana Fussel",
     "Fussel please bring me the yellow banana",
     "Can you bring me the yellow banana Fussel",
     "Fussel can you bring me the yellow banana please",
     "Fussel Bring me the biggest yellow banana",
     "Can you please bring me the biggest yellow banana fussel",
     "Fussel go to the table and bring me the yellow banana",
     "Go to the table fussel and bring me the yellow banana and the apple",
     "Go to the table and bring the banana to me",
     "Go to the table and bring the yellow banana to me",
     "Go to the banana and bring it to me",
     "Can you go to the table and bring me the yellow banana fussel",
     "Can you please go to the table and bring me the yellow banana fussel",
     "Fussel can you please go to the table and bring me the yellow banana",
     "Bring me the yellow banana from the table fussel",
     "Fussel go to the table and bring me the yellow banana from there",
     "Take the yellow banana from the table and bring it to me fussel",
     "Fussel take the yellow banana from the table and bring it to me",
     "Fussel go to the table and bring me the yellow banana from there",
     "Fussel there is a yellow banana on the table, please bring it to me",
     "There is a yellow banana on the table fussel, please bring it to me",
     "From the table bring me the yellow banana fussel"]

# ADD would, could
text_analyser = analyse.TextAnalyser()

for text in s:
    text_analyser.actions_from_text(text, grammars.grammar4, draw_tree=True)

