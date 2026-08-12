logger.error(f"Error syncing traffic for {u['id']}: {e}")


async def sync_panel_status_task(bot: Bot):
    """Sync user status from Remnawave panel to bot every 5 minutes."""
    users = await db_fetch("SELECT * FROM users WHERE is_active = TRUE AND panel_uuid IS NOT NULL")
    for u in users:
        try:
            rw_user = await rw_get_user_by_uuid(u["panel_uuid"])
            if rw_user is None:
                # User deleted from panel
                await db_execute(
                    "UPDATE users SET is_active = FALSE, panel_uuid = NULL, panel_short_uuid = NULL WHERE id = $1",
                    u["id"],
                )
                await bot.send_message(
                    u["id"],
                    "⚠️ <b>Ваша подписка была отключена в панели.</b>\n\n"
                    "Обратитесь в поддержку.",
                    parse_mode="HTML",
                )
            elif rw_user.get("status") == "DISABLED":
                await db_execute("UPDATE users SET is_active = FALSE WHERE id = $1", u["id"])
                await bot.send_message(
                    u["id"],
                    "⚠️ <b>Ваша подписка была отключена в панели.</b>\n\n"
                    "Обратитесь в поддержку.",
                    parse_mode="HTML",
                )
            elif rw_user.get("expireAt"):
                # Sync expiration
                panel_expire = datetime.fromisoformat(rw_user["expireAt"].replace("Z", "+00:00"))
                if panel_expire != u["subscription_end"]:
                    await db_execute(
                        "UPDATE users SET subscription_end = $1 WHERE id = $2",
                        panel_expire, u["id"],
                    )
        except Exception as e:
            logger.error(f"Error syncing panel status for {u['id']}: {e}")


async def monthly_reset_task(bot: Bot):
    """Reset monthly traffic on 1st day of month at 00:00 MSK."""
    now = now_msk()
    if now.day != 1 or now.hour != 0 or now.minute >= 10:
        return

    users = await db_fetch("SELECT * FROM users WHERE is_active = TRUE")
    for u in users:
        try:
            # Recalc ref traffic
            ref_bonus = await recalc_ref_traffic(u["id"])
            new_base = config.DEFAULT_TRAFFIC_GB

            await db_execute(
                "UPDATE users SET base_traffic_gb = $1, used_traffic_gb = 0, daily_ref_count = 0 WHERE id = $2",
                new_base, u["id"],
            )

            if u["panel_uuid"]:
                await rw_reset_traffic(u["panel_uuid"])
                await rw_update_user(
                    u["panel_uuid"],
                    traffic_limit_gb=new_base + ref_bonus,
                )
        except Exception as e:
            logger.error(f"Error monthly reset for {u['id']}: {e}")

    logger.info("Monthly reset completed")


async def cleanup_tickets_task():
    try:
        await db_execute("DELETE FROM tickets WHERE status = 'closed' AND closed_at < NOW() - INTERVAL '7 days'")
        await db_execute("DELETE FROM notifications WHERE sent_at < NOW() - INTERVAL '30 days'")
    except Exception as e:
        logger.error(f"Error cleaning up: {e}")


# =============================================================================
# MAIN
# =============================================================================
async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    await get_pool()
    await bot.set_my_commands([
        {"command": "start", "description": "Главное меню"},
        {"command": "admin", "description": "Админ-панель (только админы)"},
    ])

    web_app = await init_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, config.WEB_HOST, config.WEB_PORT)
    await site.start()
    logger.info(f"Web server started on {config.WEB_HOST}:{config.WEB_PORT}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_subscriptions_task, "interval", minutes=10, args=[bot])
    scheduler.add_job(send_notifications_task, "interval", minutes=30, args=[bot])
    scheduler.add_job(sync_traffic_task, "interval", minutes=5, args=[bot])
    scheduler.add_job(sync_panel_status_task, "interval", minutes=5, args=[bot])
    scheduler.add_job(monthly_reset_task, "interval", minutes=10, args=[bot])
    scheduler.add_job(cleanup_tickets_task, "interval", hours=24)
    scheduler.start()
    logger.info("Scheduler started")

    logger.info("Bot started polling")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await close_pool()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
