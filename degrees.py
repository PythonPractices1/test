import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

QueueFrontier=[]
explored=[]
TempPath=[]
found=False
iter=0
def shortest_path(source, target):
    # global QueueFrontier
    # global explored
    # global TempPath
    # global found
    # global iter
    # """
    # Returns the shortest list of (movie_id, person_id) pairs
    # that connect the source to the target.

    # If no possible path, returns None.
    # """
    # if source==target:
    #     found=True
    #     iter-=1
    # else:
        
    #     ts=[]
    #     pid=[]
    #     QueueFrontier.append(source)
    #     ns=neighbors_for_person(source)
    #     nl=list(ns)
    #     ts.extend(nl)
    #     for movie_id, person_id in ts:
    #         if person_id not in explored:
    #             pid.append([person_id,movie_id])
    #     QueueFrontier.extend(neighbor_id for neighbor_id, movie_id in pid)
    #     explored.append(QueueFrontier[0])
    #     QueueFrontier=QueueFrontier[1:]
    #     TempPath.append([QueueFrontier[0],access_movie(QueueFrontier[0],pid)])
    #     iter+=1
    #     shortest_path(QueueFrontier[0],target)
    #     if found==False:
    #         TempPath.pop()
    #     iter-=1
    #     if iter==0 and TempPath:
    #         return TempPath
    #     elif iter==0 and not TempPath:
    #         return None
    if source == target:
        return []

    # Initialize the frontier with the starting position
    QueueFrontier = [[(None, source)]]
    explored = set()

    while QueueFrontier:
        # Get the next path from the frontier
        path = QueueFrontier.pop(0)
        node = path[-1][1]

        # If this node has not been explored yet
        if node not in explored:
            # Mark it as explored
            explored.add(node)

            # Check all neighbors
            for movie_id, neighbor in neighbors_for_person(node):
                new_path = path + [(movie_id, neighbor)]

                # If we found the target, return the path
                if neighbor == target:
                    return new_path[1:]

                # Otherwise, add the new path to the frontier
                QueueFrontier.append(new_path)

    # If we exhaust the frontier without finding the target, return None
    return None


    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def access_movie(person_id, arr):
    for neighbor_id, movie_id in arr:
        if neighbor_id == person_id:
            return movie_id


if __name__ == "__main__":
    main()
