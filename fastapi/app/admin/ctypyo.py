from django.contrib import admin

from ..models import Currency, Block, Provider

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass