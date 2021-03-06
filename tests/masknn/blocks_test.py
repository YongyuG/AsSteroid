import pytest
import torch
from asteroid.masknn import blocks


@pytest.mark.parametrize("mask_act", ["relu", "softmax"])
@pytest.mark.parametrize("out_chan", [None, 10])
def test_tdconvnet(mask_act, out_chan):
    in_chan, n_src = 20, 2
    model = blocks.TDConvNet(in_chan=in_chan, n_src=n_src, mask_act=mask_act,
                             n_blocks=2, n_repeats=2, bn_chan=10, hid_chan=11,
                             skip_chan=12, out_chan=out_chan)
    batch, n_frames = 2, 24
    inp = torch.randn(batch, in_chan, n_frames)
    out = model(inp)
    _ = model.get_config()
    out_chan = out_chan if out_chan else in_chan
    assert out.shape == (batch, n_src, out_chan, n_frames)


@pytest.mark.parametrize("mask_act", ["relu", "softmax"])
@pytest.mark.parametrize("out_chan", [None, 10])
@pytest.mark.parametrize("hop_size", [None, 5])
def test_dprnn(mask_act, out_chan, hop_size):
    in_chan, n_src = 20, 2
    model = blocks.DPRNN(in_chan=in_chan, n_src=n_src, mask_act=mask_act,
                         chunk_size=20, n_repeats=2, bn_chan=10, hid_size=11,
                         out_chan=out_chan, hop_size=hop_size)
    batch, n_frames = 2, 78
    inp = torch.randn(batch, in_chan, n_frames)
    out = model(inp)
    _ = model.get_config()
    out_chan = out_chan if out_chan else in_chan
    assert out.shape == (batch, n_src, out_chan, n_frames)