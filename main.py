from instagrapi import Client
import random
from utils.UserDetail import get_UserDetails
from datetime import datetime
from utils.ConnectionString import getConsString
from sqlalchemy import create_engine,text
import pandas as pd
import logging
import string
from utils.EnvVariable import checkEnvVariable ,EnvVariableException
import LogConfig
from DiscordWebHookMessage import sendDiscordMessage
log_filename = LogConfig.Path + LogConfig.FileName
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
# Create a stream handler to logger.info log messages to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
# Define the log message format
log_format = logging.Formatter('%(asctime)s - [ %(levelname)s ]  - %(message)s')
# Set the format for the file handler and stream handler
file_handler.setFormatter(log_format)
stream_handler.setFormatter(log_format)
# Add the file handler and stream handler to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
timeout = 60
def time_now():
    return  str(datetime.now())[:-7]
def rollBack():
        try:
            logger.info(" [START] Rollback")
            engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
            con = engine.connect()
            con.execute(text("DROP TABLE IF EXISTS follower_latest"))
            con.execute(text("CREATE TABLE follower_latest AS SELECT * FROM follower_latest_backup"))
            con.execute(text("DROP TABLE IF EXISTS follower_old"))
            con.execute(text("CREATE TABLE follower_old AS SELECT * FROM follower_old_backup"))
            con.commit()
            logger.info(" [END] Rollback")
        except Exception as ex:
            raise ex
        finally:
            if not con.closed:
                con.close       
def takeBackup():
    try:
        engine = create_engine(getConsString())
        con = engine.connect()
        logger.info(" [START] CREATING BACKUP TABLE FOR LATEST AND OLD DATA")
        con.execute(text("DROP TABLE IF EXISTS follower_latest_backup"))
        con.execute(text("CREATE TABLE follower_latest_backup AS SELECT * FROM follower_latest"))
        con.execute(text("DROP TABLE IF EXISTS follower_old_backup"))
        con.execute(text("CREATE TABLE follower_old_backup AS SELECT * FROM follower_old"))
        con.commit()
        logger.info(" [END] CREATING BACKUP TABLE FOR LATEST AND OLD DATA")
    except Exception as ex:
        raise ex
    finally:
        if not con.closed:
            con.close
def getIGFollower(user,password,username):
    insta_client = Client()
    delay_range = [2, 10]
    userlogrequired = True
    try:
        Session = insta_client.load_settings("setting.json")
    except FileNotFoundError fe:
        logger.info(f"File not found : "+ str(fe))
        Sesson = False
    follower_detail = ''
    if Session:
        try:
            insta_client.set_settings(Session)
            insta_client.login(user,password)
            try:
                insta_client.get_timeline_feed()
                userlogrequired = False
            except Exception:
                logger.info("Session is invalid, need to login via username and password")
                old_session = insta_client.get_settings()
                insta_client.set_settings({})
                insta_client.set_uuids(old_session["uuids"])
                insta_client.login(user, password)
                userlogrequired = False
        except Exception as e:
            logger.info(f"Couldn't login user using session information: {str(e)}")
    if userlogrequired:
        insta_client.login(user,password)
        insta_client.dump_settings("session.json")
    try:
        outputFile = open('follower.csv','w',encoding='utf-8')
        outputFile.write("userid,username,fullname\n")
        userid = insta_client.user_id_from_username(username)        
        user_follower_list = insta_client.user_followers(userid)
        for follower in user_follower_list:
            usershort = user_follower_list[follower]
            follower_detail = usershort.pk + "," + usershort.username.replace(',',' ') + ',' + usershort.full_name.replace(',',' ') + "\n"
            logger.info(follower_detail)
            outputFile.write(follower_detail)
        outputFile.close()
    except Exception as Exp:
        raise Exp
    except BaseException as Bexp:
        raise Bexp
def handleOldDump(conn):
    try:
        logger.info("[START] Dropping and Creating Follower_old table")
        conn.execute(text("DROP table if exists follower_old"));
        conn.commit()
        conn.execute(text("create table follower_old as select * from follower_latest"))
        conn.commit()
        logger.info("[END] Dropping and Creating Follower_old table")
    except Exception as ex:
        #ex.with_traceback()
        raise ex
def handleLatestDump():
    try:

        engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
        df_iter = pd.read_csv('follower.csv',iterator=True,chunksize=200)
        df = pd.read_csv('follower.csv')
        logger.info(df.columns)
        df['url'] = df.apply(lambda row : 'https://instagram.com/' + str(row['username']),axis=1)
        df['dateadded'] = time_now()
        df.head(0).to_sql(name = 'follower_latest',con=engine, if_exists='replace',index=False)
        logger.info("[START] Inserting Latest Data in Batch")
        batch_no = 1
        while True:
            try:
                df_chunk = next(df_iter)
                df_chunk['url'] = df_chunk.apply(lambda row : 'https://instagram.com/' + row['username'],axis=1)
                df_chunk['dateadded'] = df_chunk.apply(lambda row : time_now(),axis=1)
                df_chunk.to_sql(name = 'follower_latest',con=engine, if_exists='append',method = 'multi',index=False,)
                logger.info(f"Batch #{batch_no} is completed")
                batch_no = batch_no + 1
            except StopIteration as e:
                logger.info('Data Insertion completed')
                break
            except Exception as ex:
                logger.error(f'Failed while inserting Batch # {batch_no}')
                raise ex
        logger.info("[END] Inserting Latest Data")
    except Exception as ex:
        raise ex
