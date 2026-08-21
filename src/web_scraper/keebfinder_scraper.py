from playwright.sync_api import sync_playwright

from src.database.repo.keebfinder_repo import save_keyboards

BASE_URL = "https://keeb-finder.com"

def scrape_keyboards() -> list[dict]:

    print(f"Extracting product links from {BASE_URL}")
    keyboard_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()
        page_number = 1

        while page_number < 49:
            full_URL = f"{BASE_URL}/keyboards?page={page_number}"
            page.goto(full_URL)
            
            keyboard_divs = page.locator('div.mt-2')


            for i in range(keyboard_divs.count()):
                keyboard_div = keyboard_divs.nth(i)
                kf_link = keyboard_div.locator('a.mb-1.font-h4.text-h4-md').get_attribute("href")
                title = keyboard_div.locator('a.mb-1.font-h4.text-h4-md').inner_text()
                v_link = keyboard_div.locator('a.underline.overflow-hidden.whitespace-nowrap').get_attribute("href")

                spec_divs = keyboard_div.locator('div.inline.text-body2-md')

                profile = mount = None

                wired = None
                wireless = None
                hotswap = None
                rgb = None
                white_led = None
                knob = None
                hall_effect = None
                rapid_trigger = None
                metal_case = None
                qmk = None
                via = None

                raw_specs = []
                
                for j in range(spec_divs.count()):
                    spec_div = spec_divs.nth(j)
                    spec = spec_div.inner_text()

                    raw_specs.append(spec)
                    
                    if "%" in spec:
                        profile = spec
                    elif "Numpad" in spec:
                        profile = "numpad"
                    elif "Macropad" in spec:
                        profile = "macropad"
                    elif "Wired" in spec:
                        wired = True
                    elif "Wireless" in spec:
                        wireless = True
                    elif "Hotswap" in spec:
                        hotswap = True
                    elif "RGB" in spec:
                        rgb = True
                    elif "White LEDs" in spec:
                        white_led = True
                    elif "Knob" in spec:
                        knob = True
                    elif "HE" in spec:
                        hall_effect = True
                    elif "Rapid Trigger" in spec:
                        rapid_trigger = True
                    elif "Alu Case" in spec or "Metal Case" in spec:
                        metal_case = True
                    elif "Mount" in spec:
                        mount = spec
                    elif "VIA" in spec:
                        via = True
                    elif "QMK" in spec:
                        qmk = True
                    
                keyboard = {
                    "source_url": kf_link,
                    "vendor_url" : v_link,

                    "title": title,
                    "price": None,
                    "keyboard_profile": profile,
                    "wired": wired,
                    "wireless": wireless,
                    "hotswap": hotswap,
                    "rgb": rgb,
                    "white_led": white_led,
                    "knob": knob,
                    "hall_effect": hall_effect,
                    "rapid_trigger": rapid_trigger,
                    "metal_case": metal_case,
                    "mount": mount,
                    "via_support": via,
                    "qmk_support": qmk,

                    "raw_specifications": raw_specs
                }

                keyboard_list.append(keyboard)
            page_number += 1
        browser.close()
    print(f"Keyboards Collected: {len(keyboard_list)}")

    save_keyboards(keyboard_list)

    return list(keyboard_list)


scrape_keyboards()