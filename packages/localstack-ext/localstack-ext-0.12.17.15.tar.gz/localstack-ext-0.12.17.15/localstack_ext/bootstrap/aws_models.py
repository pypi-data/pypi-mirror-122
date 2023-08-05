from localstack.utils.aws import aws_models
SMlTx=super
SMlTY=None
SMlTR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  SMlTx(LambdaLayer,self).__init__(arn)
  self.cwd=SMlTY
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.SMlTR.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(RDSDatabase,self).__init__(SMlTR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(RDSCluster,self).__init__(SMlTR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(AppSyncAPI,self).__init__(SMlTR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(AmplifyApp,self).__init__(SMlTR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(ElastiCacheCluster,self).__init__(SMlTR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(TransferServer,self).__init__(SMlTR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(CloudFrontDistribution,self).__init__(SMlTR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,SMlTR,env=SMlTY):
  SMlTx(CodeCommitRepository,self).__init__(SMlTR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
