from sklearn.base import BaseEstimator, TransformerMixin

class Base(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.node_id = ""
        self.node_name = ""
        self.description = ""
        self.isParallel = "false"
        self.total_time = 0
        self.total_input = 0
        self.total_output = 0
        self.data_container_type="pandas"
        self.start_datetime = ""
        self.end_datetime = ""
        self.breakpoint = "false"


    def fit(self):
        pass
    