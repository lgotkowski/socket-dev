
gramar1 = """
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

gramar2 = """
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

gramar3 = """"""