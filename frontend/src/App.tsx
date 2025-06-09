import React, { useState } from 'react';
import { Container, Box, Typography, Paper, Button } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import { VoiceRecognition } from './components/VoiceRecognition';
import { TextToSpeech } from './components/TextToSpeech';
import { VoiceSettings, defaultSettings } from './components/VoiceSettings';
import { PEARLSModel } from './components/PEARLSModel';

// Get the API URL from environment variable or use localhost as fallback
const API_URL = "https://simbox-debrief-ai-agent.onrender.com";

function App() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [voiceSettings, setVoiceSettings] = useState<VoiceSettings>(defaultSettings);
  const [showSettings, setShowSettings] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');

  const handleTranscript = async (text: string) => {
    setIsProcessing(true);
    try {
      const response = await fetch(`${API_URL}/debrief`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setCurrentResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
      setCurrentResponse('Sorry, I encountered an error processing your input.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            PEARLS Debriefing Assistant
          </Typography>
          <Button
            startIcon={<SettingsIcon />}
            onClick={() => setShowSettings(true)}
            variant="outlined"
          >
            Voice Settings
          </Button>
        </Box>

        <Paper sx={{ p: 3, mb: 3 }}>
          <PEARLSModel />
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <VoiceRecognition
            onTranscript={handleTranscript}
            settings={voiceSettings}
            isProcessing={isProcessing}
          />
        </Paper>

        {currentResponse && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Response:
            </Typography>
            <Typography>{currentResponse}</Typography>
            <TextToSpeech
              text={currentResponse}
              settings={voiceSettings}
            />
          </Paper>
        )}

        <VoiceSettings
          open={showSettings}
          onClose={() => setShowSettings(false)}
          settings={voiceSettings}
          onSettingsChange={setVoiceSettings}
        />
      </Box>
    </Container>
  );
}

export default App; 