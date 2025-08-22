import type { PageLoad } from './$types';

// This `load` function runs on the server or in the browser before the page is rendered.
// It provides data to the corresponding +page.svelte component.
export const load: PageLoad = () => {
    return {
        title: 'Learn - Environmental Awareness & Education',
        description: 'Educational resources about environmental monitoring, climate change, and how to interpret planetary health data.'
    };
};
