from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTMiddleware:
    protected_resolvers = ('createDiary', 'updateDiary', 'deleteDiary')

    def resolve(self, next, root, info, **kwargs):
        """
        quey と mutation のリゾルバ呼び出しの前処理
        """
        if info.field_name not in self.protected_resolvers:
            return next(root, info, **kwargs)
        
        req = info.context
        if 'HTTP_AUTHORIZATION' not in req.META.keys():
            raise Exception('認証情報がありません')
        
        try:
            user_auth_tuple = JWTAuthentication().authenticate(req)
            info.context.user = user_auth_tuple[0]
        except Exception as e:
            raise e
        
        return next(root, info, **kwargs)
