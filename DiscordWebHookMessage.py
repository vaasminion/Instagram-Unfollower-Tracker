import requests #dependency
from utils.ConnectionString import getConsString
from utils.GetParameter import getParameter
from sqlalchemy import text, create_engine
timeout = 60
def sendDiscordMessage(logger):
    try:
        cur = None
        failed_counter = 0
        engine = create_engine(getConsString(),connect_args={'connect_timeout': timeout})
        cur = engine.connect()
        url = getParameter('discord_webhook_instagram_url',cur)
        sql = 'select * from status order by no desc limit 1;'
        status = cur.execute(text(sql)).fetchall()
        sql = 'select count(*) from follower_latest;'
        count = cur.execute(text(sql)).fetchone()
        content = '**Instagram Alert Status '
        content = content + str(status[0][3]) #status
        content = content + ' : '
        content = content + str(status[0][1]) + '**' + '\n' #time
        if status[0][1] == 'Failed':
            content = content + 'Reason: ' + status[0][2] + '\n'
            failed_counter = 1
        if(not failed_counter):
            content = content + "Follower : " + str(count[0]) +'\n'
            content = content + 'Who unfollowed you \n'
            sql = 'select * from unfollower'
            unfollowerlist = cur.execute(text(sql)).fetchall()
            n = 1
            if len(unfollowerlist):
                for unfollower in unfollowerlist:
                    content = content + str(n) + ' : ' + unfollower[1] + ' | ' +str(unfollower[2]) + ' | ' + unfollower[3] + ' | ' + unfollower[4] + '\n'
                    n  = n+1
            else:
                content = content + 'No one unfollowed you. \n\n'
        
            content = content + '\n'
            content = content + 'Who followed you. \n' 
            sql = 'select * from follower'
            followerlist = cur.execute(text(sql)).fetchall()
            n = 1
            if len(followerlist):
                for follower in followerlist:
                    content = content + str(n) + ' : ' + follower[1] + ' | ' +str(follower[2]) + ' | ' + follower[3] + ' | ' + follower[4] + '\n'
                    n  = n+1
                content = content + '\n'
            else:
                content = content + 'No one followed you \n\n'
        
        #content = content + '-------------------------------------------------------\n'
        logger.info(content)
        if(len(content) > 2000):
            chunks = [content[i:i + 2000] for i in range(0, len(content), 2000)]
            for chunk in chunks:
                data = {"username": "Instagram Bot","embeds": [
                {
                    "description": chunk,"title": ""
                }
                ]
            }

                response = requests.post(url, json=data)

            if response.status_code != 204:
                logger.info(f"Failed to send message. Status code: {response.status_code}")
            else:
                logger.info("Message sent successfully!")
        else:
            data = {"username": "Instagram Bot","embeds": [
                {
                    "description": content,"title": ""
                }
                ]
            }
            result = requests.post(url, json = data)

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logger.error("An error occurred", exc_info=True)
            else:
                logger.info("Payload delivered successfully, code {}.".format(result.status_code))

    except Exception as e:
        logger.error("An error occurred", exc_info=True)
    finally:
        if cur is not None:
            if not cur.closed:
                cur.close()
