from bs4 import BeautifulSoup as bs
import requests as rq

username = input('Enter github Username: ').strip()

res = rq.get(f'https://github.com/{username}')


# Function to fetch users

def github_follow(context):
    soup = bs(rq.get(f"https://github.com/{username}?tab={context}").text, 'lxml')
    items = soup.find_all("span", class_="Link--secondary")
    
    users = []
    for item in items:
        users.append(item.text)
    return users

# Finding Difference and Intersect

def find_difference(list1, list2):
    result = []
    for name in list1:
        if name not in list2:
            result.append(name)
    return result


def loader():
    print(f'Account found for user: {username}')
    
    followers = github_follow("followers")
    followers_count = len(followers)
    print(f'{username} has {followers_count} followers')
    
    following = github_follow("following")
    following_count = len(following)
    print(f'{username} is following {following_count} user(s)')
    
    following_not_followers = find_difference(following, followers)
    following_not_followers_count = len(following_not_followers)
    print(f'{username} has {following_not_followers_count} user(s) not following back')
    
    followers_not_following = find_difference(followers, following)
    followers_not_following_count = len(followers_not_following)
    print(f'{username} is not following {followers_not_following_count} user(s) back')
    
    return 'success'

    
# Retriev status
status = res.status_code

if status == 200:
    
    loader()
    
elif status == 404:
    print(f'404 bad request\nPage not found!\nAccount not found for user: {username}')
