"""

Utilities for attaching weak lensing observables from maps to weighted number counts retrieved from
the milennium simulation

"""


from pathlib import Path
import heinlein
import lenskappa
import pandas as pd
from itertools import product
import numpy as np
import astropy.units as u
import multiprocessing as mp
from functools import partial

def attach_wlm(wnc_path: Path, redshift: float, wlm_path: Path = None, inplace=True, threads = 1,*args, **kwargs):
    """
    Arguments:
    
    wnc_path: Path to the weighted number counts files. No particular filename is necessar, we just 
    expect somewhere in the name to find the tuple that tells us which field it is from
    
    redshift: Redshift cutoff used when computing weighted number counts

    wlm_path (optional): Path to the location of the weak lensing maps. If not provided,
    will look for them in heinlein

    inplace (optional): Whether or not to modify the weighte number count files in place. 
    If true, will add columns to the files. If false, will create new files.
    
    """
    if wlm_path is None:
        p = heinlein.get_path("ms", "wl_maps")
        if p is None:
            raise FileNotFoundError("No path found for weak lensing maps")
        wlm_path = p
    
    main_path = Path(lenskappa.__file__).parents[0]
    ms_distances_path = main_path / "datasets" / "surveys" / "ms" / "Millennium_distances.txt"
    ms_distances = pd.read_csv(ms_distances_path, delim_whitespace=True)
    ms_redshifts = ms_distances["Redshift"]
    closest_above = ms_redshifts[ms_redshifts > redshift].min()
    closest_below = ms_redshifts[ms_redshifts < redshift].max()

    if abs((redshift - closest_above) / redshift) <= 0.05:
        plane_redshift = closest_above

    elif abs((redshift - closest_below) / redshift) < 0.05:
        plane_redshift = closest_below

    while True:
        print(f"The closest redshift planes to z = {redshift} are z = {closest_above} and z = {closest_below}")
        print(f"Would you like to use one of these, or average the planes?")
        choice = input(f"Closest (A)bove ({closest_above}), closest (B)elow ({closest_below}), or avera(G)e: ").upper()
        if choice not in ["A", "B", "G"]:
            print("Invalid input")
            continue
        if choice == "A":
            plane_redshift = [closest_above]
        elif choice == "B":
            plane_redshift = [closest_below]
        elif choice == "G":
            plane_redshift = [closest_above, closest_below]
        break
    
    plane_numbers = ms_distances["PlaneNumber"][ms_redshifts.isin(plane_redshift)]
    field_labels = list(range(8))
    field_labels = list(product(field_labels, field_labels))

    wnc_files = [f for f in wnc_path.glob("*.csv")]
    f_ = partial(load_single_field, wnc_files = wnc_files, plane_numbers = plane_numbers, wlm_path = wlm_path, inplace = inplace)
    with mp.Pool(threads) as p:
        wnc_dfs = p.map(f_, field_labels)
    return pd.concat(wnc_dfs)

def load_single_field(field, wnc_files, plane_numbers, wlm_path, inplace=True):
        print(f"Working on field {field}")
        wnc_file = [f for f in wnc_files if f"{field[0]}_{field[1]}" in f.name]
        if len(wnc_file) != 1:
            print(f"Unable to find a uniuqe set of weighted number counts for field {field}")
            exit()
        wnc_data = pd.read_csv(wnc_file[0])
        wl_data = load_field_wlm(field, plane_numbers, wlm_path)
        coords = list(zip(wnc_data["ra"], wnc_data["dec"]))
        indices = [get_index_from_position(*c) for c in coords]
        index_arrays = tuple(map(list, zip(*indices)))
        kappa_total = np.sum([d['kappa'] for d in wl_data.values()], axis = 0) / len(wl_data)
        gamma_total = np.sum([d['gamma'] for d in wl_data.values()], axis = 0) / len(wl_data)
        kappas = kappa_total[index_arrays[0], index_arrays[1]]
        gammas = gamma_total[index_arrays[0], index_arrays[1]]

        wnc_data["kappa"] = kappas
        wnc_data["gamma"] = gammas
        if inplace:
            wnc_data.to_csv(wnc_file[0], index=False)
        else:
            output_fname = wnc_file[0].stem + "_with_kg.csv"
            output_path = wnc_file[0].parents[0] / output_fname
            wnc_data.to_csv(output_path, index=True)

        return wnc_data

def load_field_wlm(field_label, plane_numbers, wlm_path):
    possible_filetypes = [".kappa", ".gamma_1", ".gamma_2", ".Phi"]
    searchname = "*N_4096_ang_4_rays_to_plane_29_f.*"
    files = [f for f in wlm_path.glob(searchname) if f.suffix in possible_filetypes]
    data = {}
    if not files:

        dirs = [path for path in wlm_path.glob("*") if path.is_dir()]
        dirnames = [path.name for path in dirs]
        if all(k in dirnames for k in ["kappa", "gamma"]):
            kappa = load_kappa(field_label, wlm_path / "kappa")
            gamma = load_gamma(field_label, wlm_path / "gamma")
            return {"kappa": kappa, "gamma": gamma}
        elif all([any([str(pn) in name for name in dirnames]) for pn in plane_numbers]):
            #Found a directory for all the requested planes
            for pn in plane_numbers:
                plane_dir = [d for d in dirs if str(pn) in d.name]
                if len(plane_dir) != 1:
                    print("OOPS!")
                    exit()
                data.update({pn: load_field_wlm(field_label, [pn], plane_dir[0])})
            return data
        else:
            print("Unable to understand structure of weak lensing map directory")
            exit()

def load_kappa(field_label, path):
    basename = f"GGL_los_8_{field_label[0]}_{field_label[1]}_N_4096_ang_4_rays_to_plane"
    files = [file for file in path.glob("*.kappa") if basename in file.stem]
    if len(files) != 1:
        print(f"Found wrong number of files for kappa map for field {field_label}")
        exit()

    kf = files[0]
    kappa =  np.fromfile(kf, np.float32).reshape((4096, 4096))
    return kappa

def load_gamma(field_label, path):
    basename = f"GGL_los_8_{field_label[0]}_{field_label[1]}_N_4096_ang_4_rays_to_plane"

    gamma1_files = [file for file in path.glob("*.gamma_1") if basename in file.stem]
    gamma2_files = [file for file in path.glob("*.gamma_2") if basename in file.stem]
    if len(gamma1_files) != 1 or len(gamma2_files) != 1:
        print(gamma1_files)
        print(gamma2)
        print(f"Found wrong number of gamma files for field {field_label}")
        exit()
    gamma1 = np.fromfile(gamma1_files[0], np.float32).reshape((4096, 4096))
    gamma2 = np.fromfile(gamma2_files[0], np.float32).reshape((4096, 4096))
    return np.sqrt(gamma1**2 + gamma2**2)


def get_index_from_position(pos_x, pos_y):
    """
    Returns the index of the nearest grid point given an angular position.
    
    """

    if pos_x > 2:
        pos_x = pos_x - 360
    pos_x = pos_x*u.deg
    pos_y = pos_y*u.deg

    l_field = (4.0*u.degree)
    n_pix = 4096.0
    l_pix = l_field/n_pix

    x_pix = (pos_x + 2.0*u.deg)/l_pix - 0.5
    y_pix = (pos_y + 2.0*u.deg)/l_pix - 0.5
    return int(round(x_pix.value)), int(round(y_pix.value))
