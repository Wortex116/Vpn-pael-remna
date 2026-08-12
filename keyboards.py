"""Inline keyboards for PotyjnoVPN bot."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_main(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚀 Мой VPN", callback_data="vpn_menu"),
         InlineKeyboardButton(text="👤 Кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="👥 Рефералы", callback_data="referral"),
         InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
        [InlineKeyboardButton(text="💰 Донат", callback_data="donate"),
         InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="💬 Поддержка", callback_data="support")],
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="🔧 Админка", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_vpn(can_extend: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📋 Получить подписку", callback_data="get_sub")],
        [InlineKeyboardButton(text="📱 Сброс устройств", callback_data="reset_devices"),
         InlineKeyboardButton(text="🔄 Новая ссылка", callback_data="reset_link")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ]
    if can_extend:
        buttons.insert(1, [InlineKeyboardButton(text="🔄 Продлить подписку", callback_data="extend_sub")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Детальная статистика", callback_data="detailed_stats")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_referral() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Копировать ссылку", callback_data="copy_ref")],
        [InlineKeyboardButton(text="📊 Мои рефералы", callback_data="my_refs")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_help() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍎 iOS", url="https://apps.apple.com/ru/app/incy/id6756943388"),
         InlineKeyboardButton(text="🤖 Android", url="https://play.google.com/store/apps/details?id=llc.itdev.incy")],
        [InlineKeyboardButton(text="💻 Windows", url="https://github.com/INCY-DEV/incy-platforms"),
         InlineKeyboardButton(text="🐧 Linux", url="https://github.com/INCY-DEV/incy-platforms")],
        [InlineKeyboardButton(text="🍏 macOS", url="https://github.com/INCY-DEV/incy-platforms")],
        [InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/mel1ste")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_donate(donate_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Поддержать проект", url=donate_url)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_confirm_sub(channel: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 К подписке", url=f"https://t.me/{channel.lstrip('@')}")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")],
    ])


def kb_extend() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Продлить подписку", callback_data="extend_sub")],
        [InlineKeyboardButton(text="👥 Пригласить друга", callback_data="referral")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_admin() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
         InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔍 Поиск", callback_data="admin_search"),
         InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_admin_user_actions(user_id: int, is_active: bool) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📋 Логи рефералов", callback_data=f"admin_reflogs:{user_id}")],
    ]
    if is_active:
        buttons.append([InlineKeyboardButton(text="❌ Заблокировать", callback_data=f"admin_block:{user_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="✅ Разблокировать", callback_data=f"admin_unblock:{user_id}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_search")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_support_menu(has_ticket: bool = False, ticket_id: int = 0, status: str = "") -> InlineKeyboardMarkup:
    if has_ticket:
        buttons = [
            [InlineKeyboardButton(text="📋 Мой тикет", callback_data="my_ticket")],
        ]
        if status == "open":
            buttons.insert(1, [InlineKeyboardButton(text="❌ Закрыть тикет", callback_data=f"user_close_ticket:{ticket_id}")])
        buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать тикет", callback_data="create_ticket")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
    ])


def kb_ticket_admin(ticket_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Взять в работу", callback_data=f"take_ticket:{ticket_id}")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data=f"close_ticket:{ticket_id}")],
    ])


def kb_pagination(page: int, total_pages: int, prefix: str) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text="◀️", callback_data=f"{prefix}_page:{page - 1}"))
    row.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        row.append(InlineKeyboardButton(text="▶️", callback_data=f"{prefix}_page:{page + 1}"))
    buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
