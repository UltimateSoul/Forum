

class StripeWebhookEvents:
    SUCCEEDED_PAYMENT_INTENT = 'payment_intent.succeeded'


class StripeWebhookMixin(StripeWebhookEvents):
    pass
