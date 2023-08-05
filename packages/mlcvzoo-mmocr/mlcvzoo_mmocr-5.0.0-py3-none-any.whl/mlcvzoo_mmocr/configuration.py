# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""
Definition of the MMOCRConfig that is used to configure the MMOCRModel (and subclasses).
"""

from __future__ import annotations

import logging
from typing import Optional

import related
from attr import define
from mlcvzoo_base.configuration.class_mapping_config import (
    ClassMappingConfig,
    ClassMappingModelClassesConfig,
)
from mlcvzoo_mmdetection.configuration import (
    MMDetectionConfig,
    MMDetectionDistributedTrainConfig,
    MMDetectionInferenceConfig,
    MMDetectionTrainArgparseConfig,
    MMDetectionTrainConfig,
)

logger = logging.getLogger(__name__)


@define
class MMOCRTrainArgparseConfig(MMDetectionTrainArgparseConfig):
    __related_strict__ = True
    # argparse parameter from mmdetection:

    # The checkpoint file to load from.
    load_from: Optional[str] = related.StringField(required=False, default=None)

    # Memory cache config for image loading speed-up during training.
    mc_config: Optional[str] = related.StringField(required=False, default=None)

    # NOTE: The following argparse arguments from mmdet.tools.train will not be used in this
    #       configuration.
    #
    # - local_rank: int = related.StringField(default=0) rank for distributed training

    def check_values(self) -> bool:
        if self.load_from is not None:
            logger.warning(
                "DEPRECATED: The load_from config attribute is no longer supported "
                "and will be removed in future versions"
            )

        if self.mc_config is not None:
            logger.warning(
                "DEPRECATED: The mc_config config attribute is no longer supported "
                "and will be removed in future versions"
            )

        return True


@define
class MMOCRTrainConfig(MMDetectionTrainConfig):
    """
    argparse parameter from mmdetection/tools/train.py
    """

    __related_strict__ = True

    argparse_config: MMOCRTrainArgparseConfig = related.ChildField(
        cls=MMOCRTrainArgparseConfig
    )

    multi_gpu_config: Optional[MMDetectionDistributedTrainConfig] = related.ChildField(
        cls=MMDetectionDistributedTrainConfig, required=False, default=None
    )


@define
class MMOCRInferenceConfig(MMDetectionInferenceConfig):
    __related_strict__ = True

    # Whether the output polygon should be formatted to represent a rect, or
    # the polygon should be kept as it is
    to_rect_polygon: bool = related.BooleanField(default=False, required=False)


@define
class MMOCRConfig(MMDetectionConfig):
    __related_strict__ = True

    __text_class_id__ = 0
    __text_class_name__ = "text"

    inference_config: MMOCRInferenceConfig = related.ChildField(
        cls=MMOCRInferenceConfig
    )

    train_config: MMOCRTrainConfig = related.ChildField(cls=MMOCRTrainConfig)

    class_mapping: ClassMappingConfig = related.ChildField(
        cls=ClassMappingConfig,
        default=ClassMappingConfig(
            mapping=[],
            model_classes=[
                # OCR models only detect text, therefore it has this default class mapping
                ClassMappingModelClassesConfig(
                    class_id=__text_class_id__,
                    class_name=__text_class_name__,
                )
            ],
            number_model_classes=1,
        ),
    )
