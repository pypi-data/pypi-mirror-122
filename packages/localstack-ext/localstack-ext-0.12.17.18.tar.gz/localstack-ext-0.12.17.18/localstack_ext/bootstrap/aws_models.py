from localstack.utils.aws import aws_models
TciKj=super
TciKn=None
TciKq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TciKj(LambdaLayer,self).__init__(arn)
  self.cwd=TciKn
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TciKq.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(RDSDatabase,self).__init__(TciKq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(RDSCluster,self).__init__(TciKq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(AppSyncAPI,self).__init__(TciKq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(AmplifyApp,self).__init__(TciKq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(ElastiCacheCluster,self).__init__(TciKq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(TransferServer,self).__init__(TciKq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(CloudFrontDistribution,self).__init__(TciKq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TciKq,env=TciKn):
  TciKj(CodeCommitRepository,self).__init__(TciKq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
