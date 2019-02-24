
grammar1 = """
        Char: {<CHAR>}
        Adv: {<RB>}
        Adj: {<J.*>}
        Object: {<N.*>}
        Action: {<V.*>}
        Direction: {<RP>}
        Prep: {<PRP.*>}
        Desc: {<Adv|Adj>+}
        Seq: {<CC|,>}
        Rel: {<IN|TO>}
        
        CharDesc: {<DT>*<Desc>*<Char>}
        ActDesc: {<Desc>*<Action><Desc>*}
        ObjDesc: {<DT>*<Desc>*<Object>}
        
        ActPrep: {<ActDesc><Prep>}
        
        CharDescList: {(<DT>*<CharDesc><Seq><DT>*<CharDesc>)+ | <DT>*<CharDesc>+}
        ObjDescList: {(<DT>*<ObjDesc><Seq><DT>*<ObjDesc>)+ | <DT>*<ObjDesc>+}
        
        ActRel: {<ActDesc><Rel>*<ObjDescList><Seq><ActPrep><Desc>* | <ActDesc|ActPrep><Rel>*<ObjDescList><Desc>* | <ActPrep><Desc>*}
        """

grammar2 = """
        Char: {<CHAR>}
        Adv: {<RB>}
        Adj: {<J.*>}
        Object: {<N.*>}
        Action: {<V.*>}
        Direction: {<RP>}
        Prep: {<PRP.*>}
        Desc: {<Adv|Adj>+}
        Seq: {<CC|,>}
        Rel: {<IN|TO>}

        CharDesc: {<DT>*<Desc>*<Char>}
        ActDesc: {<Desc>*<Action><Desc>*}
        ObjDesc: {<DT>*<Desc>*<Object>}

        ActPrep: {<ActDesc><Prep>}

        CharDescList: {(<DT>*<CharDesc><Seq><DT>*<CharDesc>)+ | <DT>*<CharDesc>+}
        ObjDescList: {(<DT>*<ObjDesc><Seq><DT>*<ObjDesc>)+ | <DT>*<ObjDesc>+}

        ActRel: {<ActDesc><Rel>*<ObjDescList><Seq><ActPrep><Desc>*<Rel>*<Prep>* | <ActDesc><Rel>*<ObjDescList><Seq><ActPrep><ObjDescList>* | <ActDesc|ActPrep><Rel>*<ObjDescList><Desc>* | <ActPrep><Desc>*}
        """

grammar3 = """
        Char: {<CHAR>}
        Item: {<N.*>}
        Action: {<V.*>}
        
        Adv: {<RB>}
        Adj: {<J.*>}
        Num: {<CD>}
        Dir: {<RP>}
        
        Src: {<IN>}
        Dst: {<TO>}
        
        Pointer: {<PRP.*>}
        
        Desc: {<Adv|Adj|Num|Dir>+}
        Seq: {<CC|,>}
        Rel: {<Src|Dst>}
        Mod: {<MD>}
        
        
        
        CharDesc: {<DT>*<Desc>*<Char><Rel>*}
        ActDesc: {<Rel>*<Pointer>*<Desc>*<Action><Pointer>*<Desc>*<Rel>*<Pointer>*<Desc>*}
        ItemDesc: {<DT>*<Desc>*<Item>}
        
        """

grammar4 = """
        Char: {<CHAR>}
        Item: {<N.*>}
        Action: {<V.*>}

        Adv: {<RB>}
        Adj: {<J.*>}
        Num: {<CD>}
        Dir: {<RP>}

        Src: {<IN>}
        Dst: {<TO>}

        Pointer: {<PRP.*>|<Char|Item><POS>}

        Desc: {<Adv|Adj|Num|Dir>+}
        Seq: {<CC|,>}
        Mod: {<MD>}

        CharDesc: {<DT>*<Desc>*<Char>}
        ActDesc: {<Desc>*<Action><Desc>*}
        ItemDesc: {<Pointer><DT>*<Desc>*<Item>}
        
        CharSeq: {(<CharDesc><Seq><CharDesc>)+}
        ItemSeq: {(<ItemDesc><Seq><ItemDesc>)+}
        PointerSeq: {(<Pointer><Seq><Pointer>)+}
        
        Actors: {(<CharDesc|CharSeq>)+}
        Items: {(<ItemDesc|ItemSeq|Pointer|PointerSeq>)+}
        
        Location: <Src>{<Items>}
        
        
        Cmd: {<Src>*<Items>*<ActDesc><Dst>*<Items><Src|Dst>*<Items>*<Src>*<Items>*<Desc>*}

        """
#Location: {(?<=<Src>)<Items>}
#Location: {<Src><Items>}
#Location: {<Src>(?=<Items>)}

# <Pointer><Dst><Pointer>
# how to put only a part of the match into the "Pointer" group


#Cmd: {<Src>*<ItemDesc|Pointer>*<ActDesc><Dst>*<ItemDesc|Pointer><Src|Dst>*<ItemDesc|Pointer>*<Src>*<ItemDesc|Pointer>*<Desc>*}




# TODO: add Item sequence
# TODO: multiple characters
# TODO: who is the actor or actors
# TODO: Handle the 'is VBZ' Action problem

