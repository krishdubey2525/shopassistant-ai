from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .products import (
    create_products_table,
    add_sample_products,
    get_all_products,
    get_product_by_id,
    search_products,
    filter_products
)

from .models import (
    Product,
    ProductSearchResponse,
    ChatRequest,
    ChatResponse
)

from .ai_service import (
    ask_ai,
    extract_product_requirements,
    choose_best_product,
    generate_final_response
)


app = FastAPI(
    title="ShopAssist AI",
    description="AI-powered e-commerce assistant",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# STARTUP
# --------------------------------------------------

@app.on_event("startup")
def startup():

    create_products_table()
    add_sample_products()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to ShopAssist AI",
        "status": "running"
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# GET ALL PRODUCTS
# --------------------------------------------------

@app.get(
    "/products",
    response_model=list[Product]
)
def products():

    return get_all_products()


# --------------------------------------------------
# SEARCH PRODUCTS
# --------------------------------------------------

@app.get(
    "/products/search",
    response_model=ProductSearchResponse
)
def search(query: str):

    results = search_products(query)

    return {
        "products": results,
        "total": len(results)
    }


# --------------------------------------------------
# FILTER PRODUCTS
# --------------------------------------------------

@app.get(
    "/products/filter",
    response_model=list[Product]
)
def filter_product_list(
    category: str | None = None,
    max_price: float | None = None,
    min_price: float | None = None,
    min_rating: float | None = None,
    brand: str | None = None
):

    return filter_products(
        category=category,
        max_price=max_price,
        min_price=min_price,
        min_rating=min_rating,
        brand=brand
    )


# --------------------------------------------------
# GET PRODUCT BY ID
# --------------------------------------------------

@app.get(
    "/products/{product_id}",
    response_model=Product
)
def product(product_id: int):

    result = get_product_by_id(product_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return result


# --------------------------------------------------
# GENERAL AI CHAT
# --------------------------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat_endpoint(request: ChatRequest):

    response = ask_ai(request.message)

    return {
        "response": response,
        "product": None
    }


# --------------------------------------------------
# AI PRODUCT RECOMMENDATION
# --------------------------------------------------

@app.post(
    "/recommend",
    response_model=ChatResponse
)
def recommend_endpoint(request: ChatRequest):

    # ----------------------------------------------
    # 1. Extract requirements
    # ----------------------------------------------

    requirements = extract_product_requirements(
        request.message
    )


    # ----------------------------------------------
    # 2. Filter products from database
    # ----------------------------------------------

    products = filter_products(
        category=requirements.category,
        max_price=requirements.max_price,
        min_price=requirements.min_price,
        min_rating=requirements.min_rating,
        brand=requirements.brand
    )


    # ----------------------------------------------
    # 3. Validate products
    # ----------------------------------------------

    validated_products = []

    for product in products:

        # Category validation
        if requirements.category:

            if (
                product["category"].lower()
                != requirements.category.lower()
            ):
                continue


        # Maximum price validation
        if requirements.max_price is not None:

            if product["price"] > requirements.max_price:
                continue


        # Minimum price validation
        if requirements.min_price is not None:

            if product["price"] < requirements.min_price:
                continue


        # Rating validation
        if requirements.min_rating is not None:

            if product["rating"] < requirements.min_rating:
                continue


        # Brand validation
        if requirements.brand:

            if (
                product["brand"].lower()
                != requirements.brand.lower()
            ):
                continue


        validated_products.append(product)


    # ----------------------------------------------
    # 4. No matching products
    # ----------------------------------------------

    if not validated_products:

        return {
            "response": (
                "I couldn't find a suitable product "
                "matching your requirements."
            ),
            "product": None
        }


    # ----------------------------------------------
    # 5. AI selects from verified products
    # ----------------------------------------------

    selected_id = choose_best_product(
        request.message,
        validated_products
    )


    # ----------------------------------------------
    # 6. Validate AI selection
    # ----------------------------------------------

    selected_product = None

    for product in validated_products:

        if product["id"] == selected_id:

            selected_product = product
            break


    # ----------------------------------------------
    # 7. Safety fallback
    # ----------------------------------------------

    if selected_product is None:

        selected_product = validated_products[0]


    # ----------------------------------------------
    # 8. Generate AI explanation
    # ----------------------------------------------

    response = generate_final_response(
        request.message,
        selected_product,
        requirements
    )


    # ----------------------------------------------
    # 9. Return response + product data
    # ----------------------------------------------

    return {
        "response": response,
        "product": selected_product
    }