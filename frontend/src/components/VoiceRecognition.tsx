import React, { useEffect, useRef, useState } from 'react';
import { Button, Box, Typography, CircularProgress, Alert } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import { VoiceSettings } from './VoiceSettings';

// Add type definitions for the Web Speech API
declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
  }
}

interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  length: number;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onstart: ((this: SpeechRecognition, ev: Event) => any) | null;
  onend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => any) | null;
  start(): void;
  stop(): void;
  abort(): void;
}

interface VoiceRecognitionProps {
  onTranscript: (text: string) => void;
  settings: VoiceSettings;
  isProcessing: boolean;
}

export function VoiceRecognition({ onTranscript, settings, isProcessing }: VoiceRecognitionProps) {
  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const silenceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const lastTranscriptRef = useRef<string>('');

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      
      recognition.continuous = settings.continuousMode;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        setError(null);
        lastTranscriptRef.current = '';
      };

      recognition.onend = () => {
        setIsListening(false);
        if (silenceTimerRef.current) {
          clearTimeout(silenceTimerRef.current);
          silenceTimerRef.current = null;
        }
      };

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          lastTranscriptRef.current = finalTranscript;
          onTranscript(finalTranscript);
        }
        setInterimTranscript(interimTranscript);

        // Reset silence timer
        if (silenceTimerRef.current) {
          clearTimeout(silenceTimerRef.current);
        }
        if (settings.continuousMode) {
          silenceTimerRef.current = setTimeout(() => {
            if (lastTranscriptRef.current) {
              onTranscript(lastTranscriptRef.current);
              lastTranscriptRef.current = '';
            }
          }, settings.silenceThreshold);
        }
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('Speech recognition error:', event.error);
        setError(`Speech recognition error: ${event.error}`);
        setIsListening(false);
      };
    } catch (err) {
      setError('Failed to initialize speech recognition. Please try refreshing the page.');
      console.error('Speech recognition initialization error:', err);
    }

    return () => {
      const recognition = recognitionRef.current;
      if (recognition) {
        try {
          recognition.stop();
        } catch (err) {
          console.error('Error stopping recognition:', err);
        }
      }
      if (silenceTimerRef.current) {
        clearTimeout(silenceTimerRef.current);
      }
    };
  }, [settings.continuousMode, settings.silenceThreshold, onTranscript]);

  const toggleListening = () => {
    const recognition = recognitionRef.current;
    if (!recognition) {
      setError('Speech recognition is not available. Please refresh the page.');
      return;
    }

    try {
      if (isListening) {
        recognition.stop();
      } else {
        recognition.start();
      }
    } catch (err) {
      setError('Failed to toggle speech recognition. Please try again.');
      console.error('Error toggling recognition:', err);
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
      {error && (
        <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
          {error}
        </Alert>
      )}

      <Button
        variant="contained"
        color={isListening ? 'secondary' : 'primary'}
        onClick={toggleListening}
        disabled={isProcessing || !!error}
        startIcon={isListening ? <MicOffIcon /> : <MicIcon />}
        sx={{ minWidth: 200 }}
      >
        {isListening ? 'Stop Listening' : 'Start Listening'}
      </Button>

      {isListening && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CircularProgress size={20} />
          <Typography variant="body2" color="text.secondary">
            Listening...
          </Typography>
        </Box>
      )}

      {interimTranscript && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {interimTranscript}
        </Typography>
      )}
    </Box>
  );
} 