def pushToDb():
    try:    
        engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
        con = engine.connect()
        logger.info("[START] Handling OLD DUMP TABLE")
        handleOldDump(con)
        logger.info("[END] Handling OLD DUMP TABLE")
        logger.info("[START] Handling LATEST DUMP TABLE")
        handleLatestDump()
        logger.info("[END] Handling LATEST DUMP TABLE")
    except Exception as ex: 
        #ex.with_traceback()
        raise ex
    finally:
        if not con.closed:
            con.close
def prepareUnfollowerlist():
    try:
        engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
        conn = engine.connect()
        sql_1 = text('select * from follower_old where userid not in (select userid from follower_latest);')  #query to fetch who unfollow me
        sql_2 = text('select * from follower_latest where userid not in (select userid from follower_old);') # query new follower
        conn.execute(text("DROP TABLE IF EXISTS follower"))
        conn.execute(text("DROP TABLE IF EXISTS unfollower"))
        conn.commit()
        result = conn.execute(sql_1).fetchall()
        #logger.info(f'unfollower: {len(result)} {result}')
        logger.info("UNFOLLOWER LIST")
        for i in result:
            logger.info(i)
        result2 = conn.execute(sql_2).fetchall()
        #logger.info(f'follower: {len(result2)} {result2}')
        #logger.info('follower: ',len(result2) ,result2)
        logger.info("FOLLOWER LIST")
        for i in result2:
            logger.info(i)
        logger.info('CREATING UNFOLLOWER TABLE')
        sql = 'create table unfollower as select * from follower_old where userid not in (select userid from follower_latest);'
        conn.execute(text(sql))
        sql = 'insert into unfollowerrecord select * from follower_old where userid not in (select userid from follower_latest);'
        conn.execute(text(sql))
        logger.info('CREATING FOLLOWER TABLE')
        sql = 'create table follower as select * from follower_latest where userid not in (select userid from follower_old);'
        conn.execute(text(sql))
        sql = 'insert into followerrecord select * from follower_latest where userid not in (select userid from follower_old);'
        conn.execute(text(sql))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        if not conn.closed:
            conn.close()
def checkExistingProcess(connection,unique_id):
    try:
        sql = 'insert into instascript_tracker(unique_id,status,date) VALUES (:unique_id,:status,:date)'
        para = {'unique_id': unique_id,'status' : 'W' , 'date' : time_now()}
        connection.execute(text(sql),para)
        connection.commit()
        sql = "select * from instascript_tracker where status = :status;"
        para = {'status' : 'P'}
        result = connection.execute(text(sql),para).fetchall()
        if len(result):
            raise Exception("Previous Process is running")
        else:
            sql = "update instascript_tracker set status = :status where unique_id = :unique_id and status = 'W'"
            para = {'status': 'P','unique_id': unique_id}
            connection.execute(text(sql),para)
            connection.commit()
    except Exception as e:
        raise e
if __name__ == '__main__':
    try:
        loginusername = ''
        loginpassword = ''
        username = ''
        logger.info("Starting : " + time_now())
        connection = None
        checkEnvVariable()
        unique_id = res = ''.join(random.choices(string.ascii_lowercase + string.digits,k = 10))
        logger.info(unique_id)
        engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
        connection = engine.connect()
        checkExistingProcess(connection,unique_id)
        takeBackup()
        loginusername,loginpassword,username = get_UserDetails(connection)
        getIGFollower(str(loginusername),str(loginpassword),str(username))
        pushToDb()
        prepareUnfollowerlist()
        sql = "update instascript_tracker set status = :status where unique_id = :unique_id and status = 'P'"
        para = {'status': 'S','unique_id': unique_id}
        connection.execute(text(sql),para)
        sql = 'insert into status(status,reason,ended_time) values (:status,:reason,:ended_time)'
        para = {'status':'Success','reason':'NA','ended_time':time_now()}
        connection.execute(text(sql),para)
        logger.info("Completed" + time_now())
        connection.commit()
    except EnvVariableException as Evx:
        logger.error(str(Evx))
    except Exception as ex:
        rollBack()
        logger.error("EXCEPTION MESSAGE: " + str(ex)) 
        logger.error("An error occurred", exc_info=True)
        sql = "update instascript_tracker set status = :status where unique_id = :unique_id"
        para = {'status': 'F','unique_id': unique_id}
        connection.execute(text(sql),para)
        sql = 'insert into status(status,reason,ended_time) values (:status,:reason,:ended_time)'
        para = {'status':'Failed','reason':str(ex),'ended_time':time_now()}
        connection.execute(text(sql),para)
        connection.commit()
    except BaseException as Bexp:
        logger.error("Exception while logging in : " + str(Bexp))
        sql = "update instascript_tracker set status = :status where unique_id = :unique_id"
        para = {'status': 'F','unique_id': unique_id}
        connection.execute(text(sql),para)
        sql = 'insert into status(status,reason,ended_time) values (:status,:reason,:ended_time)'
        para = {'status':'Failed','reason':str(Bexp),'ended_time':time_now()}
        connection.execute(text(sql),para)
        connection.commit()
    finally:
        sendDiscordMessage(logger)
        if connection is not None:
            if not connection.closed:
                connection.close()
