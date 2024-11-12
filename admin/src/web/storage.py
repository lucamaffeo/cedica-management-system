from minio import Minio

class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        minio_server = app.config.get('MINIO_SERVER')
        access_key = app.config.get('MINIO_ACCESS_KEY')
        secret_key = app.config.get('MINIO_SECRET_KEY')
        secure = app.config.get('MINIO_SECURE', False)

        if not all([minio_server, access_key, secret_key]):
            raise ValueError('Minio configuration missing.')

        self._client = Minio(minio_server, access_key=access_key, secret_key=secret_key, secure=secure)

        app.storage = self

        return app

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def delete_file(self, bucket_name, file_path):
        if not self._client:
            raise ValueError("Minio client not initialized")
        self._client.remove_object(bucket_name, file_path)

storage = Storage()
