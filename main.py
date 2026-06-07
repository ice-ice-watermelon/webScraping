import logging
from config.log import log_init
from data.data import data_get
from sqlalchemy import create_engine

if __name__ == '__main__':
    #log日志初始化
    log_init()

    #获取清洗后的数据
    cleaned_df = data_get()

    #数据入库
    if cleaned_df is not None and not cleaned_df.empty:
        logging.info("开始连接MySQL")

        db_url = "mysql+pymysql://root:123456@localhost:3306/webScraping?charset=utf8mb4"
        engine = create_engine(db_url)

        cleaned_df.to_sql(name='tb_douban_movies', con=engine, if_exists='replace', index=False)
        logging.info("成功保存至MySQL")
    else:
        logging.error("未成功保存至MySQL")