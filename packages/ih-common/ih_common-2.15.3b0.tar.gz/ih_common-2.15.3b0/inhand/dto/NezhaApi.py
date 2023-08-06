import uuid

class ApiInfo:
    def __init__(self,path,method,scope=None):
        self.path=path
        self.method=method
        self.scope=scope
        suid = str(uuid.uuid4())
        self.uid= ''.join(suid.split("-"))

    def createApiEntry(self,prefix):
        api_prefix = '{}.http.routers.{}'.format(prefix, self.uid)
        if self.scope is not None:
            tags=[]
            tags.append("{}.rule=Path(`{}`) && Method(`{}`)".format(api_prefix, self.path, self.method))
            if '' != self.scope:
                tags.append("{}.metadata.nezha.scopes={}".format(api_prefix,self.scope))
                tags.append("{}.middlewares=nezha@internal`)".format(api_prefix))
                return tags
            else:
                return []

    @staticmethod
    def parseApiController(file):
        #ToDo: 读取fast api 中controller，解析得到ApiInfo的集合
        pass