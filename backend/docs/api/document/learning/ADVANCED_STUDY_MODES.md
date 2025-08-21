# 🎯 Advanced Study Modes - Detailed Documentation

## 📋 Overview

Advanced Study Modes provide enhanced learning experiences beyond traditional flashcard study. This document details the three advanced modes: **Write Mode**, **Spell Mode**, and **Test Mode**.

## ✍️ Write Mode

### 🎯 Purpose
Write Mode challenges users to type answers from memory, promoting active recall and improving vocabulary retention.

### 🔧 Features
- **Fuzzy Matching**: Intelligent answer comparison using sequence matching algorithm
- **Detailed Feedback**: Specific suggestions for improvement
- **Confidence Tracking**: User confidence level recording (1-5 scale)
- **Response Time Analysis**: Performance timing metrics
- **Progress Tracking**: Real-time session progress

### 📊 Accuracy Calculation
```python
# Fuzzy matching algorithm
def calculate_accuracy(user_answer: str, correct_answer: str) -> float:
    # Normalize strings (remove punctuation, lowercase)
    user_norm = re.sub(r'[^\w\s]', '', user_answer.lower().strip())
    correct_norm = re.sub(r'[^\w\s]', '', correct_answer.lower().strip())
    
    # Use sequence matcher for fuzzy matching
    return SequenceMatcher(None, user_norm, correct_norm).ratio()
```

### 🎯 Accuracy Thresholds
- **90%+**: Excellent - Very close to correct answer
- **80-89%**: Good - Mostly correct with minor variations
- **60-79%**: Close - On the right track
- **<60%**: Needs improvement - Review required

### 📝 API Endpoints

#### Submit Write Answer
```http
POST /api/v1/study/write/answer
```

**Request:**
```json
{
  "card_id": 1,
  "session_id": 1,
  "user_answer": "apple",
  "response_time_seconds": 4.2,
  "confidence_level": 4
}
```

**Response:**
```json
{
  "card_id": 1,
  "user_answer": "apple",
  "correct_answer": "apple",
  "is_correct": true,
  "accuracy_score": 1.0,
  "feedback": "Excellent! Your answer is very close to the correct answer.",
  "suggestions": [],
  "response_time_seconds": 4.2,
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### Get Write Progress
```http
GET /api/v1/study/write/progress/{session_id}
```

**Response:**
```json
{
  "session_id": 1,
  "total_cards": 50,
  "cards_answered": 20,
  "correct_answers": 18,
  "accuracy_percentage": 90.0,
  "average_response_time": 4.5,
  "time_remaining_seconds": 600
}
```

### 💡 Feedback Examples

#### High Accuracy (90%+)
```json
{
  "feedback": "Excellent! Your answer is very close to the correct answer.",
  "suggestions": []
}
```

#### Medium Accuracy (80-89%)
```json
{
  "feedback": "Good! Your answer is mostly correct.",
  "suggestions": ["Double-check spelling and punctuation"]
}
```

#### Low Accuracy (60-79%)
```json
{
  "feedback": "Close! You're on the right track.",
  "suggestions": [
    "Check for missing words",
    "Verify spelling",
    "Make sure you included all key terms"
  ]
}
```

#### Very Low Accuracy (<60%)
```json
{
  "feedback": "Not quite right. Let's review the correct answer.",
  "suggestions": [
    "Read the question carefully",
    "Focus on key vocabulary terms",
    "Practice with similar questions"
  ]
}
```

## 🎯 Spell Mode

### 🎯 Purpose
Spell Mode focuses on spelling accuracy with phonetic feedback and pronunciation guidance.

### 🔧 Features
- **Exact Spelling Validation**: Precise spelling accuracy checking
- **Phonetic Feedback**: Detailed spelling guidance
- **Pronunciation Tips**: Helpful pronunciation suggestions
- **Audio Integration**: Audio play tracking and support
- **Word Pattern Analysis**: Intelligent pronunciation tips

### 📊 Validation Logic
```python
def validate_spelling(user_spelling: str, correct_spelling: str) -> bool:
    return user_spelling.lower().strip() == correct_spelling.lower().strip()
