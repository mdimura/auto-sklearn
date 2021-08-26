from typing import Dict, Optional, Tuple, Union

from ConfigSpace.configuration_space import ConfigurationSpace
from sklearn.utils.validation import check_random_state

import numpy as np

from autosklearn.pipeline.base import DATASET_PROPERTIES_TYPE, PIPELINE_DATA_DTYPE
import autosklearn.pipeline.implementations.CategoryShift
from autosklearn.pipeline.components.base import AutoSklearnPreprocessingAlgorithm
from autosklearn.pipeline.constants import DENSE, SPARSE, UNSIGNED_DATA, INPUT


class CategoryShift(AutoSklearnPreprocessingAlgorithm):
    """ Add 3 to every category.
    Down in the pipeline, category 2 will be attribute to missing values,
    category 1 will be assigned to low occurence categories, and category 0
    is not used, so to provide compatibility with sparse matrices.
    """

    def __init__(self, random_state: Optional[Union[int, np.random.RandomState]] = None):
        self.random_state = check_random_state(random_state)
        self._random_seed = self.random_state.randint(np.iinfo(np.uint32).max, dtype='u8')

    def fit(self, X: PIPELINE_DATA_DTYPE, y: Optional[PIPELINE_DATA_DTYPE] = None
            ) -> 'CategoryShift':
        self.preprocessor = autosklearn.pipeline.implementations.CategoryShift\
            .CategoryShift()
        self.preprocessor.fit(X, y)
        return self

    def transform(self, X: PIPELINE_DATA_DTYPE) -> PIPELINE_DATA_DTYPE:
        if self.preprocessor is None:
            raise NotImplementedError()
        return self.preprocessor.transform(X)

    @staticmethod
    def get_properties(dataset_properties: Optional[DATASET_PROPERTIES_TYPE] = None
                       ) -> Dict[str, Optional[Union[str, int, bool, Tuple]]]:
        return {'shortname': 'CategShift',
                'name': 'Category Shift',
                'handles_missing_values': True,
                'handles_nominal_values': True,
                'handles_numerical_features': True,
                'prefers_data_scaled': False,
                'prefers_data_normalized': False,
                'handles_regression': True,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'handles_multioutput': True,
                'is_deterministic': True,
                # TODO find out of this is right!
                'handles_sparse': True,
                'handles_dense': True,
                'input': (DENSE, SPARSE, UNSIGNED_DATA),
                'output': (INPUT,),
                'preferred_dtype': None}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties: Optional[DATASET_PROPERTIES_TYPE] = None
                                        ) -> ConfigurationSpace:
        return ConfigurationSpace()
