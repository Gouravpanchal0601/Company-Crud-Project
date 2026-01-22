from playwright.sync_api import sync_playwright

def extract_body_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="load")

        links = page.evaluate(
            """
            (() => {
                // Try common selectors for main content
                const container = document.querySelector(
                  'main, article, [role="main"], .post-content, .blog-post, .content, .entry-content, .entry'
                );

                // If we found a content container, take anchors from it,
                // otherwise take all anchors but exclude those inside header/footer.
                const anchors = container
                  ? Array.from(container.querySelectorAll('a'))
                  : Array.from(document.querySelectorAll('a'));

                const filtered = anchors.filter(a => {
                    const hrefAttr = a.getAttribute('href');
                    if (!hrefAttr) return false;
                    const hrefTrim = hrefAttr.trim();
                    // exclude javascript/mail/tel links and empty fragments
                    if (
                      hrefTrim === '' ||
                      hrefTrim.startsWith('javascript:') ||
                      hrefTrim.startsWith('mailto:') ||
                      hrefTrim.startsWith('tel:')
                    ) return false;

                    // If no container, exclude anchors that live inside header/footer
                    if (!container) {
                        let el = a;
                        while (el) {
                            const tag = (el.tagName || '').toLowerCase();
                            if (tag === 'header' || tag === 'footer') return false;
                            el = el.parentElement;
                        }
                    }
                    return true;
                }).map(a => {
                    // normalize to absolute URL
                    try {
                        return new URL(a.getAttribute('href'), location.href).href;
                    } catch (e) {
                        return null;
                    }
                }).filter(Boolean);

                // remove duplicates and return
                return Array.from(new Set(filtered));
            })()
            """
        )

        browser.close()
        return links

if __name__ == "__main__":
    url = "https://www.octoparse.com/blog/top-10-most-scraped-websites"
    body_links = extract_body_links(url)
    for i, link in enumerate(body_links, start=1):
        print(f"{i}. {link}")




# from playwright.sync_api import sync_playwright

# def extract_links(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url,timeout=60000)

#         links = page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")

#         browser.close()
#         return links

# if __name__ == "__main__":
#     url = "https://www.octoparse.com/blog/top-10-most-scraped-websites"
#     all_links = extract_links(url)
    
#     for idx, link in enumerate(all_links, start=1):
#         print(f"{idx}. {link}")
