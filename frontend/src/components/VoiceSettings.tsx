import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Slider,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  SelectChangeEvent,
} from '@mui/material';

interface VoiceSettingsProps {
  open: boolean;
  onClose: () => void;
  settings: VoiceSettings;
  onSettingsChange: (settings: VoiceSettings) => void;
}

export interface VoiceSettings {
  rate: number;
  pitch: number;
  volume: number;
  voice: string;
  useVoice: boolean;
  silenceThreshold: number;
  continuousMode: boolean;
}

export const defaultSettings: VoiceSettings = {
  rate: 1,
  pitch: 1,
  volume: 1,
  voice: '',
  useVoice: true,
  silenceThreshold: 1500,
  continuousMode: true,
};

export function VoiceSettings({ open, onClose, settings, onSettingsChange }: VoiceSettingsProps) {
  const [voices, setVoices] = React.useState<SpeechSynthesisVoice[]>([]);

  React.useEffect(() => {
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      setVoices(availableVoices);
    };

    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;

    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, []);

  const handleChange = (key: keyof VoiceSettings) => (
    event: React.ChangeEvent<HTMLInputElement> | SelectChangeEvent<string>
  ) => {
    const value = 'checked' in event.target 
      ? event.target.checked 
      : event.target.value;
    
    onSettingsChange({
      ...settings,
      [key]: value,
    });
  };

  const handleSliderChange = (key: keyof VoiceSettings) => (
    _: Event,
    value: number | number[]
  ) => {
    onSettingsChange({
      ...settings,
      [key]: value,
    });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Voice Settings</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.useVoice}
                onChange={handleChange('useVoice')}
                color="primary"
              />
            }
            label="Enable Voice"
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography gutterBottom>Voice</Typography>
          <FormControl fullWidth>
            <Select
              value={settings.voice}
              onChange={handleChange('voice')}
              disabled={!settings.useVoice}
            >
              {voices.map((voice) => (
                <MenuItem key={voice.name} value={voice.name}>
                  {voice.name} ({voice.lang})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography gutterBottom>Speech Rate</Typography>
          <Slider
            value={settings.rate}
            onChange={handleSliderChange('rate')}
            min={0.5}
            max={2}
            step={0.1}
            disabled={!settings.useVoice}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value}x`}
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography gutterBottom>Pitch</Typography>
          <Slider
            value={settings.pitch}
            onChange={handleSliderChange('pitch')}
            min={0.5}
            max={2}
            step={0.1}
            disabled={!settings.useVoice}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value}x`}
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography gutterBottom>Volume</Typography>
          <Slider
            value={settings.volume}
            onChange={handleSliderChange('volume')}
            min={0}
            max={1}
            step={0.1}
            disabled={!settings.useVoice}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${Math.round(value * 100)}%`}
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <Typography gutterBottom>Silence Threshold (ms)</Typography>
          <Slider
            value={settings.silenceThreshold}
            onChange={handleSliderChange('silenceThreshold')}
            min={500}
            max={3000}
            step={100}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value}ms`}
          />
        </Box>

        <Box sx={{ mt: 3 }}>
          <FormControlLabel
            control={
              <Switch
                checked={settings.continuousMode}
                onChange={handleChange('continuousMode')}
                color="primary"
              />
            }
            label="Continuous Mode"
          />
          <Typography variant="caption" color="text.secondary" display="block">
            In continuous mode, the system will automatically detect when you stop speaking
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        <Button 
          onClick={() => onSettingsChange(defaultSettings)}
          color="secondary"
        >
          Reset to Default
        </Button>
      </DialogActions>
    </Dialog>
  );
} 