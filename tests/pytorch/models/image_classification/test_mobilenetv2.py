import pytest

from typing import Union
import torch

from neuralmagicML.pytorch.models import ModelRegistry, mobilenet_v2

from tests.pytorch.models.utils import compare_model


@pytest.mark.parametrize(
    "key,pretrained,test_input",
    [
        ("mobilenet-v2", False, True),
        ("mobilenet-v2", True, False),
        ("mobilenet-v2", "base", False),
    ],
)
def test_mobilenets_v2(key: str, pretrained: Union[bool, str], test_input: bool):
    model = ModelRegistry.create(key, pretrained)
    diff_model = mobilenet_v2()

    if pretrained:
        compare_model(model, diff_model, same=False)
        match_model = ModelRegistry.create(key, pretrained)
        compare_model(model, match_model, same=True)

    if test_input:
        input_shape = ModelRegistry.input_shape(key)
        batch = torch.randn(1, *input_shape)
        out = model(batch)
        assert isinstance(out, tuple)
        for tens in out:
            assert tens.shape[0] == 1
            assert tens.shape[1] == 1000
