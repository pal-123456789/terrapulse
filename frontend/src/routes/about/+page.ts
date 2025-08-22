import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    return {
        title: 'About TerraPulse - Planetary Health Monitoring',
        description: 'Learn about TerraPulse, an AI-powered platform for real-time planetary health monitoring and environmental anomaly prediction.'
    };
};