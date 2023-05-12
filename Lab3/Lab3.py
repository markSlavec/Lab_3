import json
import pandas as pd
import pickle
import xml.etree.ElementTree as ET
import collections
import csv

#1.1


# Загрузка файла contributors_sample.json.
with open('contributors_sample.json') as f:
    contributors = json.load(f)

# Отображение информацию о первых трех пользователях
print("(1.1):")
for i in range(3):
    user = contributors[i]
    print(f"User {i+1}:")
    print(f"Username: {user['username']}")
    print(f"Name: {user['name']}")
    print(f"Sex: {user['sex']}")
    print(f"Address: {user['address']}")
    print(f"Mail: {user['mail']}")
    print(f"Jobs: {user['jobs']}")
    print(f"ID: {user['id']}")
    print()



#1.2


# Извлечение уникальных доменов электронной почты
domains = set()
for user in contributors:
    domain = user['mail'].split('@')[1]
    domains.add(domain)

# Print unique email domains
print("(1.2):")
print("Unique email domains:")
for domain in domains:
    print(domain)
print()





#1.3


def search_by_username(username):
    # Поиск пользователя с заданным именем пользователя
    for user in contributors:
        if user['username'] == username:
            # Отображение информации о пользователе 
            print(f"Username: {user['username']}")
            print(f"Name: {user['name']}")
            print(f"Sex: {user['sex']}")
            print(f"Address: {user['address']}")
            print(f"Mail: {user['mail']}")
            print(f"Jobs: {user['jobs']}")
            print(f"ID: {user['id']}")
            return

    # Если пользователь не был найден, вызовается исключение ValueError.
    raise ValueError(f"No user with username {username} found")





#1.4



# Подсчет женщин и мужчин 
men_count = 0
women_count = 0
for user in contributors:
    if user['sex'] == 'M':
        men_count += 1
    elif user['sex'] == 'F':
        women_count += 1

# Отображение результатов
print("(1.4):")
print(f"Men: {men_count}")
print(f"Women: {women_count}")
print()





#1.5


# список словарей, содержащий нужные столбцы
contributors_list = []
for user in contributors:
    contributor_dict = {'id': user['id'], 'username': user['username'], 'sex': user['sex']}
    contributors_list.append(contributor_dict)

# DataFrame из списка словарей
contributors_df = pd.DataFrame(contributors_list)

# Print DataFrame
print("(1.5):")
print(contributors_df)
print()





#1.6


# Загрузка данных из CSV-файла в pandas DataFrame
recipes_df = pd.read_csv('recipes_sample.csv')

# Загрузка данные из файла JSON в pandas DataFrame
with open('contributors_sample.json') as f:
    contributors_data = json.load(f)
contributors_df = pd.DataFrame(contributors_data)

# Объединение: рецепты и кадры данных участников в столбце «contributor_id».
merged_df = pd.merge(recipes_df, contributors_df, on='id', how='left')

# Подсчет количества строк в объединенном DataFrame, в которых отсутствует информация о человеке.
missing_info_count = merged_df[merged_df['username'].isnull()].shape[0]

print(f'{missing_info_count} people are missing information.')
print()



################


#2.1

job_positions = {}

for contributor in contributors:
    for job in contributor['jobs']:
        job_positions.setdefault(job, []).append(contributor['username'])





#2.2


with open('job_people.pickle', 'wb') as f:
    pickle.dump(job_positions, f)

with open('job_people.json', 'w') as f:
    json.dump(job_positions, f, indent=2)





#2.3

with open('job_people.pickle', 'rb') as f:
    job_positions = pickle.load(f)

print("(2.3):")
for job, usernames in job_positions.items():
    print(f"{job}: {usernames}")
print()
print("#################################################################################")
print("#################################################################################")
print("#################################################################################")




##########


#3.1

# Parse the XML file
tree = ET.parse('steps_sample.xml')
root = tree.getroot()

recipe_steps = {}

# Loop over all the recipes in the XML file
for recipe in root.findall('recipe'):
    recipe_id = recipe.find('id').text
    steps = []
    # Loop over all the steps in the recipe
    for step in recipe.find('steps').findall('step'):
        steps.append(step.text)
    # Add the recipe and its steps to the dictionary
    recipe_steps[recipe_id] = steps

with open('steps_sample.json', 'w') as f:
    json.dump(recipe_steps, f)




#3.2

num_steps_dict = collections.defaultdict(list)

for recipe in root.findall('recipe'):
    recipe_id = recipe.find('id').text
    steps = recipe.findall('steps/step')
    num_steps = len(steps)
    num_steps_dict[num_steps].append(recipe_id)





#3.3

time_recipes = []

for recipe in root.findall('recipe'):
    recipe_id = recipe.find('id').text
    steps = recipe.findall('steps/step')
    for step in steps:
        if step.get('has_minutes') or step.get('has_hours'):
            time_recipes.append(recipe_id)
            break




#3.4


recipes = []
with open('recipes_sample.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        recipes.append(row)

steps = {}
tree = ET.parse('steps_sample.xml')
root = tree.getroot()
for recipe in root.findall('recipe'):
    recipe_id = recipe.find('id').text
    steps[recipe_id] = len(recipe.find('steps'))

for recipe in recipes:
    if recipe['n_steps'] == '':
        recipe_id = recipe['id']
        if recipe_id in steps:
            recipe['n_steps'] = steps[recipe_id]






#3.5



df = pd.read_csv('recipes_sample.csv')

if df['n_steps'].isnull().sum() > 0:

    tree = ET.parse('steps_sample.xml')

    recipes = tree.findall('recipe')

    id_to_steps = {}
    for recipe in recipes:
        id_to_steps[recipe.find('id').text] = len(recipe.findall('steps/step'))

    for i, row in df.iterrows():
        if pd.isnull(row['n_steps']):
            recipe_id = str(row['id'])
            if recipe_id in id_to_steps:
                df.loc[i, 'n_steps'] = id_to_steps[recipe_id]

df['n_steps'] = df['n_steps'].astype(int)

df.to_csv('recipes_sample_with_filled_nsteps.csv', index=False)