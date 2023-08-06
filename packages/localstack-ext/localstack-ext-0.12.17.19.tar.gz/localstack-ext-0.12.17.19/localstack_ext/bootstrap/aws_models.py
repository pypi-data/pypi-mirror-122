from localstack.utils.aws import aws_models
EJACu=super
EJACm=None
EJACt=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EJACu(LambdaLayer,self).__init__(arn)
  self.cwd=EJACm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EJACt.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(RDSDatabase,self).__init__(EJACt,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(RDSCluster,self).__init__(EJACt,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(AppSyncAPI,self).__init__(EJACt,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(AmplifyApp,self).__init__(EJACt,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(ElastiCacheCluster,self).__init__(EJACt,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(TransferServer,self).__init__(EJACt,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(CloudFrontDistribution,self).__init__(EJACt,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EJACt,env=EJACm):
  EJACu(CodeCommitRepository,self).__init__(EJACt,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
