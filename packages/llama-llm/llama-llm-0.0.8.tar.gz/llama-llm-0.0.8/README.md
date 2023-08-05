# Llama

Stop prompt tuning. Create your own Generative AI.

## Installation

```
    pip install llama-llm
```

## Setup your keys

Go to [powerml.co](https://powerml.co).  Log in to get you API key and purchase credits.

Create `~/.powerml/configure_llama.yaml` and put a key in it.

```
production:
    key: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

```

## Define the LLM interface

Define the input and output types.  Don't forget the context.  They help
the LLM understand the data.

```
class Tweet(Type):
    tweet: str = Context("a viral tweet")
    likes: int = Context("likes the tweet gets")
    retweets: int = Context("retweets the tweet gets")


class User(Type):
    username: str = Context("a user's handle on twitter")
```

## Instantiate an LLM engine

```
from llama import LLM

llm = LLM(name="feedback")
```

Define a function, call the llm to convert between types.  Mix standard python
and LLM code.

```
@llm.function
def generate_tweet(user: User) -> Tweet:
    return llm(user, output_type=Tweet)
```

## Use the LLM to generate something new

example_tweet = generate_tweet(user=User(username="llamas4sale"))

print("tweet before training", example_tweet)

## Train the LLM on your data

```
llm.add_data(
    data=[
        {
            "input": User(username="i_heart_llamas"),
            "output": Tweet(tweet="I like llamas", likes=5, retweets=3),
        },
        {
            "input": User(username="llamas4ever"),
            "output": Tweet(tweet="I like llamas so much", likes=8, retweets=5),
        },
    ]
)

example_tweet = generate_tweet(user=User(username="llamas4sale"))

print("tweet after adding data", example_tweet)
```

## Look at the results, and add your feedback to improve the LLM

```
llm.improve(on="tweet", to="have more {likes}")
llm.improve(on="tweet", to="have over 100 {retweets}")
llm.improve(
    on="tweet",
    to="make it shorter",
    good_examples=[
        Tweet(
            tweet="Move over cats and dogs, llamas are the new internet sensation! These furry and friendly creatures have captured our hearts and become the most adorable animals on the planet! From their soft wool to their quirky personalities, llamas are simply irresistible! #llamalove #cuteoverload 🦙💕🌟",
            likes=13452,
            retweets=9724,
        )
    ],
    bad_examples=[
        Tweet(
            tweet="Good evening everyone, I hope you're all having a lovely day. I was taking a walk in the countryside earlier and happened to come across a group of llamas. Llamas are interesting animals with a long history of domestication by indigenous people in South America. They're known for their wool, which is used to make various textiles, and also for their use as pack animals. Although some people may find llamas cute and quirky, they can also be quite stubborn and difficult to train. Anyway, that was my llama encounter for the day. Hope you found it mildly interesting. #llamas #naturewalk #animalencounter",
            likes=14,
            retweets=3,
        )
    ],
)
llm.improve(on="tweet", to="have no hashtags")

tweet_after_feedback = generate_tweet(user=User(username="llamas4sale"))

print("tweet after feedback", tweet_after_feedback)
```

## Build complex programs

