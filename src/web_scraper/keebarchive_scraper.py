from playwright.sync_api import sync_playwright
from datetime import datetime, timezone

from src.database.repo.keebarchive_repo import save_keycaps, save_switches

BASE_URL = "https://keebarchive.com"

SWITCH_TITLE_BLACK_LIST = [
    "Stabilizer",
    "Benefit Section",
    "Calendar",
    "Opener",
    "Fidget",
    "Springs",
    "Fidgets",
    "Container",
]

def get_product_links(URL) -> list:
    print(f"Extracting product links from {URL}")
    product_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()
        page.goto(URL)

        next_button = page.locator(
            'button:has(svg.lucide-chevron-right)'
        )

        while True:
            links = page.locator('a[href^="/product/"]')

            for i in range(links.count()):
                href = links.nth(i).get_attribute("href")

                if href:
                    product_links.add(href)

            next_button = page.locator(
                'button:has(svg.lucide-chevron-right)'
            )

            if next_button.is_disabled():
                break

            old_first_link = links.first.get_attribute("href")

            next_button.click()

            page.wait_for_function(
                """
                old_link => {
                    const firstProduct =
                        document.querySelector(
                            'a[href^="/product/"]'
                        );

                    return firstProduct &&
                           firstProduct.getAttribute("href")
                           !== old_link;
                }
                """,
                arg=old_first_link
            )

        browser.close()
    print(f"Product Links Count: {len(product_links)}")
    return list(product_links)

def extract_switch_data() -> list[dict]:
    print(f"Retrieving Switch data...")
    product_links = get_product_links("https://keebarchive.com/switches")
    switches = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()


        for link in product_links:
            full_url = BASE_URL + link
            page.goto(full_url)

            tech_spec_divs = page.locator('div.flex.items-center.justify-between.border-b.py-2.last\\:border-0')

            title_locator = page.locator("h1.tracking-tight")

            if title_locator.count() == 0:
                continue

            title = title_locator.inner_text().strip()


            if not title: continue

            if any(
                word.lower() in title.lower()
                for word in SWITCH_TITLE_BLACK_LIST
            ):
                print(f"Skipping blacklisted product: {title}")
                continue

            price_locator = page.locator('p.text-3xl', has_text = "$")
            price = (price_locator.inner_text().strip() if price_locator.count() > 0 else None)
            
            prose_locator = page.locator('div.prose')
            prose = (prose_locator.inner_text().strip() if prose_locator.count() > 0 else None)

            switch_type = feel = actuation = travel_dist = pins = fac_lubed = None
            
            for i in range(tech_spec_divs.count()):
                spec_div = tech_spec_divs.nth(i)
                spans = spec_div.locator("span")

                if spans.count() < 2:
                    continue

                spec = spans.nth(0).inner_text()
                
                if spec == "Switch Type":
                    switch_type = spans.nth(1).inner_text().strip()
                elif spec == "Feel":
                    feel = spans.nth(1).inner_text().strip()
                elif spec == "Actuation Force":
                    actuation = spans.nth(1).inner_text().strip()
                elif spec == "Travel Distance":
                    travel_dist = spans.nth(1).inner_text().strip()
                elif spec == "Pins":
                    pins = spans.nth(1).inner_text().strip()
                elif spec == "Factory Lubed":
                    fac_lubed = spans.nth(1).locator("svg.lucide-check").count() > 0

            switch = {
                "source": "keebarchive",
                "source_url": full_url,
                "extracted_at": datetime.now(timezone.utc).isoformat(),

                "title": title,
                "price": price,
                "prose": prose,
                "switch_type": switch_type,
                "feel": feel,
                "actuation_force" : actuation,
                "travel_distance" : travel_dist,
                "pins" : pins,
                "factory_lubed": fac_lubed,
            }

            switches.append(switch)
        browser.close()
    print(f"Switch Count: {len(switches)}")
    return switches

def extract_keycap_data() -> list[dict]:
    print(f"Retrieving keycap data...")
    keycap_links = get_product_links("https://keebarchive.com/keycaps")
    keycaps = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for link in keycap_links:
            full_url = BASE_URL + link
            page.goto(full_url)

            tech_spec_divs = page.locator('div.flex.items-center.justify-between.border-b.py-2.last\\:border-0')

            profile = number_of_keys = None

            title_locator = page.locator("h1.tracking-tight")

            if title_locator.count() == 0:
                continue

            title = title_locator.inner_text().strip()

            if not title:
                continue

            material = "Aluminum" if "Aluminum" in title else None
            artisan = "Artisan" in title 

            price_locator = page.locator('p.text-3xl', has_text = "$")
            price = (price_locator.inner_text().strip() if price_locator.count() > 0 else None)
            
            prose_locator = page.locator('div.prose')
            prose = (prose_locator.inner_text().strip() if prose_locator.count() > 0 else None)
            
            for i in range(tech_spec_divs.count()):
                spec_div = tech_spec_divs.nth(i)
                spans = spec_div.locator("span")

                if spans.count() < 2:
                    continue

                spec = spans.nth(0).inner_text()
                
                if material is None and spec == "Material":
                    material = spans.nth(1).inner_text().strip()
                elif spec == "Profile":
                    profile = spans.nth(1).inner_text().strip()
                elif spec == "Keys":
                    number_of_keys = spans.nth(1).inner_text().strip()
                

            keycap = {
                "source": "keebarchive",
                "source_url": full_url,
                "extracted_at": datetime.now(timezone.utc).isoformat(),

                "title": title,
                "price": price,
                "prose": prose,
                "material": material,
                "profile": profile,
                "number_of_keys" : number_of_keys,
                "artisan": artisan
            }

            keycaps.append(keycap)
            i += 1
        browser.close()
    print(f"Keycap Count: {len(keycaps)}")
    return keycaps


            



