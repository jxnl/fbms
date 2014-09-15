# Facebook Garbage Collection : Mark Sweep

We are currently developing a text classification tool to improve the quality of disussions within very large Facebook groups.
Often times the volumn of conversatinos are so great that moderation becomes diffucult without a dedicated team of moderators. 
By using Mark Sweep, Mark will preprocess all messages coming into the group so that moderators can focus on what matters.

This was build at PennApps Fall 2014 with [Jason Liu](https://github.com/jxnl), [Taylor Blau](https://github.com/ttaylorr), and [Henry Boldizsar](https://github.com/9o)

The plan is to try to detect three core propeties of a post. 

1. How spam-like is it? 
2. How hateful is the comment?
3. Is the post on topic?

Our current goal is to have a overall classification accuracy with 80% with a preference for low false-positive rates.

## Topic Classification

We plan on using mongoDB as a way to store all posts within a group and retraining the classifiers every week or two.

To allow `Mark Sweep` to adapt to shifting conversations within groups we will bootstrap the data set (resample) with a bias towards time and 
facebook likes. Before training it against the content of all other posts.

We will use exponential and weighed reservoir sampling to resample posts up to three times. 

**Exponential Reservoir sampling** will allow us to resample `k` posts with a bias towards recent posts (allowing Mark Sweep to have a preference to 
features that are new and recent such as a new event or product without marking promotional material as spam)

**Weighed Reservoir** will allow us to resample `k` posts with a bias towards posts with many likes as a way to strengthen higher quality posts.

With this bootstraped dataset we will (for each group) train a [OVA](http://en.wikipedia.org/wiki/Multiclass_classification) classifier.
After running a [GriSdgearch](http://en.wikipedia.org/wiki/Hyperparameter_optimization) over the available classifiers we have had great success with a (SVM)[http://en.wikipedia.org/wiki/Support_vector_machine] model with weighted classes using a (mono-gram/bi-gram)[http://en.wikipedia.org/wiki/N-gram] bag-of-worsd
representation of the post data.

### Externally referenced content

Mark Sweep will also investigate all meta-data available for any links a user posts and run the same classification algorithm
to determine if the linked content is relevant.

## Spam Classification 

Instead of using bag-of-words for spam classification, we decided to classify by behavoir rather than content. 
This was done with the intention of potentially moderating facebook trading groups or facebook markets without 
falsely marking everything as spam. Instead we will try to classify on behavoir and frequency. 
We will build our own feature set and use this to train and watch the spam algorithm

* Number of URLS
* Number of keywords (hateful and spammy) *a full list can be found in the spam director*
* Number of all cap'd words
* Number of times an identical post has been posted
* Number of times a single user has posted identical content on various groups (potentially use mongo's Map/Reduce)

## UserDB

Using mongoDB we can keep a tab on all offending users and let admins know when a user has passed a certain number of flags.
Flags can be set by certain actions like spam, harassment, etc.  

## Deletion

To prevent false positives Mark Sweep will only delete posts that have 95% + spam confidence and is off-topic. 
Our goal is not to discourage groups from sharing things they may be passionate about (which might sound spammy) 
but to allow admins to moderate more important conversations instead of wasting time delete obvious offenders.

# Setup

To make this as easy to use as possible to setup, we intend on automating the procses of scraping/training/testing/deploying Mark Sweep.
By just adding Mark Sweep into your group, it will do everything it needs to get started. While we are a bit uncertain on how to implement 
configurating Mark Sweep on a group to group basis. We would love to hear your ideas on how that can be done.
