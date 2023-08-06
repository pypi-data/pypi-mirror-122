import os

os.environ['twneo_config_path'] = r'/Users/pankaj/dev/git/twneo/twneo/config/config_dev.yaml'


from twneo.twitter.tweet_collector import TweetCollector
from twneo.neo4j.graph_creator import TweetsGraphCreator


def main():
    query = '(#byjus)'
    collector = TweetCollector()
    collector.max_result_per_query = 50
    results = collector.collect_tweets_for_query(query, max_count=50)
    graph_creator = TweetsGraphCreator()
    count = 0
    for json_resp in results:
        meta_data = json_resp['meta']
        count = count + meta_data['result_count']
        graph_creator.create_tweets_graph(json_resp)
        print(f"created for {count} records ")

if __name__ == '__main__':
    main()