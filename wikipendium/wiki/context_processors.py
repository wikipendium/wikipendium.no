import wikipendium.settings as settings


def google_analytics_processor(request):
    try:
        return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
                'GOOGLE_ANALYTICS_NAME': settings.GOOGLE_ANALYTICS_NAME}
    except:
        return {}


def paypal_processor(request):
    return {'PAYPAL_DONATION_PKCS7': settings.PAYPAL_DONATION_PKCS7}
