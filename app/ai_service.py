import json
import re

from ollama import chat

from .models import ProductRequirements


MODEL_NAME = "llama3.2:3b"


# --------------------------------------------------
# CATEGORY NORMALIZATION
# --------------------------------------------------

def normalize_category(text):

    if not text:
        return None

    value = text.lower().strip()

    # Laptop
    if any(word in value for word in [
        "laptop",
        "laptops",
        "notebook",
        "notebooks"
    ]):
        return "Laptop"

    # Smartphone
    if any(word in value for word in [
        "smartphone",
        "smartphones",
        "smartphon",
        "phone",
        "phones",
        "mobile",
        "mobiles"
    ]):
        return "Smartphone"

    # Headphones
    if any(word in value for word in [
        "headphone",
        "headphones",
        "headset",
        "headsets",
        "earphone",
        "earphones",
        "earbud",
        "earbuds"
    ]):
        return "Headphones"

    # Keyboard
    if any(word in value for word in [
        "keyboard",
        "keyboards"
    ]):
        return "Keyboard"

    # Mouse
    if any(word in value for word in [
        "mouse",
        "mice"
    ]):
        return "Mouse"

    # Monitor
    if any(word in value for word in [
        "monitor",
        "monitors",
        "display",
        "displays"
    ]):
        return "Monitor"

    return None


# --------------------------------------------------
# DIRECT CATEGORY DETECTION
# --------------------------------------------------

def detect_category(user_message):

    category = normalize_category(user_message)

    if category:
        return category

    return None


# --------------------------------------------------
# AI
# --------------------------------------------------

def ask_ai(message: str):

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ShopAssist AI, a helpful e-commerce "
                    "shopping assistant."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# REQUIREMENT EXTRACTION
# --------------------------------------------------

def extract_product_requirements(
    user_message: str
) -> ProductRequirements:

    # ----------------------------------------------
    # IMPORTANT:
    # Detect category directly in Python.
    # This prevents the LLM from misunderstanding
    # words such as "smartphon".
    # ----------------------------------------------

    detected_category = detect_category(user_message)


    prompt = f"""
Extract shopping requirements from the customer's request.

Customer request:
{user_message}

Return ONLY valid JSON:

{{
    "category": null,
    "max_price": null,
    "min_price": null,
    "min_rating": null,
    "brand": null,
    "search_query": null
}}

Rules:

- category must be one of:
  Laptop, Smartphone, Headphones, Keyboard, Mouse, Monitor

- max_price is the maximum budget.

- min_price is the minimum price if mentioned.

- min_rating is the minimum rating if mentioned.

- brand is the requested brand if mentioned.

- search_query contains other important requirements.

- Convert Indian currency to numbers.
  Example: ₹70,000 = 70000

- If something is not mentioned, use null.

- Return JSON only.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract structured shopping requirements. "
                    "Return JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"].strip()

    try:

        # Remove markdown JSON fences if Ollama adds them.
        content = re.sub(
            r"```json|```",
            "",
            content
        ).strip()

        data = json.loads(content)

        # ------------------------------------------
        # Python category takes priority
        # ------------------------------------------

        if detected_category:

            data["category"] = detected_category

        else:

            data["category"] = normalize_category(
                data.get("category")
            )

        return ProductRequirements(**data)

    except (json.JSONDecodeError, ValueError):

        return ProductRequirements(
            category=detected_category,
            search_query=user_message
        )


# --------------------------------------------------
# CHOOSE BEST PRODUCT
# --------------------------------------------------

def choose_best_product(
    user_message: str,
    products: list
):

    if not products:
        return None

    product_information = ""

    for product in products:

        product_information += f"""
Product ID: {product['id']}
Name: {product['name']}
Category: {product['category']}
Price: ₹{product['price']:.0f}
Brand: {product['brand']}
Rating: {product['rating']}
Description: {product['description']}

"""

    prompt = f"""
Customer request:

{user_message}

The following products have already been VERIFIED by the application:

{product_information}

Choose the BEST product for the customer.

Return ONLY the Product ID.

Do not return an explanation.
Do not return a price.
Do not return any other text.
Do not invent a product.

Example:

6
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You select the best product from a verified list. "
                    "Return only the Product ID."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"].strip()

    try:

        # Extract first integer in case model adds text.
        match = re.search(r"\d+", result)

        if match:
            return int(match.group())

    except ValueError:
        pass

    return products[0]["id"]


# --------------------------------------------------
# FINAL RESPONSE
# --------------------------------------------------

def generate_final_response(
    user_message: str,
    selected_product: dict,
    requirements: ProductRequirements
):

    if selected_product is None:

        return (
            "I couldn't find a suitable product matching "
            "your requirements."
        )

    price = selected_product["price"]
    rating = selected_product["rating"]

    facts = []

    if requirements.max_price is not None:

        if price <= requirements.max_price:

            facts.append(
                f"The product is within your "
                f"₹{requirements.max_price:,.0f} budget."
            )

        else:

            facts.append(
                f"The product is above your "
                f"₹{requirements.max_price:,.0f} budget."
            )


    if requirements.min_rating is not None:

        if rating >= requirements.min_rating:

            facts.append(
                f"It meets your minimum rating requirement "
                f"of {requirements.min_rating}."
            )

        else:

            facts.append(
                f"It does not meet your minimum rating "
                f"requirement of {requirements.min_rating}."
            )


    verified_facts = "\n".join(
        f"- {fact}"
        for fact in facts
    )


    prompt = f"""
Customer request:

{user_message}

Selected product:

Name: {selected_product['name']}
Category: {selected_product['category']}
Price: ₹{price:,.0f}
Brand: {selected_product['brand']}
Rating: {rating}
Description: {selected_product['description']}

VERIFIED FACTS:

{verified_facts}

Write a short, professional recommendation.

Rules:

- Recommend the selected product.
- Use the exact product information.
- Use the VERIFIED FACTS exactly.
- Do not calculate prices or ratings yourself.
- Do not contradict the verified facts.
- Do not invent specifications.
- Do not mention other products.
"""

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ShopAssist AI. "
                    "Write a concise recommendation using "
                    "verified facts."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]