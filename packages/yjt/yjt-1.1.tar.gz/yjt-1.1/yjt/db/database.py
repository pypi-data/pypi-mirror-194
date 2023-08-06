# -*-coding:utf-8 -*-

"""
# Time       ：2022/10/1 07:32
# Author     ：AMU
# Description：
"""
import threading
from contextlib import contextmanager

import cx_Oracle
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


# 数据库连接配置(conf)格式
# DB_CONF = {
#     'id': 'mysql_aabbcc',  # 标识, 应与 配置 key 相同
#     'driver': 'mysql+pymysql',
#     'username': 'root',
#     'password': '123456',
#     'host': '127.0.0.1',
#     'port': 3306,
#     'database': 'test',
#     'pool': {
#         # 不设置连接池参数则不使用连接池
#         'size': 10,  # 连接数
#         'overflow': 0,  # 超过连接池大小外最多创建的连接
#         'timeout': 10,  # 池中没有线程最多等待的时间
#         'recycle': 600  # 多久之后对线程池中的线程进行一次连接的回收（重置） -1
#     }
# }

# 取得 url
def _get_url(conf):
    if 'oracle' in conf.get('driver'):
        # 方法一: 支持ipv6
        # 使用ipv6时 host 配置项不需要加 [] ,但手拼字符串需要添加 []
        if 'sid' in conf:
            return URL(
                conf.get('driver'),
                username=conf.get('username'),
                password=conf.get('password'),
                host=conf.get('host'),
                port=conf.get('port'),

                # oracle+cx_oracle://YJDAILYDB:yj_DailySyS@223.85.223.128:1521/xe
                database=conf.get('sid'),

                # oracle+cx_oracle://YJDAILYDB:yj_DailySyS@223.85.223.128:1521?service_name=xe
                # query={'service_name': CONNECTIONS[name]['service_name']}
            )
        else:
            return URL(
                conf.get('driver'),
                username=conf.get('username'),
                password=conf.get('password'),
                host=conf.get('host'),
                port=conf.get('port'),

                # oracle+cx_oracle://YJDAILYDB:yj_DailySyS@223.85.223.128:1521/xe
                # database=conf.get('sid'),

                # oracle+cx_oracle://YJDAILYDB:yj_DailySyS@223.85.223.128:1521?service_name=xe
                query={'service_name': conf.get('service_name')}
            )

        # 方法二: 不支持ipv6
        # if 'sid' in conf:
        #     dsn = cx_Oracle.makedsn(
        #         conf.get('host'),
        #         conf.get('port'),
        #         sid=conf.get('sid'),
        #     )
        # else:
        #     dsn = cx_Oracle.makedsn(
        #         conf.get('host'),
        #         conf.get('port'),
        #         service_name=conf.get('service_name'),
        #     )
        # return "%s://%s:%s@%s" % (conf.get('driver'), conf.get('username'), conf.get('password'), dsn)

    else:
        return URL.create(
            drivername=conf.get('driver'),
            username=conf.get('username'),
            password=conf.get('password'),
            host=conf.get('host'),
            port=conf.get('port'),
            database=conf.get('database')
        )


# 存储所有引擎
_engines = {}
_lock = threading.Lock()


# 取得 engine
def _get_engine(conf):
    _lock.acquire()
    if conf.get('id') not in _engines:
        # print('配置标识与进程ID', conf.get('id'), os.getpid())
        if 'sqlite' in conf.get('driver'):
            # sqlite
            _engines[conf.get('id')] = create_engine(
                _get_url(conf),
                echo=False,  # 输出日志
                poolclass=NullPool,
                encoding='UTF-8',
                connect_args={'check_same_thread': False}  # 允许多线程
            )
        else:
            # mysql | oracle
            if conf.get('pool'):
                _engines[conf.get('id')] = create_engine(
                    _get_url(conf),
                    pool_size=conf.get('pool').get('size'),
                    max_overflow=conf.get('pool').get('overflow'),
                    pool_timeout=conf.get('pool').get('timeout'),
                    pool_recycle=conf.get('pool').get('recycle'),
                    pool_pre_ping=True,
                    encoding='UTF-8',
                )
            else:
                _engines[conf.get('id')] = create_engine(
                    _get_url(conf),
                    poolclass=NullPool,
                    encoding='UTF-8',
                )
    _lock.release()

    return _engines[conf.get('id')]


