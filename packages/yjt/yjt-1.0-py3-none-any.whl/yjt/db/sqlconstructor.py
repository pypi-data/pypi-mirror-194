# sql构造器
class SqlConstructor:
    """
    sql构造器:

    - table('表名'): 设置表名

    - where相关
        - where('表达式', {参数字典}): 查询条件，多个`where`之间用`and`进行连接
            - 示例: where('name=:name and sex=:sex', {'name':'su', 'sex':0})
            - 最终生成查询 name=:name and sex=:sex 同进将 {'name':'su', 'sex':0} 放入参数

        - or_where('表达式', {参数字典}): 查询条件，作用如`where`但是与前一条件之用`or`进行连接

        - where_in('字段名', [值列表]): 查询条件 and in
        - or_where_in('字段名', [值列表]): 查询条件 or in
        - where_not_in('字段名', [值列表]): 查询条件 and not in
        - or_where_not_in('字段名', [值列表]): 查询条件 or not in
            - 示例: where_in('ub_status', [1,2])
            - 最终生成查询 ub_status in (:ub_status_sc_where_in_0, :ub_status_sc_where_in_1)
            - 同进将 {'ub_status_sc_where_in_0':1, 'ub_status_sc_where_in_1':2} 放入参数

        - group_start(): 条件分组开始`(`，与前一条件进行 and 连接
        - or_group_start(): 条件分组开始`(`，与前一条件进行 or 连接
        - group_end(): 条件分组结束`)`

        - get_where(): 取得`where`结果字符串

    - group_by('字段名'): 分组，例：group_by('sex')
        - get_group_by(): 取得结果字符串

    - order_by('表达式'): 排序，例：order_by('id desc')
        - get_group_by(): 取得结果字符串

    - join('连接方式', '表名', '表达式', {参数字典}) 关联查询
        - 示例: join('inner', 'user_info as a', 'a.id=:id and a.id=b.uid', {'id':10})
        - get_join(): 取得结果字符串

    - 分页相关
        - limit(int:开始索引, int:长度): 适用于 mysql，生成 limit 0,20
        - offset(int:开始索引, int:长度): 适用于 oracle 生成 OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY，建议 select 中增加查询 rowid
        - rownum(int:开始索引, int:长度): 适用于 oracle 生成 rownum > 开始 and rownum <= 结束，结束为开始 + 长度

    - select('表达式'): 查询的需要取出的字段
        - 1. 示例: select('id, name, sex')
        - 2. get_select(): 取得结果字符串

    - insert相关，如果存在 insert_batch 设置，则结果只输出 insert_batch 的设置
        - insert({参数字典})，单条写入，如：insert({'name':'root','sex':0})
        - insert_batch([{参数字典}])，批量写入，如: insert([{'name':'cd','sex':0},{'name':'gy','sex':1}])
        - get_insert(): 取得结果字典{'keys':'str', 'values':'str'}

    - update('参数字典 或 字符串表达式', {参数字典}): 更新数据
        - get_update(): 取得结果字符串

    - 取得完整的sql表达式
        - get_sql_count('字段名'): 查询总条数(不含order by 与 分页)，默认: count(*) as count
        - get_sql_select(): 查询
        - get_sql_insert(): 写入
        - get_sql_update(): 更新
        - get_sql_delete(): 删除

    oracel rownum 分页示例:
    正常查询语句[sql_query]: select * from user_base order by id asc
    分页语句: select * from (select rownum rowno,t.* from ({sql_query}) t where rownum<:limit_end) where rowno>=:limit_start
    """

    def __init__(self, params_type: str = ':'):
        # params_type 为 `:` 时，生成 :name，适用于(pandas+oracle, execute+mysql, execute+oracle)
        # params_type 为 `%` 时，生成 %(name)s，适用于(pandas+mysql)    db_session.get_bind()
        self._params_type = params_type
        self._params = {}

        self._expression_table = None
        self._expression_select = []
        self._expression_where = []
        self._expression_where_in_batch_no = 0

        self._expression_update = []
        self._expression_update_dict = {}

        self._expression_insert = {}
        self._expression_insert_batch = []

        self._expression_join = []
        self._expression_group_by = []
        self._expression_order_by = []

        # 分页相关
        self._expression_page_limit = {}
        self._expression_page_offset = {}
        self._expression_page_rownum = {}

    # 格式化字符串
    # noinspection PyMethodMayBeStatic
    def _format_string(self, val):
        if val and isinstance(val, str):
            val = val.strip().strip(',').strip()
            if val:
                return val
            else:
                return None
        else:
            return None

    # 设置参数值
    def _set_params(self, params):
        if params and isinstance(params, dict):
            self._params.update(params)

    # 生成 where 条件 list
    def _set_where(self, operator, expression, params):
        if expression:
            expression = self._format_string(expression)
        self._expression_where.append([operator, expression])
        self._set_params(params)

    # 取得参数值
    def get_params(self):
        return self._params

    # 设置 table
    def table(self, table: str = None):
        table = self._format_string(table)
        if table:
            self._expression_table = table

    # where: and
    def where(self, expression: str = None, params: dict = None):
        self._set_where('AND', expression, params)

    # where: or
    def or_where(self, expression: str = None, params: dict = None):
        self._set_where('OR', expression, params)

    # 生成 where in
    def _where_in(self, field: str = None, values: list = None, mode: str = 'in', connect: str = 'and'):
        if field and values:
            batch_no = self._expression_where_in_batch_no
            self._expression_where_in_batch_no = batch_no + 1
            if mode != 'in':
                mode = 'not_in'

            tmp_field = []
            params = {}
            for i, v in enumerate(values):
                tmp_field_name = field + '_sc_where_' + mode + '_' + str(batch_no) + '_' + str(i)
                if self._params_type == ':':
                    tmp_field.append(':' + tmp_field_name)
                elif self._params_type == '%':
                    tmp_field.append('%(' + tmp_field_name + ')s')
                params[tmp_field_name] = v

            if mode == 'in':
                expression = field + ' IN (' + ', '.join(tmp_field) + ')'
            else:
                expression = field + ' NOT IN (' + ', '.join(tmp_field) + ')'

            if connect == 'and':
                self._set_where('AND', expression, params)
            else:
                self._set_where('OR', expression, params)

    # where in: and
    def where_in(self, field: str = None, values: list = None):
        self._where_in(field=field, values=values, mode='in', connect='and')

    # where in: or
    def or_where_in(self, field: str = None, values: list = None):
        self._where_in(field=field, values=values, mode='in', connect='or')

    # where not in: and
    def where_not_in(self, field: str = None, values: list = None):
        self._where_in(field=field, values=values, mode='not_in', connect='and')

    # where not in: or
    def or_where_not_in(self, field: str = None, values: list = None):
        self._where_in(field=field, values=values, mode='not_in', connect='or')

    # 生成分组
    # where: and (
    def group_start(self):
        self._set_where('group_start', None, None)

    # where: or (
    def or_group_start(self):
        self._set_where('or_group_start', None, None)

    # where: not (
    def not_group_start(self):
        self._set_where('not_group_start', None, None)

    # where: not (
    def or_not_group_start(self):
        self._set_where('or_not_group_start', None, None)

    # where: )
    def group_end(self):
        self._set_where('group_end', None, None)

    # 生成 where 语句
    def get_where(self):
        if self._expression_where:
            where_list = []
            for i, v in enumerate(self._expression_where):
                if v[0] == 'group_start':
                    if len(where_list) > 0:
                        where_list.extend(['AND', '('])
                    else:
                        where_list.append('(')
                    continue

                if v[0] == 'or_group_start':
                    if len(where_list) > 0:
                        where_list.extend(['OR', '('])
                    else:
                        where_list.append('(')
                    continue

                if v[0] == 'not_group_start':
                    if len(where_list) > 0:
                        where_list.extend(['NOT', '('])
                    else:
                        where_list.append('(')
                    continue

                if v[0] == 'or_not_group_start':
                    if len(where_list) > 0:
                        where_list.extend(['OR NOT', '('])
                    else:
                        where_list.append('(')
                    continue

                if v[0] == 'group_end':
                    where_list.append(')')
                    continue

                if len(where_list) > 0:
                    if where_list[-1] == '(':
                        where_list.append(v[1])
                    else:
                        where_list.extend([v[0], v[1]])
                else:
                    where_list.append(v[1])

            return ' '.join(where_list)

        else:
            return False

    # 设置 join
    def join(self, connection='inner', table: str = None, expression: str = None, params: dict = None):
        if connection and table and expression:
            table = self._format_string(table)
            expression = self._format_string(expression)

            if connection and table and expression:
                connection = connection.upper()
                self._expression_join.append(
                    '{connection} JOIN {table} ON {expression}'.format(
                        connection=connection,
                        table=table,
                        expression=expression)
                )
            self._set_params(params)

    # 取得 join
    def get_join(self):
        if self._expression_join:
            return ' '.join(self._expression_join)
        else:
            return False

    # 设置 group by
    def group_by(self, field: str = None):
        field = self._format_string(field)
        if field:
            self._expression_group_by.append(field)

    # 取得 group by
    def get_group_by(self):
        if self._expression_group_by:
            return ', '.join(self._expression_group_by)
        else:
            return False

    # 设置 order by
    def order_by(self, expression: str = None):
        expression = self._format_string(expression)
        if expression:
            self._expression_order_by.append(expression)

    # 取得最终 order by sql
    def get_order_by(self):
        if self._expression_order_by:
            return ', '.join(self._expression_order_by)
        else:
            return False

    # limit 分页
    def limit(self, start: int, length: int):
        if start >= 0 and length > 0:
            self._expression_page_offset = {}
            self._expression_page_limit = {'start': start, 'length': length}
            self._expression_page_rownum = {}

    # offset 分页
    def offset(self, start: int, length: int):
        if start >= 0 and length > 0:
            self._expression_page_limit = {}
            self._expression_page_offset = {'start': start, 'length': length}
            self._expression_page_rownum = {}

    # rownum 分页
    def rownum(self, start: int, length: int):
        if start >= 0 and length > 0:
            self._expression_page_offset = {}
            self._expression_page_limit = {}
            self._expression_page_rownum = {'start': start, 'length': length}

    # 分页结果
    def get_page(self):
        # 返回含有{sql_query}的字符串, {sql_query}用于替换为查询主体语句
        if self._expression_page_limit or self._expression_page_offset or self._expression_page_rownum:
            if self._expression_page_limit:
                self._set_params({
                    'sc_page_start': self._expression_page_limit['start'],
                    'sc_page_length': self._expression_page_limit['length']
                })
                if self._params_type == ':':
                    return '{sql_query} LIMIT :sc_page_start,:sc_page_length'
                elif self._params_type == '%':
                    return '{sql_query} LIMIT %(sc_page_start)s,%(sc_page_length)s'

            elif self._expression_page_offset:
                self._set_params({
                    'sc_page_start': self._expression_page_offset['start'],
                    'sc_page_length': self._expression_page_offset['length']
                })
                if self._params_type == ':':
                    return '{sql_query} OFFSET :sc_page_start ROWS FETCH NEXT :sc_page_length ROWS ONLY'
                elif self._params_type == '%':
                    return '{sql_query} OFFSET %(sc_page_start) ROWS FETCH NEXT %(sc_page_length)s ROWS ONLY'

            elif self._expression_page_rownum:
                self._set_params({
                    'sc_page_start': self._expression_page_rownum['start'],
                    'sc_page_end': self._expression_page_rownum['start'] + self._expression_page_rownum['length']
                })
                if self._params_type == ':':
                    # noinspection SqlDialectInspection
                    return 'SELECT * FROM ' \
                           '(SELECT rownum row_no, sc_tmp_t.* FROM ({sql_query}) sc_tmp_t WHERE rownum<=:sc_page_end) ' \
                           'WHERE row_no>:sc_page_start '
                elif self._params_type == '%':
                    # noinspection SqlDialectInspection
                    return 'SELECT * FROM ' \
                           '(SELECT rownum row_no, sc_tmp_t.* FROM ({sql_query}) sc_tmp_t WHERE rownum<=%(sc_page_end)s) ' \
                           'WHERE row_no>%(sc_page_start)s '
        else:
            return False

    # 取得总数
    def get_sql_count(self, expression: str = None):
        if not self._expression_table:
            raise Exception('SqlConstructor: [Count] Table name is not set')

        expression = self._format_string(expression)
        if expression:
            select = expression
        else:
            select = 'count(*) as count'

        # noinspection DuplicatedCode
        where = self.get_where()
        if where:
            where = ' WHERE {where}'.format(where=where)
        else:
            where = ''

        join = self.get_join()
        if join:
            join = ' {join}'.format(join=join)
        else:
            join = ''

        group_by = self.get_group_by()
        if group_by:
            group_by = ' GROUP BY {group_by}'.format(group_by=group_by)
        else:
            group_by = ''

        # noinspection SqlDialectInspection
        return 'SELECT {select} FROM {table}{join}{where}{group_by}'.format(
            select=select,
            table=self._expression_table,
            where=where,
            join=join,
            group_by=group_by)

    # 设置查询
    def select(self, select: str = None):
        select = self._format_string(select)
        if select:
            self._expression_select.append(select)

    # 取得查询
    def get_select(self):
        if self._expression_select:
            return ','.join(self._expression_select)
        else:
            return False

    # 取得最终 select sql
    def get_sql_select(self):
        if not self._expression_table:
            raise Exception('SqlConstructor: [Select] Table name is not set')

        select = self.get_select()
        if not select:
            select = '*'

        # noinspection DuplicatedCode
        where = self.get_where()
        if where:
            where = ' WHERE {where}'.format(where=where)
        else:
            where = ''

        join = self.get_join()
        if join:
            join = ' {join}'.format(join=join)
        else:
            join = ''

        group_by = self.get_group_by()
        if group_by:
            group_by = ' GROUP BY {group_by}'.format(group_by=group_by)
        else:
            group_by = ''

        order_by = self.get_order_by()
        if order_by:
            order_by = ' ORDER BY {order_by}'.format(order_by=order_by)
        else:
            order_by = ''

        # noinspection SqlDialectInspection
        sql_query = 'SELECT {select} FROM {table}{join}{where}{group_by}{order_by}'.format(
            select=select,
            table=self._expression_table,
            where=where,
            join=join,
            group_by=group_by,
            order_by=order_by
        )

        # 分页
        page = self.get_page()
        if page:
            return page.format(sql_query=sql_query)
        else:
            return sql_query

    # 单条 insert
    def insert(self, values: dict = None):
        if values:
            self._expression_insert.update(values)

    # 取得 单条 insert
    def get_insert(self):
        if self._expression_insert:
            fields = self._expression_insert.keys()
            values = []
            params = {}
            for k in fields:
                params[k + '_sc_insert'] = self._expression_insert[k]
                if self._params_type == ':':
                    values.append(':' + k + '_sc_insert')
                elif self._params_type == '%':
                    values.append('%(' + k + '_sc_insert)s')

            self._set_params(params)

            return {'keys': '(' + ', '.join(fields) + ')', 'values': '(' + ', '.join(values) + ')'}
        else:
            return False

    # 批量 insert
    def insert_batch(self, values: list = None):
        if values:
            self._expression_insert_batch.extend(values)

    # 取得 批量 insert
    def get_insert_batch(self):
        if self._expression_insert_batch:
            fields = self._expression_insert_batch[0].keys()
            values = []

            for k in fields:
                if self._params_type == ':':
                    values.append(':' + k)
                elif self._params_type == '%':
                    values.append('%(' + k + ')s')

            self._params = self._expression_insert_batch
            return {'keys': '(' + ', '.join(fields) + ')', 'values': '(' + ', '.join(values) + ')'}
        else:
            return False

    # 取得最终 insert sql，批量优先
    def get_sql_insert(self):
        if not self._expression_table:
            raise Exception('SqlConstructor: [Insert] Table name is not set')

        if not self._expression_insert and not self._expression_insert_batch:
            raise Exception('SqlConstructor: [Insert] Values is not set')

        insert = self.get_insert_batch()
        if not insert:
            insert = self.get_insert()

        # noinspection SqlDialectInspection
        return 'INSERT INTO {table} {keys} VALUES {values}'.format(
            table=self._expression_table,
            keys=insert['keys'],
            values=insert['values'])

    # 设置 update
    def update(self, values: (dict, str) = None, params: dict = None):
        if values:
            if isinstance(values, dict):
                self._expression_update_dict.update(values)
            elif isinstance(values, str):
                values = self._format_string(values)
                if values:
                    self._expression_update.append(values)

        self._set_params(params)

    # 取得 update sql
    def get_update(self):
        if self._expression_update_dict or self._expression_update:
            values = []
            if self._expression_update_dict:
                fields = self._expression_update_dict.keys()
                params = {}
                for k in fields:
                    params[k + '_sc_update'] = self._expression_update_dict[k]
                    if self._params_type == ':':
                        values.append(k + '=:' + k + '_sc_update')
                    elif self._params_type == '%':
                        values.append(k + '=%(' + k + '_sc_update)s')

                self._set_params(params)

            if self._expression_update:
                values.extend(self._expression_update)

            return ', '.join(values)
        else:
            return False

    # 取得最终 update sql
    def get_sql_update(self):
        if not self._expression_table:
            raise Exception('SqlConstructor: [Update] Table name is not set')

        values = self.get_update()
        if values:
            values = ' SET {values}'.format(values=values)
        else:
            raise Exception('SqlConstructor: [Update] Values is not set')

        join = self.get_join()
        if join:
            join = ' {join}'.format(join=join)
        else:
            join = ''

        where = self.get_where()
        if where:
            where = ' WHERE {where}'.format(where=where)
        else:
            where = ''

        # noinspection SqlDialectInspection
        return 'UPDATE {table}{join}{values}{where}'.format(
            table=self._expression_table,
            join=join,
            where=where,
            values=values)

    # 取得最终 delete sql
    def get_sql_delete(self):
        if not self._expression_table:
            raise Exception('SqlConstructor: [Delete] Table name is not set')

        join = self.get_join()
        if join:
            join = ' {join}'.format(join=join)
        else:
            join = ''

        where = self.get_where()
        if where:
            where = ' WHERE {where}'.format(where=where)
        else:
            where = ''

        # noinspection SqlDialectInspection
        return 'DELETE FROM {table}{join}{where}'.format(
            table=self._expression_table,
            join=join,
            where=where)
