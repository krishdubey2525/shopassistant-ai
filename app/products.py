from .database import get_connection


def create_products_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            brand TEXT NOT NULL,
            rating REAL NOT NULL,
            description TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_sample_products():
    connection = get_connection()

    products = [
        # -------------------------
        # LAPTOPS
        # -------------------------

        (
            "ApexBook Pro 15",
            "Laptop",
            54999,
            "Apex",
            4.5,
            "15.6 inch laptop with 16GB RAM and 512GB SSD, suitable for programming and daily productivity."
        ),

        (
            "TechNova Ultra 14",
            "Laptop",
            62999,
            "TechNova",
            4.6,
            "14 inch laptop with 16GB RAM and 512GB SSD, suitable for software development and multitasking."
        ),

        (
            "CodeMaster X15",
            "Laptop",
            69999,
            "CodeMaster",
            4.7,
            "15.6 inch performance laptop with 16GB RAM and 1TB SSD, designed for programming and development."
        ),

        (
            "ZenBook Lite 14",
            "Laptop",
            47999,
            "ZenBook",
            4.3,
            "Lightweight 14 inch laptop with 8GB RAM and 512GB SSD, suitable for students and office work."
        ),

        (
            "PowerCore Gaming 15",
            "Laptop",
            74999,
            "PowerCore",
            4.8,
            "15.6 inch laptop with 16GB RAM, 1TB SSD and dedicated graphics, suitable for gaming and development."
        ),

        # -------------------------
        # SMARTPHONES
        # -------------------------

        (
            "PixelMax 5G",
            "Smartphone",
            24999,
            "PixelMax",
            4.4,
            "5G smartphone with 8GB RAM and 128GB storage, designed for photography and everyday use."
        ),

        (
            "VisionPhone X",
            "Smartphone",
            29999,
            "Vision",
            4.7,
            "Premium smartphone with 12GB RAM, 256GB storage and an advanced camera system."
        ),

        (
            "NovaPhone 12",
            "Smartphone",
            19999,
            "Nova",
            4.2,
            "Affordable 5G smartphone with 8GB RAM and 128GB storage, suitable for everyday users."
        ),

        (
            "UltraMobile Pro",
            "Smartphone",
            34999,
            "UltraMobile",
            4.6,
            "High-performance smartphone with 12GB RAM and 256GB storage, suitable for gaming and multitasking."
        ),

        (
            "SmartOne 5G",
            "Smartphone",
            27999,
            "SmartOne",
            4.5,
            "5G smartphone with 8GB RAM and 256GB storage, offering a balanced camera and battery experience."
        ),

        # -------------------------
        # HEADPHONES
        # -------------------------

        (
            "SoundBeat Pro",
            "Headphones",
            4999,
            "SoundBeat",
            4.3,
            "Wireless headphones with active noise cancellation and long battery life."
        ),

        (
            "AudioMax ANC",
            "Headphones",
            6999,
            "AudioMax",
            4.6,
            "Wireless over-ear headphones with active noise cancellation and premium audio quality."
        ),

        (
            "BassCore Wireless",
            "Headphones",
            3499,
            "BassCore",
            4.2,
            "Affordable wireless headphones with enhanced bass and comfortable ear cushions."
        ),

        (
            "QuietZone Elite",
            "Headphones",
            8999,
            "QuietZone",
            4.8,
            "Premium wireless headphones with advanced noise cancellation and high-quality audio."
        ),

        # -------------------------
        # KEYBOARDS
        # -------------------------

        (
            "TypeMaster Mechanical",
            "Keyboard",
            3999,
            "TypeMaster",
            4.5,
            "Mechanical keyboard with RGB lighting and tactile switches, suitable for programming and gaming."
        ),

        (
            "KeyPro Wireless",
            "Keyboard",
            2499,
            "KeyPro",
            4.3,
            "Wireless keyboard with compact design and rechargeable battery for office and programming use."
        ),

        (
            "GameKeys RGB",
            "Keyboard",
            2999,
            "GameKeys",
            4.6,
            "RGB mechanical gaming keyboard with responsive switches and programmable keys."
        ),

        # -------------------------
        # MICE
        # -------------------------

        (
            "SpeedMouse X",
            "Mouse",
            1999,
            "SpeedMouse",
            4.4,
            "Wireless ergonomic mouse with adjustable DPI and comfortable grip for long working sessions."
        ),

        (
            "Precision Pro Mouse",
            "Mouse",
            2999,
            "Precision",
            4.7,
            "High-precision wireless mouse with adjustable DPI and programmable buttons."
        ),

        (
            "OfficeClick Basic",
            "Mouse",
            999,
            "OfficeClick",
            4.1,
            "Affordable wireless mouse designed for everyday office and student use."
        ),

        # -------------------------
        # MONITORS
        # -------------------------

        (
            "ViewMax 24",
            "Monitor",
            11999,
            "ViewMax",
            4.3,
            "24 inch Full HD monitor suitable for programming, office work and general productivity."
        ),

        (
            "GameView 27",
            "Monitor",
            19999,
            "GameView",
            4.6,
            "27 inch Full HD gaming monitor with high refresh rate and low response time."
        ),

        (
            "UltraDisplay 32",
            "Monitor",
            29999,
            "UltraDisplay",
            4.7,
            "32 inch high-resolution monitor suitable for development, content creation and multitasking."
        ),

        (
            "ProScreen 27 QHD",
            "Monitor",
            24999,
            "ProScreen",
            4.8,
            "27 inch QHD monitor with sharp image quality, suitable for programming and professional work."
        ),

        (
            "BudgetView 22",
            "Monitor",
            8999,
            "BudgetView",
            4.1,
            "22 inch Full HD monitor designed for students, office work and basic computing."
        )
    ]

    for product in products:
        existing = connection.execute(
            "SELECT id FROM products WHERE name = ?",
            (product[0],)
        ).fetchone()

        if existing is None:
            connection.execute("""
                INSERT INTO products
                (name, category, price, brand, rating, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, product)

    connection.commit()
    connection.close()


def get_all_products():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_product_by_id(product_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def search_products(query: str):
    connection = get_connection()

    search_term = f"%{query}%"

    rows = connection.execute("""
        SELECT * FROM products
        WHERE name LIKE ?
           OR category LIKE ?
           OR brand LIKE ?
           OR description LIKE ?
    """, (
        search_term,
        search_term,
        search_term,
        search_term
    )).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def filter_products(
    category: str | None = None,
    max_price: float | None = None,
    min_price: float | None = None,
    min_rating: float | None = None,
    brand: str | None = None
):
    connection = get_connection()

    query = "SELECT * FROM products WHERE 1=1"
    parameters = []

    if category:
        query += " AND LOWER(category) = LOWER(?)"
        parameters.append(category)

    if max_price is not None:
        query += " AND price <= ?"
        parameters.append(max_price)

    if min_price is not None:
        query += " AND price >= ?"
        parameters.append(min_price)

    if min_rating is not None:
        query += " AND rating >= ?"
        parameters.append(min_rating)

    if brand:
        query += " AND LOWER(brand) = LOWER(?)"
        parameters.append(brand)

    query += " ORDER BY rating DESC"

    rows = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]