from imlib.plotting.colors import get_random_vtkplotter_color


def load_obj_into_brainrender(
    scene,
    obj_file,
    color=None,
    alpha=0.8,
    shading="phong",
    flag=False,
    name=None,
):
    """
    Loads a single obj file into brainrender
    :param scene: brainrender scene
    :param obj_file: obj filepath
    :param color: Object color. If None, a random color is chosen
    :param alpha: Object transparency
    :param shading: Object shading type ("flat", "giroud" or "phong").
    Defaults to "phong"
    """
    obj_file = str(obj_file)
    if color is None:
        color = get_random_vtkplotter_color()
    act = scene.add_from_file(obj_file, c=color, alpha=alpha)

    if shading == "flat":
        act.GetProperty().SetInterpolationToFlat()
    elif shading == "gouraud":
        act.GetProperty().SetInterpolationToGouraud()
    else:
        act.GetProperty().SetInterpolationToPhong()

    if name is not None:
        if flag:
            act.flag(name)
