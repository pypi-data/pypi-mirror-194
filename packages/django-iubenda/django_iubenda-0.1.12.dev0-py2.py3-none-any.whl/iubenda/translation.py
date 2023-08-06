from modeltranslation.translator import register, TranslationOptions
from .models import Iubenda


@register(Iubenda)
class IubendaTranslationOptions(TranslationOptions):
    fields = ('iub_policy_id', )
