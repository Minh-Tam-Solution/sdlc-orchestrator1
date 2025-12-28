"""
VNPay Payment Routes - SDLC Orchestrator

Version: 1.0.0
Date: December 27, 2025
Status: Sprint 58 - Registration + VNPay
Authority: Backend Lead + CTO Approved
Foundation: Plan v2.2 Section 7 VNPay Integration

Purpose:
- VNPay payment URL creation (POST /payments/vnpay/create)
- VNPay return handler (GET /payments/vnpay/return)
- VNPay IPN webhook (POST /payments/vnpay/ipn)
- Payment status query (GET /payments/{vnp_txn_ref})

Security:
- HMAC-SHA512 signature verification
- Idempotent IPN handling per Plan v2.2 Section 7.3
- Terminal state immutability

Flow per Plan v2.2:
1. User clicks "Upgrade to Founder" → POST /vnpay/create
2. Redirect to VNPay gateway
3. User completes payment → VNPay redirects to /vnpay/return
4. VNPay sends IPN → POST /vnpay/ipn (server-to-server)
5. IPN handler atomically updates payment + subscription
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models import User, Subscription, PaymentHistory
from app.models.subscription import SubscriptionPlan, SubscriptionStatus, PaymentStatus
from app.services.vnpay_service import get_vnpay_service, get_plan_price

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["payments"])


# =============================================================================
# Request/Response Schemas
# =============================================================================


class VNPayCreateRequest(BaseModel):
    """Request to create VNPay payment URL."""

    plan: str = Field(..., description="Plan to purchase (founder, standard)")
    billing_period: str = Field(
        default="monthly",
        description="Billing period (monthly, annual)"
    )


class VNPayCreateResponse(BaseModel):
    """Response with VNPay payment URL."""

    payment_url: str = Field(..., description="VNPay payment URL to redirect user")
    vnp_txn_ref: str = Field(..., description="Transaction reference for tracking")
    amount: int = Field(..., description="Amount in VND")
    plan: str = Field(..., description="Plan being purchased")


class PaymentStatusResponse(BaseModel):
    """Payment status response."""

    vnp_txn_ref: str
    status: str
    amount: float
    currency: str
    plan: str
    processed_at: Optional[datetime]
    created_at: datetime


class SubscriptionResponse(BaseModel):
    """Subscription status response."""

    id: UUID
    plan: str
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    created_at: datetime


# =============================================================================
# VNPay Endpoints
# =============================================================================


@router.post("/vnpay/create", response_model=VNPayCreateResponse)
async def create_vnpay_payment(
    request_body: VNPayCreateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VNPayCreateResponse:
    """
    Create VNPay payment URL for plan upgrade.

    Per Plan v2.2 Section 7.1:
    - Generates unique transaction reference
    - Creates pending payment record
    - Returns VNPay URL for redirect

    Args:
        request_body: Plan and billing period
        request: FastAPI request (for IP address)
        db: Database session
        current_user: Authenticated user

    Returns:
        VNPayCreateResponse with payment URL

    Raises:
        HTTPException 400: Invalid plan
        HTTPException 400: Standard plan not self-service in V1
    """
    # Validate plan
    valid_plans = ["founder"]  # Only Founder is self-service in V1
    if request_body.plan not in valid_plans:
        if request_body.plan == "standard":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Standard plan requires manual setup. Please contact us at support@sdlc-orchestrator.com"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan. Valid options: {', '.join(valid_plans)}"
        )

    # Get plan pricing
    try:
        price_info = get_plan_price(request_body.plan, request_body.billing_period)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Get VNPay service
    vnpay = get_vnpay_service()

    # Generate unique transaction reference
    vnp_txn_ref = vnpay.generate_txn_ref()

    # Get client IP
    client_ip = request.client.host if request.client else "127.0.0.1"
    # Handle forwarded IP (from reverse proxy)
    forwarded_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if forwarded_ip:
        client_ip = forwarded_ip

    # Create payment record (PENDING state)
    payment = PaymentHistory(
        user_id=current_user.id,
        vnp_txn_ref=vnp_txn_ref,
        amount=price_info["price"],
        currency=price_info["currency"],
        plan=request_body.plan,
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    await db.commit()

    # Create VNPay payment URL
    order_info = f"SDLC Orchestrator - {price_info['name']} ({request_body.billing_period})"
    payment_url = vnpay.create_payment_url(
        order_id=vnp_txn_ref,
        amount=int(price_info["price"]),
        order_info=order_info,
        ip_address=client_ip,
    )

    logger.info(f"Created VNPay payment: txn_ref={vnp_txn_ref}, user={current_user.id}, plan={request_body.plan}")

    return VNPayCreateResponse(
        payment_url=payment_url,
        vnp_txn_ref=vnp_txn_ref,
        amount=int(price_info["price"]),
        plan=request_body.plan,
    )


@router.get("/vnpay/return")
async def vnpay_return_handler(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    VNPay return handler (user-facing redirect).

    Per Plan v2.2 Section 7.3.2:
    - This endpoint is READ-ONLY
    - Does NOT change payment status (that's IPN's job)
    - Only verifies signature and returns status

    VNPay redirects user here after payment.
    Frontend should redirect to /checkout/success or /checkout/failed based on response.

    Returns:
        Payment status for frontend display
    """
    params = dict(request.query_params)
    vnp_txn_ref = params.get("vnp_TxnRef")
    vnp_response_code = params.get("vnp_ResponseCode")

    logger.info(f"VNPay return: txn_ref={vnp_txn_ref}, code={vnp_response_code}")

    if not vnp_txn_ref:
        return {
            "success": False,
            "message": "Missing transaction reference",
            "redirect": "/checkout/failed",
        }

    # Verify signature (security)
    vnpay = get_vnpay_service()
    if not vnpay.verify_secure_hash(params):
        logger.warning(f"VNPay return: Invalid signature for {vnp_txn_ref}")
        return {
            "success": False,
            "message": "Invalid signature",
            "redirect": "/checkout/failed",
        }

    # Get payment record (READ-ONLY query)
    result = await db.execute(
        select(PaymentHistory).where(PaymentHistory.vnp_txn_ref == vnp_txn_ref)
    )
    payment = result.scalar_one_or_none()

    if not payment:
        return {
            "success": False,
            "message": "Payment not found",
            "redirect": "/checkout/failed",
        }

    # Return status based on VNPay response code
    # Note: Actual status update happens via IPN
    is_success = vnpay.is_success_response(params)

    return {
        "success": is_success,
        "vnp_txn_ref": vnp_txn_ref,
        "status": payment.status.value if hasattr(payment.status, 'value') else payment.status,
        "message": "Payment successful" if is_success else "Payment failed or cancelled",
        "redirect": "/checkout/success" if is_success else "/checkout/failed",
    }


