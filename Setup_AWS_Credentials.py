#!/usr/bin/env python
# coding: utf-8
# %%

# %%


get_ipython().run_cell_magic('bash', '', '\nrm -f -- ~/.env\ncp /etc/skel/.env ~/')


# %%


from dotenv import load_dotenv
load_dotenv()


# %%


get_ipython().run_cell_magic('bash', '', '\naws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"\naws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" \naws configure set region "us-east-1" \naws configure set output "text"\n')


# %%


get_ipython().run_cell_magic('bash', '', '\nbucketname="$(echo $USER"-sql-workshop"|cut -d "-" -f2-)"\necho "BUCKETNAME=s3://$bucketname" >> ~/.env\n\naws s3api create-bucket --bucket $bucketname --region us-east-1\naws s3api list-buckets | grep $bucketname ')


# %%


load_dotenv()


# %%


import os
os.environ['ATHENA_REGION']= 'us-east-1'
os.environ['ATHENA_STAGING']= os.getenv('BUCKETNAME')
os.environ['ATHENA_DATABASE']='sra'


# %%


import pyathena
import pandas as pd


#This line of code gives the connection information to AWS, this variable is used in the sql commands

athena_conn = pyathena.connect(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), ##credentials of aws_access_key_id
                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), ##credentials of aws_secret_access_key
                 s3_staging_dir=os.environ['ATHENA_STAGING'], ##where the athena query result saved - checked in S3 ,
                 region_name=os.environ['ATHENA_REGION']) ##the region you set for Athena



# %%


get_ipython().run_line_magic('reload_ext', 'sql')


# %%


import sqlalchemy
from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine


AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SCHEMA_NAME = os.getenv('ATHENA_DATABASE')
S3_STAGING_DIR = os.environ['BUCKETNAME']
AWS_REGION = "us-east-1"


conn_str = (
    "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@"\
    "athena.{region_name}.amazonaws.com/"\
    "{schema_name}?s3_staging_dir={s3_staging_dir}/"
)



# Create the SQLAlchemy connection. Note that you need to have pyathena installed for this.
connection = conn_str.format(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
        schema_name=SCHEMA_NAME,
        s3_staging_dir=S3_STAGING_DIR,
    )


# %%


get_ipython().system('echo "DATABASE_URL=$connection">> ~/.env')


# %%


load_dotenv()


# %%


get_ipython().run_line_magic('config', 'SqlMagic.displaycon = False')


# %%


get_ipython().run_cell_magic('sql', '', "\nSELECT acc, librarysource, bioproject, geo_loc_name_country_calc\nFROM sra.metadata\nWHERE organism = 'Homo sapiens'\nLIMIT 5")


# %%





# %%


#Use this code block by removing the "#" in front of the following commands 
#This is needed outside of the workshop to set up credentials for your AWS Account
#This has already been done on the workshop server but the keys will stop working after September 15,2021

#%env AWS_ACCESS_KEY_ID=<your_AWS_Access ID>
#%env AWS_SECRET_ACCESS_KEY=<your AWS Secret>
#%env BUCKETNAME=<your staging bucket name>

#!sudo pip install pyathena 
#!sudo pip install ipython-sql
#!pip install sqlalchemy


# %%




