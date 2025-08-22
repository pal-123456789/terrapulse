// @ts-nocheck
import type { PageLoad } from './$types';

// This `load` function runs on the server or in the browser before the page is rendered.
// It provides data to the corresponding +page.svelte component.
export const load = () => {
    return {
        title: 'Privacy Policy - TerraPulse',
        description: 'TerraPulse privacy policy and data usage information.'
    };
};
;null as any as PageLoad;