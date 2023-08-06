from __future__ import annotations

from typing import cast

from datalabs import load_dataset
from datalabs.features.features import ClassLabel, Sequence

from promptware.dataset import DatasetConfig


def _replace_one(names: list[str], lab: int):
    return names[lab] if lab != -1 else "_NULL_"


def _replace_labels(features: dict, example: dict) -> dict:
    new_example = {}
    for examp_k, examp_v in example.items():
        examp_f = features[examp_k]
        # Label feature
        if isinstance(examp_f, ClassLabel):
            names = cast(ClassLabel, examp_f).names
            new_example[examp_k] = _replace_one(names, examp_v)
        # Sequence feature
        elif isinstance(examp_f, Sequence):
            examp_seq = cast(Sequence, examp_f)
            # Sequence of labels
            if isinstance(examp_seq.feature, ClassLabel):
                names = cast(ClassLabel, examp_seq.feature).names
                new_example[examp_k] = [_replace_one(names, x) for x in examp_v]
            # Sequence of anything else
            else:
                new_example[examp_k] = examp_v
        # Anything else
        else:
            new_example[examp_k] = examp_v
    return new_example


def get_evaluated_data(datalab_config: DatasetConfig) -> list[dict]:
    # Construct evaluate dataset
    test_data = load_dataset(
        datalab_config.dataset_name,
        datalab_config.sub_dataset,
        split=datalab_config.split_name,
    )
    n_samples = (
        datalab_config.n_samples
        if len(test_data) > datalab_config.n_samples
        else len(test_data)
    )

    info = test_data.info

    return [_replace_labels(info.features, test_data[ind]) for ind in range(n_samples)]
