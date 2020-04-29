from pathlib import Path
from skimage.measure import regionprops

from brainio.brainio import load_any
from imlib.source.source_files import get_structures_path
from neuro.structures.IO import load_structures_as_df
from neuro.atlas_tools import paths as reg_paths

import napari
import numpy as np

amap_output_dir = (
    "/media/adam/Storage/cellfinder/analysis/inj_segment/CT_CX_142_2_test"
)


region_acronym = "RSP"
visual_check = True

left_hemisphere_value = 2
right_hemisphere_value = 1
properties_to_fetch = ["area", "bbox", "centroid"]

structures_reference_df = load_structures_as_df(get_structures_path())

region_value = int(
    structures_reference_df[
        structures_reference_df["acronym"] == region_acronym
    ]["id"]
)

region_search_string = "/" + str(region_value) + "/"
sub_regions = structures_reference_df[
    structures_reference_df["structure_id_path"].str.contains(
        region_search_string
    )
]

amap_output_dir = Path(amap_output_dir)
annotations_image = load_any(amap_output_dir / reg_paths.ANNOTATIONS)
midpoint = int(annotations_image.shape[0] // 2)

hemispheres_image = load_any(amap_output_dir / reg_paths.HEMISPHERES)

sub_region_values = list(sub_regions["id"])
region_mask = np.isin(annotations_image, sub_region_values)

left_region_mask = region_mask * (hemispheres_image == left_hemisphere_value)
right_region_mask = region_mask * (hemispheres_image == right_hemisphere_value)

left_region_summary = regionprops(left_region_mask.astype(np.int8))[0]
right_region_summary = regionprops(right_region_mask.astype(np.int8))[0]


results_dict = {
    "x_min_um_left": left_region_summary.bbox[0],
    "y_min_um_left": left_region_summary.bbox[1],
    "z_min_um_left": left_region_summary.bbox[2],
    "x_max_um_left": left_region_summary.bbox[3],
    "y_max_um_left": left_region_summary.bbox[4],
    "z_max_um_left": left_region_summary.bbox[5],
    "x_center_um_left": left_region_summary.centroid[0],
    "y_center_um_left": left_region_summary.centroid[1],
    "z_center_um_left": left_region_summary.centroid[2],
    "x_min_um_right": right_region_summary.bbox[0],
    "y_min_um_right": right_region_summary.bbox[1],
    "z_min_um_right": right_region_summary.bbox[2],
    "x_max_um_right": right_region_summary.bbox[3],
    "y_max_um_right": right_region_summary.bbox[4],
    "z_max_um_right": right_region_summary.bbox[5],
    "x_center_um_right": right_region_summary.centroid[0],
    "y_center_um_right": right_region_summary.centroid[1],
    "z_center_um_right": right_region_summary.centroid[2],
}


if visual_check:
    with napari.gui_qt():
        viewer = napari.Viewer()

        viewer.add_labels(
            np.swapaxes(hemispheres_image, 2, 0), name="Hemispheres"
        )
        viewer.add_labels(
            np.swapaxes(annotations_image, 2, 0), name="Annotations"
        )
        viewer.add_labels(np.swapaxes(region_mask, 2, 0), name=region_acronym)
        viewer.add_labels(
            np.swapaxes(left_region_mask, 2, 0), name="Left " + region_acronym,
        )
        viewer.add_labels(
            np.swapaxes(right_region_mask, 2, 0),
            name="Right " + region_acronym,
        )
