import sqlite3
import os

# Database name
DB_NAME = 'plants.db'


def initialize_database():
    # If database exists, rename it as backup
    if os.path.exists(DB_NAME):
        backup_name = f'{DB_NAME}.backup'
        os.rename(DB_NAME, backup_name)
        print(f"Created backup of existing database as {backup_name}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create `plants` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            common_name TEXT NOT NULL,
            scientific_name TEXT NOT NULL,
            growth_conditions TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT
        )
    ''')

    # Create `knowledge_base` table with plant_type column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER NOT NULL,
            plant_type TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (plant_id) REFERENCES plants (plant_id)
        )
    ''')

    # Create `chat_history` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    # Insert initial data into `plants` table
    initial_plants = [
        ("Tulip", "Tulipa", "Full sun, well-drained soil, moderate watering",
         "A spring-blooming perennial flower known for its vibrant colors and cup-shaped blooms.",
         "https://example.com/tulip.jpg"),
        ("Sunflower", "Helianthus annuus", "Full sun, fertile soil, regular watering",
         "A tall annual flower with large, bright yellow blooms that follow the sun.",
         "https://example.com/sunflower.jpg"),
        ("Rose", "Rosa", "Partial to full sun, fertile soil, regular pruning",
         "A classic garden flower known for its beautiful blooms and sweet fragrance.",
         "https://example.com/rose.jpg"),
        ("Dandelion", "Taraxacum", "Full sun, any soil, low maintenance",
         "A hardy plant with medicinal properties.", "https://example.com/dandelion.jpg"),
        ("Daisy", "Bellis perennis", "Full sun, moist soil, regular watering",
         "A cheerful flower with white petals and a yellow center.", "https://example.com/daisy.jpg")
    ]
    cursor.executemany('''
        INSERT INTO plants (common_name, scientific_name, growth_conditions, description, image_url) 
        VALUES (?, ?, ?, ?, ?)
    ''', initial_plants)

    # Insert initial data into `knowledge_base` table with plant_type
    initial_knowledge_base = [
        # Tulip knowledge
        (1, "tulip", "How do I plant tulip bulbs?",
         "Plant tulip bulbs in fall, 4-6 inches deep, pointed end up, in well-drained soil. Space bulbs 4-6 inches apart."),
        (1, "tulip", "When do tulips bloom?",
         "Tulips typically bloom in spring, usually between March and May, depending on the variety and climate."),

        # Sunflower knowledge
        (2, "sunflower", "How tall do sunflowers grow?",
         "Sunflowers can grow anywhere from 3 to 15 feet tall, depending on the variety. Giant varieties can reach up to 15 feet!"),
        (2, "sunflower", "How long do sunflowers take to grow?",
         "Sunflowers typically take 80-120 days from planting to bloom, depending on the variety."),

        # Rose knowledge
        (3, "rose", "How often should I water roses?",
         "Roses need deep watering 2-3 times per week. Water at the base of the plant to prevent leaf diseases."),
        (3, "rose", "When is the best time to prune roses?",
         "Prune roses in late winter or early spring before new growth begins. Remove dead, damaged, or crossing branches."),

        # Dandelion knowledge
        (4, "dandelion", "What are the benefits of Dandelions?",
         "Dandelions have medicinal properties and can be used in teas and salads."),

        # daisy knowledge
        (5, "daisy", "Do Daisies require a lot of maintenance?", "Daisies are low-maintenance and thrive in most conditions."),
        (5, "daisy", "What are some common types of daisies?",
         "Common types of daisies include Shasta daisies, English daisies, and Gerbera daisies."),
        (5, "daisy", "Can daisies be grown indoors?",
         "While daisies can be grown indoors, they prefer outdoor conditions and may not thrive indoors for extended periods.")

    ]
    cursor.executemany('''
        INSERT INTO knowledge_base (plant_id, plant_type, question, answer) 
        VALUES (?, ?, ?, ?)
    ''', initial_knowledge_base)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_plant_info(plant_name):
    """
    Get information about a specific plant
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT common_name, scientific_name, growth_conditions, description, image_url
        FROM plants
        WHERE LOWER(common_name) = LOWER(?)
    ''', (plant_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'name': result[0],
            'scientific_name': result[1],
            'growth_conditions': result[2],
            'description': result[3],
            'image_url': result[4]
        }
    return None


# Run the initialization
if __name__ == "__main__":
    initialize_database()