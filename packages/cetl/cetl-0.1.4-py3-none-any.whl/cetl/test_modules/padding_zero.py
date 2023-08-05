from cetl.utils.builder import TEST_TRANSFORMERS, pd
from ..utils.base import Base
from cetl.utils.transform_wrapper import timeit

@TEST_TRANSFORMERS.add()
class paddingZero(Base):
    def __init__(self, subset=None, num_digit=6):
        self.subset = subset
        self.num_digit=num_digit

    def padding_zero(self, x, num_digit=6):
        if type(x)==str:
            return x.zfill(num_digit)
        else:
            type(x)==int
            new_x = str(x).zfill(num_digit)
            return new_x

    @timeit
    def transform(self, dataframe: pd.DataFrame)-> pd.DataFrame:
        df = dataframe
        for field in self.subset:
            df[field]=df[field].apply(self.padding_zero)
        return df