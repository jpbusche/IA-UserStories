from src.reader import Reader
from src.user_stories import UserStories

path = "Wenova.md"
reader = Reader(path)
user_stories = UserStories()

context = reader.get_context(user_stories.get_question())
stories = user_stories.generate_user_stories(context)
print(stories)