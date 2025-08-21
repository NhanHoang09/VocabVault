-- Gamification Sample Data SQL Script
-- This script creates sample data for the gamification system

-- =====================================================
-- 1. SAMPLE BADGES
-- =====================================================

INSERT INTO badges (name, description, badge_type, icon_url, points_reward, criteria, rarity, is_active, created_at) VALUES
('First Steps', 'Complete your first study session', 'study_streak', 'https://example.com/badges/first-steps.png', 50, '{"study_sessions": 1}', 'common', true, NOW()),
('Streak Master', 'Maintain a 7-day study streak', 'study_streak', 'https://example.com/badges/streak-master.png', 200, '{"study_streak_days": 7}', 'rare', true, NOW()),
('Speed Demon', 'Complete a speed challenge in under 30 seconds', 'speed_demon', 'https://example.com/badges/speed-demon.png', 300, '{"speed_challenge_time": 30}', 'epic', true, NOW()),
('Perfect Memory', 'Complete a memory game with 100% accuracy', 'perfect_game', 'https://example.com/badges/perfect-memory.png', 400, '{"memory_game_accuracy": 1.0}', 'legendary', true, NOW()),
('Gravity Master', 'Type 50 words correctly in gravity game', 'game_champion', 'https://example.com/badges/gravity-master.png', 250, '{"gravity_words_correct": 50}', 'uncommon', true, NOW()),
('Match Maker', 'Complete 10 match games', 'game_champion', 'https://example.com/badges/match-maker.png', 150, '{"match_games_completed": 10}', 'common', true, NOW()),
('Fast Learner', 'Complete 5 study sessions in one day', 'fast_learner', 'https://example.com/badges/fast-learner.png', 100, '{"study_sessions_per_day": 5}', 'uncommon', true, NOW()),
('Consistent Studier', 'Study for 30 consecutive days', 'consistent_studier', 'https://example.com/badges/consistent-studier.png', 500, '{"study_streak_days": 30}', 'legendary', true, NOW());

-- =====================================================
-- 2. SAMPLE CHALLENGES
-- =====================================================

INSERT INTO challenges (name, description, challenge_type, criteria, reward_points, duration_days, is_active, is_recurring, created_at) VALUES
('Weekly Study Streak', 'Study for 7 consecutive days', 'study_streak', '{"study_days": 7}', 200, 7, true, true, NOW()),
('Speed Runner', 'Complete 5 speed challenges', 'speed_run', '{"speed_challenges_completed": 5}', 150, 14, true, false, NOW()),
('Game Master', 'Play all 4 types of games', 'game_master', '{"game_types_played": ["match", "gravity", "speed_challenge", "memory"]}', 300, 30, true, false, NOW()),
('Daily Goal', 'Study for at least 30 minutes today', 'daily_goal', '{"study_time_minutes": 30}', 50, 1, true, true, NOW()),
('Perfect Score', 'Achieve 100% accuracy in any game', 'perfect_score', '{"game_accuracy": 1.0}', 250, 7, true, false, NOW());

-- =====================================================
-- 3. SAMPLE GAME SESSIONS
-- =====================================================

-- Get user IDs and flashcard set IDs (assuming they exist)
-- Replace these with actual IDs from your database
DO $$
DECLARE
    user_id INTEGER;
    set_id INTEGER;
    session_id INTEGER;
