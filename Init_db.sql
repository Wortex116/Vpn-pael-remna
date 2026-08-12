-- ============================================================
-- PotyjnoVPN Bot — Database Schema
-- PostgreSQL
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    referral_code TEXT UNIQUE NOT NULL,
    referred_by BIGINT REFERENCES users(id) ON DELETE SET NULL,
    base_traffic_gb FLOAT DEFAULT 50.0,
    ref_traffic_gb FLOAT DEFAULT 0.0,
    used_traffic_gb FLOAT DEFAULT 0.0,
    subscription_code TEXT UNIQUE NOT NULL,
    panel_username TEXT UNIQUE NOT NULL,
    panel_uuid TEXT,
    panel_short_uuid TEXT,
    max_devices INT DEFAULT 3,
    is_subscribed BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    subscription_end TIMESTAMP WITH TIME ZONE,
    last_extended_at TIMESTAMP WITH TIME ZONE,
    daily_ref_count INT DEFAULT 0,
    last_ref_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);
CREATE INDEX IF NOT EXISTS idx_users_panel_uuid ON users(panel_uuid);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Referrals table
CREATE TABLE IF NOT EXISTS referrals (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referred_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    bonus_gb FLOAT DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    is_suspicious BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    unsubscribed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referred ON referrals(referred_id);

-- Referral logs (admin view)
CREATE TABLE IF NOT EXISTS referral_logs (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT NOT NULL,
    referred_id BIGINT NOT NULL,
    referred_username TEXT,
    referred_full_name TEXT,
    bonus_gb FLOAT DEFAULT 1.0,
    is_subscribed BOOLEAN DEFAULT FALSE,
    is_suspicious BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ref_logs_referrer ON referral_logs(referrer_id);

-- Suspicious referrals (anti-fraud alerts)
CREATE TABLE IF NOT EXISTS suspicious_refs (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT NOT NULL,
    referred_id BIGINT NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tickets
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'open',
    message_text TEXT,
    admin_id BIGINT,
    ticket_chat_id BIGINT,
    ticket_msg_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_tickets_user ON tickets(user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);

-- Notifications (anti-spam)
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notify_type TEXT NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(notify_type);
