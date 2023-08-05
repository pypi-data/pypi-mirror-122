"""
模拟 ORM 接口，实现简单的数据快速查询和更新。
以 MySQL 数据库为存储介质。
"""
import datetime
import traceback
from typing import List, Dict, Tuple, Union
import pandas as pd
from pandas import DataFrame
import warnings
import pymysql

warnings.filterwarnings("ignore")


class LightORM:
    """
    模拟ORM-api，简化ORM的初始化操作。
    由于是自用，面临的场景比较少，因此约定只支持下面这3中数据类型：
        varchar(255)
        int
        float(10,3)
    在将 dataframe 数据存储到数据库的时候，需要注意这一点。
    """

    def __init__(self, host: str, port: int, user: str, passwd: str, database: str = 'test'):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, database=database)
        self._table: str = ''  # query操作的表
        self._query_string = ""  # query的语句
        self._query_filter_condtions: List[str] = []  # query.filter的条件

    def __print(self, *args):
        """
        打印message
        """
        print(datetime.datetime.now(), *args)

    def execute(self, sql: str) -> int:
        """
        执行SQL，没有返回值
        """
        self.conn.ping()
        cur = self.conn.cursor()
        rowcount = cur.execute(sql)
        self.conn.commit()
        cur.close()
        return rowcount

    def executemany(self, sql: str, params: List[Tuple]) -> int:
        """
        批量执行sql，全部执行后再提交，加快速度
        """
        self.conn.ping()
        cur = self.conn.cursor()
        rowcount = cur.executemany(sql, params)
        self.conn.commit()
        cur.close()
        return rowcount

    def __convert_dtype(self, type_hint: str):
        """
        将数据类型转成本ORM支持的格式：
            varchar(255)
            int
            float(10,3)
        """
        type_hint = type_hint.lower()
        if 'str' in type_hint or 'varchar' in type_hint or 'object' in type_hint:
            return 'VARCHAR'
        elif 'int' in type_hint:
            return 'INTEGER'
        elif 'float' in type_hint or 'real' in type_hint:
            return 'FLOAT'
        else:
            raise Exception(f'不支持的数据类型{type_hint}，mysql只支持（int, float, str）这三种类型')

    def table_schema(self, table: str) -> Dict:
        """
        获取表的各个字段的数据类型，如果不存在这个表，则返回空字典
        table='df'
        sql = f"select * from {table} limit 1"
        conn = pymysql.connect(host=conf.dbhost, port=conf.dbport, user=conf.dbuser, passwd=conf.dbpasswd, database=conf.dbdb)
        data = pd.read_sql(sql, conn)
        """
        sql = f"desc {table}"
        try:
            data = self.__read_data(sql, 'DataFrame')[['Field', 'Type']]
            data = data.applymap(lambda x: str(x).strip().lower())
            schema = {}
            for k, v in data[['Field', 'Type']].values:
                schema[k] = self.__convert_dtype(v)
            return schema
        except:
            error = traceback.format_exc()
            self.__print(error)
            return {}

    def dataframe_schema(self, df: DataFrame) -> Dict[str, str]:
        """
        通过判断dataframe的数据类型，生成 sqlite3 的表结构 schema,
        用于快速根据datafram来创建对应的sqlite3表。
        """
        dtypes = df.dtypes.map(str).to_dict()
        schema = {}
        for k, v in dtypes.items():
            schema[k] = self.__convert_dtype(v)
        return schema


    def table_exists(self, table: str) -> bool:
        """
        判断表是否存在
        table='abcd'
        """
        sql = f"select 1 as cnt from {table} limit 1"
        try:
            self.__read_data(sql, 'DataFrame')
            return True
        except:
            return False

    def create_table(self, table: str, **kwargs):
        """
        创建表，并自动添加自增主键(id).
            varchar(255)
            int
            float(10,3)

        kwargs={'id': 'int', 'name': 'varchar', 'score': 'float'}
        db = DBMYSQL()
        db.create_table('abc', **kwargs)
        """
        # 将字段类型改为标准类型
        new_schema = {}
        for k, v in kwargs.items():
            new_schema[k.lower()] = self.__convert_dtype(v)
        new_schema['id'] = self.__convert_dtype('int')
        # 判断表是否存在，判断是否全部的数据类型都对的上才行
        need_create = False
        # 表不存在，则需要创建
        exist_schema = self.table_schema(table)
        for k, v in new_schema.items():
            if len(exist_schema) == 0:
                print(f"表不存在，将创建：{table}")
                need_create = True
                break
            if k not in exist_schema:
                print(f"新表的字段{k}在旧表不存在，将删除旧表并创建指定的新表")
                need_create = True
                break
            if exist_schema.get(k) != v:
                print(f"旧表的字段{k}的类型是{exist_schema.get(k)}，而新表的字段类型是{v}，表结构有变更，将删除老表并创建指定的新表")
                need_create = True
                break
        # 如果不需要场景新表，就直接返回了
        if not need_create:
            print(f"表({table})已经存在，且数据结构和指定的数据结构相同，不需要重复创建")
            return
        # 表不存在，则创建
        # 注意，所有的表都需要有一个虚拟的自增主键 id
        if 'id' in new_schema:
            new_schema.pop('id')

        # 开始创建的时候，需要指定字符串或者浮点数的精度
        # 项目需要，字符串用255长度，浮点数用 float(9,2)
        for k, v in new_schema.items():
            if v == 'VARCHAR':
                new_schema[k] = 'VARCHAR(255)'
            elif v == 'FLOAT':
                new_schema[k] = 'FLOAT(10,3)'
        column_string = ', '.join([f'{k} {v}' for k, v in new_schema.items()])

        sql = f"""create table {table} ( id int unsigned NOT NULL AUTO_INCREMENT, {column_string},PRIMARY KEY (id) )"""
        self.drop_table(table) if len(exist_schema) > 0 else 0
        self.execute(sql)
        self.__print(f"创建表:{table}:\n{sql}")

    def query(self, table: str):
        """
        创建查询体
        """
        self._table = table
        self._query_string = f"select * from {table} "
        self._query_filter_condtions = []
        return self

    def filter(self, **kwargs):
        """
        运算符列表：
        https://tortoise-orm.readthedocs.io/en/latest/query.html#filtering
        """
        for k, v in kwargs.items():
            # 判断运算符
            if '__' not in k:
                operator = '='
            elif k.endswith('__lt'):
                operator = '<'
            elif k.endswith('__lte'):
                operator = '<='
            elif k.endswith('__gt'):
                operator = '>'
            elif k.endswith('__gte'):
                operator = '>='
            elif k.endswith('__not'):
                operator = '<>'
            elif k.endswith('__in'):
                operator = 'in'
            else:
                raise Exception(f"不支持的运算符{k}")
            # 组装
            k = k.split('__')[0]
            # string类型需要单引号，其他的不需要单引号
            # in_[1,2,3] 需要转成标准的 in_(1,2,3)
            if isinstance(v, str):
                self._query_filter_condtions.append(
                    f"{k} {operator} '{v}'".replace('[', '(').replace(']', ')'))
            else:
                self._query_filter_condtions.append(f"{k} {operator} {v}".replace('[', '(').replace(']', ')'))
        return self

    def __create_query_sql(self):
        """
        在执行 .all() 或 .first() 之前，执行这一句，组装完整的SQL语句
        """
        if len(self._query_filter_condtions) > 0:
            where_sql = ' where ' + ' and '.join(self._query_filter_condtions)
        else:
            where_sql = ''
        sql = self._query_string + where_sql
        return sql

    def first(self) -> Dict:
        """查询第一行"""
        sql = self.__create_query_sql() + ' limit 1'
        data = self.__read_data(sql, 'records')
        return {} if len(data) == 0 else data[0]

    def all(self) -> List[Dict]:
        """
        查询所有行
        """
        sql = self.__create_query_sql()
        return self.__read_data(sql, 'records')

    def all_to_df(self) -> DataFrame:
        """
        self.all()方法返回的是list-dict格式，如果查询结果为空，就是空的list。
        在外部函数，如果尝试将空的list传参datafram，此时datafram就是没有列名的datafarame，容易导致程序报错。
        所以这里，尝试返回dataframe类型的结果，这样及时为空，也能保持正确的表结构。
        """
        sql = self.__create_query_sql()
        return self.__read_data(sql, 'DataFrame')

    def delete(self, ids: List[int]) -> int:
        """
        删除数据，一定是通过id主键来快速删除
        """
        table = self._table
        ids2 = [tuple([_id]) for _id in ids]
        sql = f"delete from {table} where id = %s"
        rowcount = self.executemany(sql, ids2)
        self.__print(f"删除 {rowcount} 条数据")
        return rowcount

    def __read_data(self, sql: str, dtype: str = 'DataFrame') -> Union[DataFrame, List[Dict]]:
        """
        从数据库读取数据
        dtype的取值：
        DataFrame，返回dataframe类型
        records，返回 list[dict]类型
        """
        self.conn.ping()
        if dtype == 'DataFrame':
            return pd.read_sql(sql, self.conn)
        elif dtype == 'records':
            return pd.read_sql(sql, self.conn).to_dict(orient='records')

    def drop_table(self, table: str):
        """
        删除表
        table='abc'
        sql = f"drop table {table}"
        conn = pymysql.connect(host=conf.dbhost, port=conf.dbport, user=conf.dbuser, passwd=conf.dbpasswd, database=conf.dbdb)
        cur = conn.cursor()
        cur.execute(sql)

        """
        sql = f"""drop table {table}"""
        schema = self.table_schema(table)
        if schema:
            self.execute(sql)
            print(f"删除表成功：{table}")
        else:
            print(f"表不存在，不需要执行删表操作：{table}")

    def __convert_data(self, row: Dict, schema: Dict):
        """
        在将数据插入数据库或者更新数据库之前，需要对数据类型进行判断,
        即：执行严格的数据类型检查
        """
        for col in row.keys():
            data_type = self.__convert_dtype(str(type(row.get(col))))  # 外部传入的数据类型
            except_type = schema.get(col)
            if except_type == 'FLOAT' and data_type == 'INTEGER':  # 如果传入的是int，而期待的float，此时可以直接转换，反之不行
                row[col] = float(row[col])
                continue
            if except_type == 'VARCHAR' and data_type != 'VARCHAR':  # 如果传入的是int，而期待的str，此时可以直接转换，反之不行
                row[col] = str(row[col])
                continue
            if except_type != data_type:
                raise Exception(f"数据类型不匹配，字段：{col} 传入的数据类想是：{data_type}，而期待的类型是：{except_type}，请检查")
        # 返回处理后的新数据
        return row

    def insert(self, data: List[Dict]) -> int:
        """
        插入数据.
        因此，这里在插入数据之前，对数据进行检查，防止插入的数据类型不正确，导致外部程序在其他位置的运行错误。
        """
        if len(data) == 0:
            return 0

        cols = list(data[0].keys())
        # 类型检查
        table = self._table
        schema = self.table_schema(table)
        for i in range(len(data)):
            row = data[i]
            data[i] = self.__convert_data(row, schema)
        # 数据插入到表中
        params = [tuple([d.get(k) for k in cols]) for d in data]  # 按字段顺序排序，非常重要
        placeholder1 = ', '.join(cols)
        placeholder2 = ', '.join(['%s' for _ in cols])
        sql = f""" insert into {table} ({placeholder1}) values ({placeholder2}) """
        rowcount = self.executemany(sql, params)
        print(f"插入{rowcount}条记录")
        return rowcount

    def update(self, data: List[Dict]) -> int:
        """
        更新记录，要求数据的每个dict都要有 _id 字段
        """
        if len(data) == 0:
            return 0

        for d in data:
            if 'id' not in d:
                raise Exception("在更新数据时，需要指定具体的id值，请检查data")

        # 数据类型检查
        cols = list(data[0].keys())
        cols.remove('id') if 'id' in cols else 0
        table = self._table
        schema = self.table_schema(table)
        for i in range(len(data)):
            row = data[i]
            data[i] = self.__convert_data(row, schema)
        #
        # 注意，警告：_id 列一定要放在最后一个位置
        cols = [c for c in data[0].keys() if c != 'id'] + ['id']
        params = [tuple([d.get(k) for k in cols]) for d in data]
        placeholder1 = ', '.join([f'{c}=%s' for c in cols[:-1]])
        # 批量更新
        sql = f"update {table} set {placeholder1} where id=%s"
        rowcount = self.executemany(sql, params)
        print(f"更新{rowcount}条记录")
        return rowcount

    def recreate_index(self, max_pkid=10000000):
        """
        当自增主键太大太大，就容易出问题，所以这里需要自动检查并处理这个问题。
        方法很简单，就是检查自增主键是否超过9kw,如果超过，就删除表并重建表结构
        """
        table = self._table
        # 如果表不存在，则不用处理
        if not self.table_exists(table):
            print("表不存在，不需要重建表")
            return
        # 查看最大id
        # 如果表没有数据，或者 _id 比较小，就不去处理了
        sql = f"select max(id) as max_id from {table}"
        data = self.__read_data(sql, 'DataFrame')
        if len(data) == 0:
            print("表没有数据，不需要重建表")
            return
        max_id = data['max_id'].iloc[0]
        if max_id <= max_pkid:
            print(f"当前的最大id是{max_id}<{max_pkid},不需要重建表")
        # 不满足上面的情况，就需要重建表了
        print(f"表{table}的自增主键id的值{max_id}已经超过{max_pkid}，此处尝试创建表，使得主键id再次从0开始")
        # 先把所有的数据都读取出来
        sql = f"select * from {table}"
        data = self.__read_data(sql, 'DataFrame')
        del data['id']
        #
        # 创建表sql
        schema = self.table_schema(table)
        if 'id' in schema:
            schema.pop('id')
        # 先删表再建表
        print(f"开始删除表:{table}")
        self.drop_table(table)
        self.create_table(table, **schema)
        print(f"完成重建表：{table}")
        # 导入数据
        data = data.to_dict(orient='records')
        rowcount = self.query(table).insert(data)
        print(f"完成将之前的数据导入到新表，数据：{rowcount}")




