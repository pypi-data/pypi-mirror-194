def load_best_model_weight(model):
    """
    :param cchess_alphazero.agent.model.CChessModel model:
    :return:
    """
    return model.load(model.config.resource.model_best_config_path, model.config.resource.model_best_weight_path)


def need_to_reload_best_model_weight(model):
    """

    :param cchess_alphazero.agent.model.CChessModel model:
    :return:
    """
    print("start reload the best model if changed")
    digest = model.fetch_digest(model.config.resource.model_best_weight_path)
    if digest != model.digest:
        return True

    print("the best model is not changed")
    return False
