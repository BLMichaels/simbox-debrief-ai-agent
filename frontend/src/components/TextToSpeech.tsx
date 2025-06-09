import React, { useEffect, useRef, useState } from 'react';
import { Alert } from '@mui/material';
import { VoiceSettings } from './VoiceSettings';

interface TextToSpeechProps {
  text: string;
  settings: VoiceSettings;
  onSpeakEnd?: () => void;
}

export function TextToSpeech({ text, settings, onSpeakEnd }: TextToSpeechProps) {
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!settings.useVoice || !text) return;

    try {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utteranceRef.current = utterance;

      // Apply voice settings
      if (settings.voice) {
        const voices = window.speechSynthesis.getVoices();
        const selectedVoice = voices.find(voice => voice.name === settings.voice);
        if (selectedVoice) {
          utterance.voice = selectedVoice;
        }
      }

      utterance.rate = settings.rate;
      utterance.pitch = settings.pitch;
      utterance.volume = settings.volume;

      // Handle speech end
      utterance.onend = () => {
        setError(null);
        if (onSpeakEnd) {
          onSpeakEnd();
        }
      };

      // Handle speech errors
      utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event);
        setError('Failed to speak the text. Please try again.');
        if (onSpeakEnd) {
          onSpeakEnd();
        }
      };

      // Speak the text
      window.speechSynthesis.speak(utterance);
    } catch (err) {
      console.error('Speech synthesis error:', err);
      setError('Speech synthesis is not supported in your browser.');
    }

    // Cleanup function
    return () => {
      if (utteranceRef.current) {
        window.speechSynthesis.cancel();
      }
    };
  }, [text, settings, onSpeakEnd]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (utteranceRef.current) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return null;
} 