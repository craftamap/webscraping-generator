import requests
import yattag
import typing
import dataclasses
import os
import random
from pathlib import Path
import json
from pydantic import BaseModel

class User(BaseModel):
    name: str
    mail: str
    phone: str
    city: str
    image: str
    uuid: str


def get_users() -> typing.List[User]:
    # Get 100 random user
    response = requests.get("https://randomuser.me/api/?results=100&nat=de")
    data = response.json()
    users: typing.List[User] = []
    for user_data in data["results"]:
        name = f"{user_data['name']['first']} {user_data['name']['last']}"
        mail = user_data["email"]
        phone = user_data["phone"]
        city = user_data["location"]["city"]
        image = user_data["picture"]["large"]
        uuid = user_data["login"]["uuid"]
        users.append(User(name=name, mail=mail, phone=phone, city=city, image=image, uuid=uuid))

    return users


def generate_overview(users: typing.List[User]) -> typing.Dict[str, str]:
    css = """
        body {
            font-family: sans-serif;
        }

        ul {
            padding: 0;
        }
        li {
            display: block;
            padding: 8px 16px;
            border: solid 1px #bbbbbb;
            border-bottom: none;
            width: 400px;
        }
        li:first-of-type{
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        li:last-of-type{
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
            border-bottom: solid 1px #bbbbbb;
        }
        .name {
            display: block;
            font-size: 1.2em;
        }
        footer a {
            padding: 0 20px;
        }
    """
    pages: typing.List[str] = {}
    no_pages = int(len(users)/10)
    for idx in range(no_pages):
        doc, tag, text = yattag.Doc().tagtext()
        with tag('html'):
            with tag("head"):
                with tag("meta", charset="utf-8"):
                    pass
                with tag("style"):
                    text(css)
            with tag('body'):
                with tag('header'):
                    with tag('h1'):
                        text("Fabians Webscraping Adventure")
                with tag('content'):
                    with tag('h2'):
                        text("Users")
                    with tag('ul'):
                        for x in users[idx*10:10+idx*10]:
                            with tag('li'):
                                with tag('span', klass="name"):
                                    text(x.name)
                                with tag("a", klass="profile", href=f"users/{x.uuid}.html"):
                                    text("Profil")
                with tag('footer'):
                    if idx != 0:
                        with tag("a", href=f"{idx}.html", klass="prev"):
                            text("<")
                    with tag("a", href="#"):
                        text(idx+1)
                    if idx != no_pages-1:
                        with tag("a", href=f"{idx+2}.html", klass="next"):
                            text(">")
        pages[str(idx+1)] = doc.getvalue()
    return pages

def generate_profiles(users: typing.List[User]) -> typing.Dict[str, str]:
    css = """
        body {
            font-family: sans-serif;
        }
        .content {
            width: 600px;
            margin: 0 auto;
        }
        h3 {
            text-align: center;
        }
        img {
            margin: 0 auto;
            display: block;
            border-radius: 50%;
        }
        .holy-user {
            color: gold;
        }

        .hidden {
            display: none;
        }
    """
    holy_user = random.choice(users)
    print("HOLY USER: ",  holy_user)
    profiles = {}
    for user in users:
        doc, tag, text = yattag.Doc().tagtext()
        with tag('html'):
            with tag("head"):
                with tag("meta", charset="utf-8"):
                    pass
                with tag("style"):
                    text(css)
            with tag('body'):
                with tag('header'):
                    with tag('h1'):
                        text("Fabians Webscraping Adventure")
                with tag('content'):
                    with tag('h2'):
                        text("User")
                    with tag("div", klass="content"):
                        with tag("img", src=user.image):
                            pass
                        with tag("h3", klass="name holy-user" if user == holy_user else "name"):
                            text(user.name)
                        with tag("p"):
                            with tag("b"):
                                text("E-Mail: ")
                            with tag("span", klass="mail"):
                                text(user.mail)
                        with tag("p"):
                            with tag("b"):
                                text("Phone Number: ")
                            with tag("span", klass="phone"):
                                text(user.phone)
                        with tag("p"):
                            with tag("b"):
                                text("City: ")
                            with tag("span", klass="city"):
                                text(user.city)
                        with tag("p", klass="hidden"):
                            with tag("b"):
                                text("Flag: ")
                            with tag("span", klass="flag"):
                                text("OLA-WEBSCRAPING-nS7KugKGCE")
        profiles[user.uuid] = doc.getvalue()


    return profiles


class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, User):
                return o.dict()
            return super().default(o)


def main():
    Path("dist").mkdir(exist_ok=True)
    Path("dist/users").mkdir(exist_ok=True)
    users = get_users()
    overview_pages = generate_overview(users)
    with open("dist/users.json", "w") as output:
        json.dump(users, output, cls=EnhancedJSONEncoder)
    for idx, overview_page in overview_pages.items():
        with open("dist/"+idx+".html", "w") as output:
            output.write(overview_page)
    profiles = generate_profiles(users)
    for idx, overview_page in profiles.items():
        with open("dist/users/"+idx+".html", "w") as output:
            output.write(overview_page)


if __name__ == "__main__":
    main()
