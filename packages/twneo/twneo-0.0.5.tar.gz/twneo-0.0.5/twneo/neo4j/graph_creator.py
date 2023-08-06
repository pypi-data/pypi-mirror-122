from neo4j import GraphDatabase
from nltk.tokenize import TweetTokenizer
from twneo.config.config import TWNEO_CONFIG

TWNEO_CONFIG = TWNEO_CONFIG['TWNEO_CONFIG']

from twneo.twitter.tweet_collector import TweetCollector

class TweetsGraphCreator:


    def __init__(self):
        self.db_name = TWNEO_CONFIG['NEO4J']['database']
        self.uri = TWNEO_CONFIG['NEO4J']['uri']
        self.user = TWNEO_CONFIG['NEO4J']['user']
        self.password = TWNEO_CONFIG['NEO4J']['password']
        self.tweet_tokenizer = TweetTokenizer()
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def create_user(self, tx, user, userId , location = 'NA'):
        sql = """ MERGE (u:User {name: $user, userId:$userId})
        MERGE (l:Location {location : $location})
        MERGE (u)-[:lives_in]->(l)
         """
        tx.run(sql, user=user, location = location, userId =userId, relation='lives_in')
        print(sql, user, userId, location)

    def create_tweet(self, tx, tweetId, text=None, retweet_count=0):
        sql = """ MERGE (t:Tweet {tweetId: $tweetId})
            """
        tx.run(sql, tweetId=tweetId)
        if text is not None:
            sql = """ match (t:Tweet {tweetId: $tweetId})
            set t.text = $text
                        """
            tx.run(sql, tweetId=tweetId,text=text)
            sql = """ match (t:Tweet {tweetId: $tweetId})
                       set t.retweetCount = $retweet_count
                                   """
            tx.run(sql, tweetId=tweetId, text=text,retweet_count=retweet_count)

        print(sql, tweetId, text)


    def create_user_mention_relation(self, tx, userId,userName, tweetId, relation_name='retweets'):
        sql = "merge (t:Tweet {tweetId: $tweetId}) " \
              "merge (u:User {name: $userName, userid:$userId}) "\
              f"MERGE (u)-[:{relation_name}]->(t)"
        tx.run(sql,
               userId=userId, tweetId=tweetId, userName=userName
               )
        print(sql, userId, userName)

    def create_user_retweet_relation(self, tx, userId, tweetId, relation_name='retweets'):
        sql = "merge (t:Tweet {tweetId: $tweetId}) " \
              "merge (u:User {  userId:$userId}) " \
              f"MERGE (u)-[:{relation_name}]->(t)"
        tx.run(sql,
               userId=userId, tweetId=tweetId,
               )
        print(sql, userId)

    def create_tweets_graph(self, json_resp):
        with self.driver.session(database= self.db_name) as session:

            all_referenced_tweet_ids = []
            for user_dict in json_resp['includes']['users']:
                uname = user_dict['username']
                userid = user_dict['id']
                location = user_dict['location'] if 'location' in user_dict else 'NA'
                session.write_transaction(self.create_user, uname,userid, location)

            for json_data in json_resp['data']:
                text = json_data['text']
                tweet_id = json_data['id']
                type = 'retweet' if text.startswith('RT @') else 'tweet'
                retweet_count  = json_data['public_metrics'] ['retweet_count']
                if type=='tweet' :
                    session.write_transaction(self.create_tweet, tweet_id, text, retweet_count)

            for json_data in json_resp['data']:

                user_id = json_data['author_id']
                entities = json_data['entities']
                if 'mentions' not in entities:
                    continue
                mentions = entities['mentions']
                text = json_data['text']
                type = 'retweet' if text.startswith('RT @') else 'tweet'


                if  type=='retweet':
                    referenced_tweets = json_data['referenced_tweets']
                    referenced_tweet = [referenced_tweet for referenced_tweet in referenced_tweets if
                                        referenced_tweet['type'] == 'retweeted']
                    for mention in mentions:
                        if   mention['start']==3  :
                            relation_type = 'retweets'
                            referenced_tweet_id = referenced_tweet[0]['id']
                            all_referenced_tweet_ids.append(referenced_tweet_id)
                            session.write_transaction(self.create_user_retweet_relation, user_id, referenced_tweet_id, relation_type)
                else :
                    session.write_transaction(self.create_user_retweet_relation, user_id, json_data['id'],
                                              'tweets')
                    for mention in mentions:
                        relation_type = 'mentioned_in'
                        session.write_transaction(self.create_user_mention_relation,  mention['id'], mention['username'], json_data['id'], relation_type)
            start =0
            end = 100

            collector = TweetCollector()
            # create a relation for all the referenced tweets

            while start<len(all_referenced_tweet_ids) :
                ref_ids = all_referenced_tweet_ids[start:end]
                ref_tweet_details =collector.collect_tweets_details(ref_ids)
                start = start+100
                end= end+100
                for user_dict in ref_tweet_details['includes']['users']:
                    uname = user_dict['username']
                    userid = user_dict['id']
                    location = user_dict['location'] if 'location' in user_dict else 'NA'
                    session.write_transaction(self.create_user, uname, userid, location)

                for tweet in ref_tweet_details['data']:
                    tweet_text = tweet['text']
                    tweet_id = tweet['id']
                    retweet_count = tweet['public_metrics']['retweet_count']
                    user_id = tweet['author_id']
                    session.write_transaction(self.create_tweet,tweet_id,tweet_text, retweet_count)
                    session.write_transaction(self.create_user_retweet_relation, user_id, tweet_id,
                                              "tweeted")

                    entities = tweet['entities']
                    if 'mentions' not in entities:
                        continue
                    mentions = entities['mentions']
                    for mention in mentions:
                        session.write_transaction(self.create_user_mention_relation,  mention['id'], mention['username'], tweet_id, "mentioned_in")