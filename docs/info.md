<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a purely combinational 8-bit adder. It takes two 8-bit operands — Addend A on the dedicated inputs (`ui[7:0]`) and Addend B on the bidirectional pins configured as inputs (`uio[7:0]`) — and outputs their 8-bit sum on the dedicated outputs (`uo[7:0]`). The result wraps around on overflow (modulo 256). No clock or reset is required.

## How to test

1. Set `ui[7:0]` to the first operand (Addend A, 0–255).
2. Set `uio[7:0]` to the second operand (Addend B, 0–255).
3. Read the sum from `uo[7:0]`.

Example: set `ui` = 20 and `uio` = 30, then `uo` should read 50.

## External hardware

None required.
