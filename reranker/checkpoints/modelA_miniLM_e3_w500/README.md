---
tags:
- sentence-transformers
- cross-encoder
- reranker
- generated_from_trainer
- dataset_size:16200
- loss:FitMixinLoss
base_model: cross-encoder/ms-marco-MiniLM-L6-v2
pipeline_tag: text-ranking
library_name: sentence-transformers
---

# CrossEncoder based on cross-encoder/ms-marco-MiniLM-L6-v2

This is a [Cross Encoder](https://www.sbert.net/docs/cross_encoder/usage/usage.html) model finetuned from [cross-encoder/ms-marco-MiniLM-L6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2) using the [sentence-transformers](https://www.SBERT.net) library. It computes scores for pairs of texts, which can be used for text reranking and semantic search.

## Model Details

### Model Description
- **Model Type:** Cross Encoder
- **Base model:** [cross-encoder/ms-marco-MiniLM-L6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2) <!-- at revision c5ee24cb16019beea0893ab7796b1df96625c6b8 -->
- **Maximum Sequence Length:** 256 tokens
- **Number of Output Labels:** 1 label
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Documentation:** [Cross Encoder Documentation](https://www.sbert.net/docs/cross_encoder/usage/usage.html)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Cross Encoders on Hugging Face](https://huggingface.co/models?library=sentence-transformers&other=cross-encoder)

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import CrossEncoder

# Download from the 🤗 Hub
model = CrossEncoder("cross_encoder_model_id")
# Get scores for pairs of texts
pairs = [
    ['explain to 15 minutes at 400 f', "W hy do so w ith y o u r h ealth and com fort? L e t us ta k e over y o u r h eating worries. T u rn y o u r Fuel Oil requirem ents over to us. W e will check y o u r supply periodically, delivering when needed. T h e b est grade of Oil available in th e m ost m odern equipm ent by courteous drivers. SOUTHERN ASPHALT FUEL O IL COM PANY, Inc. Dial 4-3611 F o r E m ergency Deliveries D ial 4-4556; 4-4369 S f f C . g t ff y l B L C / f a-P-Jktu'ce."],
    ['explain printing paper and coming closer and closer to getting it just right', 'R.D. Willey Extension 4-H Natural Resources Specialist Clemson University. This information is supplied with the understanding that no discrimination is intended and no endorsement by the Clemson University Cooperative Extension Service is implied. All recom- mendations are for South Carolina conditions and may not apply to other areas. (New 4/99. Reviewed 2/01. Revised 9/05.) The Clemson University Cooperative Extension Service offers its programs to people of all ages regardless of race national origin political beliefs sexual orientation marital or family status and is an equal opportunity employer. Clemson University Cooperating with U.S. Department of Agriculture South Carolina Counties Extension Service South Carolina. Issued in Furtherance of Cooperative Extension Work in Agriculture and Home Economics Acts of May 8 and June 30 1914 Public Service Activities'],
    ['explain pressure caused by prosthetic devices', 'Setting up a Food Drying Business: A Step-by-step Guide Fabrice Thuillier ITDG Publishing ISBN 1 85339 498 X Drying Foodstuffs Jean Françoia Rozis Backuys Publishers Construction and Use of a Simple Solar Drier to Preserve Food for Off Season HEDON Household Energy Network 4'],
    ['explain the tropics, the evergreen scrub forests of temperate areas, and in desert', "------------------------------------------------------------------------ ------------------------------------------------------------------------ OPPOSE THE ILLEGAL U.S. ------------------------------------------------------------------------ ------------------------------------------------------------------------ * * * This entire list was downloaded in pieces from unknown sources via Limewire ( http://www.limewire.com )and re- compiled using the Openoffice.org office productivity suite (which I highly recommend, go to http://www.openoffice.org and download it, it's open-source, completely free, and superior to Micro$oft's shitty, bug-ridden proprietary programs and formats.) My profound thanks to whoever made the information in this text available."],
    ['explain energy and matter could be produced with the corresponding stimulation', "wetgroundWeed 2to6ft.high greenishPerennial ito3ft.tall fls.blueAnnualweed fls.blueAnnual spottedHerb 4to8ft.tall fls.yellowWeed 2to5ft.tall weakpricklesonstemandIvs.Herb withstinginghairs ito2ft.tall inwoodsBiennial fls.whiteFern inwetgroundHerb 4to10in.high leaflets3RANGEWorld-wideNfld.toMinn Tenn.andKans.OverN.A.andEuropeN.S.toMinn. s.toFla.andKans. alsowestcoastDel.toFla. w.toKans.andTex.N.S.toWash. andOre.N.S.toB.C. andN.M.AtlanticPacifictoN.B.toMinn. s.toFla.andKans.AtlantictoPacificNfld.toSask. s.toGulfMass toMinn.s.toFla.andTex.IndexINSEASONPAGESpring164Spring152andsummerSpring140andsummerSpring158Spring162andsummerMayandJuneMaytoJulyMayandJuneMayandJuneMayandJuneSpring136Spring165and167161161138165 Index268SCIENTIFICANDCOMMONNAMESPhytolaccadecan-dra(PokeWeed)Plantagomajor(CommonPlan-tain)Polygonatumbiflo-rum(TrueSolo-mon's-Seal)PolygonumPersi-caria(Lady'sThumb)Portulacaoleracea(Purslane)Pterisaquilina(Bracken)Radiculanastur-tium-aquaticum(WaterCress)Radiculapalustris(MarshCress)Rhexiavirginica(MeadowBeauty)Rumexcrispus(CurledDock)SabalPalmetto(CabbagePalm)Scirpusvalidus(GreatBulrush)Sonchusoleraceus(SowThistle)CHARACTERISTICSWeed 4to8ft.tall fr.purpleinracemesWeed Ivs.nearlyentireatbase Ms.inspikePerennial Ivs.whitishbeneath fls.lilylike fr.blueberryAnnual 10to20in.high ra-cernedpanicleAnnualweed groundsCoarsefern 2to5ft.tall wide-spreadingPerennial inbrooksandditches Ivs.pepperyPlant erectxoto20in.tall Ivs.deep-cut fls.yellowPerennial fls.purplePerennial 2to3ft.tall Ivs.largeandwavyTree 20to70ft.high Ivs.fan-shapedUpright 3to8ft.tall inpondsandswampsAnnual 2to5ft.tall fls.yellowRANGEMe.toMinn. s.toFla.toTex.INSEASONPAGESpring142AtlantictoSpring166PacificN.B.toOnt.andMich. s.toFla.andTenn.ThroughoutU.S.Spring162SpringandNearlySpringthroughouttoN.A.fallThroughoutU.S.N.C.toFla.163144Spring135N.S.toGa. Nearly148w.toIda.throughandCalif.yearOvermuchSpring149ofN.A.Me.toFla. Spring165w.tola. andLa.summerThroughoutSpring139U.S.Spring136andNearlySpring162 throughout196N.A.NearlySpring166throughoutandU.S.summer 269Index Index270 271IndexSCIENTIFICANDCOMMONNAMESOenotherabiennis(EveningPrim-rose)Orontiumaquati-cum(GoldenClub)Osmorhizalon-gistyiis(SweetMyrrh)Peltandravirginica(ArrowArum)Sagittarialatifolia(Arrowhead)SmilaxBona-nox(BristlyGreen-brier)Smilaxpseudo-china(ChinaBrier)Typhalatifolia(Cattail)ZamiaFloridana(FloridaArrow-root)CHARACTERISTICSBiennial flsyellowHerbaceous Ivs.floatingRootaiomatic fls.inumbelsherbs inshallowwater rootbulbousRoottuberous Ivs.arrow-shaped plant1-3ft.tall inwaterHigh-climbing steinsangledwithspines i-seededHigh-climbing i-t03-seeded rootlargeInshallowwater Ivs.l/2toiin.wide spikexin.indiam.Low Ivs.pinnate rootstemthickFla.penin.Allseasons196BeverageandFlavoringPlantsBenzoinaestivale(Spicebush)Cassiaoccidentalis(CoffeeSenna)Shrub 5-15ft.high entirePlant pods4in.longMe.toMich. andKans.Va.toKans. s.toFla.andTex.Allseasons207Summer221andautumn Index272in.indiam. 273IndexSCIENTIFICANDCOMMONNAMESRhuscanadensis(FragrantSu-mac)CHARACTERISTICSShrub fr.redclusteredRANGEVt.toOnt.andMinn. s.toFla.andTex.INSEASONPAGESummer213andautumnRhuscopallina(DwarfSumac)Shruborsmalltree fr.panicled acidMe.toMinn. s.toFla.andTex.Summer213andautumnRhusglabra(SmoothSumac)Sassafrasvariifo-lium(Sassafras)Shrub 5-10ft.high fr.panicled aromaticN.S.toMinn. s.toFla.andla.Mass s.toFla.andTex.Summer213andautumnAll205seasonsSolidagoodora(SweetGolden-rod)Trilisaodoratis-sima(CarolinaVanilla)Plant odorofanisePerennialherb com-positefamily odorofva-nillaMe.toVt. w.toMo.andTex.Va.toFla. w.toLa.Late219summerSpring223andTriosteumperfolia-tum(HorseGen-tian)Tsugacanadensis(Hemlock)Herb 2or3ft.tall Ivs.clasping fr.orangeEvergreentree Ivs.YT.in.long lightbe-neath cone24'n-longMass s.toAla.andMo.Can.toAla.Summer222andautumnAll220seasonsAcerNegundo(BoxElder)Acerrubrum(RedMaple)SugarsandGumsTree(maple) Ivs.oppositecompound fr.wingedForesttree Ivs.withsharplobesMe.toMan. s.toFla.andMex.N.S.toMan. s.toFla.andTex.Feb.toAprilFeb.toApril231230 Index274SCIENTIFICANDCOMMONNAMESAcersaccharinum(SilverMaple)Acersaccharum(SugarMaple)LiquidambarSty-raciflua(SweetGum)Phragmitescom-munis(ReedGrass)Silphiumlaciniatum(CompassPlant)CHARACTERISTICSForesttree Ivs.withdeeplobesForesttree barkdarkgray Ivs.pointedlobes roundedsinusesTree coastalplain Ivs.star-shaped fr.bur-likeCoarsegrass 5-12ft.high swampyground plumelikepanicleRoughperennial 6-10ft.high leafedgesvertical fl.headlargeRANGEN.B.toFla. w.toS.D.andOkla.Nfld.toMan. s.toFla.andTex.Conn toFla.andTex.ThroughoutU.S.ands.Can.OhiotoS.D. La.fandTex.INSEASONPAGEFeb.231toAprilFeb.toApril228Summer227Summer226Summer232 EDIBLEPLANTS275 Index276SCIENTIFICANDCOMMONNAMESFragariavesca(WoodStraw-berry)Fragariavirginiana(WildStraw-berry)Mitchellarepens(Partridgeberry)Morusalba(WhiteMulberry)Morusnigra(BlackMulberry)MorusrubraMulberry)(RedOpuntiaRafinesquii(WesternPricklyPear)Passifloralutea(YellowPassionFlower)Podophyllumpelta-tum(MayApple)Prunusamericana(WildPlum)Prunusangustifo-lia(ChickasawPlum)CHARACTERISTICSStemlessherb seedsonsurfaceStemless berryscarlet seedsinpitsCreeping ever-greenherb l/Zin.indiam.Tree Ivs.smoothandshining fr.whiteTree similartolastbutfr.black Ivs.roughTree Ivs.largeandlobed fr.itoil/2in.long purple-blackCactus fr.ito2in.long tendril-climb-ing fr.1/2in.indiam. pur-piePlant 2Ivs.fr.pulpy 2in.longTree slightlythorny fr.iin.indiam. redoryellowSmalltree slightlythorny y*to$4in.indiam.RANGEN.B.toN.J. w.toOre.N.B.toSask. s.toFla.andTex.N.S.toMinn. s.toFla.andTex.Easternstatesw.toplainsEasternstatesw.toplainsW.N.E. s.toGulfMich s.toTex.Pa.toKans. s.toFla.andTex.Que.toFla. w.toplainsConn Tex.andN.M.Del.toFla. w.toKans.andTex.INSEASONPAGEJune2iandJulyJune20andJulyJulytoSept.JunetoAug.81NearlyallyearJunetoAug.JunetoAug.JulyandAug.Autumn63Autumn60JulyandAug.4045PrunushortulanaSmalltree spread-W.Va.toJuly43(WildGooseing fr.brightredKans. s.toandPlum)Miss andAug.Tex. 277IndexSCIENTIFICANDCOMMONNAMESPrunuspennsylva-nica(PinCherry)Prunusserotina(BlackWildCherry)Prunusvirginiana(ChokeCherry)PrunusWatsonii(SandPlum)Pyrusangustifolia(Narrow-LeavedCrabApple)Pyrusioensis(WesternCrabApple)Ribesaureum(GoldenCur-rant)RibesCynosbati(WildGoose-berry)Ribesfloridum(WildBlackCur-rant)Ribesgracile(Mis-souriGooseberry)Ribesoxyacantho-ides(SmoothGooseberry)Ribessetosum(BristlyGoose-berry)CHARACTERISTICSSmallslendertree fr.inumbels l/4in.indiam.Largetree fr.inracemes l/$in.indiam.Shruborsm.tree fr.inracemes ^jin.indiam.Shrub slightlyspiny >}$in.indiam. fr.iin.indiam.Smalltree Ivs.woollybeneath"],
]
scores = model.predict(pairs)
print(scores.shape)
# (5,)

# Or rank different texts based on similarity to a single text
ranks = model.rank(
    'explain to 15 minutes at 400 f',
    [
        "W hy do so w ith y o u r h ealth and com fort? L e t us ta k e over y o u r h eating worries. T u rn y o u r Fuel Oil requirem ents over to us. W e will check y o u r supply periodically, delivering when needed. T h e b est grade of Oil available in th e m ost m odern equipm ent by courteous drivers. SOUTHERN ASPHALT FUEL O IL COM PANY, Inc. Dial 4-3611 F o r E m ergency Deliveries D ial 4-4556; 4-4369 S f f C . g t ff y l B L C / f a-P-Jktu'ce.",
        'R.D. Willey Extension 4-H Natural Resources Specialist Clemson University. This information is supplied with the understanding that no discrimination is intended and no endorsement by the Clemson University Cooperative Extension Service is implied. All recom- mendations are for South Carolina conditions and may not apply to other areas. (New 4/99. Reviewed 2/01. Revised 9/05.) The Clemson University Cooperative Extension Service offers its programs to people of all ages regardless of race national origin political beliefs sexual orientation marital or family status and is an equal opportunity employer. Clemson University Cooperating with U.S. Department of Agriculture South Carolina Counties Extension Service South Carolina. Issued in Furtherance of Cooperative Extension Work in Agriculture and Home Economics Acts of May 8 and June 30 1914 Public Service Activities',
        'Setting up a Food Drying Business: A Step-by-step Guide Fabrice Thuillier ITDG Publishing ISBN 1 85339 498 X Drying Foodstuffs Jean Françoia Rozis Backuys Publishers Construction and Use of a Simple Solar Drier to Preserve Food for Off Season HEDON Household Energy Network 4',
        "------------------------------------------------------------------------ ------------------------------------------------------------------------ OPPOSE THE ILLEGAL U.S. ------------------------------------------------------------------------ ------------------------------------------------------------------------ * * * This entire list was downloaded in pieces from unknown sources via Limewire ( http://www.limewire.com )and re- compiled using the Openoffice.org office productivity suite (which I highly recommend, go to http://www.openoffice.org and download it, it's open-source, completely free, and superior to Micro$oft's shitty, bug-ridden proprietary programs and formats.) My profound thanks to whoever made the information in this text available.",
        "wetgroundWeed 2to6ft.high greenishPerennial ito3ft.tall fls.blueAnnualweed fls.blueAnnual spottedHerb 4to8ft.tall fls.yellowWeed 2to5ft.tall weakpricklesonstemandIvs.Herb withstinginghairs ito2ft.tall inwoodsBiennial fls.whiteFern inwetgroundHerb 4to10in.high leaflets3RANGEWorld-wideNfld.toMinn Tenn.andKans.OverN.A.andEuropeN.S.toMinn. s.toFla.andKans. alsowestcoastDel.toFla. w.toKans.andTex.N.S.toWash. andOre.N.S.toB.C. andN.M.AtlanticPacifictoN.B.toMinn. s.toFla.andKans.AtlantictoPacificNfld.toSask. s.toGulfMass toMinn.s.toFla.andTex.IndexINSEASONPAGESpring164Spring152andsummerSpring140andsummerSpring158Spring162andsummerMayandJuneMaytoJulyMayandJuneMayandJuneMayandJuneSpring136Spring165and167161161138165 Index268SCIENTIFICANDCOMMONNAMESPhytolaccadecan-dra(PokeWeed)Plantagomajor(CommonPlan-tain)Polygonatumbiflo-rum(TrueSolo-mon's-Seal)PolygonumPersi-caria(Lady'sThumb)Portulacaoleracea(Purslane)Pterisaquilina(Bracken)Radiculanastur-tium-aquaticum(WaterCress)Radiculapalustris(MarshCress)Rhexiavirginica(MeadowBeauty)Rumexcrispus(CurledDock)SabalPalmetto(CabbagePalm)Scirpusvalidus(GreatBulrush)Sonchusoleraceus(SowThistle)CHARACTERISTICSWeed 4to8ft.tall fr.purpleinracemesWeed Ivs.nearlyentireatbase Ms.inspikePerennial Ivs.whitishbeneath fls.lilylike fr.blueberryAnnual 10to20in.high ra-cernedpanicleAnnualweed groundsCoarsefern 2to5ft.tall wide-spreadingPerennial inbrooksandditches Ivs.pepperyPlant erectxoto20in.tall Ivs.deep-cut fls.yellowPerennial fls.purplePerennial 2to3ft.tall Ivs.largeandwavyTree 20to70ft.high Ivs.fan-shapedUpright 3to8ft.tall inpondsandswampsAnnual 2to5ft.tall fls.yellowRANGEMe.toMinn. s.toFla.toTex.INSEASONPAGESpring142AtlantictoSpring166PacificN.B.toOnt.andMich. s.toFla.andTenn.ThroughoutU.S.Spring162SpringandNearlySpringthroughouttoN.A.fallThroughoutU.S.N.C.toFla.163144Spring135N.S.toGa. Nearly148w.toIda.throughandCalif.yearOvermuchSpring149ofN.A.Me.toFla. Spring165w.tola. andLa.summerThroughoutSpring139U.S.Spring136andNearlySpring162 throughout196N.A.NearlySpring166throughoutandU.S.summer 269Index Index270 271IndexSCIENTIFICANDCOMMONNAMESOenotherabiennis(EveningPrim-rose)Orontiumaquati-cum(GoldenClub)Osmorhizalon-gistyiis(SweetMyrrh)Peltandravirginica(ArrowArum)Sagittarialatifolia(Arrowhead)SmilaxBona-nox(BristlyGreen-brier)Smilaxpseudo-china(ChinaBrier)Typhalatifolia(Cattail)ZamiaFloridana(FloridaArrow-root)CHARACTERISTICSBiennial flsyellowHerbaceous Ivs.floatingRootaiomatic fls.inumbelsherbs inshallowwater rootbulbousRoottuberous Ivs.arrow-shaped plant1-3ft.tall inwaterHigh-climbing steinsangledwithspines i-seededHigh-climbing i-t03-seeded rootlargeInshallowwater Ivs.l/2toiin.wide spikexin.indiam.Low Ivs.pinnate rootstemthickFla.penin.Allseasons196BeverageandFlavoringPlantsBenzoinaestivale(Spicebush)Cassiaoccidentalis(CoffeeSenna)Shrub 5-15ft.high entirePlant pods4in.longMe.toMich. andKans.Va.toKans. s.toFla.andTex.Allseasons207Summer221andautumn Index272in.indiam. 273IndexSCIENTIFICANDCOMMONNAMESRhuscanadensis(FragrantSu-mac)CHARACTERISTICSShrub fr.redclusteredRANGEVt.toOnt.andMinn. s.toFla.andTex.INSEASONPAGESummer213andautumnRhuscopallina(DwarfSumac)Shruborsmalltree fr.panicled acidMe.toMinn. s.toFla.andTex.Summer213andautumnRhusglabra(SmoothSumac)Sassafrasvariifo-lium(Sassafras)Shrub 5-10ft.high fr.panicled aromaticN.S.toMinn. s.toFla.andla.Mass s.toFla.andTex.Summer213andautumnAll205seasonsSolidagoodora(SweetGolden-rod)Trilisaodoratis-sima(CarolinaVanilla)Plant odorofanisePerennialherb com-positefamily odorofva-nillaMe.toVt. w.toMo.andTex.Va.toFla. w.toLa.Late219summerSpring223andTriosteumperfolia-tum(HorseGen-tian)Tsugacanadensis(Hemlock)Herb 2or3ft.tall Ivs.clasping fr.orangeEvergreentree Ivs.YT.in.long lightbe-neath cone24'n-longMass s.toAla.andMo.Can.toAla.Summer222andautumnAll220seasonsAcerNegundo(BoxElder)Acerrubrum(RedMaple)SugarsandGumsTree(maple) Ivs.oppositecompound fr.wingedForesttree Ivs.withsharplobesMe.toMan. s.toFla.andMex.N.S.toMan. s.toFla.andTex.Feb.toAprilFeb.toApril231230 Index274SCIENTIFICANDCOMMONNAMESAcersaccharinum(SilverMaple)Acersaccharum(SugarMaple)LiquidambarSty-raciflua(SweetGum)Phragmitescom-munis(ReedGrass)Silphiumlaciniatum(CompassPlant)CHARACTERISTICSForesttree Ivs.withdeeplobesForesttree barkdarkgray Ivs.pointedlobes roundedsinusesTree coastalplain Ivs.star-shaped fr.bur-likeCoarsegrass 5-12ft.high swampyground plumelikepanicleRoughperennial 6-10ft.high leafedgesvertical fl.headlargeRANGEN.B.toFla. w.toS.D.andOkla.Nfld.toMan. s.toFla.andTex.Conn toFla.andTex.ThroughoutU.S.ands.Can.OhiotoS.D. La.fandTex.INSEASONPAGEFeb.231toAprilFeb.toApril228Summer227Summer226Summer232 EDIBLEPLANTS275 Index276SCIENTIFICANDCOMMONNAMESFragariavesca(WoodStraw-berry)Fragariavirginiana(WildStraw-berry)Mitchellarepens(Partridgeberry)Morusalba(WhiteMulberry)Morusnigra(BlackMulberry)MorusrubraMulberry)(RedOpuntiaRafinesquii(WesternPricklyPear)Passifloralutea(YellowPassionFlower)Podophyllumpelta-tum(MayApple)Prunusamericana(WildPlum)Prunusangustifo-lia(ChickasawPlum)CHARACTERISTICSStemlessherb seedsonsurfaceStemless berryscarlet seedsinpitsCreeping ever-greenherb l/Zin.indiam.Tree Ivs.smoothandshining fr.whiteTree similartolastbutfr.black Ivs.roughTree Ivs.largeandlobed fr.itoil/2in.long purple-blackCactus fr.ito2in.long tendril-climb-ing fr.1/2in.indiam. pur-piePlant 2Ivs.fr.pulpy 2in.longTree slightlythorny fr.iin.indiam. redoryellowSmalltree slightlythorny y*to$4in.indiam.RANGEN.B.toN.J. w.toOre.N.B.toSask. s.toFla.andTex.N.S.toMinn. s.toFla.andTex.Easternstatesw.toplainsEasternstatesw.toplainsW.N.E. s.toGulfMich s.toTex.Pa.toKans. s.toFla.andTex.Que.toFla. w.toplainsConn Tex.andN.M.Del.toFla. w.toKans.andTex.INSEASONPAGEJune2iandJulyJune20andJulyJulytoSept.JunetoAug.81NearlyallyearJunetoAug.JunetoAug.JulyandAug.Autumn63Autumn60JulyandAug.4045PrunushortulanaSmalltree spread-W.Va.toJuly43(WildGooseing fr.brightredKans. s.toandPlum)Miss andAug.Tex. 277IndexSCIENTIFICANDCOMMONNAMESPrunuspennsylva-nica(PinCherry)Prunusserotina(BlackWildCherry)Prunusvirginiana(ChokeCherry)PrunusWatsonii(SandPlum)Pyrusangustifolia(Narrow-LeavedCrabApple)Pyrusioensis(WesternCrabApple)Ribesaureum(GoldenCur-rant)RibesCynosbati(WildGoose-berry)Ribesfloridum(WildBlackCur-rant)Ribesgracile(Mis-souriGooseberry)Ribesoxyacantho-ides(SmoothGooseberry)Ribessetosum(BristlyGoose-berry)CHARACTERISTICSSmallslendertree fr.inumbels l/4in.indiam.Largetree fr.inracemes l/$in.indiam.Shruborsm.tree fr.inracemes ^jin.indiam.Shrub slightlyspiny >}$in.indiam. fr.iin.indiam.Smalltree Ivs.woollybeneath",
    ]
)
# [{'corpus_id': ..., 'score': ...}, {'corpus_id': ..., 'score': ...}, ...]
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 16,200 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                                      | sentence_1                                                                                           | label                                                          |
  |:--------|:------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                                          | string                                                                                               | float                                                          |
  | details | <ul><li>min: 15 characters</li><li>mean: 65.99 characters</li><li>max: 114 characters</li></ul> | <ul><li>min: 156 characters</li><li>mean: 1338.25 characters</li><li>max: 14045 characters</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.16</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                                                                | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | label            |
  |:------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>explain to 15 minutes at 400 f</code>                                               | <code>W hy do so w ith y o u r h ealth and com fort? L e t us ta k e over y o u r h eating worries. T u rn y o u r Fuel Oil requirem ents over to us. W e will check y o u r supply periodically, delivering when needed. T h e b est grade of Oil available in th e m ost m odern equipm ent by courteous drivers. SOUTHERN ASPHALT FUEL O IL COM PANY, Inc. Dial 4-3611 F o r E m ergency Deliveries D ial 4-4556; 4-4369 S f f C . g t ff y l B L C / f a-P-Jktu'ce.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                             | <code>1.0</code> |
  | <code>explain printing paper and coming closer and closer to getting it just right</code> | <code>R.D. Willey Extension 4-H Natural Resources Specialist Clemson University. This information is supplied with the understanding that no discrimination is intended and no endorsement by the Clemson University Cooperative Extension Service is implied. All recom- mendations are for South Carolina conditions and may not apply to other areas. (New 4/99. Reviewed 2/01. Revised 9/05.) The Clemson University Cooperative Extension Service offers its programs to people of all ages regardless of race national origin political beliefs sexual orientation marital or family status and is an equal opportunity employer. Clemson University Cooperating with U.S. Department of Agriculture South Carolina Counties Extension Service South Carolina. Issued in Furtherance of Cooperative Extension Work in Agriculture and Home Economics Acts of May 8 and June 30 1914 Public Service Activities</code> | <code>0.0</code> |
  | <code>explain pressure caused by prosthetic devices</code>                                | <code>Setting up a Food Drying Business: A Step-by-step Guide Fabrice Thuillier ITDG Publishing ISBN 1 85339 498 X Drying Foodstuffs Jean Françoia Rozis Backuys Publishers Construction and Use of a Simple Solar Drier to Preserve Food for Off Season HEDON Household Energy Network 4</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | <code>0.0</code> |
* Loss: [<code>FitMixinLoss</code>](https://sbert.net/docs/package_reference/cross_encoder/losses.html#fitmixinloss)

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `fp16`: True

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `overwrite_output_dir`: False
- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `per_gpu_train_batch_size`: None
- `per_gpu_eval_batch_size`: None
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 3
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: {}
- `warmup_ratio`: 0.0
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `save_safetensors`: True
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `no_cuda`: False
- `use_cpu`: False
- `use_mps_device`: False
- `seed`: 42
- `data_seed`: None
- `jit_mode_eval`: False
- `bf16`: False
- `fp16`: True
- `fp16_opt_level`: O1
- `half_precision_backend`: auto
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: 0
- `ddp_backend`: None
- `tpu_num_cores`: None
- `tpu_metrics_debug`: False
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `past_index`: -1
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_min_num_params`: 0
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `fsdp_transformer_layer_cls_to_wrap`: None
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch
- `optim_args`: None
- `adafactor`: False
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `use_legacy_prediction_loop`: False
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_inputs_for_metrics`: False
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `fp16_backend`: auto
- `push_to_hub_model_id`: None
- `push_to_hub_organization`: None
- `mp_parameters`: 
- `auto_find_batch_size`: False
- `full_determinism`: False
- `torchdynamo`: None
- `ray_scope`: last
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_tokens_per_second`: False
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 0.4936 | 500  | 0.7164        |
| 0.9872 | 1000 | 0.2987        |
| 1.4808 | 1500 | 0.2395        |
| 1.9743 | 2000 | 0.2377        |
| 2.4679 | 2500 | 0.1861        |
| 2.9615 | 3000 | 0.1947        |


### Framework Versions
- Python: 3.11.0rc1
- Sentence Transformers: 5.1.2
- Transformers: 4.57.1
- PyTorch: 2.6.0+cu124
- Accelerate: 1.11.0
- Datasets: 4.3.0
- Tokenizers: 0.22.1

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->