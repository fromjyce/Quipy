from neo4j import GraphDatabase

uri = "DATABASE_URI"
user = "DATABASE_USERNAME"
password = "DATABASE_PASSWORD"
driver = GraphDatabase.driver(uri, auth=(user, password))
def add_person(driver, name, age):
    with driver.session() as session:
        query = (
            "MERGE (p:Person {name: $name}) "
            "SET p.age = $age "
            "RETURN p"
        )
        result = session.run(query, name=name, age=age)
        return result.single()
def find_person(driver, name):
    with driver.session() as session:
        query = (
            "MATCH (p:Person {name: $name}) "
            "RETURN p.name AS name, p.age AS age"
        )
        result = session.run(query, name=name)
        return result.single()




add_person(driver, "Walter", 30)
person = find_person(driver, "Alice")
print(f"Found person: {person['name']}, Age: {person['age']}")
driver.close()
