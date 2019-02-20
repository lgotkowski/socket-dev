
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

        Pointer: {<PRP.*>}

        Desc: {<Adv|Adj|Num|Dir>+}
        Seq: {<CC|,>}
        Mod: {<MD>}

        CharDesc: {<DT>*<Desc>*<Char>}
        ActDesc: {<Desc>*<Action><Desc>*}
        ItemDesc: {<DT>*<Desc>*<Item>}
        
        Cmd: {<Src>*<ItemDesc|Pointer>*<ActDesc><Dst>*<ItemDesc|Pointer><Src|Dst>*<ItemDesc|Pointer>*<Src>*<ItemDesc|Pointer>*}

        """

# TODO: add Item sequence
# TODO: multiple characters
# TODO: who is the actor or actors
# TODO: Handle the 'is VBZ' Action problem

#Sum: {<Src>*<ItemDesc|Pointer>*<ActDesc><Dst>*<ItemDesc|Pointer><Src|Dst>*<ItemDesc|Pointer>*<Src>*<ItemDesc|Pointer>* | <ActDesc><Pointer><ItemDesc><Src>*<ItemDesc|Pointer>* | <ActDesc><ItemDesc|Pointer><Dst><ItemDesc|Pointer>}