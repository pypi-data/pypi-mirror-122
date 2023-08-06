def _module_factory(pt, index, module):
    if module in ["BM25", "QLM", "DFR", "PL2", "InL2", "DLH", "DPH", "DFRee", "DFI0", "DirichletLM", "DFIC", "DFIZ",
                  "InB2", "InL2"]:
        return pt.BatchRetrieve(index, wmodel=module, verbose=False)

    elif module == "HiemstraLM":
        return pt.BatchRetrieve(index, wmodel="Hiemstra_LM", verbose=False)

    # elif module == "DirichletLM":
    #    return pt.BatchRetrieve(index, wmodel="Dirichlet_LM", verbose=False)

    elif module == "InexpB2":
        return pt.BatchRetrieve(index, wmodel="In_expB2", verbose=False)

    elif module == "InexpC2":
        return pt.BatchRetrieve(index, wmodel="In_expC2", verbose=False)
    elif module == "JsKLs":
        return pt.BatchRetrieve(index, wmodel="Js_KLs", verbose=False)

    elif module == "TFIDF":
        return pt.BatchRetrieve(index, wmodel="TF_IDF", verbose=False)

    elif module in ["Bo1QueryExpansion", "RM3", "AxiomaticQE", "KLQueryExpansion"]:
        return getattr(pt.rewrite, module)(index, verbose=False)


def get_pipeline(pt, index, config):
    components = config.split("_")
    retriever = _module_factory(pt, index, components[2])

    if components[3] == 'none':

        return retriever

    else:

        return retriever >> _module_factory(pt, index, components[3]) >> retriever