@router.post("/vnpay/ipn")
async def vnpay_ipn_handler(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    VNPay IPN webhook handler (server-to-server).

    Per Plan v2.2 Section 7.3.3:
    - This is the SINGLE SOURCE OF TRUTH for payment state
    - Idempotent: Same IPN called N times → Same response, 1 state change
    - Terminal states (completed/failed) are immutable
    - Subscription activation is ATOMIC with payment completion

    VNPay Response Codes:
    - 00: Success (Confirmed)
    - 01: Order not found
    - 02: Already updated (idempotent)
    - 97: Invalid signature
    - 99: Unknown error

    Returns:
        VNPay response format: {"RspCode": "XX", "Message": "..."}
    """
    try:
        # Parse IPN params
        params = dict(request.query_params)
        vnp_txn_ref = params.get("vnp_TxnRef")
        vnp_response_code = params.get("vnp_ResponseCode")
        vnp_transaction_no = params.get("vnp_TransactionNo")

        logger.info(f"VNPay IPN received: txn_ref={vnp_txn_ref}, code={vnp_response_code}")

        # 1. Verify signature (security)
        vnpay = get_vnpay_service()
        if not vnpay.verify_secure_hash(params):
            logger.warning(f"VNPay IPN: Invalid signature for {vnp_txn_ref}")
            return {"RspCode": "97", "Message": "Invalid signature"}

        # 2. Find payment by idempotency key (with row lock)
        result = await db.execute(
            select(PaymentHistory)
            .where(PaymentHistory.vnp_txn_ref == vnp_txn_ref)
            .with_for_update()  # Row lock for concurrency
        )
        payment = result.scalar_one_or_none()

        if not payment:
            logger.error(f"VNPay IPN: Payment not found: {vnp_txn_ref}")
            return {"RspCode": "01", "Message": "Order not found"}

        # 3. Idempotency check (terminal states)
        if payment.is_terminal():
            logger.info(f"VNPay IPN: Already processed: {vnp_txn_ref} → {payment.status}")
            return {"RspCode": "02", "Message": "Already updated"}

        # 4. Process based on VNPay response
        now = datetime.utcnow()

        if vnp_response_code == "00":
            # Success: Activate subscription atomically
            payment.status = PaymentStatus.COMPLETED
            payment.processed_at = now
            payment.vnp_transaction_no = vnp_transaction_no
            payment.vnpay_response_code = vnp_response_code

            # Get or create subscription
            sub_result = await db.execute(
                select(Subscription).where(Subscription.user_id == payment.user_id)
            )
            subscription = sub_result.scalar_one_or_none()

            if subscription:
                # Update existing subscription
                subscription.plan = SubscriptionPlan(payment.plan)
                subscription.status = SubscriptionStatus.ACTIVE
                subscription.current_period_start = now
                subscription.current_period_end = now + timedelta(days=30)
            else:
                # Create new subscription
                subscription = Subscription(
                    user_id=payment.user_id,
                    plan=SubscriptionPlan(payment.plan),
                    status=SubscriptionStatus.ACTIVE,
                    current_period_start=now,
                    current_period_end=now + timedelta(days=30),
                )
                db.add(subscription)

            # Link payment to subscription
            payment.subscription_id = subscription.id

            logger.info(f"VNPay IPN: Payment completed: {vnp_txn_ref}, user={payment.user_id}")

        else:
            # Failure
            payment.status = PaymentStatus.FAILED
            payment.processed_at = now
            payment.vnp_transaction_no = vnp_transaction_no
            payment.vnpay_response_code = vnp_response_code
            payment.error_message = f"VNPay error code: {vnp_response_code}"

            logger.warning(f"VNPay IPN: Payment failed: {vnp_txn_ref}, code={vnp_response_code}")

        await db.commit()

        return {"RspCode": "00", "Message": "Confirmed"}

    except Exception as e:
        logger.exception(f"VNPay IPN error: {e}")
        await db.rollback()
        return {"RspCode": "99", "Message": "Unknown error"}


# =============================================================================
# Payment Status Endpoints
# =============================================================================


@router.get("/{vnp_txn_ref}", response_model=PaymentStatusResponse)
async def get_payment_status(
    vnp_txn_ref: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PaymentStatusResponse:
    """
    Get payment status by transaction reference.

    Args:
        vnp_txn_ref: VNPay transaction reference
        db: Database session
        current_user: Authenticated user

    Returns:
        PaymentStatusResponse with current status

    Raises:
        HTTPException 404: Payment not found
        HTTPException 403: Not authorized to view this payment
    """
    result = await db.execute(
        select(PaymentHistory).where(PaymentHistory.vnp_txn_ref == vnp_txn_ref)
    )
    payment = result.scalar_one_or_none()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Security: Only allow user to view their own payments
    if payment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this payment"
        )

    return PaymentStatusResponse(
        vnp_txn_ref=payment.vnp_txn_ref,
        status=payment.status.value if hasattr(payment.status, 'value') else payment.status,
        amount=float(payment.amount),
        currency=payment.currency,
        plan=payment.plan,
        processed_at=payment.processed_at,
        created_at=payment.created_at,
    )


# =============================================================================
# Subscription Endpoints
# =============================================================================


@router.get("/subscriptions/me", response_model=SubscriptionResponse)
async def get_my_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SubscriptionResponse:
    """
    Get current user's subscription.

    Returns:
        SubscriptionResponse with current subscription details

    Raises:
        HTTPException 404: No subscription found
    """
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription found"
        )

    return SubscriptionResponse(
        id=subscription.id,
        plan=subscription.plan.value if hasattr(subscription.plan, 'value') else subscription.plan,
        status=subscription.status.value if hasattr(subscription.status, 'value') else subscription.status,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        created_at=subscription.created_at,
    )
