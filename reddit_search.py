import re
import sys
import time

import cPickle
import praw

def build_list():
    r = praw.Reddit(user_agent="mermoosescraper")
    subs = [
         'insightfulquestions',
         'changemymind',
         'freethought',
         'askscience',
         'askphilosophy',
         'existentialism',
         'philosophyofscience',
         'humanism',
         'askanthropology',
         'asksocialscience',
         'cogsci',
         'neuropsychology',
         'feminism',
         'politicaldiscussion',
         'moderatepolitics',
         'literature',
         'askhistorians',
         'foodforthought',
         'truereddit',
         'depthhub',
         'worldnews',
    ]

    posts = {}
    post_scores = {}
    comments = {}
    current_time = time.time()

    for sub in subs:
        try:
            list_of_posts = []
            for thing in r.search('', subreddit=sub, sort='hot', limit=1):
                list_of_posts.append(thing)
            print 'Looking through %d posts from r/%s' % (len(list_of_posts), sub)
            for thing in list_of_posts:
                key = (thing.url, thing.title)
                posts[key] = []
                post_scores[key] = 0
                for comment in thing.comments:
                    try:
                        contents = (str(comment.body), str(comment.author), str(comment.score))
                        score = len(comment.body) * comment.score
                        posts[key].append([comment.body, score])
                        post_scores[key] = max(post_scores[thing.url], score)

                    except:
                        pass
        except Exception, e:
            print "error:", e

    pickle_list = []

    for post in sorted(posts.keys(), key=lambda x: post_scores[x], reverse=True):

        post_tuple = [post, []]
        
        for comment in sorted(posts[post], key=lambda x: x[1], reverse=True):
            post_tuple[1].append(comment[0])

        pickle_list.append(post_tuple)

    print 'commencing pickle'
    with open('unviewed.txt', 'wb') as outfile:
        cPickle.dump(pickle_list, outfile)


def output(s, outfile):
    print s
    outfile.write(s + '\n')


def view_list():
    with open('unviewed.txt', 'rb') as infile:
        pickle_list = cPickle.load(infile)
    with open('viewed.txt', 'a') as outfile:
        for index in range(len(pickle_list)):
            post_tuple = pickle_list[index]
            output('url: '+ str(post_tuple[0][0]), outfile)
            output('title:' + str(post_tuple[0][1]), outfile)
            for comment in post_tuple[1]:
                output(comment, outfile)
                output('----'*20, outfile)
                if raw_input('another comment?' )[:1].lower() == 'n':
                    break
            output('===='*20, outfile)
            output('===='*20, outfile)
            if raw_input('another post?' )[:1].lower() == 'n':
                break

    pickle_list = pickle_list[index + 1:]
    with open('unviewed.txt', 'wb') as outfile:
        cPickle.dump(pickle_list, outfile)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'build':
            build_list()
        elif sys.argv[1] == 'view':
            view_list()
        else:
            print 'Usage: python reddit_search (build | view)'
    else:
        print 'Usage: python reddit_search (build | view)'


if __name__ == "__main__":
    main()