# 取得 sessionmaker
def get_sessionmaker(conf):
    engine = _get_engine(conf)
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


class GetDependsSessions:
    """
    为fastapi注入返回数据库连接

    * 使用方法(方法使用 async 时需要手动 close 连接，防止并发出问题)

    @router.api_route(
        path='/depends_sessions',
        methods=['GET'],
        summary='数据库连接装饰器',
    )
    def test_decorator(
        request: Request,
        db_mysql:sqlalchemy.orm.session.Session = Depends(core.lib.database.GetDependsSessions(conf1)),
        db_oracle:sqlalchemy.orm.session.Session = Depends(core.lib.database.GetDependsSessions(conf2)),
    ):
        res1 = db_mysql.execute("select * from table").fetchall()
        res2 = db_oracle.execute("select * from table").fetchall()
    """

    def __init__(self, *args):
        for v in args:
            self.db_conf = v
            break

    def __call__(self) -> sqlalchemy.orm.session.Session:
        db = get_sessionmaker(self.db_conf)()
        try:
            yield db
        except Exception as e:
            # print('db session except:', db)
            db.rollback()
            raise e
        finally:
            if db:
                # print('db session close:', db)
                db.close()


@contextmanager  # 装饰器形式的上下文管理器
def get_with_session(conf: dict = None) -> sqlalchemy.orm.session.Session:
    """
    取得 session

    :param conf:
    :return:

    * 使用方法自动关闭连接
    * 使用上下文管理器对session和事务操作进行封装

    with core.lib.database.get_with_session(conf) as db:
        try:
            db.execute(sql)
        except BaseException as be:
            print(str(be))

    """
    db = get_sessionmaker(conf)()
    try:
        # print('session open:', db)
        yield db
    except Exception as e:
        # print('session except:', db)
        db.rollback()
        raise e
    finally:
        if db:
            # print('session close:', db)
            db.close()


def get_func_session(conf: dict, parameter_name: str = 'db'):
    """
    为普通函数装饰器返回数据库连接(自动关闭连接)

    :param conf: 数据库配置
    :param parameter_name: 对应方法参数名称
    :return:

    * 使用方法:

    @core.lib.database.get_func_session(conf1, "db_mysql")
    @core.lib.database.get_func_session(conf2, "db_oracle")
    def test(
        string: str,
        db_mysql:sqlalchemy.orm.session.Session = None,
        db_oracle:sqlalchemy.orm.session.Session = None
    ):
        res1 = db_mysql.execute("select * from table").fetchall()
        res2 = db_oracle.execute("select * from table").fetchall()

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # print('**kwargs', kwargs)
            with get_with_session(conf) as s:
                # if parameter_name in kwargs.keys():
                #     kwargs[parameter_name][conf.get('id')]: sqlalchemy.orm.session.Session = s
                # else:
                #     kwargs[parameter_name]: Dict[str, sqlalchemy.orm.session.Session] = {conf.get('id'): s}
                kwargs[parameter_name]: sqlalchemy.orm.session.Session = s
                # 直接返回
                return func(*args, **kwargs)

        return wrapper

    return decorator


# 直接取出数据
# db_res = db.execute(sql_str, sql_params).fetchall()
# db_raw = core.lib.utils_dbs.row_to_dict(db_res) # 将数据转为字典


# pandas取出数据
# db_res = db.execute(sql_str, sql_params)
# db_raw = pd.DataFrame(data=db_res.fetchall(), columns=db_res.keys())
# db_raw['calc_day_time'] = db_raw['day_id'].apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:])
# db_raw = db_raw.to_dict(orient='records') # 将pandas转字典输出


# 将字典载入pandas
# db_raw = pd.DataFrame(db_raw)
# db_raw['calc_day_time'] = db_raw['day_id'].apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:])
# db_raw = db_raw.to_dict(orient='records') # 将pandas转字典输出


# pandas直接取出数据
# exp.1
# engine = core.database.get_engine('oracle_jk')  # 取得引擎
# pd_res = pd.read_sql(sql='select * from user_base where ub_login_name=:name', params={'name':'su'}, con=engine)
# exp.2
# pd_res = pd.read_sql(sql='select * from user_base', params={}, con=db_session.get_bind())


__all__ = ["get_sessionmaker", "GetDependsSessions", "get_with_session", "get_func_session"]
