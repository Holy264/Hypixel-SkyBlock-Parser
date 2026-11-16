# 2 слой работает с repository 

import asyncio
from collections import defaultdict
from core.utils.normalize_item_name import normalize_item_name

import logging
from core.hypixel_client import HypixelClient,extract_item_meta
from repositories.auction_repo import AuctionRepository

logger = logging.getLogger(__name__)

    
class AuctionService:
    PAGE_DELAY = 0.3
    def __init__(self, client: HypixelClient, repo: AuctionRepository):
        self.client = client
        self.repo = repo
        
    async def fetch_and_save(self):
        try:
            first_page = await self.client.get_auctions(page=0)
        except Exception:
            logger.exception("[auction] первая страница недоступна")
            return 0 
        total_pages = first_page.get('totalPages', 1)
        all_auctions = first_page.get('auctions', [])
        
        logger.info("[auction] totalPages=%d", total_pages)
        
        for page in range(1, total_pages):
            await asyncio.sleep(self.PAGE_DELAY)
            try: 
                page_data = await self.client.get_auctions(page=page)
                
            except Exception:
                logger.exception("[auction] страница %d не загрузилась, пропускаем", page)
                continue
            
            all_auctions.extend(page_data.get('auctions', []))
            logger.info(
                "[auction] page %d/%d, накоплено %d",
                page + 1, total_pages, len(all_auctions))
        
        lowest_bins = {}
        listings_count = defaultdict(int)
        
        for auction in all_auctions:
            if auction.get("bin") is not True:
                continue
            name = normalize_item_name(auction.get("item_name")) 
            price = auction.get("starting_bid")
            if not name or price is None:
                continue
            tier = auction.get("tier")
            tier = str(tier).strip().upper() if tier else ''

            key = (name, tier)
            listings_count[key] += 1
            if key not in lowest_bins or price < lowest_bins[key]["price"]:
                lowest_bins[key] = {"price": price, "tier": tier}
            
            
        bin_count = sum(1 for a in all_auctions if a.get('bin') is True)      
              
        logger.info(
            "[auction] BIN=%d, уникальных предметов=%d",
            bin_count, len(lowest_bins),
        )
        
        to_save = [
        {
            "item_name": name,
            "tier": tier,
            "lowest_bin": int(data["price"]),
            "listings_count": listings_count[(name, tier)],
        }
        for (name, tier), data in lowest_bins.items()
        ]
        
        logger.info(f"[auction] к сохранению: {len(to_save)}")
        
        await self.repo.save_prices(to_save)
        return len(to_save)
        
        
    async def fetch_and_save_sales(self):
        """Продажи из /skyblock/auctions_ended."""
        try:
            ended = await self.client.get_auctions_ended()
        except Exception as e:
            logger.warning("[auction] auctions_ended недоступен: %s", e)
            return 0 
        
        sales = ended.get('auctions', [])
        logger.info(f"[auction] продаж получено из API: {len(sales)}")
        
        to_save = []
        for sale in sales:
            auction_uuid = sale.get('auction_id') or sale.get('uuid')
            if not auction_uuid:
                continue
            
            item_bytes = sale.get('item_bytes')
            if not item_bytes:
                continue
            meta = extract_item_meta(item_bytes)
            if meta is None:
                logger.debug("[auction] NBT не распарсился: %s", auction_uuid)
                continue
            raw_name, tier = meta
            name = normalize_item_name(raw_name)
            if not name:
                continue
            
            price = sale.get('price')
            if price is None:
                continue
            
            bin_val = sale.get("bin")
            if bin_val is None:
                logger.debug("[auction] sale без bin: %s", auction_uuid)
                continue
                        
            to_save.append({
                'auction_uuid': auction_uuid,
                'item_name': name,
                'tier': tier,
                'price': int(price),
                'bin': bin_val
            })
        logger.info(f"[auction] к сохранению продаж: {len(to_save)}")
        
        saved = await self.repo.save_sales(to_save)
        return saved