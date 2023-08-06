# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/03/23 12:04
# Project:      CFHL Transactional Backend
# Module Name:  offer
# Description:
# ****************************************************************
from zibanu.django.db import models
from typing import Any


class Offer(models.Manager):
    def get_balance(self, user: Any) -> float:
        qs = self.filter(user__exact=user).all()
        balance = 0
        if qs is not None:
            for offer in qs:
                balance = balance + (offer.kg_offered - offer.kg_received)
        return balance

    def get_active_offers(self, user: Any) -> list:
        qs = self.filter(user__exact=user).all()
        offer_list = [offer for offer in qs if offer.is_active]
        return offer_list
