import React from 'react';
import { Typography, Box, Paper } from '@mui/material';

interface PEARLSPhase {
  name: string;
  description: string;
  color: string;
}

const PEARLS_PHASES: PEARLSPhase[] = [
  {
    name: 'P - Preparation',
    description: 'Review learning objectives and set the stage for the debriefing session',
    color: '#4CAF50',
  },
  {
    name: 'E - Engagement',
    description: 'Encourage active participation and create a safe learning environment',
    color: '#2196F3',
  },
  {
    name: 'A - Assessment',
    description: 'Evaluate performance and identify key learning points',
    color: '#FFC107',
  },
  {
    name: 'R - Reflection',
    description: 'Facilitate self-reflection and discussion of actions taken',
    color: '#FF9800',
  },
  {
    name: 'L - Learning',
    description: 'Extract key lessons and reinforce important concepts',
    color: '#9C27B0',
  },
  {
    name: 'S - Summary',
    description: 'Summarize key points and plan for future improvement',
    color: '#F44336',
  },
];

export function PEARLSModel() {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        PEARLS Framework
      </Typography>
      <Typography variant="body1" paragraph>
        The PEARLS framework provides a structured approach to debriefing simulation experiences.
        Each phase builds upon the previous one to create a comprehensive learning experience.
      </Typography>
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
        {PEARLS_PHASES.map((phase) => (
          <Paper
            key={phase.name}
            sx={{
              p: 2,
              borderLeft: `4px solid ${phase.color}`,
              '&:hover': {
                boxShadow: 3,
              },
            }}
          >
            <Typography variant="h6" gutterBottom sx={{ color: phase.color }}>
              {phase.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {phase.description}
            </Typography>
          </Paper>
        ))}
      </Box>
    </Box>
  );
} 