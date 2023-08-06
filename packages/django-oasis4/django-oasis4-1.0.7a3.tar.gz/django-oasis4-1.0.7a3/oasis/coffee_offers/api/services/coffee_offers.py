# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         1/03/23 10:10
# Project:      CFHL Transactional Backend
# Module Name:  coffee_offers
# Description:
# ****************************************************************
from coffee_price.models import Price
from coffee_price.lib.serializers import PriceListSerializer
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from oasis.coffee_offers import models
from oasis.coffee_offers.api.serializers import CoffeeWareHouseListSerializer
from oasis.lib.choices import CustomerType
from oasis.models import AssociateBalance
from rest_framework import status
from rest_framework.response import Response
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework import viewsets


class CoffeeOffers(viewsets.ViewSet):

    def pre_load(self, request) -> Response:
        try:
            now = timezone.now()
            to_date = now + timedelta(days=settings.COFFEE_OFFERS_DAYS_DELTA)
            # TODO: Remove at production release
            if settings.DEBUG:
                now = datetime(2022, 12, 14, 12, 00)
            user = self._get_user(request)
            # Validate EXCLUDED
            if settings.COFFEE_OFFERS_LOCKED_SEGMENT != 0 and user.profile.segment == settings.COFFEE_OFFERS_LOCKED_SEGMENT:
                raise ValidationError(_("The partner/client is blocked for coffee offers."))
            # Load Price List
            price_qs = Price.objects.get_products_price_by_date(date_to_search=now)
            price_serializer = PriceListSerializer(instance=price_qs, many=True, context={"kg": True})
            # Load Warehouse List
            warehouse_qs = models.CoffeeWareHouse.objects.order_by("location_name").all()
            warehouse_serializer = CoffeeWareHouseListSerializer(instance=warehouse_qs, many=True)

            # Calculate QUOTA in Kg.
            if user.profile.segment == settings.COFFEE_OFFERS_TRADER_SEGMENT:
                quota = settings.COFFEE_OFFERS_TRADER_QUOTA
            else:
                if user.profile.type == CustomerType.PARTNER:
                    quota = AssociateBalance.objects.get_quota(user.profile.document_id)
                else:
                    quota = settings.COFFEE_OFFERS_DEFAULT_QUOTA

            if settings.COFFEE_OFFERS_CALCULATE_QUOTA:
                quota = quota - models.Offer.objects.get_balance(user)

            data_return = {
                "quota": quota,
                "percent": settings.COFFEE_OFFERS_PRICE_DELTA,
                "to_date": to_date,
                "offers": models.Offer.objects.get_active_offers(user),
                "prices": price_serializer.data,
                "warehouses": warehouse_serializer.data
            }
            status_return = status.HTTP_200_OK
        except Exception as exc:
            raise APIException(msg=_("Not controlled exception."), error=str(exc)) from exc
        else:
            return Response(status=status_return, data=data_return)
