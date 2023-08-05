from localstack.utils.aws import aws_models
IrpmY=super
IrpmP=None
Irpmo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IrpmY(LambdaLayer,self).__init__(arn)
  self.cwd=IrpmP
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Irpmo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(RDSDatabase,self).__init__(Irpmo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(RDSCluster,self).__init__(Irpmo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(AppSyncAPI,self).__init__(Irpmo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(AmplifyApp,self).__init__(Irpmo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(ElastiCacheCluster,self).__init__(Irpmo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(TransferServer,self).__init__(Irpmo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(CloudFrontDistribution,self).__init__(Irpmo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Irpmo,env=IrpmP):
  IrpmY(CodeCommitRepository,self).__init__(Irpmo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