BEGIN
    -- Get first user and flashcard set
    SELECT id INTO user_id FROM users LIMIT 1;
    SELECT id INTO set_id FROM flashcard_sets LIMIT 1;
    
    IF user_id IS NOT NULL AND set_id IS NOT NULL THEN
        -- Create sample game sessions
        INSERT INTO game_sessions (user_id, game_type, set_id, start_time, end_time, duration_seconds, score, max_score, accuracy_rate, cards_played, correct_answers, incorrect_answers, created_at) VALUES
        (user_id, 'match', set_id, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1 hour 45 minutes', 900, 750, 800, 0.94, 40, 38, 2, NOW() - INTERVAL '2 hours'),
        (user_id, 'gravity', set_id, NOW() - INTERVAL '1 day', NOW() - INTERVAL '23 hours 30 minutes', 1800, 1200, 1500, 0.80, 50, 40, 10, NOW() - INTERVAL '1 day'),
        (user_id, 'speed_challenge', set_id, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '45 minutes', 2700, 900, 1000, 0.90, 30, 27, 3, NOW() - INTERVAL '3 days'),
        (user_id, 'memory', set_id, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '12 minutes', 720, 1600, 1600, 1.00, 32, 32, 0, NOW() - INTERVAL '5 days'),
        (user_id, 'match', set_id, NOW() - INTERVAL '1 week', NOW() - INTERVAL '1 week' + INTERVAL '8 minutes', 480, 600, 800, 0.75, 24, 18, 6, NOW() - INTERVAL '1 week');
        
        -- Get session IDs for game-specific data
        SELECT id INTO session_id FROM game_sessions WHERE user_id = user_id ORDER BY created_at DESC LIMIT 1;
        
        -- Create Match Game data
        INSERT INTO match_games (session_id, moves_count, matches_found, total_pairs, time_bonus, perfect_match_bonus, created_at) VALUES
        ((SELECT id FROM game_sessions WHERE game_type = 'match' LIMIT 1), 45, 19, 20, 150, 0, NOW()),
        ((SELECT id FROM game_sessions WHERE game_type = 'match' ORDER BY created_at DESC LIMIT 1), 52, 12, 12, 80, 0, NOW());
        
        -- Create Gravity Game data
        INSERT INTO gravity_games (session_id, words_typed, words_correct, words_incorrect, combo_multiplier, max_combo, time_bonus, created_at) VALUES
        ((SELECT id FROM game_sessions WHERE game_type = 'gravity' LIMIT 1), 50, 40, 10, 3.5, 15, 300, NOW());
        
        -- Create Speed Challenge data
        INSERT INTO speed_challenges (session_id, total_questions, questions_answered, correct_answers, incorrect_answers, time_limit_seconds, time_remaining_seconds, average_response_time, fastest_response_time, slowest_response_time, streak_count, max_streak, created_at) VALUES
        ((SELECT id FROM game_sessions WHERE game_type = 'speed_challenge' LIMIT 1), 30, 30, 27, 3, 300, 45, 4.2, 1.5, 12.0, 8, 12, NOW());
        
        -- Create Memory Game data
        INSERT INTO memory_games (session_id, total_cards, cards_revealed, matches_found, moves_count, time_limit_seconds, time_remaining_seconds, created_at) VALUES
        ((SELECT id FROM game_sessions WHERE game_type = 'memory' LIMIT 1), 32, 32, 16, 48, 600, 120, NOW());
    END IF;
END $$;

-- =====================================================
-- 4. SAMPLE POINTS TRANSACTIONS
-- =====================================================

DO $$
DECLARE
    user_id INTEGER;
BEGIN
    SELECT id INTO user_id FROM users LIMIT 1;
    
    IF user_id IS NOT NULL THEN
        INSERT INTO points_transactions (user_id, points, transaction_type, description, reference_id, reference_type, created_at) VALUES
        (user_id, 50, 'study', 'Study session completed', 1, 'study_session', NOW() - INTERVAL '2 hours'),
        (user_id, 75, 'game', 'Game session completed', 1, 'game_session', NOW() - INTERVAL '1 hour'),
        (user_id, 200, 'badge', 'Badge earned: First Steps', 1, 'badge', NOW() - INTERVAL '3 hours'),
        (user_id, 25, 'bonus', 'Bonus points awarded', NULL, 'bonus', NOW() - INTERVAL '4 hours'),
        (user_id, 100, 'challenge', 'Challenge completed: Daily Goal', 1, 'challenge', NOW() - INTERVAL '5 hours'),
        (user_id, 60, 'study', 'Study session completed', 2, 'study_session', NOW() - INTERVAL '1 day'),
        (user_id, 90, 'game', 'Game session completed', 2, 'game_session', NOW() - INTERVAL '23 hours'),
        (user_id, 150, 'badge', 'Badge earned: Streak Master', 2, 'badge', NOW() - INTERVAL '2 days'),
        (user_id, 40, 'bonus', 'Bonus points awarded', NULL, 'bonus', NOW() - INTERVAL '3 days'),
        (user_id, 200, 'challenge', 'Challenge completed: Weekly Study Streak', 1, 'challenge', NOW() - INTERVAL '1 week');
    END IF;
END $$;

-- =====================================================
-- 5. SAMPLE USER BADGES
-- =====================================================

DO $$
DECLARE
    user_id INTEGER;
    badge_id INTEGER;
BEGIN
    SELECT id INTO user_id FROM users LIMIT 1;
    
    IF user_id IS NOT NULL THEN
        -- Award First Steps badge
        SELECT id INTO badge_id FROM badges WHERE name = 'First Steps' LIMIT 1;
        IF badge_id IS NOT NULL THEN
            INSERT INTO user_badges (user_id, badge_id, context_data, earned_at) VALUES
            (user_id, badge_id, '{"earned_at": "' || NOW()::text || '"}', NOW() - INTERVAL '3 hours');
        END IF;
        
        -- Award Streak Master badge
        SELECT id INTO badge_id FROM badges WHERE name = 'Streak Master' LIMIT 1;
        IF badge_id IS NOT NULL THEN
            INSERT INTO user_badges (user_id, badge_id, context_data, earned_at) VALUES
            (user_id, badge_id, '{"earned_at": "' || NOW()::text || '"}', NOW() - INTERVAL '2 days');
        END IF;
        
        -- Award Match Maker badge
        SELECT id INTO badge_id FROM badges WHERE name = 'Match Maker' LIMIT 1;
        IF badge_id IS NOT NULL THEN
            INSERT INTO user_badges (user_id, badge_id, context_data, earned_at) VALUES
            (user_id, badge_id, '{"earned_at": "' || NOW()::text || '"}', NOW() - INTERVAL '1 week');
        END IF;
        
        -- Award Perfect Memory badge
        SELECT id INTO badge_id FROM badges WHERE name = 'Perfect Memory' LIMIT 1;
        IF badge_id IS NOT NULL THEN
            INSERT INTO user_badges (user_id, badge_id, context_data, earned_at) VALUES
            (user_id, badge_id, '{"earned_at": "' || NOW()::text || '"}', NOW() - INTERVAL '5 days');
        END IF;
    END IF;
END $$;

-- =====================================================
-- 6. SAMPLE LEADERBOARD ENTRIES
-- =====================================================

DO $$
DECLARE
    user_id INTEGER;
    now_date TIMESTAMP := NOW();
    week_start TIMESTAMP := now_date - INTERVAL '1 day' * EXTRACT(DOW FROM now_date);
    month_start TIMESTAMP := DATE_TRUNC('month', now_date);
    year_start TIMESTAMP := DATE_TRUNC('year', now_date);
BEGIN
    SELECT id INTO user_id FROM users LIMIT 1;
    
    IF user_id IS NOT NULL THEN
        -- Daily leaderboard
        INSERT INTO leaderboard_entries (user_id, category, period_start, period_end, score, rank, study_time_minutes, cards_studied, games_played, badges_earned, created_at) VALUES
        (user_id, 'daily', DATE_TRUNC('day', now_date), DATE_TRUNC('day', now_date) + INTERVAL '1 day', 1250, 15, 120, 45, 3, 2, now_date);
        
        -- Weekly leaderboard
        INSERT INTO leaderboard_entries (user_id, category, period_start, period_end, score, rank, study_time_minutes, cards_studied, games_played, badges_earned, created_at) VALUES
        (user_id, 'weekly', week_start, week_start + INTERVAL '7 days', 3500, 8, 480, 150, 12, 4, now_date);
        
        -- Monthly leaderboard
        INSERT INTO leaderboard_entries (user_id, category, period_start, period_end, score, rank, study_time_minutes, cards_studied, games_played, badges_earned, created_at) VALUES
        (user_id, 'monthly', month_start, month_start + INTERVAL '1 month', 12500, 5, 1800, 450, 35, 8, now_date);
        
        -- All-time leaderboard
        INSERT INTO leaderboard_entries (user_id, category, period_start, period_end, score, rank, study_time_minutes, cards_studied, games_played, badges_earned, created_at) VALUES
        (user_id, 'all_time', year_start, year_start + INTERVAL '1 year', 25000, 3, 3600, 800, 75, 12, now_date);
    END IF;
END $$;

-- =====================================================
-- 7. SAMPLE USER CHALLENGES
-- =====================================================

DO $$
DECLARE
    user_id INTEGER;
    challenge_id INTEGER;
BEGIN
    SELECT id INTO user_id FROM users LIMIT 1;
    
    IF user_id IS NOT NULL THEN
        -- Weekly Study Streak challenge (completed)
        SELECT id INTO challenge_id FROM challenges WHERE name = 'Weekly Study Streak' LIMIT 1;
        IF challenge_id IS NOT NULL THEN
            INSERT INTO user_challenges (user_id, challenge_id, progress_data, is_completed, completed_at, started_at) VALUES
            (user_id, challenge_id, '{"current_progress": 100, "target": 100, "study_days": 7}', true, NOW() - INTERVAL '1 day', NOW() - INTERVAL '8 days');
        END IF;
        
        -- Speed Runner challenge (in progress)
        SELECT id INTO challenge_id FROM challenges WHERE name = 'Speed Runner' LIMIT 1;
        IF challenge_id IS NOT NULL THEN
            INSERT INTO user_challenges (user_id, challenge_id, progress_data, is_completed, completed_at, started_at) VALUES
            (user_id, challenge_id, '{"current_progress": 60, "target": 100, "speed_challenges_completed": 3}', false, NULL, NOW() - INTERVAL '5 days');
        END IF;
        
        -- Game Master challenge (not started)
        SELECT id INTO challenge_id FROM challenges WHERE name = 'Game Master' LIMIT 1;
        IF challenge_id IS NOT NULL THEN
            INSERT INTO user_challenges (user_id, challenge_id, progress_data, is_completed, completed_at, started_at) VALUES
            (user_id, challenge_id, '{"current_progress": 75, "target": 100, "game_types_played": ["match", "gravity", "speed_challenge"]}', false, NULL, NOW() - INTERVAL '10 days');
        END IF;
        
        -- Daily Goal challenge (completed today)
        SELECT id INTO challenge_id FROM challenges WHERE name = 'Daily Goal' LIMIT 1;
        IF challenge_id IS NOT NULL THEN
            INSERT INTO user_challenges (user_id, challenge_id, progress_data, is_completed, completed_at, started_at) VALUES
            (user_id, challenge_id, '{"current_progress": 100, "target": 100, "study_time_minutes": 45}', true, NOW() - INTERVAL '2 hours', DATE_TRUNC('day', NOW()));
        END IF;
        
        -- Perfect Score challenge (not completed)
        SELECT id INTO challenge_id FROM challenges WHERE name = 'Perfect Score' LIMIT 1;
        IF challenge_id IS NOT NULL THEN
            INSERT INTO user_challenges (user_id, challenge_id, progress_data, is_completed, completed_at, started_at) VALUES
            (user_id, challenge_id, '{"current_progress": 0, "target": 100, "best_accuracy": 0.94}', false, NULL, NOW() - INTERVAL '3 days');
        END IF;
    END IF;
END $$;

-- =====================================================
-- SUMMARY
-- =====================================================

SELECT 
    'Badges' as table_name,
    COUNT(*) as record_count
FROM badges
UNION ALL
SELECT 
    'Challenges' as table_name,
    COUNT(*) as record_count
FROM challenges
UNION ALL
SELECT 
    'Game Sessions' as table_name,
    COUNT(*) as record_count
FROM game_sessions
UNION ALL
SELECT 
    'Points Transactions' as table_name,
    COUNT(*) as record_count
FROM points_transactions
UNION ALL
SELECT 
    'User Badges' as table_name,
    COUNT(*) as record_count
FROM user_badges
UNION ALL
SELECT 
    'Leaderboard Entries' as table_name,
    COUNT(*) as record_count
FROM leaderboard_entries
UNION ALL
SELECT 
    'User Challenges' as table_name,
    COUNT(*) as record_count
FROM user_challenges
ORDER BY table_name;
