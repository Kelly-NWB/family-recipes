"""Add sister's Prized cookbook collection to recipes.json / recipes.js."""
from __future__ import annotations

import json
from pathlib import Path

PRIZED_RECIPES = [
    {
        "id": "prized-marinara-sauce",
        "title": "Marinara Sauce",
        "collection": "prized",
        "sourcePage": 3,
        "category": "sauce",
        "ingredients": [
            "6–8 cloves garlic, chopped",
            "3–4 Tbsp olive oil",
            "1 Tbsp red pepper flakes",
            "Garlic salt, to taste",
            "1–2 Tbsp basil (or ~8 fresh basil leaves)",
            "2 cans quality tomato sauce",
            "1 can whole peeled tomatoes, crushed",
        ],
        "steps": [
            "Combine garlic, olive oil, red pepper flakes, garlic salt and basil in a pan. Let soften and cook on low heat.",
            "Add tomato sauce and crushed whole tomatoes.",
            "Simmer at least 20 minutes. Enjoy!",
        ],
        "notes": [
            "This sauce is the base to all of my red sauce recipes — lasagna, tomato soup, spaghetti, etc.",
            "Most pasta and Italian recipes here won't have exact measurements. I rarely measure except when baking. I love garlic — dabble until it suits your taste.",
        ],
        "pending": False,
    },
    {
        "id": "prized-spicy-shrimp-pasta",
        "title": "Spicy Shrimp Pasta",
        "collection": "prized",
        "sourcePage": 4,
        "category": "main",
        "ingredients": [
            "Garlic (approx. 1 head), chopped",
            "Garlic salt",
            "Dried red pepper flakes (approx. 2 tsp)",
            "Olive oil (approx. 4–6 Tbsp)",
            "Shrimp, peeled (30–40 pieces)",
            "Half and half (approx. 2 cups)",
            "Asiago or Romano cheese, grated (approx. 1 cup)",
            "Pasta (3–4 servings)",
        ],
        "steps": [
            "Bring water to boil in a pan large enough for pasta — it should float and move freely, never packed tight.",
            "In a saucepan heat olive oil, chopped garlic and red pepper flakes. Cook until garlic begins to soften and spices release their aroma.",
            "Pour in half and half; reduce heat to simmer. Once the cream sauce has reduced, season with garlic salt and more red pepper flakes as needed. Add grated cheese and stir constantly as it melts.",
            "Begin cooking pasta; let sauce continue to simmer on low. When pasta is nearly done, add raw shrimp to the cream sauce and cook until pink and curled.",
            "Drain pasta and stir into cream sauce. Let simmer a few more minutes so pasta is coated. Garnish with grated cheese and serve immediately.",
        ],
        "pending": False,
    },
    {
        "id": "prized-tomato-bisque",
        "title": "Tomato Bisque",
        "collection": "prized",
        "sourcePage": 5,
        "category": "main",
        "ingredients": [
            "8 cloves garlic, chopped",
            "2 Tbsp red pepper flakes",
            "1 Tbsp basil",
            "Butter",
            "2 cans whole stewed tomatoes, pureed",
            "1 can tomato sauce",
            "2 cups half and half",
            "½ cup cream",
        ],
        "steps": [
            "Sauté garlic, red pepper flakes and basil in butter until garlic has softened.",
            "Add pureed stewed tomatoes and tomato sauce. Simmer about 15 minutes.",
            "Add half and half and cream. Simmer until thick — about 20–30 minutes.",
            "Serve with crusty bread or hearty grilled cheese sandwiches.",
        ],
        "notes": [
            "Leftover soup is best warmed on the stovetop, not the microwave — cream tends to separate when microwaved.",
        ],
        "pending": False,
    },
    {
        "id": "prized-blue-cheese-stuffed-burgers",
        "title": "Blue Cheese Stuffed Burgers",
        "collection": "prized",
        "sourcePage": 6,
        "category": "main",
        "ingredients": [
            "Blue cheese crumbles",
            "Hamburger",
            "Coarsely chopped pepper",
            "Buns and condiments",
        ],
        "steps": [
            "Make two thin patties and indent the middle of both to create a small well for the cheese. Add cheese, then put the two patties together. Crimp edges to seal in the cheese.",
            "Generously apply cracked black pepper to both sides of the patty.",
            "BBQ or broil to your liking.",
        ],
        "pending": False,
    },
    {
        "id": "prized-baked-brie",
        "title": "Baked Brie",
        "collection": "prized",
        "sourcePage": 8,
        "category": "appetizer",
        "ingredients": [
            "1 block of brie",
            "4–6 cloves garlic, chopped",
            "Toasted bread",
            "Olive oil",
        ],
        "steps": [
            "Cut a criss-cross pattern in the top of the brie.",
            "Spread chopped garlic on top, drizzle with olive oil.",
            "Bake at 400° for about 15 minutes, or until the cheese is oozing and the garlic is golden.",
        ],
        "notes": [
            "A favorite comfort food — easy and best with toasted bread. Sometimes I add sliced Granny Smith apples and grapes to the plate.",
            "Delicious with red wine or dark beer.",
        ],
        "pending": False,
    },
    {
        "id": "prized-fondant-balls",
        "title": "Grandma Prescott's Fondant Balls",
        "collection": "prized",
        "sourcePage": 9,
        "author": "Grandma Prescott",
        "category": "candy",
        "ingredients": [
            "2 lbs powdered sugar",
            "2 sticks butter, melted",
            "1 bag coconut (smaller size)",
            "1 cup chopped walnuts",
            "1 can sweetened condensed milk",
            "1 bag semi-sweet chocolate chips",
            "1 square paraffin wax",
        ],
        "steps": [
            "Combine sugar, butter, milk, coconut and nuts. Mix by hand.",
            "Roll into small balls — approximately ½ inch in diameter. Chill.",
            "Melt chocolate and paraffin over low heat. Dip chilled balls to coat and place on waxed paper.",
        ],
        "notes": [
            "Oh those beloved coconut balls — the pure joy of receiving Grandma Prescott's candy.",
        ],
        "pending": False,
    },
    {
        "id": "prized-southern-creamy-pralines",
        "title": "Southern Creamy Pralines",
        "collection": "prized",
        "sourcePage": 10,
        "category": "candy",
        "ingredients": [
            "2 cups sugar",
            "1 cup light cream",
            "¾ tsp baking soda",
            "1½ Tbsp butter",
            "2 cups pecan halves",
        ],
        "steps": [
            "Combine sugar and soda in a heavy saucepan; mix well.",
            "Stir in cream and bring to a boil over medium heat, stirring constantly.",
            "Reduce heat and cook to soft-ball stage (234°). Mixture will caramelize slightly.",
            "Remove from heat. Add butter and stir in pecans.",
            "Beat until thick, 2–3 minutes. Drop from tablespoon onto waxed paper.",
            "If candy becomes too stiff, add 1 Tbsp hot water. Makes 30 pralines.",
        ],
        "pending": False,
    },
    {
        "id": "prized-herman-starter",
        "title": "Herman Starter",
        "collection": "prized",
        "sourcePage": 11,
        "category": "bread",
        "ingredients": [
            "1 package dry yeast dissolved in 1 cup warm water",
            "2 cups all-purpose flour",
            "½ cup white sugar",
            "Feeding: ½ cup white sugar, 1 cup flour, 1 cup milk",
        ],
        "steps": [
            "Mix yeast water, flour and sugar. Do not use metal bowls or spoons.",
            "Cover loosely and store at room temperature. Stir daily.",
            "On day 5, refrigerate. Continue stirring daily.",
            "On day 10, the starter is ready for baking. Divide in half — keep one half, give the other away with feeding instructions.",
            "To feed: add ½ cup sugar, 1 cup flour and 1 cup milk. Stir well.",
            "On day 15, starter is again ready to bake or share.",
        ],
        "pending": False,
    },
    {
        "id": "prized-herman-cake",
        "title": "Herman Cake",
        "collection": "prized",
        "sourcePage": 12,
        "category": "dessert",
        "ingredients": [
            "CAKE: 2 cups Herman sourdough starter",
            "2/3 cup vegetable oil",
            "2 eggs",
            "2 cups all-purpose flour",
            "1½ tsp ground cinnamon",
            "½ tsp baking soda",
            "2 tsp baking powder",
            "1 cup white sugar",
            "FILLING: 1 cup packed brown sugar",
            "3 Tbsp all-purpose flour",
            "1 tsp ground cinnamon",
            "¼ cup butter, melted",
            "GLAZE: ½ cup butter",
            "¼ cup milk",
            "1 cup packed brown sugar",
        ],
        "steps": [
            "Combine wet cake ingredients, then add dry ingredients one cup at a time, mixing well each time.",
            "Combine filling ingredients and set aside.",
            "Pour batter into a greased 9×13 pan. Dollop filling on batter and swirl through with a sharp knife.",
            "Bake at 350° for 30–40 minutes.",
            "For glaze: bring butter, milk and brown sugar to a slow boil; cook 3 minutes.",
            "Top cake with glaze while still warm. Best when slightly warm.",
        ],
        "pending": False,
    },
    {
        "id": "prized-german-chocolate-cake",
        "title": "German Chocolate Cake",
        "collection": "prized",
        "sourcePage": 13,
        "category": "dessert",
        "ingredients": [
            "4-oz package Baker's Sweetened Chocolate",
            "½ cup boiling water",
            "1 cup butter",
            "2 cups sugar",
            "4 egg yolks",
            "4 egg whites",
            "1 tsp vanilla",
            "2½ cups sifted cake flour",
            "1 tsp baking soda",
            "1 cup buttermilk",
        ],
        "steps": [
            "Melt chocolate in ½ cup boiling water.",
            "Cream butter and sugar until fluffy. Add egg yolks one at a time while mixing. Add chocolate.",
            "Add milk and flour in alternating ½-cup increments.",
            "Whip egg whites in a clean dry metal bowl until stiff peaks form. Slowly fold into chocolate mixture — do not stir.",
            "Grease and flour two 8-inch round pans. Bake at 350° for 30–40 minutes.",
        ],
        "pending": False,
    },
    {
        "id": "prized-german-chocolate-frosting",
        "title": "German Chocolate Frosting",
        "collection": "prized",
        "sourcePage": 14,
        "category": "sauce",
        "ingredients": [
            "1 cup sugar",
            "3 beaten egg yolks",
            "½ cup butter",
            "1 tsp vanilla",
            "1⅓ cup Baker's Angel Flake Coconut",
            "1 cup chopped pecans",
        ],
        "steps": [
            "Mix milk, sugar, vanilla, butter and egg yolks in saucepan.",
            "Cook over medium heat 12 minutes, stirring constantly.",
            "Remove from heat. Add pecans and coconut. Cool frosting completely.",
            "After cake has cooled, remove rounds from pans. Use frosting to layer cakes and frost top and sides.",
        ],
        "pending": False,
    },
    {
        "id": "prized-killer-coffee-cake",
        "title": "Killer Coffee Cake",
        "collection": "prized",
        "sourcePage": 15,
        "category": "dessert",
        "ingredients": [
            "CAKE: ½ cup brown sugar",
            "½ cup granulated sugar",
            "1 stick soft butter",
            "2 eggs",
            "¼ cup sour cream",
            "½ cup milk",
            "1½ cups flour",
            "½ Tbsp baking powder",
            "1 Tbsp vanilla",
            "FILLING: ½ cup brown sugar",
            "½ Tbsp cinnamon",
            "TOPPING: 2 sticks butter, melted",
            "½ cup granulated sugar",
            "½ cup brown sugar",
            "2½ cups flour",
            "½ Tbsp cinnamon",
        ],
        "steps": [
            "Mix sugars and butter until light and fluffy. Add eggs one at a time. Add sour cream and beat until just incorporated.",
            "Starting with flour, add flour and milk in alternating pours — about ⅓ of each at a time. Scrape down bowl sides.",
            "Mix brown sugar and cinnamon for filling.",
            "Place dry topping ingredients in a large bowl; mix with hands. Pour in melted butter and stir until fully incorporated and crumble forms clumps.",
            "Spread half the batter in a greased 9×13 pan. Sprinkle filling evenly. Dollop remaining batter on top and spread gently.",
            "Sprinkle crumble topping over batter. Swirl filling through batter with a sharp knife.",
            "Bake at 350° for 40–50 minutes.",
        ],
        "pending": False,
    },
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "recipes.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))

    data["recipes"] = [r for r in data["recipes"] if r.get("collection") != "prized"]
    data["recipes"].extend(PRIZED_RECIPES)

    prized_collection = {
        "id": "prized",
        "title": "Prized",
        "subtitle": "The Cookbook",
        "author": "Christy C.",
        "cover": "assets/prized-cover.png",
        "type": "prized",
        "source": "SnapSis-c00kbook",
        "recipeCount": len(PRIZED_RECIPES),
    }

    data["collections"] = [c for c in data["collections"] if c["id"] != "prized"]
    data["collections"].append(prized_collection)

    payload = json.dumps(data, indent=2, ensure_ascii=False)
    data_path.write_text(payload + "\n", encoding="utf-8")
    (root / "data" / "recipes.js").write_text(
        f"window.RECIPE_DATA = {payload};\n", encoding="utf-8"
    )
    print(f"Added Prized collection with {len(PRIZED_RECIPES)} recipes.")


if __name__ == "__main__":
    main()