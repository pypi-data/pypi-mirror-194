import time
from typing import List, Optional, Any

import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

from rcd_dev_kit.database_manager.s3_operator import S3Operator
from rcd_dev_kit.database_manager.redshift_operator import RedshiftOperator, send_to_redshift, \
    send_metadata_to_redshift, find_tables_by_column_name, read_from_redshift
from rcd_dev_kit.database_manager.snowflake_operator import SnowflakeOperator
from sqlalchemy import text
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.engine import URL
from snowflake.sqlalchemy import URL
import sqlalchemy
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer, write_pandas
import sqlparse
import re
import json