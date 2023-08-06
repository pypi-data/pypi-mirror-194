# Copyright (c) 2021, Apple Inc. All rights reserved.
#
# Use of this source code is governed by a BSD-3-clause license that can be
# found in the LICENSE.txt file or at https://opensource.org/licenses/BSD-3-Clause

import os

import pytest
import paddle
import paddlevision

import coremltools as ct
from coremltools._deps import _HAS_PADDLE, MSG_PADDLE_NOT_FOUND

if _HAS_PADDLE:
    import paddle
    import paddlevision


@pytest.mark.skipif(not _HAS_PADDLE, reason=MSG_PADDLE_NOT_FOUND)
class TestPaddlePaddleConverter:
    @staticmethod
    def test_no_inputs():
        model = paddlevision.models.mobilenet_v2()
        model.eval()

        example_input = paddle.rand(1, 3, 256, 256)

        traced_model = paddle.jit.trace(model, example_input)

        with pytest.raises(ValueError) as e:
            ct.convert(traced_model)
        e.match(r'Expected argument for paddle "inputs" not provided')


    @staticmethod
    def test_pth_extension(tmpdir):
        # test for issue: https://github.com/apple/coremltools/issues/917
        class TestModule(paddle.nn.Module):
            def __init__(self):
                super(TestModule, self).__init__()
                self.linear = paddle.nn.Linear(10, 20)

            def forward(self, x):
                return self.linear(x)

        model = TestModule()
        model.eval()
        example_input = paddle.rand(1, 10)
        traced_model = paddle.jit.trace(model, example_input)
        model_path = os.path.join(str(tmpdir), "paddle_model.pth")
        traced_model.save(model_path)

        ct.convert(
            model_path,
            source='paddle',
            inputs=[
                ct.TensorType(
                    shape=example_input.shape,
                )
            ],
        )
