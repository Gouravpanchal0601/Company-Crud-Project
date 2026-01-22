from playwright.sync_api import sync_playwright
import sys
import json
import re

MAIN_URL = "https://www.octoparse.com/blog/top-10-most-scraped-websites"

URLS=[
"https://www.octoparse.com/",
"https://www.octoparse.com/blog",
"https://www.octoparse.com/blog/tag/web-scraping",
"https://www.octoparse.com/blog/author/ansel-barrett",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#best-web-scraping-tool-for-anyone",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#what-types-of-websites-are-popular-for-scraping",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#e-commerce-sites",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#directories-sites-for-leads",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#social-media-sites",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#others",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-10-most-scraped-websites",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-10-craigslist",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-9-x-twitter",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-8-indeed",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-7-tripadvisor",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-6-google",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-5-yellowpages",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-4-etsy",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-3-linkedin",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-2-ebay",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#top-1-amazon",
"https://www.octoparse.com/blog/top-10-most-scraped-websites#final-thoughts",
"https://www.octoparse.com/blog/what-is-web-scraping-basics-and-use-cases",
"https://www.octoparse.com/template",
"https://www.octoparse.com/download/latest",
"https://www.octoparse.com/signup",
"https://www.octoparse.com/template/contact-details-scraper",
"https://www.octoparse.com/use-cases/e-commerce",
"https://www.semrush.com/website/top/",
"https://www.octoparse.com/scraping-templates/amazon-scraper",
"https://www.octoparse.com/blog/list-crawling-guide",
"https://www.octoparse.com/blog/how-to-extract-emails",
"https://www.octoparse.com/blog/how-to-extract-phone-number",
"https://www.octoparse.com/blog/how-to-find-social-media-profiles",
"https://www.octoparse.com/blog/is-web-crawling-legal-well-it-depends",
"https://www.octoparse.com/use-cases",
"https://www.craigslist.org/",
"https://www.octoparse.com/blog/how-to-scrape-data-from-craigslist",
"https://www.octoparse.com/template/craigslist-scraper",
"https://x.com/",
"https://www.businessofapps.com/data/twitter-statistics/",
"https://www.octoparse.com/blog/how-to-extract-data-from-twitter",
"https://www.octoparse.com/blog/website-crawler-sentiment-analysis",
"https://www.octoparse.com/template/twitter-scraper-by-account-url",
"https://www.indeed.com/",
"https://www.octoparse.com/blog/how-to-scrape-indeed-job-posting",
"https://www.octoparse.com/template/indeed-job-listing-scraper",
"https://www.tripadvisor.com/",
"https://www.octoparse.com/blog/web-scraping-tripadvisor",
"https://www.octoparse.com/template/tripadvisor-scraper-hotel-details",
"https://www.google.com/",
"https://www.octoparse.com/blog/export-google-maps-search-results-to-excel",
"https://www.octoparse.com/template/google-search-scraper",
"https://www.yellowpages.com/",
"https://www.octoparse.com/blog/yellow-pages-scraper",
"https://www.octoparse.com/template/yellow-page-scraper",
"https://www.etsy.com/",
"https://www.octoparse.com/blog/how-to-scrape-etsy",
"https://www.octoparse.com/template/etsy-product-scraper",
"https://www.linkedin.com/",
"https://www.octoparse.com/blog/scrape-linkedin-public-data",
"https://www.octoparse.com/template/linkedin-job-details-scraper",
"https://www.ebay.com/",
"https://www.octoparse.com/blog/how-to-scrape-ebay-listings",
"https://www.octoparse.com/template/ebay-scraper-store-listing",
"https://www.amazon.com/",
"https://www.octoparse.com/blog/scrape-product-data-from-amazon",
"https://www.octoparse.com/template/amazon-product-scraper-by-keywords",
"https://www.octoparse.com/download",
"https://www.octoparse.com/blog/scraping-data-from-website-to-excel",
"https://www.octoparse.com/blog/export-html-table-to-excel",
"https://www.octoparse.com/blog/9-best-free-web-crawlers-for-beginners",
"https://www.octoparse.com/blog/web-scraping-and-ecommerce-business",
"https://www.octoparse.com/blog/tag/octoparse",
"https://www.octoparse.com/blog/tag/e-commerce",
"https://www.octoparse.com/blog/tag/big-data",
"https://www.octoparse.com/blog/tag/lead-generation",
"https://www.octoparse.com/blog/tag/social-media",
"https://www.octoparse.com/blog/tag/real-estate",
"https://www.linkedin.com/cws/share?url=https://www.octoparse.com/blog/top-10-most-scraped-websites",
"https://twitter.com/intent/tweet?text=Top%2010%20Most%20Scraped%20Websites%20in%202025%20%7c%20Octoparse%20https://www.octoparse.com/blog/top-10-most-scraped-websites%20via%20@octoparse",
"https://www.octoparse.com/blog/top-sitemap-crawlers",
"https://www.octoparse.com/blog/top-30-free-web-scraping-software",
"https://www.octoparse.com/blog/top-data-extraction-tools",
"https://www.octoparse.com/blog/best-data-scraping-tools-for-2021"
]