```

### 🎵 Phonetic Feedback Generation
```python
def generate_phonetic_feedback(user_spelling: str, correct_spelling: str) -> str:
    if user_spelling.lower().strip() == correct_spelling.lower().strip():
        return "Perfect spelling!"
    
    user_words = user_spelling.lower().split()
    correct_words = correct_spelling.lower().split()
    
    if len(user_words) != len(correct_words):
        return f"Check the number of words. You wrote {len(user_words)}, but there should be {len(correct_words)}."
    
    feedback_parts = []
    for i, (user_word, correct_word) in enumerate(zip(user_words, correct_words)):
        if user_word != correct_word:
            feedback_parts.append(f"Word {i+1}: '{user_word}' should be '{correct_word}'")
    
    return " ".join(feedback_parts) if feedback_parts else "Check your spelling carefully."
```

### 🎵 Pronunciation Tips Generation
```python
def generate_pronunciation_tips(word: str) -> List[str]:
    tips = []
    
    # Consonant combinations
    if any(char in word.lower() for char in ['th', 'ch', 'sh', 'ph']):
        tips.append("Pay attention to consonant combinations")
    
    # Silent letters
    if word.lower().endswith('e'):
        tips.append("The final 'e' is often silent")
    
    # Long words
    if len(word) > 8:
        tips.append("Break the word into syllables")
    
    # Vowel sounds
    if any(char in word.lower() for char in ['a', 'e', 'i', 'o', 'u']):
        tips.append("Focus on vowel sounds")
    
    return tips
