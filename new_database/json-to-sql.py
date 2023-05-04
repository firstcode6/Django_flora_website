import itertools
import json

# Opening JSON file help-pages
file = open('help-pages.json', encoding="utf8")
help_data = json.load(file)
print("The number of i18n stories=", len(help_data))

categories = list()
categories_i18n = list()
languages = list()
stories = list()
stories_i18n = list()
pages = list()
new_id_page = 0

geolocations = list()

#################################################################################
#################################################################################
#################################################################################
geolocation = {
    "model": "main_app.Geolocations",
    "pk": 1,
    "fields": {
        "name": "Germany"
    }
}
geolocations.append(geolocation)

geolocation = {
    "model": "main_app.Geolocations",
    "pk": 2,
    "fields": {
        "name": "France"
    }
}
geolocations.append(geolocation)

geolocation = {
    "model": "main_app.Geolocations",
    "pk": 3,
    "fields": {
        "name": "Austria"
    }
}
geolocations.append(geolocation)

geolocation = {
    "model": "main_app.Geolocations",
    "pk": 4,
    "fields": {
        "name": "Italy"
    }
}
geolocations.append(geolocation)
#################################################################################
#################################################################################
#################################################################################

for s in help_data:
    if 'mark_deleted' in s:
        continue

    language = {
        "model": "main_app.Languages",
        "fields": {
            "language": s["language"]
        }
    }
    languages.append(language)

    category = {
        "model": "main_app.Categories",
        "pk": 1,
        "fields": {
            "category_priority": s["category_priority"]
        }
    }
    categories.append(category)

    category_i18n = {
        "model": "main_app.Categories_i18n",
        "pk": 1,
        "fields": {
            "name": s["category"],
            "language": s["language"],
            "category": 1
        }
    }
    categories_i18n.append(category_i18n)

    category_id = 0
    if (s["category"] == 'News') or (s["category"] == 'Aktuelles'):
        category_id = 1

    if (s["category"] == 'Tips') or (s["category"] == 'Tipps'):
        category_id = 2

    if (s["fresh_after"] == ''):
        s["fresh_after"] = None

    if (s["fresh_before"] == ''):
        s["fresh_before"] = None

    if not 'hide_in_stories' in s:
        s["hide_in_stories"] = False

    story = {
        "model": "main_app.Stories",
        "pk": s["global_story_id"],
        "fields": {
            "category": category_id,
            "post_priority": s["post_priority"],
            "fresh_after": s["fresh_after"],
            "fresh_before": s["fresh_before"],
            "clients_eligible": s.get("clients_eligible"),
            "hide_in_stories": s["hide_in_stories"],
            "geolocations": s.get("geolocations"),
            "deleted": False,
        }
    }
    stories.append(story)

    story_i18n = {
        "model": "main_app.Stories_i18n",
        "pk": s["id"],
        "fields": {
            "story": s["global_story_id"],
            "language": s["language"],
            "title": s["title"],
            "subtitle": s["subtitle"],
            "title_icon": s["title_icon"],
            "title_image": s["title_image"]
        }
    }
    stories_i18n.append(story_i18n)

    num_order=0

    for p in s['pages']:
        new_id_page += 1
        num_order += 100
        page = {
            "model": "main_app.Pages",
            "pk": new_id_page,
            "fields": {
                "story_i18n": s["id"],
                "image": p["image"],
                "icon": p["icon"],
                "headline": p["headline"],
                "text": p["text"],
                "mark_deleted": False,
                "order": num_order,
            }
        }
        pages.append(page)


#################################################################################
#################################################################################
#################################################################################


def remove_duplicates(list_dupl, key='pk'):
    done = set()
    result = []
    for d in list_dupl:
        if d[key] not in done:
            done.add(d[key])  # note it down for further iterations
            result.append(d)
    return result


def remove_duplicates_fields(list_dupl, key):
    done = set()
    result = []
    for d in list_dupl:
        if d["fields"][key] not in done:
            done.add(d["fields"][key])  # note it down for further iterations
            result.append(d)
    return result


stories = remove_duplicates(stories)
languages = remove_duplicates_fields(languages, 'language')
categories = remove_duplicates_fields(categories, 'category_priority')
categories_i18n = remove_duplicates_fields(categories_i18n, 'name')

for i in range(len(categories)):
    categories[i]["pk"] = i + 1

for i in range(len(categories_i18n)):
    categories_i18n[i]["pk"] = i + 1

    if (categories_i18n[i]["fields"]["name"] == 'News') or (categories_i18n[i]["fields"]["name"] == 'Aktuelles'):
        categories_i18n[i]["fields"]["category"] = 1

    if (categories_i18n[i]["fields"]["name"] == 'Tips') or (categories_i18n[i]["fields"]["name"] == 'Tipps'):
        categories_i18n[i]["fields"]["category"] = 2

print("len languages=", len(languages))
print("len categories=", len(categories))
print("len categories_i18n=", len(categories_i18n))
print("len stories=", len(stories))
print("len stories_i18n=", len(stories_i18n))
print("len pages=", len(pages))



# The number of i18n stories= 231
# len languages= 19
# len categories= 2
# len categories_i18n= 4
# len stories= 77
# len stories_i18n= 223
# len pages= 1102
# 1427

#################################################################################
#################################################################################
#################################################################################

# with open('languages.json', 'w') as fp:
#     json.dump(languages, fp)
#
# with open('categories.json', 'w') as fp:
#     json.dump(categories, fp)
#
# with open('categories_i18n.json', 'w') as fp:
#     json.dump(categories_i18n, fp)
#
# with open('stories.json', 'w') as fp:
#     json.dump(stories, fp)
#
# with open('stories_i18n.json', 'w') as fp:
#     json.dump(stories_i18n, fp)

with open('pages.json', 'w') as fp:
    json.dump(pages, fp)

#################################################################################
#################################################################################
#################################################################################

all_list = list()
all_list.append(geolocations)
all_list.append(languages)
all_list.append(categories)
all_list.append(categories_i18n)
all_list.append(stories)
all_list.append(stories_i18n)
all_list.append(pages)

new_database = list(itertools.chain(*all_list))
print(len(new_database))

with open('new_database.json', 'w') as fp:
    json.dump(new_database, fp)
