-- Test Data for My Vocabulary Vault
-- This script creates sample users, flashcard sets, and flashcards

-- Clear existing test data (optional)
-- DELETE FROM flashcards WHERE card_metadata->>'created_by' = 'test_script';
-- DELETE FROM flashcard_sets WHERE title IN ('Basic English Vocabulary', 'Programming Terms', 'Spanish Basics', 'Math Formulas', 'Science Terms');
-- DELETE FROM users WHERE email IN ('john.doe@example.com', 'jane.smith@example.com', 'admin@vocabularyvault.com');

-- Create test users
INSERT INTO users (email, username, full_name, hashed_password, is_active, is_superuser, total_points, level, experience_points, study_streak_days, longest_streak, total_study_time_minutes, total_cards_studied, total_correct_answers, total_incorrect_answers, average_accuracy, study_preferences, notification_settings, privacy_settings, created_at, updated_at)
VALUES 
    ('john.doe@example.com', 'johndoe', 'John Doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.G', true, false, 150, 3, 450, 5, 7, 120, 45, 38, 7, 0.84, '{"preferred_mode": "flashcards", "daily_goal": 20}', '{"email_notifications": true, "push_notifications": false}', '{"profile_public": true}', NOW(), NOW()),
    ('jane.smith@example.com', 'janesmith', 'Jane Smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.G', true, false, 200, 4, 600, 8, 12, 180, 60, 52, 8, 0.87, '{"preferred_mode": "learn", "daily_goal": 30}', '{"email_notifications": true, "push_notifications": true}', '{"profile_public": false}', NOW(), NOW()),
    ('admin@vocabularyvault.com', 'admin', 'System Administrator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.G', true, true, 500, 8, 1500, 15, 20, 300, 100, 95, 5, 0.95, '{"preferred_mode": "test", "daily_goal": 50}', '{"email_notifications": true, "push_notifications": true}', '{"profile_public": true}', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

-- Get user IDs
DO $$
DECLARE
    john_id INTEGER;
    jane_id INTEGER;
    admin_id INTEGER;
BEGIN
    SELECT id INTO john_id FROM users WHERE email = 'john.doe@example.com';
    SELECT id INTO jane_id FROM users WHERE email = 'jane.smith@example.com';
    SELECT id INTO admin_id FROM users WHERE email = 'admin@vocabularyvault.com';

    -- Create flashcard sets
    INSERT INTO flashcard_sets (user_id, title, description, category, tags, is_public, is_featured, total_cards, study_count, created_at, updated_at)
    VALUES 
        (john_id, 'Basic English Vocabulary', 'Essential English words for beginners', 'English', '["beginner", "vocabulary", "english"]', true, true, 10, 25, NOW(), NOW()),
        (john_id, 'Programming Terms', 'Common programming terminology and concepts', 'Programming', '["programming", "tech", "computer-science"]', true, false, 10, 15, NOW(), NOW()),
        (jane_id, 'Spanish Basics', 'Basic Spanish vocabulary for travelers', 'Spanish', '["spanish", "travel", "beginner"]', true, false, 10, 8, NOW(), NOW()),
        (jane_id, 'Math Formulas', 'Important mathematical formulas and equations', 'Mathematics', '["math", "formulas", "education"]', false, false, 5, 3, NOW(), NOW()),
        (admin_id, 'Science Terms', 'Scientific terminology and definitions', 'Science', '["science", "biology", "chemistry", "physics"]', true, true, 8, 12, NOW(), NOW())
    ON CONFLICT DO NOTHING;
END $$;

-- Create flashcards for Basic English Vocabulary
INSERT INTO flashcards (set_id, front_content, back_content, card_type, media_url, difficulty, mastery_level, mastery_score, review_count, correct_count, incorrect_count, card_metadata, created_at, updated_at)
SELECT 
    fs.id,
    card.front,
    card.back,
    'text',
    NULL,
    card.difficulty,
    'not_learned',
    0.0,
    0,
    0,
    0,
    '{"created_by": "test_script"}',
    NOW(),
    NOW()
FROM flashcard_sets fs
CROSS JOIN (VALUES 
    ('Hello', 'Xin chào', 'easy'),
    ('Goodbye', 'Tạm biệt', 'easy'),
    ('Thank you', 'Cảm ơn', 'easy'),
    ('Please', 'Làm ơn', 'easy'),
    ('Sorry', 'Xin lỗi', 'easy'),
    ('Yes', 'Có', 'easy'),
    ('No', 'Không', 'easy'),
    ('Water', 'Nước', 'medium'),
    ('Food', 'Thức ăn', 'medium'),
    ('House', 'Nhà', 'medium')
) AS card(front, back, difficulty)
WHERE fs.title = 'Basic English Vocabulary'
ON CONFLICT DO NOTHING;

-- Create flashcards for Programming Terms
INSERT INTO flashcards (set_id, front_content, back_content, card_type, media_url, difficulty, mastery_level, mastery_score, review_count, correct_count, incorrect_count, card_metadata, created_at, updated_at)
SELECT 
    fs.id,
    card.front,
    card.back,
    'text',
    NULL,
    card.difficulty,
    'not_learned',
    0.0,
    0,
    0,
    0,
    '{"created_by": "test_script"}',
    NOW(),
    NOW()
FROM flashcard_sets fs
CROSS JOIN (VALUES 
    ('Variable', 'A container that stores data values', 'easy'),
    ('Function', 'A reusable block of code that performs a specific task', 'medium'),
    ('Loop', 'A programming construct that repeats a block of code', 'medium'),
    ('Array', 'A data structure that stores multiple values in a single variable', 'medium'),
    ('Object', 'An instance of a class that contains data and methods', 'hard'),
    ('Class', 'A blueprint for creating objects with properties and methods', 'hard'),
    ('API', 'Application Programming Interface - a set of rules for building software', 'medium'),
    ('Database', 'An organized collection of structured information or data', 'medium'),
    ('Algorithm', 'A step-by-step procedure for solving a problem', 'hard'),
    ('Debugging', 'The process of finding and fixing errors in code', 'medium')
) AS card(front, back, difficulty)
WHERE fs.title = 'Programming Terms'
ON CONFLICT DO NOTHING;

-- Create flashcards for Spanish Basics
INSERT INTO flashcards (set_id, front_content, back_content, card_type, media_url, difficulty, mastery_level, mastery_score, review_count, correct_count, incorrect_count, card_metadata, created_at, updated_at)
SELECT 
    fs.id,
    card.front,
    card.back,
    'text',
    NULL,
    card.difficulty,
    'not_learned',
    0.0,
    0,
    0,
    0,
    '{"created_by": "test_script"}',
    NOW(),
    NOW()
FROM flashcard_sets fs
CROSS JOIN (VALUES 
    ('Hola', 'Hello', 'easy'),
    ('Adiós', 'Goodbye', 'easy'),
    ('Gracias', 'Thank you', 'easy'),
    ('Por favor', 'Please', 'easy'),
    ('Lo siento', 'Sorry', 'easy'),
    ('Sí', 'Yes', 'easy'),
    ('No', 'No', 'easy'),
    ('Agua', 'Water', 'medium'),
    ('Comida', 'Food', 'medium'),
    ('Casa', 'House', 'medium')
) AS card(front, back, difficulty)
WHERE fs.title = 'Spanish Basics'
ON CONFLICT DO NOTHING;

-- Create flashcards for Math Formulas
INSERT INTO flashcards (set_id, front_content, back_content, card_type, media_url, difficulty, mastery_level, mastery_score, review_count, correct_count, incorrect_count, card_metadata, created_at, updated_at)
SELECT 
    fs.id,
    card.front,
    card.back,
    'text',
    NULL,
    card.difficulty,
    'not_learned',
    0.0,
    0,
    0,
    0,
    '{"created_by": "test_script"}',
    NOW(),
    NOW()
FROM flashcard_sets fs
CROSS JOIN (VALUES 
    ('Area of Circle', 'A = πr²', 'medium'),
    ('Pythagorean Theorem', 'a² + b² = c²', 'medium'),
    ('Quadratic Formula', 'x = (-b ± √(b² - 4ac)) / 2a', 'hard'),
    ('Slope Formula', 'm = (y₂ - y₁) / (x₂ - x₁)', 'medium'),
    ('Distance Formula', 'd = √((x₂ - x₁)² + (y₂ - y₁)²)', 'medium')
) AS card(front, back, difficulty)
WHERE fs.title = 'Math Formulas'
ON CONFLICT DO NOTHING;

-- Create flashcards for Science Terms
INSERT INTO flashcards (set_id, front_content, back_content, card_type, media_url, difficulty, mastery_level, mastery_score, review_count, correct_count, incorrect_count, card_metadata, created_at, updated_at)
SELECT 
    fs.id,
    card.front,
    card.back,
    'text',
    NULL,
    card.difficulty,
    'not_learned',
    0.0,
    0,
    0,
    0,
    '{"created_by": "test_script"}',
    NOW(),
    NOW()
FROM flashcard_sets fs
CROSS JOIN (VALUES 
    ('Atom', 'The smallest unit of matter that retains the properties of an element', 'medium'),
    ('Molecule', 'A group of atoms bonded together', 'medium'),
    ('Cell', 'The basic structural and functional unit of all living organisms', 'medium'),
    ('DNA', 'Deoxyribonucleic acid - the molecule that carries genetic information', 'hard'),
    ('Photosynthesis', 'The process by which plants convert sunlight into energy', 'medium'),
    ('Gravity', 'A force that attracts objects toward each other', 'easy'),
    ('Evolution', 'The process of change in all forms of life over generations', 'medium'),
    ('Ecosystem', 'A community of living organisms and their environment', 'medium')
) AS card(front, back, difficulty)
WHERE fs.title = 'Science Terms'
ON CONFLICT DO NOTHING;

-- Update total_cards count for all sets
UPDATE flashcard_sets 
SET total_cards = (
    SELECT COUNT(*) 
    FROM flashcards 
    WHERE flashcards.set_id = flashcard_sets.id
);

-- Print summary
SELECT 
    'Test Data Summary' as info,
    (SELECT COUNT(*) FROM users WHERE email IN ('john.doe@example.com', 'jane.smith@example.com', 'admin@vocabularyvault.com')) as users_created,
    (SELECT COUNT(*) FROM flashcard_sets WHERE title IN ('Basic English Vocabulary', 'Programming Terms', 'Spanish Basics', 'Math Formulas', 'Science Terms')) as sets_created,
    (SELECT COUNT(*) FROM flashcards WHERE card_metadata->>'created_by' = 'test_script') as cards_created;
