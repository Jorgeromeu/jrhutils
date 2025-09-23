from einops import rearrange

def hwc_to_chw(x):
    """
    Convert (..., H, W, C) -> (..., C, H, W).
    For grayscale (H, W), returns (1, H, W).
    Works with NumPy arrays or torch tensors.
    """
    if x.ndim >= 3:
        return rearrange(x, "... h w c -> ... c h w")
    else:
        raise ValueError(f"Unsupported shape={x.shape}; expected (..., h, w, c) with c>=1.")


def chw_to_hwc(x):
    """
    Convert (..., C, H, W) -> (..., H, W, C).
    """
    if x.ndim < 3:
        raise ValueError(f"Unsupported shape={x.shape}; expected (..., c, h, w) with c>=1.")

    return rearrange(x, "... c h w -> ... h w c")
