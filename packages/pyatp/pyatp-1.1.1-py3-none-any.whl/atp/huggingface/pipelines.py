#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: pipelines.py
@time: 2023/02/23
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union
from transformers.configuration_utils import PretrainedConfig
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
from transformers.feature_extraction_utils import PreTrainedFeatureExtractor
from transformers import Pipeline
from transformers import pipeline as t_pipeline
from transformers.pipelines import get_task

import os

cache_dir = "/Users/yangyanbo/cache/"


def pipeline(
        task: str = None,
        model: Optional = None,
        config: Optional[Union[str, PretrainedConfig]] = None,
        tokenizer: Optional[Union[str, PreTrainedTokenizer, PreTrainedTokenizerFast]] = None,
        feature_extractor: Optional[Union[str, PreTrainedFeatureExtractor]] = None,
        framework: Optional[str] = None,
        revision: Optional[str] = None,
        use_fast: bool = True,
        use_auth_token: Optional[Union[str, bool]] = None,
        device: Optional[Union[int, str, "torch.device"]] = None,
        device_map=None,
        torch_dtype=None,
        trust_remote_code: Optional[bool] = None,
        model_kwargs: Dict[str, Any] = None,
        pipeline_class: Optional[Any] = None,
        **kwargs,
) -> Pipeline:
    if task is None and model is None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline without either a task or a model "
            "being specified. "
            "Please provide a task class or a model"
        )
    if model is None and tokenizer is not None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline with tokenizer specified but not the model as the provided tokenizer"
            " may not be compatible with the default model. Please provide a PreTrainedModel class or a"
            " path/identifier to a pretrained model when providing tokenizer."
        )
    if model is None and feature_extractor is not None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline with feature_extractor specified but not the model as the provided"
            " feature_extractor may not be compatible with the default model. Please provide a PreTrainedModel class"
            " or a path/identifier to a pretrained model when providing feature_extractor."
        )

    if task is None and model is not None:
        if not isinstance(model, str):
            raise RuntimeError(
                "Inferring the task automatically requires to check the hub with a model_id defined as a `str`."
                f"{model} is not a valid model_id."
            )
        task = get_task(model, use_auth_token)

    local_path = os.path.join(cache_dir, model)
    if os.path.exists(local_path):
        model = local_path
    return t_pipeline(task=task, model=model, config=config, tokenizer=tokenizer, feature_extractor=feature_extractor,
                      framework=framework, revision=revision, use_fast=use_fast, use_auth_token=use_auth_token,
                      device=device,
                      device_map=device_map, torch_dtype=torch_dtype, trust_remote_code=trust_remote_code,
                      model_kwargs=model_kwargs, pipeline_class=pipeline_class, **kwargs)