```

### 📝 API Endpoints

#### Submit Spell Answer
```http
POST /api/v1/study/spell/answer
```

**Request:**
```json
{
  "card_id": 1,
  "session_id": 1,
  "user_spelling": "apple",
  "response_time_seconds": 3.8,
  "audio_played": true
}
```

**Response:**
```json
{
  "card_id": 1,
  "user_spelling": "apple",
  "correct_spelling": "apple",
  "is_correct": true,
  "phonetic_feedback": "Perfect spelling!",
  "pronunciation_tips": [
    "Focus on vowel sounds",
    "Break the word into syllables"
  ],
  "response_time_seconds": 3.8,
  "created_at": "2024-01-15T10:40:00Z"
}
```

#### Get Spell Progress
```http
GET /api/v1/study/spell/progress/{session_id}
```

**Response:**
```json
{
  "session_id": 1,
  "total_cards": 50,
  "cards_answered": 15,
  "correct_spellings": 14,
  "accuracy_percentage": 93.3,
  "average_response_time": 4.2,
  "audio_plays_count": 8
}
```

### 💡 Feedback Examples

#### Perfect Spelling
```json
{
  "phonetic_feedback": "Perfect spelling!",
  "pronunciation_tips": [
    "Focus on vowel sounds",
    "Break the word into syllables"
  ]
}
```

#### Incorrect Spelling
```json
{
  "phonetic_feedback": "Word 1: 'aple' should be 'apple'",
  "pronunciation_tips": [
    "Pay attention to consonant combinations",
    "Focus on vowel sounds"
  ]
}
```

#### Wrong Word Count
```json
{
  "phonetic_feedback": "Check the number of words. You wrote 2, but there should be 1.",
  "pronunciation_tips": [
    "Focus on vowel sounds"
  ]
}
```

## 📝 Test Mode

### 🎯 Purpose
Test Mode provides comprehensive assessment with multiple question types and detailed analytics.

### 🔧 Features
- **Multiple Question Types**: MCQ, True/False, Fill-in-blank, Matching
- **Customizable Parameters**: Question count, time limits, difficulty
- **Comprehensive Analytics**: Detailed performance analysis
- **Personalized Recommendations**: AI-generated study suggestions
- **Real-time Scoring**: Points-based assessment system

### 📊 Question Types

#### Multiple Choice
```json
{
  "question_type": "multiple_choice",
  "question_text": "What is the meaning of: apple?",
  "options": [
    "A fruit",
    "A vegetable", 
    "A color",
    "A number"
  ],
  "correct_answer": "A fruit",
  "explanation": "The correct answer is 'A fruit'",
  "difficulty": "medium",
  "points": 1
}
```

#### True/False
```json
{
  "question_type": "true_false",
  "question_text": "'apple' means 'a fruit'",
  "options": ["True", "False"],
  "correct_answer": "True",
  "explanation": "The correct meaning is 'a fruit'",
  "difficulty": "easy",
  "points": 1
}
```

#### Fill-in-Blank
```json
{
  "question_type": "fill_in_blank",
  "question_text": "Complete: apple = _____",
  "correct_answer": "a fruit",
  "explanation": "The answer is 'a fruit'",
  "difficulty": "medium",
  "points": 1
}
```

### 📝 API Endpoints

#### Create Test Session
```http
POST /api/v1/study/test/sessions
```

**Request:**
```json
{
  "set_id": 1,
  "question_count": 20,
  "time_limit_minutes": 30,
  "include_explanations": true,
  "question_types": ["multiple_choice", "true_false", "fill_in_blank"]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "set_id": 1,
  "question_count": 20,
  "time_limit_minutes": 30,
  "include_explanations": true,
  "started_at": "2024-01-15T11:00:00Z",
  "ended_at": null,
  "total_score": 0,
  "max_score": 20,
  "accuracy_percentage": 0.0,
  "time_taken_seconds": null,
  "questions_answered": 0,
  "correct_answers": 0,
  "created_at": "2024-01-15T11:00:00Z"
}
```

#### Generate Test Questions
```http
POST /api/v1/study/test/generate?set_id=1&question_count=20&question_types=multiple_choice&question_types=true_false
```

**Response:**
```json
[
  {
    "id": 1,
    "question_type": "multiple_choice",
    "question_text": "What is the meaning of: apple?",
    "options": [
      "A fruit",
      "A vegetable",
      "A color", 
      "A number"
    ],
    "correct_answer": "A fruit",
    "explanation": "The correct answer is 'A fruit'",
    "difficulty": "medium",
    "points": 1
  },
  {
    "id": 2,
    "question_type": "true_false",
    "question_text": "'apple' means 'a fruit'",
    "options": ["True", "False"],
    "correct_answer": "True",
    "explanation": "The correct meaning is 'a fruit'",
    "difficulty": "easy",
    "points": 1
  }
]
```

#### Calculate Test Results
```http
POST /api/v1/study/test/calculate-result?time_taken_seconds=1800
```

**Request:**
```json
[
  {
    "question_id": 1,
    "user_answer": "A fruit",
    "is_correct": true,
    "points_earned": 1,
    "response_time_seconds": 5.2,
    "explanation": "The correct answer is 'A fruit'"
  },
  {
    "question_id": 2,
    "user_answer": "True",
    "is_correct": true,
    "points_earned": 1,
    "response_time_seconds": 3.1,
    "explanation": "The correct meaning is 'a fruit'"
  }
]
```

**Response:**
```json
{
  "test_session_id": 1,
  "total_score": 18,
  "max_score": 20,
  "accuracy_percentage": 90.0,
  "time_taken_seconds": 1800,
  "questions_answered": 20,
  "correct_answers": 18,
  "question_results": [...],
  "performance_analysis": {
    "average_response_time": 4.5,
    "total_time_taken": 1800,
    "questions_per_minute": 0.67,
    "type_performance": {
      "multiple_choice": {
        "correct": 12,
        "total": 15,
        "accuracy": 80.0
      },
      "true_false": {
        "correct": 6,
        "total": 5,
        "accuracy": 100.0
      }
    }
  },
  "recommendations": [
    "Good progress! Review areas of weakness",
    "Try write mode to improve recall",
    "Focus on multiple choice questions"
  ]
}
```

### 📊 Performance Analysis

#### Score Calculation
```python
def calculate_test_score(question_results: List[TestQuestionResponse]) -> dict:
    total_score = sum(result.points_earned for result in question_results)
    max_score = len(question_results)
    correct_answers = sum(1 for result in question_results if result.is_correct)
    accuracy_percentage = (correct_answers / len(question_results) * 100) if question_results else 0
    
    return {
        "total_score": total_score,
        "max_score": max_score,
        "accuracy_percentage": accuracy_percentage,
        "questions_answered": len(question_results),
        "correct_answers": correct_answers
    }
