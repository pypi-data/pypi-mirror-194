import logging
import typing
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.managers import WalletTransactionManager
from ob_dj_store.core.stores.models._store import PaymentMethod
from ob_dj_store.core.stores.utils import validate_currency
from ob_dj_store.utils.helpers import wallet_media_upload_to

logger = logging.getLogger(__name__)


class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets",
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=wallet_media_upload_to, null=True, blank=True)
    image_thumbnail_medium = models.ImageField(
        upload_to="wallets/", null=True, blank=True
    )
    currency = models.CharField(
        max_length=3,
        default="KWD",
        validators=[
            validate_currency,
        ],
    )

    class Meta:
        unique_together = ("user", "currency")

    def __str__(self) -> typing.Text:
        return f"Wallet(PK={self.pk})"

    @property
    def balance(self) -> Decimal:
        from ob_dj_store.core.stores.models import WalletTransaction

        query = self.transactions.aggregate(
            balance=Coalesce(
                models.Sum(
                    "amount",
                    filter=models.Q(type=WalletTransaction.TYPE.CREDIT),
                ),
                models.Value(Decimal(0)),
                output_field=models.DecimalField(),
            )
            - Coalesce(
                models.Sum(
                    "amount", filter=models.Q(type=WalletTransaction.TYPE.DEBIT)
                ),
                models.Value(Decimal(0)),
                output_field=models.DecimalField(),
            )
        )
        return query["balance"]

    def top_up_wallet(self, amount: Decimal, payment_method: PaymentMethod):
        from ob_dj_store.core.stores.models import Order, Payment

        user = self.user
        order = Order.objects.create(
            customer=user,
            payment_method=payment_method,
            extra_infos={
                "is_wallet_fill_up": True,
                "amount": str(amount),
                "currency": self.currency,
            },
        )
        payment = Payment.objects.create(
            orders=[
                order,
            ],
            user=user,
            currency=self.currency,
            method=payment_method,
            amount=amount,
        )
        return payment.payment_url


class WalletTransaction(models.Model):
    """

    As a user, I should be able to view my wallet transactions (debit/credit).
    WalletTransaction type should be one of two types, either debit or credit.

    """

    class TYPE(models.TextChoices):
        CREDIT = "CREDIT", _("credit")
        DEBIT = "DEBIT", _("debit")

    wallet = models.ForeignKey(
        "stores.Wallet",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    type = models.CharField(
        max_length=100,
        choices=TYPE.choices,
    )

    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )

    objects = WalletTransactionManager()

    # Audit
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return f"WalletTransaction (PK={self.pk})"
