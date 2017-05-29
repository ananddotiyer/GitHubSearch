#!/usr/bin/env python
import datetime
from operator import getitem
import requests
import json

input_args = {
    "q": "model based testing",
    "language": "Python"
}

language = "python"

meta_data = [
    ("full_name",),
    ("owner","login"),
    ("description",),
    ("svn_url",),
    ("homepage",),
    ("updated_at",),
    ("language",),
    ("watchers",)
]

def get_inputs (input_args):
    if input_args["language"]:
        prompt_language = "Your default language is {0}.\n" \
                            "Hit Enter to continue, or key in another language [Eg.Java]".format (input_args["language"])
        default_language = raw_input (prompt_language)
        if not default_language == "":
            input_args["language"] = default_language

    input_args["q"] = raw_input ("What are you searching for? [Eg.model based testing]: ")
    return input_args

def print_header (f):
    for columns in meta_data:
        f.write ('"%s",' %(str(columns)))
    f.write ("\n")

def print_column (f, print_this):
    if type (print_this) == int:
        print_this = str (print_this)
    elif print_this is None:
        print_this = ''
    else:
        print_this = print_this.encode('utf-8')
    f.write ('"%s",' %(print_this))

#main program

input_args = get_inputs (input_args)

f = open ("{0}_{1}.csv".format (input_args["q"], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')), "w")

#Add pagination like &page=2
keys = input_args.keys()
values = input_args.values()
url = "https://api.github.com/search/repositories?{0}='{1}'+{2}:{3}&sort=stars&order=desc".format (keys[0], values[0], keys[1], values[1])

response = json.loads (requests.get (url).text)

print_header(f)

for repo in response["items"]:
    for columns in meta_data:
        columns = list(columns)
        print_column (f, reduce(getitem, columns, repo))
    f.write ("\n")

f.close ()