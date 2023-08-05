import time

import pandas as pd
from dwhutils.TechFields import add_technical_col
from pandas_upsert_to_mysql import Upsert
# from Librarys.TechFiels import Techfields
from sqlalchemy import MetaData
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import load_config


def load(data: pd.DataFrame, db_con, t_name: str, date: str, schema: str = None, commit_size: int = 10000):
    load_dotenv()
    config_file = load_config.get_db_config()
    kp_path = load_config.get_keypass_config()
    conf_r = load_config.get_entity_configs()
    con_s = "mysql+pymysql://root:123456@82.165.203.114:3306/src?charset=utf8mb4"  # 'postgresql://postgres:123456@OKRAMER-MAC:5432/BANK'
    con = create_engine(con_s, echo=False, pool_recycle=3600)
    temp_table = t_name + time.time().__str__()
    metadata = MetaData(bind=db_con)
    metadata.reflect(bind=db_con, schema=schema)
    alltabs = metadata.sorted_tables
    trans = [i for i in alltabs if 'trans' in i.name]
    tmptbl = trans[0]
    tmptbl.name = temp_table

    data = add_technical_col(data=data, t_name=t_name, date=None)
    Upsert(engine=con).to_mysql(df=data,
                                target_table=trans[0],
                                temp_table=tmptbl,
                                if_record_exists='update')
