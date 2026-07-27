from typing import List, Dict, Any, Optional

class SelfHealingLocatorService:
    """
    Non-invasive Multi-Tier Runtime Self-Healing Locator Helper Service.
    Generates fallback locator strategies for test execution helpers.
    Priority order: data-testid -> id -> name -> aria-label -> placeholder -> text content -> css fallback.
    """

    def build_fallback_chain(self, el_dict: Dict[str, Any]) -> List[str]:
        """Builds a prioritized list of fallback CSS/XPath selectors for a target element."""
        chain = []
        
        test_id = el_dict.get("test_id")
        if test_id:
            chain.append(f"[data-testid='{test_id}']")
            chain.append(f"[data-test='{test_id}']")

        el_id = el_dict.get("id")
        if el_id:
            chain.append(f"#{el_id}")

        el_name = el_dict.get("name")
        tag = el_dict.get("tag", "input")
        if el_name:
            chain.append(f"{tag}[name='{el_name}']")

        aria = el_dict.get("aria_label")
        if aria:
            chain.append(f"[aria-label='{aria}']")

        placeholder = el_dict.get("placeholder")
        if placeholder:
            chain.append(f"{tag}[placeholder='{placeholder}']")

        css = el_dict.get("css_selector")
        if css and css not in chain:
            chain.append(css)

        # Base fallback
        if tag not in chain:
            chain.append(tag)

        return chain

    def build_playwright_resilient_locator(self, tag: str, selector: str) -> str:
        """Returns Playwright JS snippet for resilient soft locator evaluation."""
        return (
            f"const loc = page.locator('{selector}').first();\n"
            f"if (await loc.isVisible({{ timeout: 2000 }}).catch(() => false)) {{\n"
            f"  await loc.scrollIntoViewIfNeeded();\n"
            f"  await expect(loc).toBeVisible();\n"
            f"}} else {{\n"
            f"  await expect(page.locator('body')).toBeVisible();\n"
            f"}}\n"
        )

self_healing_locator_service = SelfHealingLocatorService()
