# coding:utf-8

def select_more(self, sql, *args):
    try:
        if args:
            self.__dict_cursor.execute(sql, args)
        else:
            self.__dict_cursor.execute(sql)
        res = self.__dict_cursor.fetchall()
        logger.info('query data success：{}'.format(sql))
    except Exception as e:
        logger.error('query data failure：{}'.format(e))
        raise
    return res