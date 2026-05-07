# selenium-python-starter

A drop-in Selenium 4 + pytest scaffold with the page-object model.

## What this repo does

- Wires up Selenium 4 with `webdriver-manager` as a fallback. Selenium 4
  ships with Selenium Manager which auto-matches driver binaries — both
  paths work out of the box.
- Page-object model in `pages/` (`BasePage`, `HomePage`).
- Headless-first config; flip with `HEADED=1`.
- Browser switching via `BROWSER=chrome|firefox|edge` env var.
- Auto-screenshots on failure (hooked in `conftest.py`).
- Network-free unit tests of page-object logic so you can run
  `pytest -m headless` without a browser.

## Project layout

- `pages/` - page objects.
- `tests/test_pages_unit.py` - mock-driver unit tests (no browser).
- `tests/test_home_e2e.py` - browser-driven smoke tests.
- `conftest.py` - driver fixture, browser switching, screenshot-on-failure.
- `pytest.ini` - markers (`smoke`, `regression`, `headless`, `flaky`).
- `Dockerfile` - includes Chrome so the suite is self-contained in CI.
- `docker-compose.yml` - run via Docker; commented hint for Selenium Grid.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
cp .env.example .env

pytest -m headless                 # fast, no browser needed
pytest -m smoke                    # full smoke incl. browser launch
pytest                             # everything
```

Or with Docker (Chrome bundled in the image):

```bash
docker compose run --rm test
```

## Common commands

| Command | Description |
|---|---|
| `pytest` | Run all tests. |
| `pytest -m smoke` | Smoke subset. |
| `pytest -m headless` | No-browser unit tests of page-object logic. |
| `BROWSER=firefox pytest` | Run against Firefox. |
| `HEADED=1 pytest` | Show the browser. |

## Playwright vs Selenium

Playwright is generally a better choice for new test suites: faster, more
reliable auto-waiting, built-in tracing. Selenium still earns its place when:

- You need a specific browser/version combination Playwright doesn't ship
  (older IE-mode, niche Edge configurations, Safari on Linux).
- You already have a corporate Selenium Grid you must use.
- You're testing a desktop browser-based app that requires native automation
  hooks Playwright doesn't expose.

If neither applies, prefer `playwright-python-starter` next door.

## Adding a new page object

1. Create `pages/my_page.py` extending `BasePage`. Define locators as class
   constants (`(By.CSS_SELECTOR, "...")` tuples).
2. Export it from `pages/__init__.py`.
3. Add a fixture in `conftest.py`:
   ```python
   @pytest.fixture
   def my_page(driver, base_url):
       return MyPage(driver, base_url)
   ```

## Selenium Grid

Uncomment the `selenium-hub` service in `docker-compose.yml`, then have your
fixture build a `webdriver.Remote` pointing at `http://selenium-hub:4444/wd/hub`.
The page objects don't change — they take any `WebDriver` instance.
