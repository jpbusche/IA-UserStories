import sys
from src.reader import Reader
from src.agents.user_stories import UserStories
from src.agents.tasks import Tasks


user_stories_agent = UserStories()
tasks = Tasks()

def main():
    result = {}
    if len(sys.argv) < 2:
        raise Exception("Is necessary to pass a file path!")
    reader = Reader(sys.argv[1])
    user_stories = generate_user_stories(reader)
    for user_storie in user_stories:
        result[user_storie] = generate_tasks(reader, user_storie)
    print(result)

def generate_user_stories(reader):
    context = reader.get_context(user_stories_agent.get_question())
    return user_stories_agent.generate_response(context)

def generate_tasks(reader, user_storie):
    tasks.format_question(user_storie)
    context = reader.get_context(tasks.get_question())
    return tasks.generate_response(context)


if __name__ == "__main__":
    main()