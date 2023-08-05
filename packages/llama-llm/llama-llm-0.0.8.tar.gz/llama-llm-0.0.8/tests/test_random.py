from llama import Type, Context, LLM

import unittest


class Story(Type):
    story: str = Context("the body of the story")


class Tone(Type):
    tone: str = Context("The tone of the story")


class Descriptors(Type):
    likes: str = Context("things you like")
    favorite_song: str = Context("your favorite song")
    tone: Tone = Context("tone of the story")


llm = LLM(name="test_random")


@llm.function
def write_story(descriptors: Descriptors) -> Story:
    story = llm(
        input=descriptors, output_type=Story, random=True
    )

    return story


class TestRandom(unittest.TestCase):
    def test_random(self):
        descriptors = Descriptors(
            likes="llamas and other animals",
            favorite_song="never let me go",
            tone=Tone(tone="cheeky"),
        )

        story = write_story(descriptors)

        print(story)
