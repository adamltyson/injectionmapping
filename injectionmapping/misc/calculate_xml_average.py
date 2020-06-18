import pandas as pd
import numpy as np
from glob import glob
from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from tqdm import tqdm
from imlib.IO.cells import get_cells
from imlib.cells.cells import Cell


def parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        dest="directory",
        type=str,
        help="Directory containing cellfinder xml files",
    )

    parser.add_argument(
        "--all",
        dest="all",
        action="store_true",
        help="Use all positions in the cell file, not just the 'cells' (type 2)",
    )
    return parser


def main(
    pixel_size_x=10, pixel_size_y=10, pixel_size_z=10, max_z=13200,
):
    args = parser().parse_args()
    print(
        f"Calculating centroid positions for cells in: {Path(args.directory).stem}"
    )
    if args.all:
        print("Including all cell positions")
    else:
        print(f"Only including cell positions of type: {Cell.CELL}")
    xml_files = glob(args.directory + "/*.xml")
    results = []
    for xml_file in xml_files:
        print(f"Processing: {Path(xml_file).stem}")
        cells = get_cells(xml_file)
        positions = []
        for cell in tqdm(cells):
            if args.all or (cell.type == Cell.CELL):
                positions.append([cell.x, cell.y, cell.z])
        if positions:  # only if cells included
            positions = np.array(positions)
            means = positions.mean(axis=0)
            results.append([Path(xml_file).stem] + means.tolist())

    df = pd.DataFrame(results)
    df.columns = ["file", "x_center_um", "y_center_um", "z_center_um"]
    df["x_center_um"] = df["x_center_um"] * pixel_size_x
    df["y_center_um"] = df["y_center_um"] * pixel_size_y
    df["z_center_um"] = df["z_center_um"] * pixel_size_z
    # df["z"] = max_z - cells["z"]
    filename = Path(args.directory) / "summary.csv"
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    main()
