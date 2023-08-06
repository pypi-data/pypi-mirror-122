from localstack.utils.aws import aws_models
eDlrp=super
eDlrg=None
eDlrc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  eDlrp(LambdaLayer,self).__init__(arn)
  self.cwd=eDlrg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.eDlrc.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(RDSDatabase,self).__init__(eDlrc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(RDSCluster,self).__init__(eDlrc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(AppSyncAPI,self).__init__(eDlrc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(AmplifyApp,self).__init__(eDlrc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(ElastiCacheCluster,self).__init__(eDlrc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(TransferServer,self).__init__(eDlrc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(CloudFrontDistribution,self).__init__(eDlrc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,eDlrc,env=eDlrg):
  eDlrp(CodeCommitRepository,self).__init__(eDlrc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
