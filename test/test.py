# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# 7-segment encodings for hex digits 0–F (active high)
# uo_out[0]=a, [1]=b, [2]=c, [3]=d, [4]=e, [5]=f, [6]=g
SEG = {
    0x0: 0x3F,  # 0: a b c d e f
    0x1: 0x06,  # 1: b c
    0x2: 0x5B,  # 2: a b d e g
    0x3: 0x4F,  # 3: a b c d g
    0x4: 0x66,  # 4: b c f g
    0x5: 0x6D,  # 5: a c d f g
    0x6: 0x7D,  # 6: a c d e f g
    0x7: 0x07,  # 7: a b c
    0x8: 0x7F,  # 8: a b c d e f g
    0x9: 0x6F,  # 9: a b c d f g
    0xA: 0x77,  # A: a b c e f g
    0xB: 0x7C,  # b: c d e f g
    0xC: 0x39,  # C: a d e f
    0xD: 0x5E,  # d: b c d e g
    0xE: 0x79,  # E: a d e f g
    0xF: 0x71,  # F: a e f g
}

# Test vectors: (input, is_prime)
# uo_out[7] = is_prime (decimal point)
# uo_out[6:0] = SEG[input & 0xF]
TEST_VECTORS = [
    (0,   False),  # 0: not prime
    (1,   False),  # 1: not prime (by definition)
    (2,   True),   # 2: smallest prime
    (3,   True),   # 3: prime
    (4,   False),  # 4 = 2²
    (7,   True),   # 7: prime
    (9,   False),  # 9 = 3²
    (15,  False),  # 15 = 3 × 5
    (17,  True),   # 17: prime
    (25,  False),  # 25 = 5²
    (97,  True),   # 97: prime
    (100, False),  # 100 = 2² × 5²
    (127, True),   # 127: Mersenne prime (2⁷ − 1)
    (128, False),  # 128 = 2⁷
    (251, True),   # 251: largest prime ≤ 255
    (255, False),  # 255 = 3 × 5 × 17
]


@cocotb.test()
async def test_prime_detector(dut):
    dut._log.info("Prime Number Detector - Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset (combinational design — reset not needed but good practice)
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Testing prime detection")

    for n, expected_prime in TEST_VECTORS:
        dut.ui_in.value = n
        await ClockCycles(dut.clk, 1)

        out = int(dut.uo_out.value)
        actual_prime = bool((out >> 7) & 1)
        actual_seg   = out & 0x7F
        expected_seg = SEG[n & 0xF]

        status = "prime" if expected_prime else "composite"
        dut._log.info(
            f"n={n:3d} (0x{n:02X})  seg=0x{actual_seg:02X}  dp={int(actual_prime)}  [{status}]"
        )

        assert actual_prime == expected_prime, (
            f"n={n}: expected {'prime' if expected_prime else 'composite'}, "
            f"got {'prime' if actual_prime else 'composite'} (uo_out=0x{out:02X})"
        )
        assert actual_seg == expected_seg, (
            f"n={n}: segment mismatch — expected 0x{expected_seg:02X}, got 0x{actual_seg:02X}"
        )

    dut._log.info(f"All {len(TEST_VECTORS)} test vectors passed")
