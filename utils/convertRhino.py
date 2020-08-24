import ghpythonlib.treehelpers as th
import Rhino


class ToRhino ():

    def __init__(self):
        pass


layerTree = [list() for _ in layernames]

for i in range(len(layernames)):
    objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layernames[i])

    if objs:
        geoms = [obj.Geometry for obj in objs]
        layerTree[i].extend(geoms)

layerTree = th.list_to_tree(layerTree, source=[0,0])
a = layerTree
