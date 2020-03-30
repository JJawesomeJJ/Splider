#description it is autoload modules
import importlib
def easyimport( Moudule, class_name):
    return importlib.import_module(Moudule + "." + class_name)
def loadclass(Moudule,class_name):
    return getattr(easyimport(Moudule,class_name), class_name)
def load_method(Moudule,class_name,METHOD,*args):
    class_obj=loadclass(Moudule, class_name)
    return getattr(loadclass(Moudule,class_name),METHOD)(class_obj,*args)