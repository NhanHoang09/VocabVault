'use client';

import { useState, useCallback } from 'react';
import { Flashcard, StudySession, ProgressStats } from '@/types';
import { STUDY_CONFIG } from '@/constants';
import { api } from '@/lib/api';

interface UseStudyReturn {
  currentCard: Flashcard | null;
  sessionCards: Flashcard[];
  sessionStats: {
    total: number;
    correct: number;
    incorrect: number;
    currentIndex: number;
  };
  isLoading: boolean;
  startSession: (category?: string, difficulty?: string) => Promise<void>;
  answerCard: (isCorrect: boolean) => Promise<void>;
  endSession: () => Promise<StudySession>;
  getProgressStats: () => Promise<ProgressStats>;
}

export function useStudy(): UseStudyReturn {
  const [currentCard, setCurrentCard] = useState<Flashcard | null>(null);
  const [sessionCards, setSessionCards] = useState<Flashcard[]>([]);
  const [sessionStats, setSessionStats] = useState({
    total: 0,
    correct: 0,
    incorrect: 0,
    currentIndex: 0,
  });
  const [isLoading, setIsLoading] = useState(false);

  const startSession = useCallback(
    async (category?: string, difficulty?: string) => {
      try {
        setIsLoading(true);

        // Get flashcards for session
        const response = await api.get('/study/session', {
          params: {
            category,
            difficulty,
            limit: STUDY_CONFIG.DAILY_GOAL_DEFAULT,
          },
        });

        const cards: Flashcard[] = response.data;
        setSessionCards(cards);
        setCurrentCard(cards[0] || null);
        setSessionStats({
          total: cards.length,
          correct: 0,
          incorrect: 0,
          currentIndex: 0,
        });
      } catch (error) {
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const answerCard = useCallback(
    async (isCorrect: boolean) => {
      if (!currentCard) return;

      try {
        setIsLoading(true);

        // Update session stats
        setSessionStats(prev => ({
          ...prev,
          correct: prev.correct + (isCorrect ? 1 : 0),
          incorrect: prev.incorrect + (isCorrect ? 0 : 1),
          currentIndex: prev.currentIndex + 1,
        }));

        // Send answer to backend
        await api.post('/study/answer', {
          wordId: currentCard.id,
          isCorrect,
          masteryLevel: isCorrect
            ? currentCard.masteryLevel + 1
            : Math.max(0, currentCard.masteryLevel - 1),
        });

        // Move to next card
        const nextIndex = sessionStats.currentIndex + 1;
        if (nextIndex < sessionCards.length) {
          setCurrentCard(sessionCards[nextIndex]);
        } else {
          setCurrentCard(null); // Session completed
        }
      } catch (error) {
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [currentCard, sessionCards, sessionStats.currentIndex]
  );

  const endSession = useCallback(async (): Promise<StudySession> => {
    try {
      const response = await api.post('/study/session/end', {
        totalWords: sessionStats.total,
        correctAnswers: sessionStats.correct,
        incorrectAnswers: sessionStats.incorrect,
        duration: Date.now(), // This should be calculated from session start time
      });

      // Reset session state
      setCurrentCard(null);
      setSessionCards([]);
      setSessionStats({
        total: 0,
        correct: 0,
        incorrect: 0,
        currentIndex: 0,
      });

      return response.data;
    } catch (error) {
      throw error;
    }
  }, [sessionStats]);

  const getProgressStats = useCallback(async (): Promise<ProgressStats> => {
    try {
      const response = await api.get('/study/progress');
      return response.data;
    } catch (error) {
      throw error;
    }
  }, []);

  return {
    currentCard,
    sessionCards,
    sessionStats,
    isLoading,
    startSession,
    answerCard,
    endSession,
    getProgressStats,
  };
}
