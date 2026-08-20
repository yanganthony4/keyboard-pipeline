from playwright.sync_api import sync_playwright
from datetime import datetime, timezone

BASE_URL = "https://keeb-finder.com"

def get_keyboard_links() -> list[dict]:
    print(f"Extracting product links from {BASE_URL}")
    keyboard_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page_number = 1

        while page_number < 2:
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
                wired = wireless = hotswap = rgb = white_led = knob = hall_effect = rapid_trigger = metal_case = qmk = via = False
                
                for j in range(spec_divs.count()):
                    spec_div = spec_divs.nth(j)
                    spec = spec_div.inner_text()
                    
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
                    "source": "keebfinder",
                    "source_url": kf_link,
                    "vendor_url" : v_link,
                    "extracted_at": datetime.now(timezone.utc).isoformat(),

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
                    "qmk_support": qmk
                }

                keyboard_list.append(keyboard)
            page_number += 1
        browser.close()
    print(f"Keyboard Count: {len(keyboard_list)}")
    return list(keyboard_list)
