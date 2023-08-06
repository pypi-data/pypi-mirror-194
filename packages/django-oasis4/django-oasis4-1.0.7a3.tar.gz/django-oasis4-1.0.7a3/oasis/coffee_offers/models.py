# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         23/02/23 16:02
# Project:      CFHL Transactional Backend
# Module Name:  models
# Description:
# ****************************************************************
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oasis.coffee_offers.lib import managers
from oasis.coffee_offers.lib.choices import CoffeeOffersStates
from oasis.coffee_offers.lib.validators import greater_than_today
from oasis.coffee_offers.lib.validators import validate_oasis_statuses
from oasis.models import CoffeeWareHouse
from oasis.models import Product
from zibanu.django.db import models


class StateMachine(models.Model):
    state = models.IntegerField(null=False, blank=False, verbose_name=_("State"), choices=CoffeeOffersStates.choices,
                                default=CoffeeOffersStates.NEW)
    from_state = models.IntegerField(null=True, blank=True, verbose_name=_("From State"),
                                     choices=CoffeeOffersStates.choices)
    oasis_state = models.CharField(max_length=1, null=False, blank=False, verbose_name=_("Oasis State"))
    oasis_status = models.CharField(max_length=1, null=False, blank=False, verbose_name=_("Oasis Status"),
                                    validators=[validate_oasis_statuses])
    notify_user = models.BooleanField(default=True, null=False, blank=False, verbose_name=_("Notify User"))
    notify_coffee_area = models.BooleanField(default=False, null=False, blank=False,
                                             verbose_name=_("Notify Coffee Area"))
    notify_legal_area = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Notify Legal Area"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("state", "from_state"), name="UNQ_CoffeeOffer_StateMachine")
        ]


class Offer(models.DatedModel):
    # Field List
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="offers",
                             related_query_name="user")
    contract = models.IntegerField(blank=False, null=False, verbose_name=_("Contract No"))
    warehouse = models.ForeignKey(CoffeeWareHouse, null=False, blank=False, verbose_name=_("Warehouse"),
                                  on_delete=models.PROTECT, related_query_name="warehouses")
    product = models.ForeignKey(Product, null=False, blank=False, verbose_name=_("Product"), on_delete=models.PROTECT)
    kg_offered = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False,
                                     verbose_name=_("Kg Offered"))
    kg_received = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False, default=0,
                                      verbose_name=_("Kg Received"))
    status = models.IntegerField(choices=CoffeeOffersStates.choices, default=CoffeeOffersStates.NEW, null=False,
                                 blank=False, verbose_name=_("Status"))
    delivery_date = models.DateField(blank=False, null=False, verbose_name=_("Delivery Date"),
                                     validators=[greater_than_today])
    # Set default Manager
    objects = managers.Offer()

    @property
    def is_active(self) -> bool:
        return self.status in [CoffeeOffersStates.SIGNED, CoffeeOffersStates.PARTIAL]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("contract",), name="UNQ_Offer_Contract")
        ]

