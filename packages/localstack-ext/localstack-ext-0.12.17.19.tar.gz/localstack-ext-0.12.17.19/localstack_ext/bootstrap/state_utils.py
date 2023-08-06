import logging
Ulgte=bool
UlgtR=hasattr
Ulgty=set
UlgtO=True
Ulgtj=False
UlgtA=isinstance
UlgtB=dict
Ulgtz=getattr
Ulgta=None
Ulgtc=str
Ulgtd=Exception
UlgtC=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[Ulgte,Set]:
 if UlgtR(obj,"__dict__"):
  visited=visited or Ulgty()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return UlgtO,visited
  visited.add(wrapper)
 return Ulgtj,visited
def get_object_dict(obj):
 if UlgtA(obj,UlgtB):
  return obj
 obj_dict=Ulgtz(obj,"__dict__",Ulgta)
 return obj_dict
def is_composite_type(obj):
 return UlgtA(obj,(UlgtB,OrderedDict))or UlgtR(obj,"__dict__")
def api_states_traverse(api_states_path:Ulgtc,side_effect:Callable[...,Ulgta],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except Ulgtd as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 with UlgtC(state_file,"rb")as f:
  try:
   return dill.loads(f.read())
  except Ulgtd as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
