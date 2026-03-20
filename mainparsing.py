import requests


print("=== Задание 1 ===")
url_github = "https://api.github.com/search/repositories"
params_github = {"q": "html"}

response_github = requests.get(url_github, params=params_github)
print("Статус-код:", response_github.status_code)
print("JSON-ответ:")
print(response_github.json())
print()


print("=== Задание 2 ===")
url_posts = "https://jsonplaceholder.typicode.com/posts"
params_posts = {"userId": 1}

response_posts = requests.get(url_posts, params=params_posts)
print("Статус-код:", response_posts.status_code)
print("Записи userId=1:")
print(response_posts.json())
print()


print("=== Задание 3 ===")
post_data = {"title": "foo", "body": "bar", "userId": 1}

response_create = requests.post(url_posts, json=post_data)
print("Статус-код:", response_create.status_code)
print("Ответ после POST:")
print(response_create.json())