def test_db():
    # 实例化
    dbfile = '/Users/10015535/Downloads/sqlite3.db'
    db = LightORM()

    # 测试删除表
    db.drop_table('abc')
    db.drop_table('abcd')

    # 创建表：1定义表结构 2创建表
    schema = {'from_warehouse_id': 'int',
              'to_warehouse_id': 'int',
              'business_type': 'int',
              'time': 'str',
              'time_idx': 'int',
              'pred_box_count': 'int',
              'pred_plate_count': 'float'}

    db.create_table('abc', **schema)

    # 获取表结构
    db.table_schema('abc')

    # 修改数据类型，测试是否会重建表
    schema['pred_plate_count'] = 'int'
    db.create_table('abc', **schema)

    # 测试：根据dataframe来创建表

    df = pd.DataFrame({
        'a': [1, 2, 3, 4, 5],
        'b': ['a', 'b', 'c', 'd', 'e'],
        'c': [str(d)[:10] for d in pd.date_range(start='2021-01-01', periods=5)],
        'g': ['a', 'a', 'b', 'b', 'b']
    })
    schema = db.dataframe_schema(df)
    db.create_table('df', **schema)
    db.table_schema('df')
    db.drop_table('df')
    # 插入数据
    data = df.to_dict(orient='records')
    db.query('df').insert(data)

    # 查询数据
    rows = db.query('df').all()
    rows = db.query('df').filter(a__gte=2).all()
    df = db.query('df').all_to_df()

    # 删除数据
    ids = [r.get('id') for r in rows]
    db.query('df').delete(ids)

    # 更新
    row = db.query('df').first()
    row['c'] = '123'
    db.query('df').update([row])

    # 重做索引
    # 插入很多数据，然后测试重建表索引
    #
    del df['id']
    data = df.to_dict(orient='records')
    for i in range(10):
        db.query('df').insert(data)
    # 1、先删除小于 id<=20 的记录
    rows = db.query('df').filter(id__lte=20).all()
    ids = [r.get('id') for r in rows]
    db.query('df').delete(ids)

    # 2、重做索引
    db.query('df').recreate_index(max_pkid=20)

    # 3、查看重做后的做引
    db.query('df').all_to_df()
