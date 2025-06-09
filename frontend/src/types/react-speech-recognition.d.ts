declare module 'react-speech-recognition' {
  export interface SpeechRecognitionOptions {
    continuous?: boolean;
    interimResults?: boolean;
    maxAlternatives?: number;
    grammars?: any;
  }

  export interface SpeechRecognitionState {
    transcript: string;
    listening: boolean;
    browserSupportsSpeechRecognition: boolean;
    resetTranscript: () => void;
    startListening: (options?: SpeechRecognitionOptions) => Promise<void>;
    stopListening: () => void;
  }

  export function useSpeechRecognition(options?: SpeechRecognitionOptions): SpeechRecognitionState;
} 