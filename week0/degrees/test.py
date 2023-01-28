# Author   : Martin Užák <uzak+git@mailbox.org>
# Creation : 2022-10-14 01:19

from degrees import *

directory = "small"

# Load data from files into memory
print("Loading data...")
load_data(directory)
print("Data loaded.")

source = person_id_for_name("Kevin Bacon")
target = person_id_for_name("Mandy Patinkin")    # 3
#target = person_id_for_name("Valeria Golino")    # 2
#target = person_id_for_name("Demi Moore")   # 1
#target = source # 0

path = shortest_path(source, target)

if path is None:
    print("Not connected.")
else:
    degrees = len(path)
    print(f"{degrees} degrees of separation.")
    path = [(None, source)] + path
    print("path", path)
    for i in range(degrees):
        person1 = people[path[i][1]]["name"]
        person2 = people[path[i + 1][1]]["name"]
        movie = movies[path[i + 1][0]]["title"]
        print(f"{i + 1}: {person1} and {person2} starred in {movie}")