```

#### Performance Analysis
```python
def analyze_performance(question_results: List[TestQuestionResponse], time_taken: int) -> dict:
    response_times = [result.response_time_seconds for result in question_results]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Analyze by question type
    type_performance = {}
    for result in question_results:
        question_type = result.question_type  # Would need to be added to response
        if question_type not in type_performance:
            type_performance[question_type] = {"correct": 0, "total": 0}
        
        type_performance[question_type]["total"] += 1
        if result.is_correct:
            type_performance[question_type]["correct"] += 1
    
    # Calculate accuracy for each type
    for qtype in type_performance:
        total = type_performance[qtype]["total"]
        correct = type_performance[qtype]["correct"]
        type_performance[qtype]["accuracy"] = (correct / total * 100) if total > 0 else 0
    
    return {
        "average_response_time": avg_response_time,
        "total_time_taken": time_taken,
        "questions_per_minute": len(question_results) / (time_taken / 60) if time_taken > 0 else 0,
        "type_performance": type_performance
    }
```

#### Recommendation Generation
```python
def generate_recommendations(accuracy: float, analysis: dict) -> List[str]:
    recommendations = []
    
    if accuracy < 60:
        recommendations.extend([
            "Focus on reviewing difficult concepts",
            "Consider using flashcards mode for practice"
        ])
    elif accuracy < 80:
        recommendations.extend([
            "Good progress! Review areas of weakness",
            "Try write mode to improve recall"
        ])
    else:
        recommendations.extend([
            "Excellent performance! Keep up the good work",
            "Consider challenging yourself with harder questions"
        ])
    
    if analysis.get("average_response_time", 0) > 10:
        recommendations.append("Work on improving response speed")
    
    # Add type-specific recommendations
    type_performance = analysis.get("type_performance", {})
    for qtype, perf in type_performance.items():
        if perf.get("accuracy", 100) < 70:
            recommendations.append(f"Focus on {qtype.replace('_', ' ')} questions")
    
    return recommendations
```

## 📈 Study Modes Comparison

| Feature | Write Mode | Spell Mode | Test Mode |
|---------|------------|------------|-----------|
| **Answer Type** | Free text | Free text | Mixed |
| **Validation** | Fuzzy matching | Exact spelling | Multiple types |
| **Feedback** | Detailed suggestions | Phonetic guidance | Comprehensive |
| **Scoring** | Accuracy percentage | Binary | Points-based |
| **Progress Tracking** | Real-time | Real-time | Analytics |
| **Question Types** | Single | Single | Multiple |
| **Time Pressure** | Optional | Optional | Configurable |
| **Audio Support** | No | Yes | Optional |
| **Difficulty Levels** | Adaptive | Fixed | Configurable |

## 🎯 Best Practices

### Write Mode Implementation
1. **Clear Prompts**: Provide context for expected answers
2. **Fuzzy Matching**: Allow for minor spelling variations (80% threshold)
3. **Detailed Feedback**: Give specific improvement suggestions
4. **Confidence Tracking**: Use confidence levels for adaptive learning
5. **Response Time Analysis**: Track performance timing

### Spell Mode Implementation
1. **Exact Validation**: Require precise spelling accuracy
2. **Phonetic Support**: Provide pronunciation guidance
3. **Audio Integration**: Include audio playback options
4. **Error Analysis**: Track common spelling mistakes
5. **Word Pattern Tips**: Generate intelligent pronunciation suggestions

### Test Mode Implementation
1. **Question Variety**: Mix different question types
2. **Time Management**: Set appropriate time limits
3. **Difficulty Progression**: Increase difficulty gradually
4. **Detailed Analytics**: Provide comprehensive performance insights
5. **Personalized Recommendations**: Generate study suggestions

## 🔧 Configuration Options

### Write Mode Configuration
```python
WRITE_MODE_CONFIG = {
    "fuzzy_match_threshold": 0.8,  # 80% accuracy threshold
    "max_response_time": 300,      # 5 minutes max
    "confidence_levels": 5,        # 1-5 scale
    "feedback_detailed": True      # Enable detailed feedback
}
```

### Spell Mode Configuration
```python
SPELL_MODE_CONFIG = {
    "case_sensitive": False,       # Case-insensitive validation
    "allow_partial": False,        # Require complete words
    "audio_required": False,       # Audio not required
    "phonetic_feedback": True,     # Enable phonetic feedback
    "pronunciation_tips": True     # Enable pronunciation tips
}
```

### Test Mode Configuration
```python
TEST_MODE_CONFIG = {
    "default_question_count": 10,  # Default questions
    "max_question_count": 50,      # Maximum questions
    "default_time_limit": 30,      # Default time (minutes)
    "max_time_limit": 120,         # Maximum time (minutes)
    "include_explanations": True,  # Include explanations
    "points_per_question": 1,      # Points per question
    "difficulty_progression": True # Enable difficulty progression
}
```

## 🚀 Integration Examples

### Frontend Integration (React)
```javascript
// Write Mode Example
const submitWriteAnswer = async (cardId, sessionId, answer) => {
  const response = await fetch('/api/v1/study/write/answer', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      card_id: cardId,
      session_id: sessionId,
      user_answer: answer,
      response_time_seconds: responseTime,
      confidence_level: confidence
    })
  });
  
  const result = await response.json();
  return result;
};

