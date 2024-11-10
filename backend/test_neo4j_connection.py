# test_neo4j_connection.py

from neo4j import GraphDatabase

def test_connection():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "W78HGMmr9LY6OHNhvK4onOAxvfZar_pl5XurZP47qHM"  # Replace with your password

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            print("Connection successful:", result.single()[0])
    except Exception as e:
        print("Connection failed:", e)
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()