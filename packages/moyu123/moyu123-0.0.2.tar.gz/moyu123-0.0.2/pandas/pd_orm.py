"""
pandas dataframe 的快捷操作

source_df: 更新数据的来源
target_df：更新数据的去处
on：left join 的关联条件
source_col：源表的字段名



"""
from typing import List

import pandas as pd
from pandas import DataFrame


class PDORM:
    def __init__(self):
        self.left_df: DataFrame = DataFrame()
        self.right_df: DataFrame = DataFrame()
        self.__filter_string = ""  # 将条件拼接转换成pandas.query能识别的格式
        self.__left_join_on_cols = []  # 左右表关联的条件字段

    def query(self, data: DataFrame):
        """
        重置关联查询条件
        """
        self.left_df = data
        self.__filter_string = ""
        self.__left_join_on_cols = []
        return self

    def filter(self, **kwargs):
        """
        模拟orm的逻辑操作，不支持复杂的 in，not in 操作
        """
        filter_string = self.__filter_string
        for k, v in kwargs.items():
            if '__' not in k:
                operator = '=='
            elif k.endswith('__lt'):
                operator = '<'
            elif k.endswith('__lte'):
                operator = '<='
            elif k.endswith('__gt'):
                operator = '>'
            elif k.endswith('__gte'):
                operator = '>='
            elif k.endswith('__not'):
                operator = '!='
            else:
                raise Exception(f"不支持的运算符{k}")
            k = k.split('__')[0]
            if isinstance(v, str):
                if "'" in v:
                    raise Exception(f'值不应该包含单引号，请检查：{v}')
                filter_string = filter_string + f" & {k}{operator}'{v}' "
            else:
                filter_string = filter_string + f" & {k}{operator}{v} "
        self.__filter_string = filter_string
        return self

    def __create_query_string(self):
        """
        组装生成 query_string
        """
        self.__filter_string = self.__filter_string.strip()
        if self.__filter_string.startswith('&'):
            self.__filter_string = self.__filter_string[1:]
        if self.__filter_string.endswith('&'):
            self.__filter_string = self.__filter_string[:-1]

    def all(self) -> DataFrame:
        """
        执行查询操作，即前面的都是 map 操作，这里是 action 操作。
        """
        self.__create_query_string()
        return self.left_df.query(self.__filter_string)

    def left_join(self, right_df: DataFrame, on: List[str]):
        """
        联合更新，即 sql 中的 left join right_df on cols 的功能
        """
        self.right_df = right_df
        self.__left_join_on_cols = on

    def update(self, **kwargs):
        """
        filter后，获得 index, 然后更新某些列值
        """
        self.__create_query_string()
        idx = self.left_df.eval(self.__filter_string)
        for col, value in kwargs.items():
            self.left_df.loc[idx, col] = value
        return self.left_df

    def join_update(self, source_df: DataFrame, join_on: List[str], source_col: str, target_col: str) -> DataFrame:
        """
        用原表的source_col字段去更新目标表的target_col字段，即：
        update target x
        from source y
        set x.col1 = y.col2
        where x.join_col = y.join_col

        注意，只更新满足条件的行，如果原来的 target_df 是有数据的，进行条件覆盖更新，而不是全部更新目标列
        """
        target_df = self.left_df
        for col in join_on:
            if col not in target_df.columns or col not in source_df.columns:
                raise Exception(f"联合更新函数，要求左右两边的dataframe有相同的列{col}")

        source_col2 = source_col + '_tmp'
        source = source_df.rename(columns={source_col: source_col2})
        source['__tmp'] = 1
        need_cols = join_on + [source_col2, '__tmp']
        source = source[need_cols]
        #
        cnt1 = len(target_df)
        df = pd.merge(left=target_df, right=source, on=join_on, how='left')
        cnt2 = len(df)
        # 判断是否存在重复记录导致膨胀
        if cnt1 != cnt2:
            raise Exception("source表存在重复记录，导致关联后的target表数据增加，请检查")
        #
        # 查询满足条件的index
        df['__tmp'] = df['__tmp'].fillna(0)
        self.__create_query_string()
        if self.__filter_string.strip():
            _filter_string = self.__filter_string + ' & ' + '__tmp==1'
        else:
            _filter_string = '__tmp==1'
        idx = df.eval(_filter_string)
        # 更新
        # 只更新满足条件的行，而不是全部行
        df.loc[idx, target_col] = df.loc[idx, source_col2]
        df.drop(columns=['__tmp', source_col2], inplace=True)
        return df

    def insert_if_not_exists(self, source_df: DataFrame, duplicates_on: List[str]):
        """
        模拟db的操作，如果记录不存在则插入，如果在数据库中已经有这条记录，就不插入了
        通过 duplicates_on 来判断是否已经存在。
        因此要求源表和目标表都要有相同的列，即 duplicates_on.

        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': ['a', 'b', 'c', 'd', 'e'],
            'c': [str(d)[:10] for d in pd.date_range(start=today, periods=5)],
            'g': ['a','a','b','b','b']
        })

        """
        # 看看两边的列(字段）是否一样
        target_cols = list(self.left_df.columns)
        source_cols = list(source_df.columns)
        not_exists_cols1 = [col for col in target_cols if col not in source_cols]
        not_exists_cols2 = [col for col in source_cols if col not in target_cols]
        if len(not_exists_cols1):
            print(f"在目标df中存在，但是在新增df中不存在的列是：{not_exists_cols1}，会导致insert的结果dataframe增加新列")
        if len(not_exists_cols2):
            print(f"在目标df中不存在，但是在新增df中存在的列是：{not_exists_cols2}，会导致insert的结果dataframe增加新列")
        #
        # 只需要选择 join_on 的列
        target_df = self.left_df.copy()[duplicates_on].drop_duplicates()
        # 找出那些在数据库中不存在的记录
        target_df['__tmp'] = 1
        df = pd.merge(left=source_df, right=target_df, on=duplicates_on, how='left')
        df['__tmp'] = df['__tmp'].fillna(0)
        new_data = df.query("__tmp==0")
        del new_data['__tmp']
        #
        # 将找出来的新数据添加到目标表中
        union_df = pd.concat([self.left_df, new_data], ignore_index=True)
        return union_df

    def column_concat(self, new_column: str, *args):
        """
        将 dataframe 的几列拼接成一列，通常是用于生成由多列指定的唯一id
        比如：pkid = id_name_sex 这样的格式
        """
        self.left_df[new_column] = ''
        for col in args:
            self.left_df[new_column] = self.left_df[new_column] + '_' + self.left_df[col].apply(str)
        self.left_df[new_column] = self.left_df[new_column].apply(lambda x: x.strip()[1:])
        return self.left_df

    def column_un_concat(self, column: str, new_columns: List[str]):
        """
        column_concat 的反向操作
        """
        data = [d.split('_') for d in self.left_df[column].values]
        for i, col in enumerate(new_columns):
            datai = [r[i] for r in data]
            self.left_df[col] = datai
        return self.left_df

    def join_filter(self, source_df: DataFrame, join_on: List[str]) -> DataFrame:
        """
        使用 inner_join 筛选目标表（target_df）中的数据，即在 source_df 中出现的 group_ids 是要留下的，其余的删除。
        """
        _sdf = source_df[join_on].drop_duplicates()
        return pd.merge(left=self.left_df, right=_sdf, on=join_on, how='inner')

    def join_delete(self, source_df: DataFrame, join_on: List[str]) -> DataFrame:
        """
        join_filter 的反向操作，删除那些在 source_df 出现过的 group-ids。
        """
        _sdf = source_df[join_on].drop_duplicates()
        _sdf['__delete'] = 1
        data = pd.merge(left=self.left_df, right=_sdf, on=join_on, how='left')
        data['__delete'] = data['__delete'].fillna(0)
        data = data.query('__delete==0')
        data.drop(columns=['__delete'])
        return data


def test_pddb():
    """
    """
    pddb = PDDB()

    df = pd.DataFrame({
        'a': [1, 2, 3, 4, 5],
        'b': ['a', 'b', 'c', 'd', 'e'],
        'c': [str(d)[:10] for d in pd.date_range(start='2021-01-01', periods=5)],
        'g': ['a', 'a', 'b', 'b', 'b']
    })

    # 根据自身信息筛选查询
    pddb.query(df).filter(a__gte=2).all()

    pddb.query(df).filter(a=2).all()

    # 更新数据
    pddb.query(df).filter(a__gte=2).update(g=4)

    # 用外部数据来更新自身
    df2 = df.copy()
    df2['g'] = 2
    pddb.query(df).join_update(df2, join_on=['a'], source_col='g', target_col='g')

    # 部分更新
    df2 = df.copy()
    df2['g'] = 3
    pddb.query(df).filter(a__gte=3).join_update(df2, join_on=['a'], source_col='g', target_col='g')

    # 插入不存在的数据
    df2 = df.copy()
    df2 = pddb.query(df2).filter(a__gte=4).update(a=10)
    pddb.query(df).insert_if_not_exists(df2, duplicates_on=['a', 'b'])