// Spell Mode Example
const submitSpellAnswer = async (cardId, sessionId, spelling) => {
  const response = await fetch('/api/v1/study/spell/answer', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      card_id: cardId,
      session_id: sessionId,
      user_spelling: spelling,
      response_time_seconds: responseTime,
      audio_played: audioPlayed
    })
  });
  
  const result = await response.json();
  return result;
};

// Test Mode Example
const generateTestQuestions = async (setId, questionCount) => {
  const response = await fetch(`/api/v1/study/test/generate?set_id=${setId}&question_count=${questionCount}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  const questions = await response.json();
  return questions;
};
```

### Mobile Integration (React Native)
```javascript
// Write Mode with real-time feedback
const WriteModeScreen = () => {
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  
  const handleSubmit = async () => {
    const startTime = Date.now();
    const result = await submitWriteAnswer(cardId, sessionId, answer);
    const responseTime = (Date.now() - startTime) / 1000;
    
    setFeedback({
      isCorrect: result.is_correct,
      accuracyScore: result.accuracy_score,
      feedback: result.feedback,
      suggestions: result.suggestions
    });
  };
  
  return (
    <View>
      <TextInput
        value={answer}
        onChangeText={setAnswer}
        placeholder="Type your answer..."
      />
      <Button title="Submit" onPress={handleSubmit} />
      {feedback && (
        <View>
          <Text>Accuracy: {feedback.accuracyScore * 100}%</Text>
          <Text>{feedback.feedback}</Text>
          {feedback.suggestions.map((suggestion, index) => (
            <Text key={index}>• {suggestion}</Text>
          ))}
        </View>
      )}
    </View>
  );
};
```

## 📊 Analytics and Reporting

### Performance Metrics
- **Accuracy Trends**: Track improvement over time
- **Response Time Analysis**: Identify performance bottlenecks
- **Question Type Performance**: Analyze strengths and weaknesses
- **User Engagement**: Monitor study session completion rates

### Data Export
```python
def export_study_data(user_id: int, date_range: tuple) -> dict:
    """Export comprehensive study data for analysis"""
    return {
        "write_mode_sessions": get_write_sessions(user_id, date_range),
        "spell_mode_sessions": get_spell_sessions(user_id, date_range),
        "test_mode_sessions": get_test_sessions(user_id, date_range),
        "performance_summary": calculate_performance_summary(user_id, date_range),
        "recommendations": generate_personalized_recommendations(user_id)
    }
```

## 🔗 Related Documentation

- [Learning API Overview](./README.md)
- [Flashcard API Documentation](../flashcards/README.md)
- [Gamification API Documentation](../gamification/README.md)
- [Analytics API Documentation](../analytics/README.md)

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Advanced Study Modes