#        ItemDescLs: {<ItemDesc>+(<Seq><ItemDesc|Pointer>)*}


grammar5 = """
        CharName: {<CHAR>}
        ItemType: {<N.*>}
        ActionType: {<V.*>}

        Adv: {<RB>}
        Adj: {<J.*>}
        Num: {<CD>}
        Dir: {<RP>}
        
        
        Dst: {<IN>*<TO>} # for the case 'next to' -> IN TO
        Src: {<IN>}

        Pointer: {<PRP>}
        Pointers: {(<Pointer><Seq><Pointer>)+}
        

        Attr: {<Adv|Adj|Num|Dir>+}
        Seq: {<CC|,>}
        Mod: {<MD>}

        Char: {<Attr>*<CharName>}
        Chars: {(<Char><Seq><Char>)+}
        
        Owner: {<PRP.>|<Char><POS>}
        Owners: {(<Owner><Seq><Owner>)+}
        
        Item: {<Owners*>*<Attr>*<ItemType>}
        Items: {(<Item><Seq><DT>*<Item>)+}
                
        Location: {<Src|Dst><Items*|Charss>}
        Target: <ActionType>{<Pointers*|Chars*|Items*>}
        Target: <Target><Seq>{<Pointers*|Chars*|Items*>}
        Targets:<ActionType>{(<Target><Seq><Target>)+}
        
        Action: {<Attr>*<ActionType><Attr>*}


        Cmd: {<Src>*<Items>*<ActDesc><Dst>*<Items><Src|Dst>*<Items>*<Src>*<Items>*<Attr>*}

        """

    # TODO: Actor and (cmd?)

grammar6 = """
        CharName: {<CHAR>}
        ItemType: {<N.*>}
        ActionType: {<V.*>}

        Adv: {<RB>}
        Adj: {<J.*>}
        Num: {<CD>}
        Dir: {<RP>}


        Dst: {<IN>*<TO>} # for the case 'next to' -> IN TO
        Src: {<IN>}

        Pointer: {<PRP>}
        Pointers: {(<Pointer><Seq><Pointer>)+}


        Attr: {<Adv|Adj|Num|Dir>+}
        Seq: {<CC|,>}
        Mod: {<MD>}

        Char: {<Attr>*<CharName>}
        Chars: {(<Char><Seq><Char>)+}

        Owner: {<PRP.>|<Char><POS>}
        Owners: {(<Owner><Seq><Owner>)+}

        Item: <Owners*>*{<Attr>*<ItemType>}
        Items: {(<Item><Seq><DT>*<Item>)+}
        
        Action: {<Attr>*<ActionType><Attr>*}

        LocationSrc: <Items*|Chars*|Pointers*><Src><DT>*{<Items*|Chars*|Pointers*>}
        LocationSrc: <Src><DT>*<Owner>*{<Items*|Chars*|Pointers*>}<Action>
        
        Direction: <Items*|Chars*|Pointers*><.*>*<Dst><.*>*{<Items*|Chars*|Pointers*>}
        
        Direction: <Action><Dst|Src>*<DT>*<Owner>*{<Items*|Chars*|Pointers*>}.*(?!<Dst|Src>)<.*>*(?=<Items*|Chars*|Pointers*>)
        Direction: <Items*|Chars*|Pointers*>.*<Action><Dst|Src>*<DT>*<Owner>*{<Items*|Chars*|Pointers*>}.*(?!<Dst|Src>)<.*>*
    

        """

# item somethimes becomes direction which is wrong

#Target: {Char | Pointer | Item}
#Direction: {}


grammar7 = """
        CharName: {<CHAR>}
        ItemType: {<N.*>}
        ActionType: {<V.*>}

        Num: {<CD>}

        Dst: {<IN>*<TO>} # for the case 'next to' -> IN TO
        Src: {<IN>}

        Pointer: {<PRP>}
        Pointers: {(<Pointer><Seq><Pointer>)+}


        Attr: {<RB|J.*|RP>+}
        Seq: {<CC|,>}
        Mod: {<MD>}

        Char: {<Attr>*<CharName>}
        Chars: {(<Char><Seq><Char>)+}

        Owner: {<PRP.>|<Char><POS>}
        Owners: {(<Owner><Seq><Owner>)+}

        Item: <Owners*>*{<Attr>*<ItemType>}
        Items: {(<Item><Seq><DT>*<Item>)+}

        Action: {<Attr>*<ActionType><Attr>*}

        LocationSrc: <Items*|Chars*|Pointers*><Src><DT>*{<Items*|Chars*|Pointers*>}
        LocationSrc: <Src><DT>*<Owner>*{<Items*|Chars*|Pointers*>}<Action>

        Direction: <Items*|Chars*|Pointers*><.*>*<Dst><.*>*{<Items*|Chars*|Pointers*>}

        Direction: <Action><Dst|Src>*<DT>*<Owner>*{<Items*|Chars*|Pointers*>}.*(?!<Dst|Src>)<.*>*(?=<Items*|Chars*|Pointers*>)
        Direction: <Items*|Chars*|Pointers*>.*<Action><Dst|Src>*<DT>*<Owner>*{<Items*|Chars*|Pointers*>}.*(?!<Dst|Src>)<.*>*


        """