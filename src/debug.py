from language import analyse
from language import grammars

text_analyser = analyse.TextAnalyser()


s = ["Fussel bring me the banana",
     "Bring me the banana Fussel",
     "Please bring me the yellow banana Fussel",
     "Fussel please bring me the yellow banana",
     "Can you bring me the yellow banana Fussel",
     "Fussel can you bring me the yellow banana please",
     "Fussel Bring me the biggest yellow banana",
     "Can you please bring me the biggest yellow banana fussel",
     "Fussel go to the table and bring me the yellow banana",
     "Go to the table fussel and bring me the yellow banana",
     "Can you go to the table and bring me the yellow banana fussel",
     "Can you please got to the table and bring me the yellow banana fussel",
     "Fussel can you please go to the table and bring me the yellow banana",
     "Bring me the yellow banana from the table fussel",
     "Take the yellow banana from the table and bring it to me fussel",
     "Fussel take the yellow banana from the table and bring it to me",
     "Fussel go to the table and bring me the yellow banana from there",
     "Fussel there is a yellow banana on the table, please bring it to me",
     "There is a yellow banana on the table fussel, please bring it to me",
     "From the table bring me the yellow banana fussel"]

# ADD would, could

for text in s:
     text_tagged = text_analyser._tag_text(text)

     grammar_tree = text_analyser._build_grammar_tree(text, grammar=grammars.gramar3)

     tags = [("RB", "Adv"),
             ("J", "Adj"),
             ("N", "Object"),
             ("V", "Action"),
             ("RP", "Direction"),
             ("PRP", "Prep"),
             ("Adv", "Desc"),
             ("Adj", "Desc"),
             ("CC", "Seq"),
             (",", "Seq"),
             ("IN", "Rel"),
             ("TO", "Rel")]

     for i in range(len(text_tagged)):
          word, tag = text_tagged[i]
          for t in tags:
               if tag.startswith(t[0]):
                    text_tagged[i] = (word, t[1])


     print(text_tagged)
     grammar_tree.draw()