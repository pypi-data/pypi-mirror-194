from ..utils.builder import FUNCTIONAL_TRANSFORMERS
from ..utils.base import Base
from ..utils.transform_wrapper import transform_wrapper
import copy

@FUNCTIONAL_TRANSFORMERS.add()
class parallelTransformer(Base):
    def __init__(self, transformers: list):
        super().__init__()
        self.transformers = transformers


    def transform(self, X)-> list:
        if isinstance(X, list):
            X=X
        elif X is None:
            X = ""
            X = [X for i in range(len(self.transformers))]
        else:
            X = [copy.deepcopy(X) for i in range(len(self.transformers))]

        # print(X)
        # assert len(X)>0
        outputs = []
        for i, transformer in enumerate(self.transformers):
            if hasattr(transformer, "breakpoint"):
                if transformer.breakpoint=="true":
                    # print(transform.node_name, "has breakpoint", transform.breakpoint)
                    outputs.append(transformer.transform(X[i]))
                    print("break")
                    return outputs

            outputs.append(transformer.transform(X[i]))
        return outputs

