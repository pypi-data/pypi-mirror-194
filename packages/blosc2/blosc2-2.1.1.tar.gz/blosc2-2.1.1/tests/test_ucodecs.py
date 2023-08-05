#######################################################################
# Copyright (C) 2019-present, Blosc Development team <blosc@blosc.org>
# All rights reserved.
#
# This source code is licensed under a BSD-style license (found in the
# LICENSE file in the root directory of this source tree)
#######################################################################

import sys

import numpy as np
import pytest

import blosc2


@pytest.mark.parametrize(
    "codec_name, id, dtype, cparams",
    [
        ("codec1", 160, np.dtype(np.int32), {"filters": [blosc2.Filter.NOFILTER], "filters_meta": [0]}),
        ("codec1", 180, np.dtype(np.float64), {}),
        ("codec1", 255, np.dtype(np.uint8), {"filters": [blosc2.Filter.NOFILTER], "filters_meta": [0]}),
    ],
)
@pytest.mark.parametrize(
    "nchunks, contiguous, urlpath",
    [
        (2, True, None),
        (1, True, "test_codec.b2frame"),
        (5, False, None),
        (3, False, "test_codecilters.b2frame"),
    ],
)
def test_ucodecs(contiguous, urlpath, cparams, nchunks, codec_name, id, dtype):
    blosc2.remove_urlpath(urlpath)

    cparams["nthreads"] = 1
    cparams["codec"] = id
    dparams = {"nthreads": 1}
    chunk_len = 20 * 1000
    blocksize = chunk_len / 10
    cparams["blocksize"] = blocksize

    def encoder1(input, output, meta, schunk):
        nd_input = input.view(dtype)
        if np.max(nd_input) == np.min(nd_input):
            output[0 : schunk.typesize] = input[0 : schunk.typesize]
            n = nd_input.size.to_bytes(4, sys.byteorder)
            output[schunk.typesize : schunk.typesize + 4] = [n[i] for i in range(4)]
            return schunk.typesize + 4
        else:
            # memcpy
            return 0

    def decoder1(input, output, meta, schunk):
        nd_input = input.view(np.int32)
        nd_output = output.view(dtype)
        nd_output[0 : nd_input[1]] = [nd_input[0]] * nd_input[1]
        return nd_input[1] * schunk.typesize

    if id not in blosc2.ucodecs_registry:
        blosc2.register_codec(codec_name, id, encoder1, decoder1)
    if "f" in dtype.str:
        data = np.linspace(0, 50, chunk_len * nchunks, dtype=dtype)
    else:
        fill_value = 341 if dtype == np.int32 else 33
        data = np.full(chunk_len * nchunks, fill_value, dtype=dtype)

    schunk = blosc2.SChunk(
        chunksize=chunk_len * dtype.itemsize,
        data=data,
        contiguous=contiguous,
        urlpath=urlpath,
        cparams=cparams,
        dparams=dparams,
    )

    out = np.empty(chunk_len * nchunks, dtype=dtype)
    schunk.get_slice(0, chunk_len * nchunks, out=out)
    if "f" in dtype.str:
        assert np.allclose(data, out)
    else:
        assert np.array_equal(data, out)

    blosc2.remove_urlpath(urlpath)
