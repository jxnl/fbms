# Facebook Garbage Collection : Mark Sweep

We are currently developing a text classification tool to improve the quality of discussions within very large Facebook groups.
Often times the volume of conversations are so great that moderation becomes difficult without a dedicated team.

This was build at PennApps Fall 2014 with [Jason Liu](https://github.com/jxnl), [Taylor Blau](https://github.com/ttaylorr), and [Henry Boldizsar](https://github.com/9o)

The plan is to try to detect three core properties of a post. 

1. How spam-like is it? 
2. How hateful is the comment?
3. Is the post on topic?

Our current goal is to have a overall classification accuracy with 80% with a preference for low false-positive rates.

## Service Orientation

The goal is to develop a series of restful services that are independent of eachother. Perhaps with Flask.
By being loosely coupled we allow other clients to use our REST api and to build ontop of the platform.
 
    POST : classify/ontopic/<int:groupid>/
    POST : classify/spam/
    POST : classify/troll/
    POST : search/

    GET  : classify/ontopic/<int:groupid>/<int:postid>/ 
    GET  : classify/spam/<int:postid>/
    GET  : classify/spam/<int:groupid>/<int:userid>/
    GET  : classify/troll/<int:postid>/
    GET  : classify/troll/<int:groupid>/<int:userid>/
    GET  : search/<int:groupid>/<int:limit>
    GET  : search/<int:postid>/comments/
    GET  : search/<int:postid>/likes/
    GET  : search/<int:userid>/<int:limit>


## Topic Classification

The plan is to crawl all the HH subgroups and then persist everything on mongoDB. Training of the data can be done on a daily basis.

To allow `Mark Sweep` to adapt to shifting conversations themes within a group we will resample some posts with a bias towards time and 
Facebook likes. To do this will we use exponential and weighed reservoir sampling to resample posts up to three times.

With this bootstrapped dataset we will (for each group) train a [OVA](http://en.wikipedia.org/wiki/Multiclass_classification) classifier.
After running a [GridSearch](http://en.wikipedia.org/wiki/Hyperparameter_optimization) over the available classifiers to fine the ideal hyper parameters. 
We have had great success with a (SVM)[http://en.wikipedia.org/wiki/Support_vector_machine] model with weighted classes using a (mono-gram/bi-gram)[http://en.wikipedia.org/wiki/N-gram] bag-of-words
representation of the post data.

## Spam Classification

Instead of using bag-of-words for spam classification, we decided to classify by behaviour rather than content.

* Number of URLS
* Number of keywords (hateful and spammy) *a full list can be found in the spam director*
* Number of all cap'd words
* Number of times an identical post has been posted
* Number of times a single user has posted identical content on various groups (potentially use mongo's Map/Reduce)

## Troll Classification

Thanks to an app called [Hater News](https://github.com/kevinmcalear/hater_news) we found a data set of troll posts so we will use that to detec

## Deletion

To prevent false positives Mark Sweep will only delete posts that have 95% + spam confidence and is off-topic. 
Our goal is not to discourage groups from sharing things they may be passionate about (which might sound spammy) 
but to allow admins to moderate more important conversations instead of wasting time delete obvious offenders.

# Setup

To make this as easy to use as possible to setup, we intend on automating the process of scraping/training/testing/deploying Mark Sweep.
By just adding Mark Sweep into your group, it will do everything it needs to get started. While we are a bit uncertain on how to implement 
configuring Mark Sweep on a group to group basis. We would love to hear your ideas on how that can be done.
