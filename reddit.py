import praw
import pymongo

class REDDIT:

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["reddit"]
    mycol = mydb["reddit_posts"]

    reddit = praw.Reddit(
        client_id="buyo6b-krGWIJ3qm4oJZcg",
        client_secret="FaRa2WxWVxwgeBkwDL0xzl-vRosC0g",
        user_agent="my user agent"
    )

    def duplicate_control(self, post_dict):
        if self.mycol.find_one({'id': post_dict['id']}):
            return True
        else:
            return False

    def main(self):
        while True:
            sub = ['Yatirim']
            for s in sub:
                subreddit = self.reddit.subreddit(s)


                for submission in subreddit.new(limit=1000):
                    ##### Acessing comments on the post
                    data = {
                            "title": submission.title,
                            "score": submission.score,
                            "id": submission.id,
                            "url": submission.url,
                            "comms_num": submission.num_comments,
                            "created": submission.created,
                            "body": submission.selftext
                        }

                    if self.duplicate_control(data) == False:
                        self.mycol.insert_one(data)

if __name__ == "__main__":
    red = REDDIT()
    red.main()
