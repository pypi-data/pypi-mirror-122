from rl_inventory_api.constants import Colors, Certifies, Series, Tradeable, Rarities


class Item:
    def __init__(self, product_id, name, slot, paint, certification, certification_value, certification_label, quality,
                 crate, tradeable, amount, instance_id):
        self.product_id = int(product_id)
        self.name = name
        self.slot = slot
        self.paint = paint
        self.certification = certification
        self.certification_value = int(certification_value)
        self.certification_label = certification_label
        self.quality = quality
        self.crate = crate
        self.tradeable = tradeable
        self.amount = int(amount)
        self.instance_id = int(instance_id)

    def is_painted(self):
        return self.paint != Certifies.NONE

    def is_certificate(self):
        return self.certification_label != Certifies.NONE

    def is_tradeable(self):
        return self.tradeable == Tradeable.TRUE

    def is_non_crate(self):
        return self.crate == Series.NON_CRATE

    def is_uncommon(self):
        return self.quality == Rarities.UNCOMMON

    def is_rare(self):
        return self.quality == Rarities.RARE

    def is_very_rare(self):
        return self.quality == Rarities.VERY_RARE

    def is_import(self):
        return self.quality == Rarities.IMPORT

    def is_exotic(self):
        return self.quality == Rarities.EXOTIC

    def is_black_market(self):
        return self.quality == Rarities.BLACK_MARKET

    def is_limited(self):
        return self.quality == Rarities.LIMITED

    def is_ncr(self):
        return self.is_non_crate() and self.is_rare()

    def is_ncvr(self):
        return self.is_non_crate() and self.is_very_rare()

    def is_nci(self):
        return self.is_non_crate() and self.is_import()

    def is_nce(self):
        return self.is_non_crate() and self.is_exotic()


