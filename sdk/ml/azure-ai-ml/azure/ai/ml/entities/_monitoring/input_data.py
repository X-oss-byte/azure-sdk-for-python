# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azure.ai.ml._restclient.v2023_04_01_preview.models import MonitoringInputData as RestMonitoringInputData
from azure.ai.ml._utils._experimental import experimental
from azure.ai.ml._utils.utils import camel_to_snake, snake_to_camel
from azure.ai.ml.constants._monitoring import MonitorDatasetContext
from azure.ai.ml.entities._inputs_outputs import Input
from azure.ai.ml.entities._mixins import RestTranslatableMixin


@experimental
class MonitorInputData(RestTranslatableMixin):
    """Monitor input data.

    :keyword input_dataset: Input data used by the monitor
    :type input_dataset: Optional[~azure.ai.ml.Input]
    :keyword dataset_context: The context of the input dataset. Accepted values are "model_inputs",
        "model_outputs", "training", "test", "validation", and "ground_truth".
    :type dataset_context: Optional[Union[str, ~azure.ai.ml.constants.MonitorDatasetContext]]
    :keyword target_column_name: The target column in the given input dataset.
    :type target_column_name: Optional[str]
    :keyword pre_processing_component: The ARM (Azure Resource Manager) resource ID of the component resource used to
        preprocess the data.
    :type pre_processing_component: Optional[str]
    """

    def __init__(
        self,
        *,
        input_dataset: Input = None,
        dataset_context: MonitorDatasetContext = None,
        target_column_name: str = None,
        pre_processing_component: str = None,
    ) -> None:
        self.input_dataset = input_dataset if isinstance(input_dataset, Input) else Input(**input_dataset)
        self.dataset_context = dataset_context
        self.target_column_name = target_column_name
        self.pre_processing_component = pre_processing_component

    def _to_rest_object(self) -> RestMonitoringInputData:
        rest_asset = {"uri": self.input_dataset.path, "jobInputType": self.input_dataset.type}
        return RestMonitoringInputData(
            data_context=snake_to_camel(self.dataset_context),
            asset=rest_asset,
            preprocessing_component_id=self.pre_processing_component,
            target_column_name=self.target_column_name,
        )

    @classmethod
    def _from_rest_object(cls, obj: RestMonitoringInputData) -> "MonitorInputData":
        return cls(
            input_dataset=Input(path=obj.asset["uri"], type=obj.asset["jobInputType"]),
            dataset_context=camel_to_snake(obj.data_context),
            target_column_name=obj.target_column_name,
            pre_processing_component=obj.preprocessing_component_id,
        )
