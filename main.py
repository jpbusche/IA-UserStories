import sys
from src.reader import Reader
from src.user_stories import UserStories


user_stories_agent = UserStories()

def main():
    if len(sys.argv) < 2:
        raise Exception("Is necessary to pass a file path!")
    reader = Reader(sys.argv[1])
    user_stories = generate_user_stories(reader)
    print(user_stories)

def generate_user_stories(reader):
    context = reader.get_context(user_stories_agent.get_question)
    return user_stories_agent.generate_user_stories(context)

if __name__ == "__main__":
    main()