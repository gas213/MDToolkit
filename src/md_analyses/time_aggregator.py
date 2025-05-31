from md_dataclasses.box import Box
from md_dataclasses.vector3d import Vector3D

def update_atom_extremes(overall_extremes: Box, new_extremes: Box) -> Box:
    return new_extremes if overall_extremes is None else Box(
        Vector3D(
            min(overall_extremes.lo.x, new_extremes.lo.x),
            min(overall_extremes.lo.y, new_extremes.lo.y),
            min(overall_extremes.lo.z, new_extremes.lo.z)
        ),
        Vector3D(
            max(overall_extremes.hi.x, new_extremes.hi.x),
            max(overall_extremes.hi.y, new_extremes.hi.y),
            max(overall_extremes.hi.z, new_extremes.hi.z)
        )
    )

def update_avg_scalar(avg: float, val_new: float, count_new: int) -> float:
    return val_new if (avg is None or count_new == 1) else (avg * (count_new - 1) + val_new) / count_new

def update_avg_profile(profile_avg: dict[str, float], profile_new: dict[str, float], count_new: int) -> dict[str, float]:
    if profile_avg is None or count_new == 1: return profile_new
    num_factor = count_new - 1
    div_factor = 1.0 / float(count_new)
    for bin, val_new in profile_new.items():
        profile_avg[bin] = (profile_avg[bin] * num_factor + val_new) * div_factor
    return profile_avg