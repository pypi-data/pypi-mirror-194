from bs4 import BeautifulSoup as bs
import requests as rq


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
    details = {}
    print(f'Account found for user: {username}')

    
    details['repos'] = repos
    print(f'{username} has {len(repos)} repositories')
    
    followers = github_follow("followers")
    details['followers'] = followers

    followers_count = len(followers)
    details['followers_count'] = followers_count
    print(f'{username} has {followers_count} followers')
    
    following = github_follow("following")
    details['following'] = following

    following_count = len(following)
    details['following_count'] = following_count
    print(f'{username} is following {following_count} user(s)')
    
    following_not_followers = find_difference(following, followers)
    details['following_not_followers'] = following_not_followers

    following_not_followers_count = len(following_not_followers)
    details['following_not_followers_count'] = following_not_followers_count
    print(f'{username} has {following_not_followers_count} user(s) not following back')
    
    followers_not_following = find_difference(followers, following)
    details['followers_not_following'] = followers_not_following

    followers_not_following_count = len(followers_not_following)
    print(f'{username} is not following {followers_not_following_count} user(s) back')
    return details
    

def check():
    global username
    username = input('Enter github Username: ').strip()
    res = rq.get(f'https://github.com/{username}')

    # Retriev status
    status = res.status_code
    if status == 200:
        check_repo()
        loader()
    elif status == 404:
        print(f'404 bad request\nPage not found!\nAccount not found for user: {username}')


def check_repo():
    # <span title="24" data-view-component="true" class="Counter">24</span>
    link = f"https://github.com/{username}?tab=repositories"
    req = bs(rq.get(link).text, 'lxml')
    items = req.find_all('h3', class_="wb-break-all")

    global repos
    repos = []
    for item in items:
        a = item.find('a')
        repos.append(a.text.strip())
    
check()