DATE_PATTERNS = [
    r"\b(20\d{2}[-/]\d{1,2}[-/]\d{1,2})\b",
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December|"
    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+\d{1,2},\s*\d{4}\b",
    r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    r"\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b",
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
]

def find_date_in_text(text):
    if not text:
        return None
    for pat in DATE_PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return m.group(0)
    return None

def extract_headings_and_paragraphs(page):
    data = page.evaluate("""
    () => {
        function visibleText(el) {
            try {
                const style = window.getComputedStyle(el);
                if (style && (style.display === 'none' || style.visibility === 'hidden' || parseFloat(style.opacity) === 0)) {
                    return '';
                }
            } catch (e) {}
            return el.innerText ? el.innerText.trim() : '';
        }

        const mainContainer = document.querySelector("main, article, [role='main']") || document.body;
        const headingSelector = 'h1, h2, h3, h4, h5, h6, [role=heading]';
        const headings = Array.from(mainContainer.querySelectorAll(headingSelector));
        const results = [];

        for (const h of headings) {
            const headingText = visibleText(h);
            if (!headingText) continue;

            let el = h.nextElementSibling;
            const collected = [];

            while (el && !el.matches(headingSelector)) {
                const tag = el.tagName ? el.tagName.toUpperCase() : '';
                if (['P','DIV','LI','SECTION','ARTICLE','BLOCKQUOTE','PRE'].includes(tag)) {
                    const text = visibleText(el);
                    if (text) {
                        const cleaned = text.replace(/\\s+/g, ' ').trim();
                        if (cleaned) collected.push(cleaned);
                    }
                }
                el = el.nextElementSibling;
            }

            results.push({
                heading: headingText,
                paragraphs: collected
            });
        }
        return results;
    }
    """)
    return data

def scrape_url(page, url, id_val):
    try:
        # timeout ko high rakha aur networkidle ko load pe change kiya
        page.goto(url, wait_until="load", timeout=60000)
        page.wait_for_timeout(500)

        raw = extract_headings_and_paragraphs(page)

        parts = []
        for item in raw:
            heading = item.get("heading", "").strip()
            paragraphs = item.get("paragraphs", [])

            if not heading and not paragraphs:
                continue

            if heading:
                parts.append(heading)
            for para in paragraphs:
                if para:
                    parts.append(para)

        context_text = "\n\n".join(parts).strip()
        if not context_text:
            return None

        date_found = find_date_in_text(context_text)

        obj = {
            "id": id_val,
            "url_link": url,
            "context": context_text
        }
        if date_found:
            obj["date"] = date_found

        return obj

    except Exception as e:
        # agar page open nahi hota to skip karna
        print(f"⚠️ Skipping URL (error): {url}\n   Reason: {e}", file=sys.stderr)
        return None

def main(out_file="new_headings_and_paragraphs.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        all_results = []

        # First main URL
        main_result = scrape_url(page, MAIN_URL, 0)
        if main_result:
            all_results.append(main_result)

        # Other URLs
        for idx, link in enumerate(URLS, start=1):
            res = scrape_url(page, link, idx)
            if res:
                all_results.append(res)

        # Save JSON
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        # Print results
        for it in all_results:
            print(json.dumps(it, ensure_ascii=False, indent=2))
            print()

        context.close()
        browser.close()

if __name__ == "__main__":
    main()
