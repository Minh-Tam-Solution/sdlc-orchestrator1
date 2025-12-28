"""
VNPay Payment Service - SDLC Orchestrator

Version: 1.0.0
Date: December 27, 2025
Status: Sprint 58 - Registration + VNPay
Authority: Backend Lead + CTO Approved
Foundation: Plan v2.2 Section 7 VNPay Integration

Purpose:
- VNPay URL generation with secure hash
- VNPay signature verification
- Payment URL creation for Founder plan

VNPay Documentation: https://sandbox.vnpayment.vn/apis/

Security:
- HMAC-SHA512 signature verification
- Idempotent IPN handling (see routes/payments.py)
"""

import hashlib
import hmac
import logging
import urllib.parse
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class VNPayService:
    """
    VNPay payment integration service.

    Handles:
    - Payment URL generation
    - Signature verification
    - Response parsing

    Per Plan v2.2 Section 7:
    - Founder Plan: 2,500,000 VND/month
    - Standard Plan: Manual billing (not self-service in V1)
    """

    # VNPay API version
    VERSION = "2.1.0"

    # VNPay command codes
    COMMAND_PAY = "pay"
    COMMAND_REFUND = "refund"

    # Currency code (VND only for VNPay)
    CURRENCY_VND = "VND"

    # Locale
    LOCALE_VN = "vn"
    LOCALE_EN = "en"

    # Response codes
    SUCCESS_CODE = "00"

    def __init__(self):
        """Initialize VNPay service with configuration."""
        settings = get_settings()

        # VNPay configuration from settings
        self.tmn_code = settings.VNPAY_TMN_CODE
        self.hash_secret = settings.VNPAY_HASH_SECRET
        self.payment_url = settings.VNPAY_URL
        self.return_url = settings.VNPAY_RETURN_URL

        # Validate configuration
        if not all([self.tmn_code, self.hash_secret, self.payment_url]):
            logger.warning("VNPay configuration incomplete - payments will fail")

    def _hmac_sha512(self, key: str, data: str) -> str:
        """
        Generate HMAC-SHA512 hash.

        Args:
            key: Secret key
            data: Data to hash

        Returns:
            Hex-encoded hash string
        """
        return hmac.new(
            key.encode("utf-8"),
            data.encode("utf-8"),
            hashlib.sha512
        ).hexdigest()

    def _build_query_string(self, params: dict) -> str:
        """
        Build sorted query string for signing.

        VNPay requires parameters to be sorted alphabetically.

        Args:
            params: Dictionary of parameters

        Returns:
            URL-encoded query string
        """
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())

        # Build query string
        query_parts = []
        for key, value in sorted_params:
            if value is not None and value != "":
                query_parts.append(f"{key}={urllib.parse.quote_plus(str(value))}")

        return "&".join(query_parts)

    def create_payment_url(
        self,
        order_id: str,
        amount: int,
        order_info: str,
        ip_address: str,
        locale: str = LOCALE_VN,
        bank_code: Optional[str] = None,
    ) -> str:
        """
        Create VNPay payment URL.

        Args:
            order_id: Unique order ID (our vnp_txn_ref)
            amount: Amount in VND (integer, will be multiplied by 100)
            order_info: Order description
            ip_address: Customer IP address
            locale: Locale (vn or en)
            bank_code: Optional bank code for direct payment

        Returns:
            Full payment URL to redirect user

        Example:
            url = vnpay.create_payment_url(
                order_id="ORD123",
                amount=2500000,  # 2.5M VND
                order_info="Upgrade to Founder Plan",
                ip_address="192.168.1.1"
            )
        """
        # Create timestamp in VNPay format
        create_date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Build parameters
        params = {
            "vnp_Version": self.VERSION,
            "vnp_Command": self.COMMAND_PAY,
            "vnp_TmnCode": self.tmn_code,
            "vnp_Amount": amount * 100,  # VNPay expects amount * 100
            "vnp_CurrCode": self.CURRENCY_VND,
            "vnp_TxnRef": order_id,
            "vnp_OrderInfo": order_info,
            "vnp_OrderType": "250000",  # Bill payment
            "vnp_Locale": locale,
            "vnp_ReturnUrl": self.return_url,
            "vnp_IpAddr": ip_address,
            "vnp_CreateDate": create_date,
        }

        # Add bank code if specified
        if bank_code:
            params["vnp_BankCode"] = bank_code

        # Build query string and sign
        query_string = self._build_query_string(params)
        secure_hash = self._hmac_sha512(self.hash_secret, query_string)

        # Build final URL
        payment_url = f"{self.payment_url}?{query_string}&vnp_SecureHash={secure_hash}"

        logger.info(f"Created VNPay payment URL for order {order_id}, amount={amount} VND")

        return payment_url

    def verify_secure_hash(self, params: dict) -> bool:
        """
        Verify VNPay response signature.

        Args:
            params: Dictionary of VNPay response parameters

        Returns:
            True if signature is valid, False otherwise
        """
        # Extract secure hash from params
        received_hash = params.get("vnp_SecureHash", "")

        if not received_hash:
            logger.warning("No vnp_SecureHash in response")
            return False

        # Remove hash params for verification
        verify_params = {k: v for k, v in params.items() if k not in ["vnp_SecureHash", "vnp_SecureHashType"]}

        # Build query string and calculate expected hash
        query_string = self._build_query_string(verify_params)
        expected_hash = self._hmac_sha512(self.hash_secret, query_string)

        # Compare hashes (case-insensitive)
        is_valid = received_hash.lower() == expected_hash.lower()

        if not is_valid:
            logger.warning(f"VNPay signature mismatch for txn_ref={params.get('vnp_TxnRef')}")

        return is_valid

    def is_success_response(self, params: dict) -> bool:
        """
        Check if VNPay response indicates success.

        Args:
            params: Dictionary of VNPay response parameters

        Returns:
            True if payment was successful
        """
        response_code = params.get("vnp_ResponseCode", "")
        return response_code == self.SUCCESS_CODE

    def parse_return_params(self, query_string: str) -> dict:
        """
        Parse VNPay return URL query parameters.

        Args:
            query_string: Raw query string from URL

        Returns:
            Dictionary of parameters
        """
        return dict(urllib.parse.parse_qsl(query_string))

    def generate_txn_ref(self) -> str:
        """
        Generate unique transaction reference.

        Format: SDLC-{timestamp}-{uuid_short}

        Returns:
            Unique transaction reference
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        uuid_short = str(uuid4())[:8].upper()
        return f"SDLC-{timestamp}-{uuid_short}"


# Pricing constants per Plan v2.2
PLAN_PRICES = {
    "founder": {
        "monthly": 2_500_000,  # 2.5M VND/month
        "annual": 25_000_000,  # 25M VND/year (~17% discount)
        "currency": "VND",
        "name": "Founder Plan",
        "description": "Dành cho startup Việt Nam - Unlimited team members",
    },
    "standard": {
        "monthly": 750_000,  # ~$30/user/month (manual billing in V1)
        "currency": "VND",
        "name": "Standard Plan",
        "description": "For global teams - per user pricing",
    },
}


def get_plan_price(plan: str, billing_period: str = "monthly") -> dict:
    """
    Get plan pricing information.

    Args:
        plan: Plan name (founder, standard)
        billing_period: monthly or annual

    Returns:
        Dictionary with price, currency, name, description
    """
    plan_info = PLAN_PRICES.get(plan)
    if not plan_info:
        raise ValueError(f"Unknown plan: {plan}")

    price_key = billing_period if billing_period in plan_info else "monthly"
    return {
        "price": plan_info.get(price_key, plan_info["monthly"]),
        "currency": plan_info["currency"],
        "name": plan_info["name"],
        "description": plan_info["description"],
        "billing_period": billing_period,
    }


# Global service instance
_vnpay_service: Optional[VNPayService] = None


def get_vnpay_service() -> VNPayService:
    """Get or create VNPay service instance."""
    global _vnpay_service
    if _vnpay_service is None:
        _vnpay_service = VNPayService()
    return _vnpay_service
