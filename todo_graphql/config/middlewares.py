from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTMiddleware:

    # 認証が必要なリゾルバ
    protected_resolvers = ('createColumn', 'updateColumn', 'deleteColumn')

    def resolve(self, next, root, info, **kwargs):
        """
        リゾルバ実行前に呼び出される処理
        """
        # 認証が必要なもの以外はそのまま進む
        if info.field_name not in self.protected_resolvers:
            return next(root, info, **kwargs)  # 各リゾルバの呼び出し
        
        # 認証情報の確認
        req = info.context
        if 'HTTP_AUTHORIZATION' not in req.META.keys():
            raise Exception('認証情報がありません')
        
        # 認証処理
        try:
            # 返り値： (user, token)
            user_auth_tuple = JWTAuthentication().authenticate(req)
            print(user_auth_tuple)
            info.context.user = user_auth_tuple[0]
        except Exception as e:
            raise e
        return next(root, info, **kwargs)  # 各リゾルバの呼び出し
