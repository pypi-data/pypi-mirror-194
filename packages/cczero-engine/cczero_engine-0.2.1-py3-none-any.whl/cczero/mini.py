class Config:
    def __init__(self):
        self.model = ModelConfig()
        self.play = PlayConfig()


class PlayConfig:
    def __init__(self):
        self.max_processes = 1
        self.search_threads = 50
        self.vram_frac = 1.0
        self.simulation_num_per_move = 300  # just for debug
        self.c_puct = 1.5
        self.noise_eps = 0.25
        self.dirichlet_alpha = 0.2
        self.tau_decay_rate = 0.98
        self.virtual_loss = 3
        self.max_game_length = 100
        self.share_mtcs_info_in_self_play = False
        self.reset_mtcs_info_per_game = 5
        self.enable_resign_rate = 0.1
        self.resign_threshold = -0.92
        self.min_resign_turn = 20


class ModelConfig:
    def __init__(self):
        self.cnn_filter_num = 256
        self.cnn_first_filter_size = 5
        self.cnn_filter_size = 3
        self.res_layer_num = 7
        self.l2_reg = 1e-4
        self.value_fc_size = 256
        self.distributed = False
        self.input_depth = 14