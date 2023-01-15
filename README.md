# ScrapMooncell

Scraping Mooncell for the items required to level up each servant's skill and append skill levels.

What the script does:
1. Get all servants' name [here](https://fgo.wiki/w/%E8%8B%B1%E7%81%B5%E5%9B%BE%E9%89%B4/%E6%95%B0%E6%8D%AE).
2. Get servants' other info, e.g. rarity & class, [here](https://fgo.wiki/index.php?title=Widget:ServantsList/core&action=edit).
3. Visit each servant's page using names retrieved in step 1 and scrape the items required.
4. Save to a csv file.
