import boto3
import mysql.connector

## @params: [JOB_NAME]
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])
#
# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# job = Job(glueContext)
# job.init(args['JOB_NAME'], args)

ENDPOINT = "aurora-cluster-instance-1.cwtiiaz4iuby.us-east-1.rds.amazonaws.com"
PORT = "3306"
USR = "AwsTestSuite"
REGION = "us-east-1"
DBNAME = "awstestsuite"
token = "awstestsuite"

#session = boto3.Session()
client = boto3.client('rds', region_name='us-east-1')

#token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)


print('Generated Token')


try:
    conn = mysql.connector.connect(host=ENDPOINT, user=USR, passwd=token, port=PORT, database=DBNAME)

    print("4")
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))
