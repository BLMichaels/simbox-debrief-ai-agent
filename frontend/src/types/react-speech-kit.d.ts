declare module 'react-speech-kit' {
  export interface SpeechSynthesisOptions {
    text: string;
    voice?: SpeechSynthesisVoice;
    rate?: number;
    pitch?: number;
    volume?: number;
  }

  export interface SpeechSynthesisState {
    speak: (options: SpeechSynthesisOptions) => void;
    cancel: () => void;
    speaking: boolean;
    supported: boolean;
  }

  export function useSpeechSynthesis(): SpeechSynthesisState;
} 