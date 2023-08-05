from localstack.utils.aws import aws_models
YLNzm=super
YLNzy=None
YLNzi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YLNzm(LambdaLayer,self).__init__(arn)
  self.cwd=YLNzy
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YLNzi.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(RDSDatabase,self).__init__(YLNzi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(RDSCluster,self).__init__(YLNzi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(AppSyncAPI,self).__init__(YLNzi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(AmplifyApp,self).__init__(YLNzi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(ElastiCacheCluster,self).__init__(YLNzi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(TransferServer,self).__init__(YLNzi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(CloudFrontDistribution,self).__init__(YLNzi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YLNzi,env=YLNzy):
  YLNzm(CodeCommitRepository,self).__init__(YLNzi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
