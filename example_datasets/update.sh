set -x

CURRENT_DIR=$pwd
HADOOP_DIR=bellevue-bigdata/hadoop-hive-spark-hbase

rm -rf $HADOOP_DIR/docker-compose.yml
wget -P $HADOOP_DIR https://raw.githubusercontent.com/bellevue-university/dsc650-infra/main/bellevue-bigdata/hadoop-hive-spark-hbase/docker-compose.yml

NIFI_DIR=bellevue-bigdata/nifi
mkdir -p $NIFI_DIR/hadoopconf
wget -P $NIFI_DIR/hadoopconf https://raw.githubusercontent.com/bellevue-university/dsc650-infra/main/bellevue-bigdata/nifi/hadoopconf/core-site.xml

NIFI_HADOOP_CONF_DIR=bellevue-bigdata/nifi/hadoopconf
EXTERNALIP=`hostname -f`
sed -i "s|HOST|${EXTERNALIP}|g" $NIFI_HADOOP_CONF_DIR/*.xml

cd $HADOOP_DIR
docker-compose down
docker-compose up -d

set +x