"""Record a tight Family Recipes walkthrough — no dead air."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://kelly-nwb.github.io/family-recipes/"
OUT_DIR = Path(__file__).resolve().parents[1] / "demo"
OUT_DIR.mkdir(exist_ok=True)
DEST = OUT_DIR / "walkthrough-raw.webm"


def pause(page, ms: int = 600) -> None:
    page.wait_for_timeout(ms)


def smooth_scroll(page, y: int, ms: int = 500) -> None:
    page.evaluate(
        """({y, ms}) => new Promise(done => {
          const start = window.scrollY;
          const t0 = performance.now();
          const step = (t) => {
            const p = Math.min(1, (t - t0) / ms);
            const ease = 1 - Math.pow(1 - p, 3);
            window.scrollTo(0, start + (y - start) * ease);
            if (p < 1) requestAnimationFrame(step); else done();
          };
          requestAnimationFrame(step);
        })""",
        {"y": y, "ms": ms},
    )
    page.wait_for_timeout(ms + 80)


def main() -> None:
    if DEST.exists():
        DEST.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(OUT_DIR),
            record_video_size={"width": 1280, "height": 720},
            color_scheme="light",
        )
        page = context.new_page()
        page.set_default_timeout(15000)

        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_selector("#recipe-grid .recipe-card, #collections .collection-hero")
        pause(page, 400)

        # Poem — quick pan (nostalgia beat)
        page.evaluate("window.scrollTo(0, 0)")
        pause(page, 900)
        smooth_scroll(page, 220, 450)

        # Prescott collection
        prescott = page.locator('.collection-hero[data-collection-id="prescott-cousins"]')
        prescott.click(position={"x": 400, "y": 100})
        pause(page, 500)
        smooth_scroll(page, 520, 400)

        # Search + open recipe in one motion
        search = page.locator("#search")
        search.click()
        search.fill("lasagna")
        pause(page, 450)
        summary = page.locator(".recipe-card:not(.pending) summary").first
        summary.scroll_into_view_if_needed()
        pause(page, 200)
        summary.click()
        pause(page, 700)
        smooth_scroll(page, page.evaluate("window.scrollY") + 160, 350)

        # Low carb chip
        search.fill("")
        pause(page, 150)
        page.locator('button[data-collection="low-carb"]').click()
        pause(page, 500)

        # All + cover flip
        page.locator('button[data-collection="all"]').click()
        pause(page, 200)
        smooth_scroll(page, 300, 350)
        cover = page.locator('.cover-frame[data-collection="prescott-cousins"]').first
        cover.click()
        pause(page, 550)

        page.close()
        if page.video:
            page.video.save_as(DEST)
            print(f"Recording -> {DEST}")
        context.close()
        browser.close()

    if not DEST.exists():
        raise SystemExit("Recording failed.")


if __name__ == "__main__":
    main()