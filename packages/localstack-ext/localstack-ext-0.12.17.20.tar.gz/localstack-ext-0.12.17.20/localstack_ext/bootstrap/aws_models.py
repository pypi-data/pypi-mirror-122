from localstack.utils.aws import aws_models
lRiOL=super
lRiOE=None
lRiOF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lRiOL(LambdaLayer,self).__init__(arn)
  self.cwd=lRiOE
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lRiOF.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(RDSDatabase,self).__init__(lRiOF,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(RDSCluster,self).__init__(lRiOF,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(AppSyncAPI,self).__init__(lRiOF,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(AmplifyApp,self).__init__(lRiOF,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(ElastiCacheCluster,self).__init__(lRiOF,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(TransferServer,self).__init__(lRiOF,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(CloudFrontDistribution,self).__init__(lRiOF,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lRiOF,env=lRiOE):
  lRiOL(CodeCommitRepository,self).__init__(lRiOF,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
