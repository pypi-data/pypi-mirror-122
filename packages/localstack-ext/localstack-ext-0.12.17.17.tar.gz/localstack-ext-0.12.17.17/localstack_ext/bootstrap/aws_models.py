from localstack.utils.aws import aws_models
uYwES=super
uYwEc=None
uYwEB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  uYwES(LambdaLayer,self).__init__(arn)
  self.cwd=uYwEc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.uYwEB.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(RDSDatabase,self).__init__(uYwEB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(RDSCluster,self).__init__(uYwEB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(AppSyncAPI,self).__init__(uYwEB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(AmplifyApp,self).__init__(uYwEB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(ElastiCacheCluster,self).__init__(uYwEB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(TransferServer,self).__init__(uYwEB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(CloudFrontDistribution,self).__init__(uYwEB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,uYwEB,env=uYwEc):
  uYwES(CodeCommitRepository,self).__init__(uYwEB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
