"""Remnawave API client."""
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import aiohttp
from config import config

logger = logging.getLogger(__name__)


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {config.REMNAWAVE_TOKEN}",
        "Content-Type": "application/json",
    }


def _format_expire(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


async def rw_create_user(
    username: str,
    traffic_limit_gb: float,
    expire_at: datetime,
    max_devices: int = 3,
) -> Optional[Dict[str, Any]]:
    """Create a new user in Remnawave panel."""
    payload = {
        "username": username,
        "status": "ACTIVE",
        "trafficLimit": traffic_limit_gb,
        "trafficLimitUnit": "GB",
        "trafficLimitStrategy": "MONTH",
        "expireAt": _format_expire(expire_at),
        "hwidDeviceLimit": max_devices,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.REMNAWAVE_URL}/api/users",
            headers=_headers(),
            json=payload,
        ) as resp:
            if resp.status in (200, 201):
                data = await resp.json()
                return data.get("response")
            text = await resp.text()
            logger.error(f"rw_create_user failed: {resp.status} — {text}")
            return None


async def rw_get_user_by_uuid(uuid: str) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}",
            headers=_headers(),
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("response")
            return None


async def rw_get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.REMNAWAVE_URL}/api/users/by-username/{username}",
            headers=_headers(),
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("response")
            return None


async def rw_get_user_by_short_uuid(short_uuid: str) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.REMNAWAVE_URL}/api/users/by-short-uuid/{short_uuid}",
            headers=_headers(),
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("response")
            return None


async def rw_update_user(
    uuid: str,
    status: Optional[str] = None,
    traffic_limit_gb: Optional[float] = None,
    expire_at: Optional[datetime] = None,
    max_devices: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    payload: Dict[str, Any] = {}
    if status is not None:
        payload["status"] = status
    if traffic_limit_gb is not None:
        payload["trafficLimit"] = traffic_limit_gb
        payload["trafficLimitUnit"] = "GB"
    if expire_at is not None:
        payload["expireAt"] = _format_expire(expire_at)
    if max_devices is not None:
        payload["hwidDeviceLimit"] = max_devices

    if not payload:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}",
            headers=_headers(),
            json=payload,
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("response")
            text = await resp.text()
            logger.error(f"rw_update_user failed: {resp.status} — {text}")
            return None


async def rw_delete_user(uuid: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}",
            headers=_headers(),
        ) as resp:
            if resp.status in (200, 204):
                return True
            text = await resp.text()
            logger.error(f"rw_delete_user failed: {resp.status} — {text}")
            return False


async def rw_enable_user(uuid: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}/enable",
            headers=_headers(),
        ) as resp:
            return resp.status == 200


async def rw_disable_user(uuid: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}/disable",
            headers=_headers(),
        ) as resp:
            return resp.status == 200


async def rw_revoke_subscription(uuid: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}/revoke-subscription",
            headers=_headers(),
        ) as resp:
            return resp.status == 200


async def rw_reset_traffic(uuid: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.REMNAWAVE_URL}/api/users/{uuid}/reset-traffic",
            headers=_headers(),
        ) as resp:
            return resp.status == 200


async def rw_get_used_traffic(uuid: str) -> float:
    """Return used traffic in GB."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.REMNAWAVE_URL}/api/bandwidth-stats/get-user-usage/{uuid}",
            headers=_headers(),
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                response = data.get("response", {})
                total = response.get("totalBytes")
                if total is not None:
                    return total / (1024 ** 3)
                up = response.get("uploadBytes", 0)
                down = response.get("downloadBytes", 0)
                return (up + down) / (1024 ** 3)
            return 0.0


async def rw_list_users(limit: int = 100, offset: int = 0) -> Optional[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.REMNAWAVE_URL}/api/users?limit={limit}&offset={offset}",
            headers=_headers(),
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
