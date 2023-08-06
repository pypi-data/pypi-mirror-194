import pymongo


class UnableConnectServerException(Exception):
    """
    몽고 서버 연결 에러를 처리하기 위한 커스텀 익셉션
    """
    pass


def connect_mongo(addr: str, timeout=5) -> pymongo.MongoClient:
    """
    몽고 클라이언트를 만들어주는 함수.
    필요할 때마다 클라이언트를 생성하는 것보다 클라이언트 한개로 데이터베이스를 다루는게 효율적이라 함수를 따로 뺐음.
    resolve conn error - https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
    :param addr:
    :param timeout:
    :return:
    """
    import certifi
    ca = certifi.where()
    if addr.startswith('mongodb://'):
        # set a some-second connection timeout
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000)
    elif addr.startswith('mongodb+srv://'):
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000, tlsCAFile=ca)
    else:
        raise Exception(f"Invalid address: {addr}")
    try:
        srv_info = client.server_info()
        conn_str = f"Connect to Mongo Atlas v{srv_info['version']}..."
        print(conn_str, f"Server Addr : {addr}")
        return client
    except:
        raise UnableConnectServerException()