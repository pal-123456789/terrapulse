<script lang="ts">
  // This line receives the data object returned from the `load` function
  // in your +page.ts file.
  export let data;
</script>

<!-- 
  FIX: This is the correct SvelteKit way to set the page title and meta tags.
  It uses the `data` prop from the `load` function.
-->
<svelte:head>
    <title>{data.title}</title>
    <meta name="description" content={data.description} />
</svelte:head>

<div class="page-container">
    <div class="glass card">
        <div class="card-header">
            <h1>Environmental Education</h1>
            <p class="subtitle">Understanding our planet's health</p>
        </div>
        
        <div class="card-content">
            <div class="lessons-grid">
                <div class="lesson-category">
                    <h2>🔥 Wildfires</h2>
                    <div class="lesson-list">
                        <div class="lesson">
                            <h3>How Wildfires Spread</h3>
                            <p>Learn about the factors that influence wildfire behavior and spread patterns.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                        <div class="lesson">
                            <h3>Prevention & Safety</h3>
                            <p>Essential information about wildfire prevention and safety measures.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                    </div>
                </div>
                
                <div class="lesson-category">
                    <h2>🌊 Floods</h2>
                    <div class="lesson-list">
                        <div class="lesson">
                            <h3>Understanding Flood Risks</h3>
                            <p>Learn how to interpret flood maps and understand your area's risk factors.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                        <div class="lesson">
                            <h3>Flood Preparedness</h3>
                            <p>Essential steps to prepare for and respond to flood events.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                    </div>
                </div>
                
                <div class="lesson-category">
                    <h2>🌪️ Storms</h2>
                    <div class="lesson-list">
                        <div class="lesson">
                            <h3>Hurricane Formation</h3>
                            <p>Understand the meteorological processes behind hurricane development.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                        <div class="lesson">
                            <h3>Storm Tracking</h3>
                            <p>Learn how to interpret storm tracking data and predictions.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                    </div>
                </div>
                
                <div class="lesson-category">
                    <h2>📊 Data Interpretation</h2>
                    <div class="lesson-list">
                        <div class="lesson">
                            <h3>Reading Satellite Imagery</h3>
                            <p>Learn how to interpret different types of satellite data and imagery.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                        <div class="lesson">
                            <h3>Understanding Predictions</h3>
                            <p>How to interpret AI-generated predictions and confidence scores.</p>
                            <button class="btn btn-secondary">Read More</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .page-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .lessons-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
    }
    .lesson-category h2 {
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    .lesson-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    .lesson {
        padding: 15px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .lesson h3 {
        margin-bottom: 8px;
        color: var(--accent-primary);
    }
    .lesson p {
        margin-bottom: 12px;
        color: var(--text-secondary);
        line-height: 1.5;
    }
</style>
