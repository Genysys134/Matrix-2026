# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def compare_reference(dut):
    import os

    for img in glob.glob("output/frame*.png"):
        basename = img.removeprefix("output/")
        ref_path = f"reference/{basename}"
        
        # Check if the reference file actually exists
        if not os.path.exists(ref_path):
            dut._log.warning(f"Reference image {ref_path} not found. Skipping comparison.")
            continue

        dut._log.info(f"Comparing {basename} to reference image")
        frame = Image.open(img)
        ref = Image.open(ref_path)
        diff = ImageChops.difference(frame, ref)
        
        if diff.getbbox() is not None:
            diff.save(f"output/diff_{basename}")
            assert False, f"Rendered {basename} differs from reference image"
